import axios from 'axios';

export const API_BASE_URL = import.meta.env.VITE_API_URL !== undefined && import.meta.env.VITE_API_URL !== '' 
    ? import.meta.env.VITE_API_URL 
    : '';

const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

api.interceptors.request.use((config) => {
    const token = localStorage.getItem('token');
    if (token && config.headers) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

export default api;
