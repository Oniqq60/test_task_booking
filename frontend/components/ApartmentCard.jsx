'use client';

import Image from 'next/image';
import { Wifi, ParkingCircle, MapPin } from 'lucide-react';
import { useState, useMemo } from 'react';
import BookingModal from './BookingModal';

export default function ApartmentCard({ apartment }) {
  const [isBookingModalOpen, setIsBookingModalOpen] = useState(false);

  // Мемоизируем URL фото
  const photoUrl = useMemo(() => {
    const mainPhoto = apartment?.photos?.[0];
    return mainPhoto ? `/api/photos/${mainPhoto.id}` : null;
  }, [apartment?.photos]);

  // Мемоизируем цену
  const formattedPrice = useMemo(() => {
    return apartment?.price_per_day?.toLocaleString('ru-RU') || '0';
  }, [apartment?.price_per_day]);

  if (!apartment) return null;

  return (
    <>
      <div className="bg-white rounded-xl shadow-md hover:shadow-xl transition-shadow duration-300 overflow-hidden border border-gray-100">
        {/* Photo */}
        <div className="relative h-64 w-full overflow-hidden bg-gray-200">
          {photoUrl ? (
            <Image
              src={photoUrl}
              alt={apartment.title || 'Apartment'}
              fill
              className="object-cover hover:scale-105 transition-transform duration-300"
              unoptimized
              loading="lazy"
              sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
            />
          ) : (
            <div className="flex items-center justify-center h-full text-gray-400">
              Нет фото
            </div>
          )}
        </div>

        {/* Content */}
        <div className="p-5">
          {/* Title */}
          <h3 className="text-lg font-semibold text-gray-900 mb-2 line-clamp-1">
            {apartment.title}
          </h3>

          {/* Amenities */}
          <div className="flex items-center gap-2 mb-3">
            <div className="flex items-center justify-center w-8 h-8 rounded-full bg-blue-100 text-blue-600">
              <Wifi className="h-4 w-4" />
            </div>
            <div className="flex items-center justify-center w-8 h-8 rounded-full bg-blue-100 text-blue-600">
              <ParkingCircle className="h-4 w-4" />
            </div>
          </div>

          {/* Address */}
          <div className="flex items-start gap-1.5 mb-4 text-gray-600">
            <MapPin className="h-4 w-4 mt-0.5 flex-shrink-0 text-blue-500" />
            <span className="text-sm line-clamp-2">{apartment.address}</span>
          </div>

          {/* Price and Book button */}
          <div className="flex items-center justify-between">
            <div>
              <span className="text-2xl font-bold text-gray-900">
                {formattedPrice}
              </span>
              <span className="text-sm text-gray-500 ml-1">₽/сутки</span>
            </div>
            <button
              onClick={() => setIsBookingModalOpen(true)}
              className="px-6 py-2.5 bg-red-500 hover:bg-red-600 text-white font-medium rounded-full transition-colors duration-200 shadow-md hover:shadow-lg transform hover:-translate-y-0.5"
              aria-label={`Забронировать ${apartment.title}`}
            >
              Забронировать
            </button>
          </div>
        </div>
      </div>

      {/* Booking Modal */}
      {isBookingModalOpen && (
        <BookingModal
          apartment={apartment}
          onClose={() => setIsBookingModalOpen(false)}
        />
      )}
    </>
  );
}