import { useState, useEffect } from 'react';
import { sendMessage, getConversations, getConversationMessages } from '@/lib/chatService';
import { ChatMessage } from '@/lib/chatService';

export interface UseChatProps {
  userId: string;
}

export interface UseChatReturn {
  messages: ChatMessage[];
  isLoading: boolean;
  isError: boolean;
  sendMessage: (message: string) => Promise<void>;
  resetConversation: () => void;
}

/**
 * Custom hook for chat functionality
 * @param props.userId The user ID
 * @returns Chat state and functions
 */
export const useChat = ({ userId }: UseChatProps): UseChatReturn => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isError, setIsError] = useState(false);
  const [conversationId, setConversationId] = useState<number | null>(null);

  const handleSendMessage = async (message: string) => {
    if (!message.trim() || !userId) return;

    try {
      setIsLoading(true);
      setIsError(false);

      // Add user message to UI immediately
      const userMessage: ChatMessage = {
        id: Date.now(),
        role: 'user',
        content: message,
        timestamp: new Date()
      };

      setMessages(prev => [...prev, userMessage]);

      // Send message to API
      const response = await sendMessage(userId, message, conversationId || undefined);

      // Add AI response to UI
      const aiMessage: ChatMessage = {
        id: response.message_id,
        role: 'assistant',
        content: response.response,
        timestamp: new Date()
      };

      setMessages(prev => [...prev, aiMessage]);
      setConversationId(response.conversation_id);
    } catch (error) {
      console.error('Failed to send message:', error);
      setIsError(true);
    } finally {
      setIsLoading(false);
    }
  };

  const resetConversation = () => {
    setMessages([]);
    setConversationId(null);
  };

  return {
    messages,
    isLoading,
    isError,
    sendMessage: handleSendMessage,
    resetConversation
  };
};