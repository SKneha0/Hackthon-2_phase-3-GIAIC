import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { apiClient } from '@/lib/api';

type User = {
  id: number;
  email: string;
  name: string | null;
  createdAt?: string;
};

type AuthState = {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
};

export function useAuth() {
  const [authState, setAuthState] = useState<AuthState>({
    user: null,
    token: null,
    isAuthenticated: false,
    isLoading: true,
  });
  const router = useRouter();

  // Check if user is authenticated on initial load
  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      // Verify token and get user data
      apiClient.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      verifyTokenAndSetUser(token);
    } else {
      setAuthState({
        user: null,
        token: null,
        isAuthenticated: false,
        isLoading: false,
      });
    }
  }, []);

  const verifyTokenAndSetUser = async (token: string) => {
    try {
      const response = await apiClient.get('/auth/me');
      // The /auth/me endpoint returns the user profile directly, not wrapped in a user object
      const userData = {
        id: response.data.id,
        email: response.data.email,
        name: response.data.name,
        createdAt: response.data.createdAt
      };

      setAuthState({
        user: userData,
        token,
        isAuthenticated: true,
        isLoading: false,
      });
    } catch (error) {
      // Token is invalid, clear it
      localStorage.removeItem('token');
      delete apiClient.defaults.headers.common['Authorization'];
      setAuthState({
        user: null,
        token: null,
        isAuthenticated: false,
        isLoading: false,
      });
    }
  };

  const login = async (email: string, password: string) => {
    try {
      const response = await apiClient.post('/auth/signin', {
        email,
        password,
      });

      const { user, token } = response.data; // response.data is the AuthResponse

      // Store token in localStorage
      if (token) {
        localStorage.setItem('token', token);

        // Set authorization header
        apiClient.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      }

      setAuthState({
        user: user,
        token: token || null,
        isAuthenticated: true,
        isLoading: false,
      });

      router.push('/dashboard');
      return { success: true };
    } catch (error: any) {
      return {
        success: false,
        error: error.response?.data?.detail || error.response?.data?.message || 'Login failed'
      };
    }
  };

  const register = async (email: string, password: string, name: string) => {
    try {
      const response = await apiClient.post('/auth/signup', {
        email,
        password,
        name,
      });

      const { user, token } = response.data; // response.data is the AuthResponse

      // Store token in localStorage
      if (token) {
        localStorage.setItem('token', token);

        // Set authorization header
        apiClient.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      }

      setAuthState({
        user: user,
        token: token || null,
        isAuthenticated: true,
        isLoading: false,
      });

      router.push('/dashboard');
      return { success: true };
    } catch (error: any) {
      return {
        success: false,
        error: error.response?.data?.detail || error.response?.data?.message || 'Registration failed'
      };
    }
  };

  const logout = () => {
    // Clear token from localStorage
    localStorage.removeItem('token');

    // Remove authorization header
    delete apiClient.defaults.headers.common['Authorization'];

    setAuthState({
      user: null,
      token: null,
      isAuthenticated: false,
      isLoading: false,
    });

    router.push('/');
  };

  return {
    ...authState,
    login,
    register,
    logout,
  };
}