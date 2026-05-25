"use client";

import { useState, useEffect } from 'react';
import Header from '../components/Header';
import ApartmentCard from '../components/ApartmentCard';
import { apartmentsApi } from '../lib/api';

export default function Home() {
  const [apartments, setApartments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');

  const fetchApartments = async (cityFilter = '') => {
    setLoading(true);
    try {
      const params = cityFilter ? { city: cityFilter } : {};
      const data = await apartmentsApi.getAll(params);
      setApartments(data);
    } catch (error) {
      console.error("Failed to fetch apartments", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchApartments();
  }, []);

  const handleSearch = (query) => {
    setSearchQuery(query);
    fetchApartments(query);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Header onSearch={handleSearch} />

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-6">
          <h2 className="text-3xl font-bold text-gray-900">
            {searchQuery ? `Результаты поиска: "${searchQuery}"` : 'Доступные квартиры'}
          </h2>
          <p className="text-gray-600 mt-2">
            Найдено {apartments.length} квартир
          </p>
        </div>

        {loading ? (
          <div className="text-center py-20">
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
            <p className="mt-4 text-gray-600">Загрузка...</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {apartments.map((apt) => (
              <ApartmentCard key={apt.id} apartment={apt} />
            ))}
            {apartments.length === 0 && !loading && (
              <div className="col-span-full text-center text-gray-500 py-10">
                <p className="text-lg">Квартиры не найдены</p>
                <p className="text-sm mt-2">Попробуйте изменить поисковый запрос</p>
              </div>
            )}
          </div>
        )}
      </main>
    </div>
  );
}