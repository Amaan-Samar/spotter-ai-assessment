import axios from 'axios';

// Use local backend URL (Django running on port 8000)
const API_URL = 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const planTrip = async (tripData) => {
  const response = await api.post('/plan-trip/', tripData);
  return response.data;
};

export const getTrips = async () => {
  const response = await api.get('/trips/');
  return response.data;
};

export const getTrip = async (id) => {
  const response = await api.get(`/trips/${id}/`);
  return response.data;
};