/**
 * Axios HTTP Client Configuration
 * 
 * 配置 Axios 客戶端，處理所有 API 請求
 * baseURL 設為 /api，由 Vite 代理轉發至後端
 * 返回數據直接使用 res.data（後端不包裝 data.data 結構）
 */

import axios, { AxiosError, AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios';
import type { ApiError, ApiResponse } from '@/types/api';

// Base API URL (will be proxied by Vite)
const BASE_URL = '/api';

// Create Axios instance
const apiClient: AxiosInstance = axios.create({
  baseURL: BASE_URL,
  timeout: 30000, // 30 seconds
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request Interceptor
apiClient.interceptors.request.use(
  (config) => {
    // Add auth token if exists
    const token = localStorage.getItem('auth_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    
    console.log(`[API Request] ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error('[API Request Error]', error);
    return Promise.reject(error);
  }
);

// Response Interceptor
apiClient.interceptors.response.use(
  (response: AxiosResponse<ApiResponse<any>>) => {
    console.log(`[API Response] ${response.config.url} - ${response.status}`);
    return response;
  },
  (error: AxiosError<ApiError>) => {
    console.error('[API Response Error]', error);

    // Handle specific error codes
    if (error.response) {
      const { status, data } = error.response;

      switch (status) {
        case 401:
          // Unauthorized - redirect to login
          localStorage.removeItem('auth_token');
          window.location.href = '/login';
          break;
        case 403:
          // Forbidden
          console.error('Access denied');
          break;
        case 404:
          // Not found
          console.error('Resource not found');
          break;
        case 500:
          // Server error
          console.error('Server error:', data.error);
          break;
      }

      return Promise.reject({
        message: data.error || 'An error occurred',
        status,
        details: data.detail,
      });
    }

    // Network error
    if (error.request) {
      return Promise.reject({
        message: 'Network error - please check your connection',
        status: 0,
      });
    }

    return Promise.reject({
      message: error.message || 'Unknown error',
      status: 0,
    });
  }
);

// Generic API Methods
// 注意：後端直接返回數據，不包裹在 data.data 中，所以直接返回 res.data
export const api = {
  get: <T>(url: string, config?: AxiosRequestConfig) =>
    apiClient.get<T>(url, config).then((res) => res.data),

  post: <T>(url: string, data?: any, config?: AxiosRequestConfig) =>
    apiClient.post<T>(url, data, config).then((res) => res.data),

  put: <T>(url: string, data?: any, config?: AxiosRequestConfig) =>
    apiClient.put<T>(url, data, config).then((res) => res.data),

  delete: <T>(url: string, config?: AxiosRequestConfig) =>
    apiClient.delete<T>(url, config).then((res) => res.data),

  patch: <T>(url: string, data?: any, config?: AxiosRequestConfig) =>
    apiClient.patch<T>(url, data, config).then((res) => res.data),
};

export default apiClient;
