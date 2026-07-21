import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'https://jsonplaceholder.typicode.com',
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 5000,
});

// Request interceptor — attaches a mock auth token to every outgoing request
apiClient.interceptors.request.use((config) => {
  config.headers.Authorization = 'Bearer mock-student-portal-token';
  return config;
});

// Response interceptor — unwraps response.data so callers never see the Axios
// wrapper, and normalises errors into a standard { message, statusCode } shape
// so components never deal with raw HTTP status codes.
apiClient.interceptors.response.use(
  (response) => response.data,
  (error) => {
    const statusCode = error.response?.status ?? 0;
    const message = error.response
      ? `Request failed with status ${statusCode}`
      : error.message || 'Network error';
    return Promise.reject({ message, statusCode });
  }
);

export default apiClient;
