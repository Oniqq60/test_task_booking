'use client';
import { useState, useEffect, useCallback } from 'react';
import { X, Calendar, Phone, User } from 'lucide-react';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';
import { ru } from 'date-fns/locale';
import { bookingsApi, apartmentsApi } from '../lib/api';
import { useToast, TOAST_TYPES } from '@/context/ToastContext';

export default function BookingModal({ apartment, onClose }) {
  const [checkIn, setCheckIn] = useState(null);
  const [checkOut, setCheckOut] = useState(null);
  const [guestName, setGuestName] = useState('');
  const [guestPhone, setGuestPhone] = useState('+7 ');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [bookedPeriods, setBookedPeriods] = useState([]);
  
  const { addToast } = useToast();

  useEffect(() => {
    return () => {
      setCheckIn(null);
      setCheckOut(null);
      setGuestName('');
      setGuestPhone('+7 ');
      setError('');
      setBookedPeriods([]);
    };
  }, []);

  useEffect(() => {
    if (!apartment?.id) return;
    
    let isMounted = true;
    
    const loadBookedPeriods = async () => {
      try {
        const data = await apartmentsApi.getBookedPeriods(apartment.id);
        if (isMounted) {
          const fixedPeriods = data.map(p => ({
            ...p,
            check_out: new Date(new Date(p.check_out).getTime() + 24 * 60 * 60 * 1000)
          }));
          setBookedPeriods(fixedPeriods);
        }
      } catch (err) {
        console.error('Failed to load booked periods:', err);
      }
    };
    
    loadBookedPeriods();
    
    return () => {
      isMounted = false;
    };
  }, [apartment?.id]);

  const isDateBooked = useCallback((date) => {
    if (!date || !bookedPeriods.length) return false;
    const checkDate = new Date(date);
    checkDate.setHours(0, 0, 0, 0);
    
    return bookedPeriods.some(period => {
      const start = new Date(period.check_in);
      const end = new Date(period.check_out);
      start.setHours(0, 0, 0, 0);
      end.setHours(0, 0, 0, 0);
      return checkDate >= start && checkDate <= end;
    });
  }, [bookedPeriods]);

  const isDateDisabled = useCallback((date) => {
    if (!date) return true;
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    return date < today || isDateBooked(date);
  }, [isDateBooked]);

  const handlePhoneChange = (e) => {
    let value = e.target.value;
    
    if (!value.startsWith('+7')) {
      value = '+7 ' + value.replace(/[^0-9]/g, '');
    }
    
    const digits = value.replace('+7', '').replace(/[^0-9]/g, '');
    
    let formattedValue = '+7';
    if (digits.length > 0) {
      formattedValue += ' ';
      if (digits.length <= 3) {
        formattedValue += digits;
      } else if (digits.length <= 6) {
        formattedValue += `(${digits.slice(0, 3)}) ${digits.slice(3)}`;
      } else {
        formattedValue += `(${digits.slice(0, 3)}) ${digits.slice(3, 6)}-${digits.slice(6, 8)}-${digits.slice(8, 10)}`;
      }
    }
    
    if (formattedValue.length <= 18) {
      setGuestPhone(formattedValue);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    if (!checkIn || !checkOut) {
      setError('Пожалуйста, выберите даты');
      return;
    }
    if (!guestName.trim()) {
      setError('Введите ваше имя');
      return;
    }
    if (!guestPhone.trim() || guestPhone === '+7 ') {
      setError('Введите ваш телефон');
      return;
    }

    setLoading(true);
    try {
      const cleanPhone = '+7' + guestPhone.replace('+7', '').replace(/[^0-9]/g, '');
      
      await bookingsApi.create({
        apartment_id: apartment.id,
        guest_name: guestName.trim(),
        guest_phone: cleanPhone,
        check_in: checkIn.toISOString().split('T')[0],
        check_out: checkOut.toISOString().split('T')[0],
      });
      
      addToast(
        `Бронирование "${apartment.title}" успешно создано!`,
        TOAST_TYPES.SUCCESS,
        { duration: 5000 }
      );
      
      if (onClose) onClose();
      
      if (typeof window !== 'undefined') {
        setTimeout(() => window.location.reload(), 1000);
      }
      
    } catch (err) {
      let message = 'Произошла ошибка при бронировании';
      let type = TOAST_TYPES.ERROR;
      
      if (err.response?.status === 409) {
        message = 'Выбранные даты уже забронированы';
        type = TOAST_TYPES.WARNING;
      } else if (err.response?.status === 400) {
        message = 'Ошибка валидации данных';
      }
      
      addToast(message, type, { duration: 6000 });
      setError(message);
    } finally {
      setLoading(false);
    }
  };

  const calculateNights = useCallback(() => {
    if (!checkIn || !checkOut) return 0;
    const diff = checkOut.getTime() - checkIn.getTime();
    return Math.ceil(diff / (1000 * 60 * 60 * 24));
  }, [checkIn, checkOut]);

  const calculateTotal = useCallback(() => {
    return calculateNights() * (apartment?.price_per_day || 0);
  }, [calculateNights, apartment?.price_per_day]);

  const nights = calculateNights();

  useEffect(() => {
    const handleEscape = (e) => {
      if (e.key === 'Escape') {
        onClose();
      }
    };
    document.addEventListener('keydown', handleEscape);
    return () => document.removeEventListener('keydown', handleEscape);
  }, [onClose]);

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto" role="dialog" aria-modal="true">
      <div className="flex items-center justify-center min-h-screen px-4 pt-4 pb-20 text-center sm:block sm:p-0">
        <div
          className="fixed inset-0 transition-opacity bg-gray-500 bg-opacity-75"
          onClick={onClose}
          aria-hidden="true"
        />
        
        <div className="inline-block w-full max-w-lg p-6 my-8 overflow-hidden text-left align-middle transition-all transform bg-white shadow-xl rounded-2xl sm:my-8 sm:align-middle relative">
          <button
            onClick={onClose}
            className="absolute top-4 right-4 text-gray-400 hover:text-gray-600 transition-colors"
            aria-label="Закрыть"
          >
            <X className="h-6 w-6" />
          </button>

          <div className="mb-6">
            <h2 className="text-2xl font-bold text-gray-900">
              Бронирование квартиры
            </h2>
            <p className="text-gray-600 mt-1">{apartment?.title}</p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-5">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  <Calendar className="inline h-4 w-4 mr-1" />
                  Заезд
                </label>
                <DatePicker
                  selected={checkIn}
                  onChange={(date) => setCheckIn(date)}
                  selectsStart
                  startDate={checkIn}
                  endDate={checkOut}
                  minDate={new Date()}
                  filterDate={(date) => !isDateDisabled(date)}
                  locale={ru}
                  dateFormat="dd.MM.yyyy"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  placeholderText="Выберите дату"
                  isClearable
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  <Calendar className="inline h-4 w-4 mr-1" />
                  Выезд
                </label>
                <DatePicker
                  selected={checkOut}
                  onChange={(date) => setCheckOut(date)}
                  selectsEnd
                  startDate={checkIn}
                  endDate={checkOut}
                  minDate={checkIn || new Date()}
                  filterDate={(date) => !isDateDisabled(date)}
                  locale={ru}
                  dateFormat="dd.MM.yyyy"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  placeholderText="Выберите дату"
                  isClearable
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                <User className="inline h-4 w-4 mr-1" />
                Ваше имя
              </label>
              <input
                type="text"
                value={guestName}
                onChange={(e) => setGuestName(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                placeholder="Иван Иванов"
                maxLength={100}
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                <Phone className="inline h-4 w-4 mr-1" />
                Телефон
              </label>
              <input
                type="tel"
                value={guestPhone}
                onChange={handlePhoneChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                placeholder="+7 (999) 123-45-67"
                maxLength={18}
              />
            </div>

            {nights > 0 && (
              <div className="bg-gray-50 p-4 rounded-lg">
                <div className="flex justify-between text-sm mb-2">
                  <span className="text-gray-600">
                    {nights} {nights === 1 ? 'ночь' : nights < 5 ? 'ночи' : 'ночей'}
                  </span>
                  <span className="text-gray-900">
                    {apartment?.price_per_day.toLocaleString('ru-RU')} ₽ × {nights}
                  </span>
                </div>
                <div className="flex justify-between text-lg font-bold border-t border-gray-200 pt-2">
                  <span className="text-gray-900">Итого:</span>
                  <span className="text-blue-600">
                    {calculateTotal().toLocaleString('ru-RU')} ₽
                  </span>
                </div>
              </div>
            )}

            {error && (
              <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm">
                {error}
              </div>
            )}

            <button
              type="submit"
              disabled={loading}
              className="w-full py-3 px-4 bg-red-500 hover:bg-red-600 disabled:bg-gray-400 text-white font-semibold rounded-lg shadow-md hover:shadow-lg transition-all duration-200"
            >
              {loading ? 'Отправка...' : 'Отправить заявку'}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}