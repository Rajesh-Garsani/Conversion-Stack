import axios from "axios";

const environment = import.meta.env || {};
export const normalizeApiError = (error) => ({
  message: error.response?.data?.errors || error.response?.data?.message || (error.code === "ECONNABORTED" ? "The request timed out." : "The service is temporarily unavailable."),
  status: error.response?.status || 0,
});

const api = axios.create({ baseURL: environment.VITE_API_BASE_URL || "http://127.0.0.1:8000/api", timeout: 12000, headers: { Accept: "application/json" } });
api.interceptors.response.use((response) => response, (error) => Promise.reject(normalizeApiError(error)));
export const getBootstrap = () => api.get("/bootstrap/").then((r) => r.data.data);
export const getService = (slug) => api.get(`/services/${slug}/`).then((r) => r.data);
export const getProject = (slug) => api.get(`/projects/${slug}/`).then((r) => r.data);
export const getPage = (slug) => api.get(`/pages/${slug}/`).then((r) => r.data);
export const submitInquiry = (payload) => api.post("/contact/", payload).then((r) => r.data);
export default api;
