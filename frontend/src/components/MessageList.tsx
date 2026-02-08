import React from 'react';

interface Message {
  id: number;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

interface MessageListProps {
  messages: Message[];
  showTypingIndicator?: boolean;
}

const MessageList: React.FC<MessageListProps> = ({ messages, showTypingIndicator = false }) => {
  return (
    <div className="space-y-4">
      {messages.length === 0 && !showTypingIndicator ? (
        <div className="text-center text-gray-500 py-8">
          <p>No messages yet. Start a conversation!</p>
        </div>
      ) : (
        <>
          {messages.map((message) => (
            <div 
              key={message.id} 
              className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-[80%] rounded-lg px-4 py-2 ${
                  message.role === 'user'
                    ? 'bg-blue-500 text-white rounded-br-none dark:bg-blue-600'
                    : 'bg-gray-200 text-gray-800 rounded-bl-none dark:bg-gray-600 dark:text-gray-100'
                }`}
              >
                <div className="whitespace-pre-wrap">{message.content}</div>
                <div
                  className={`text-xs mt-1 ${
                    message.role === 'user' ? 'text-blue-200 dark:text-blue-300' : 'text-gray-500 dark:text-gray-300'
                  }`}
                >
                  {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                </div>
              </div>
            </div>
          ))}
          
          {showTypingIndicator && (
            <div className="flex justify-start">
              <div className="bg-gray-200 text-gray-800 rounded-lg px-4 py-2 rounded-bl-none dark:bg-gray-600 dark:text-gray-100">
                <div className="flex space-x-1">
                  <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce dark:bg-gray-300"></div>
                  <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce dark:bg-gray-300" style={{ animationDelay: '0.2s' }}></div>
                  <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce dark:bg-gray-300" style={{ animationDelay: '0.4s' }}></div>
                </div>
              </div>
            </div>
          )}
        </>
      )}
    </div>
  );
};

export default MessageList;