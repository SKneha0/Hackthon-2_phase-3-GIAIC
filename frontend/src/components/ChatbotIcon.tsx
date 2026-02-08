import React, { useState, useEffect } from 'react';
import { Bot } from 'lucide-react';

interface ChatbotIconProps {
  onOpen: () => void;
  isLoggedIn: boolean;
}

const ChatbotIcon: React.FC<ChatbotIconProps> = ({ onOpen, isLoggedIn }) => {
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    // Only show the chatbot icon when the user is logged in
    setIsVisible(isLoggedIn);
  }, [isLoggedIn]);

  if (!isVisible) {
    return null;
  }

  return (
    <div className="fixed bottom-6 right-6 z-50">
      <button
        onClick={onOpen}
        className="bg-blue-600 hover:bg-blue-700 text-white rounded-full p-4 shadow-lg transition-all duration-300 transform hover:scale-105 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50 dark:bg-blue-700 dark:hover:bg-blue-800"
        aria-label="Open chat"
      >
        <Bot size={24} />
      </button>
    </div>
  );
};

export default ChatbotIcon;