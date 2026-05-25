import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || '';
const API_V1_STR = process.env.NEXT_PUBLIC_API_V1_STR || '/api';

const api = axios.create({
  baseURL: `${API_URL}${API_V1_STR}`,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const apartmentsApi = {
  getAll: async (params = {}) => {
    const response = await api.get('/apartments', { params });
    return response.data;
  },
  
  getBookedPeriods: async (apartmentId) => {
    const response = await api.get(`/apartments/${apartmentId}/booked-periods`);
    return response.data;
  },
};

export const bookingsApi = {
  create: async (booking) => {
    await api.post('/bookings', booking);
  },
};

export const photosApi = {
  getUrl: (photoId) => {
    return `${API_URL}${API_V1_STR}/photos/${photoId}`;
  },
};

export default api;