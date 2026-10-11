import axios, { AxiosError } from 'axios';

const baseURL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const apiClient = axios.create({
  baseURL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,
});

apiClient.interceptors.response.use(
  (response) => response,
  (error: AxiosError<{ error?: string; message?: string; details?: any }>) => {
    let friendlyMessage = 'An unexpected error occurred. Please try again.';

    if (error.response?.data) {
      const data = error.response.data;
      if (data.message) {
        friendlyMessage = data.message;
      } else if (data.error) {
        friendlyMessage = `Error: ${data.error}`;
      }
    } else if (error.message) {
      friendlyMessage = error.message;
    }

    return Promise.reject(new Error(friendlyMessage));
  }
);
