import axios from "axios";

const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000/api";

const instance = axios.create({
  baseURL: API_BASE,
});

instance.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

export default {
  post: (path, data) => instance.post(path, data).then(r => r.data),
  get: (path, params) => instance.get(path, { params }).then(r => r.data),
  put: (path, data) => instance.put(path, data).then(r => r.data),
  del: (path) => instance.delete(path).then(r => r.data),
};
