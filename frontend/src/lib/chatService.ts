import apiClient from '@/lib/api';

export interface ChatMessage {
  id: number;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

export interface ChatResponse {
  response: string;
  conversation_id: number;
  message_id: number;
}

export interface Conversation {
  id: number;
  title: string;
  created_at: string;
  updated_at: string;
}

/**
 * Send a message to the chat API
 * @param userId The user ID
 * @param message The message to send
 * @param conversationId Optional conversation ID to continue an existing conversation
 * @returns The chat response
 */
export const sendMessage = async (
  userId: string,
  message: string,
  conversationId?: number
): Promise<ChatResponse> => {
  try {
    const response = await apiClient.post<ChatResponse>(`/${userId}/chat`, {
      message,
      conversation_id: conversationId
    });
    return response.data;
  } catch (error) {
    console.error('Failed to send message:', error);
    throw error;
  }
};

/**
 * Get user's conversations
 * @param userId The user ID
 * @returns List of conversations
 */
export const getConversations = async (userId: string): Promise<Conversation[]> => {
  try {
    const response = await apiClient.get<Conversation[]>(`/${userId}/conversations`);
    return response.data;
  } catch (error) {
    console.error('Failed to get conversations:', error);
    throw error;
  }
};

/**
 * Get messages for a specific conversation
 * @param userId The user ID
 * @param conversationId The conversation ID
 * @returns List of messages
 */
export const getConversationMessages = async (
  userId: string,
  conversationId: number
): Promise<ChatMessage[]> => {
  try {
    const response = await apiClient.get<ChatMessage[]>(
      `/${userId}/conversations/${conversationId}/messages`
    );
    return response.data.map(msg => ({
      ...msg,
      timestamp: new Date(msg.timestamp)
    }));
  } catch (error) {
    console.error('Failed to get conversation messages:', error);
    throw error;
  }
};