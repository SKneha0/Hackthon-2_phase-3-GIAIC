import axios, { AxiosResponse } from 'axios';

// Base API URL from environment or default to development server
const API_BASE_URL = process.env.NEXT_PUBLIC_BETTER_AUTH_URL || 'http://localhost:8000';

// Create axios instance with defaults
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000, // 30 seconds timeout
});

// Request interceptor to add auth token
apiClient.interceptors.request.use(
  (config) => {
    // Get token from wherever it's stored (localStorage, cookie, etc.)
    // This depends on your auth implementation
    const token = localStorage.getItem('auth_token'); // Adjust based on your auth system
    
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle common errors
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    // Handle specific error cases
    if (error.response?.status === 401) {
      // Token might be expired, redirect to login?
      console.error('Unauthorized access - token may be expired');
    } else if (error.response?.status === 403) {
      console.error('Forbidden access - user may not have permission');
    } else if (error.response?.status === 429) {
      console.error('Rate limit exceeded - too many requests');
    } else if (error.code === 'ECONNABORTED' || error.code === 'ERR_NETWORK') {
      console.error('Network error - connection lost or timed out');
    } else if (!error.response) {
      // Network error (server not reachable, etc.)
      console.error('Network error - unable to reach server');
    }
    
    return Promise.reject(error);
  }
);

// Chat API functions
interface ChatRequest {
  message: string;
  conversation_id?: number;
}

interface ChatResponse {
  response: string;
  conversation_id: number;
  message_id: number;
}

/**
 * Send a chat message to the backend
 */
export const sendChatMessage = async (
  userId: string,
  message: string,
  conversationId?: number
): Promise<ChatResponse> => {
  try {
    const response: AxiosResponse<ChatResponse> = await apiClient.post(
      `/api/${userId}/chat`,
      {
        message,
        conversation_id: conversationId,
      }
    );

    return response.data;
  } catch (error) {
    console.error('Error sending chat message:', error);
    throw error;
  }
};

/**
 * Get conversation history
 */
export const getConversationHistory = async (
  userId: string,
  conversationId: number
): Promise<any[]> => {
  try {
    const response = await apiClient.get(`/api/${userId}/conversations/${conversationId}/messages`);
    return response.data;
  } catch (error) {
    console.error('Error getting conversation history:', error);
    throw error;
  }
};

/**
 * Get user's conversations
 */
export const getUserConversations = async (userId: string): Promise<any[]> => {
  try {
    const response = await apiClient.get(`/api/${userId}/conversations`);
    return response.data;
  } catch (error) {
    console.error('Error getting user conversations:', error);
    throw error;
  }
};

export default apiClient;