import axios from 'axios';

// Create an axios instance with default configuration
export const apiClient = axios.create({
  baseURL:  'https://neha112-todo-backend-agent.hf.space/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add a request interceptor to include the token in all requests
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Add a response interceptor to handle errors globally
apiClient.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    // Handle specific error cases
    if (error.response?.status === 401) {
      // Token might be expired, redirect to login
      localStorage.removeItem('token');
      window.location.href = '/signin';
    }

    return Promise.reject(error);
  }
);

export default apiClient;