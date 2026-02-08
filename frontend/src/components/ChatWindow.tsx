import React, { useState, useRef, useEffect } from 'react';
import MessageList from './MessageList';
import MessageInput from './MessageInput';
import { X } from 'lucide-react';
import { sendChatMessage } from '../services/api';

interface ChatWindowProps {
  isOpen: boolean;
  onClose: () => void;
  userId: string;
}

interface Message {
  id: number;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

const ChatWindow: React.FC<ChatWindowProps> = ({ isOpen, onClose, userId }) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [showTypingIndicator, setShowTypingIndicator] = useState(false);
  const [currentConversationId, setCurrentConversationId] = useState<number | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Function to send a message via API
  const sendMessage = async (message: string) => {
    if (!message.trim() || isLoading) return;

    setIsLoading(true);
    setShowTypingIndicator(true);

    try {
      // Send message to backend
      const response = await sendChatMessage(userId, message, currentConversationId || undefined);

      // Update conversation ID if it's a new conversation
      if (!currentConversationId) {
        setCurrentConversationId(response.conversation_id);
      }

      // Add user message
      const userMessage: Message = {
        id: Date.now(),
        role: 'user',
        content: message,
        timestamp: new Date(),
      };

      // Add AI response message
      const aiMessage: Message = {
        id: response.message_id,
        role: 'assistant',
        content: response.response,
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, userMessage, aiMessage]);
    } catch (error: any) {
      console.error('Error sending message:', error);

      // Determine error type and create appropriate message
      let errorMessageContent = 'Sorry, I encountered an error processing your request. Please try again.';
      
      if (error.code === 'ECONNABORTED' || error.code === 'ERR_NETWORK') {
        errorMessageContent = 'Connection lost. Please check your internet connection and try again.';
      } else if (error.response?.status === 401) {
        errorMessageContent = 'Session expired. Please log in again.';
      } else if (error.response?.status === 403) {
        errorMessageContent = 'Access denied. Please contact support if this persists.';
      } else if (error.response?.status === 429) {
        errorMessageContent = 'Too many requests. Please wait a moment before sending another message.';
      } else if (error.response?.data?.detail) {
        // Use error message from server if available
        errorMessageContent = error.response.data.detail;
      }

      // Add error message
      const errorMessage: Message = {
        id: Date.now(),
        role: 'assistant',
        content: errorMessageContent,
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
      setShowTypingIndicator(false);
    }
  };

  // Scroll to bottom when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  return (
    <>
      {isOpen && (
        <div 
          className={`fixed bottom-24 right-6 w-96 h-[500px] bg-white dark:bg-gray-800 rounded-lg shadow-xl border border-gray-200 dark:border-gray-700 flex flex-col z-50 transition-all duration-300 ease-in-out transform ${
            isOpen ? 'translate-y-0 opacity-100' : 'translate-y-4 opacity-0 hidden'
          }`}
        >
          {/* Header */}
          <div className="bg-blue-600 dark:bg-blue-700 text-white p-4 rounded-t-lg flex justify-between items-center">
            <h3 className="font-semibold">AI Chat Assistant</h3>
            <button 
              onClick={onClose}
              className="text-white hover:text-gray-200 focus:outline-none"
              aria-label="Close chat"
            >
              <X size={20} />
            </button>
          </div>

          {/* Messages */}
          <div className="flex-1 overflow-y-auto p-4 bg-gray-50 dark:bg-gray-700">
            <MessageList messages={messages} showTypingIndicator={showTypingIndicator} />
            <div ref={messagesEndRef} />
          </div>

          {/* Input */}
          <div className="border-t border-gray-200 dark:border-gray-700 p-4 bg-white dark:bg-gray-800">
            <MessageInput 
              onSendMessage={sendMessage} 
              isLoading={isLoading} 
              userId={userId} 
            />
          </div>
        </div>
      )}
    </>
  );
};

export default ChatWindow;