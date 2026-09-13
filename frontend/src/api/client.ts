import axios from "axios";
import { useAuthStore } from "../store/authStore";

// En Docker: se inyecta por variable de entorno de build (VITE_API_URL)
// apuntando al contenedor backend-api (ej: http://backend-api:8001 a nivel interno,
// o https://tu-dominio/api si va todo detrás de un mismo reverse proxy).
const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8005";

export const api = axios.create({
  baseURL: API_URL,
});

api.interceptors.request.use((config) => {
  const token = useAuthStore.getState().token;
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      useAuthStore.getState().logout();
      window.location.href = "/login";
    }
    return Promise.reject(error);
  }
);
