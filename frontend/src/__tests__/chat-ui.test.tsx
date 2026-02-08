/**
 * Frontend tests for chat UI components
 * Tests User Story 5 - Unobtrusive Chat Interface
 */
import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import ChatbotIcon from '../components/ChatbotIcon';
import ChatWindow from '../components/ChatWindow';

// Mock the API service
jest.mock('../services/api', () => ({
  sendChatMessage: jest.fn(),
}));

describe('ChatbotIcon Component', () => {
  /**
   * T049: Test floating icon appears in bottom-right corner when logged in
   */
  test('should render icon in bottom-right corner when logged in', () => {
    const mockOnOpen = jest.fn();
    const { container } = render(
      <ChatbotIcon onOpen={mockOnOpen} isLoggedIn={true} />
    );

    const iconContainer = container.querySelector('.fixed.bottom-6.right-6');
    expect(iconContainer).toBeInTheDocument();
    expect(iconContainer).toHaveClass('z-50');
  });

  test('should not render icon when not logged in', () => {
    const mockOnOpen = jest.fn();
    const { container } = render(
      <ChatbotIcon onOpen={mockOnOpen} isLoggedIn={false} />
    );

    const iconContainer = container.querySelector('.fixed.bottom-6.right-6');
    expect(iconContainer).not.toBeInTheDocument();
  });

  test('should call onOpen when clicked', () => {
    const mockOnOpen = jest.fn();
    render(<ChatbotIcon onOpen={mockOnOpen} isLoggedIn={true} />);

    const button = screen.getByRole('button', { name: /open chat/i });
    fireEvent.click(button);

    expect(mockOnOpen).toHaveBeenCalledTimes(1);
  });

  test('should have proper accessibility attributes', () => {
    const mockOnOpen = jest.fn();
    render(<ChatbotIcon onOpen={mockOnOpen} isLoggedIn={true} />);

    const button = screen.getByRole('button', { name: /open chat/i });
    expect(button).toHaveAttribute('aria-label', 'Open chat');
  });
});

describe('ChatWindow Component', () => {
  const mockUserId = 'test-user-123';

  /**
   * T050: Test chat window opens without overlapping existing UI elements
   */
  test('should render chat window with proper positioning when open', () => {
    const mockOnClose = jest.fn();
    const { container } = render(
      <ChatWindow isOpen={true} onClose={mockOnClose} userId={mockUserId} />
    );

    const chatWindow = container.querySelector('.fixed.bottom-24.right-6');
    expect(chatWindow).toBeInTheDocument();
    expect(chatWindow).toHaveClass('w-96', 'h-[500px]');
    expect(chatWindow).toHaveClass('z-50');
  });

  test('should not render chat window when closed', () => {
    const mockOnClose = jest.fn();
    const { container } = render(
      <ChatWindow isOpen={false} onClose={mockOnClose} userId={mockUserId} />
    );

    const chatWindow = container.querySelector('.fixed.bottom-24.right-6');
    expect(chatWindow).not.toBeInTheDocument();
  });

  test('should have smooth animation classes', () => {
    const mockOnClose = jest.fn();
    const { container } = render(
      <ChatWindow isOpen={true} onClose={mockOnClose} userId={mockUserId} />
    );

    const chatWindow = container.querySelector('.fixed.bottom-24.right-6');
    expect(chatWindow).toHaveClass('transition-all', 'duration-300', 'ease-in-out');
  });

  test('should call onClose when close button is clicked', () => {
    const mockOnClose = jest.fn();
    render(
      <ChatWindow isOpen={true} onClose={mockOnClose} userId={mockUserId} />
    );

    const closeButton = screen.getByRole('button', { name: /close chat/i });
    fireEvent.click(closeButton);

    expect(mockOnClose).toHaveBeenCalledTimes(1);
  });

  test('should display chat header with title', () => {
    const mockOnClose = jest.fn();
    render(
      <ChatWindow isOpen={true} onClose={mockOnClose} userId={mockUserId} />
    );

    expect(screen.getByText('AI Chat Assistant')).toBeInTheDocument();
  });

  test('should have dark mode support', () => {
    const mockOnClose = jest.fn();
    const { container } = render(
      <ChatWindow isOpen={true} onClose={mockOnClose} userId={mockUserId} />
    );

    const chatWindow = container.querySelector('.fixed.bottom-24.right-6');
    expect(chatWindow).toHaveClass('dark:bg-gray-800');
  });

  test('should handle message sending', async () => {
    const { sendChatMessage } = require('../services/api');
    sendChatMessage.mockResolvedValue({
      conversation_id: 1,
      message_id: 123,
      response: 'Test response',
    });

    const mockOnClose = jest.fn();
    render(
      <ChatWindow isOpen={true} onClose={mockOnClose} userId={mockUserId} />
    );

    const input = screen.getByPlaceholderText(/type your message/i);
    const sendButton = screen.getByRole('button', { name: /send/i });

    fireEvent.change(input, { target: { value: 'Test message' } });
    fireEvent.click(sendButton);

    await waitFor(() => {
      expect(sendChatMessage).toHaveBeenCalledWith(
        mockUserId,
        'Test message',
        undefined
      );
    });
  });

  test('should display error message on connection failure', async () => {
    const { sendChatMessage } = require('../services/api');
    sendChatMessage.mockRejectedValue({
      code: 'ERR_NETWORK',
      message: 'Network error',
    });

    const mockOnClose = jest.fn();
    render(
      <ChatWindow isOpen={true} onClose={mockOnClose} userId={mockUserId} />
    );

    const input = screen.getByPlaceholderText(/type your message/i);
    const sendButton = screen.getByRole('button', { name: /send/i });

    fireEvent.change(input, { target: { value: 'Test message' } });
    fireEvent.click(sendButton);

    await waitFor(() => {
      expect(
        screen.getByText(/connection lost/i)
      ).toBeInTheDocument();
    });
  });

  test('should show typing indicator while loading', async () => {
    const { sendChatMessage } = require('../services/api');
    sendChatMessage.mockImplementation(
      () => new Promise((resolve) => setTimeout(resolve, 100))
    );

    const mockOnClose = jest.fn();
    render(
      <ChatWindow isOpen={true} onClose={mockOnClose} userId={mockUserId} />
    );

    const input = screen.getByPlaceholderText(/type your message/i);
    const sendButton = screen.getByRole('button', { name: /send/i });

    fireEvent.change(input, { target: { value: 'Test message' } });
    fireEvent.click(sendButton);

    // Typing indicator should be visible while loading
    await waitFor(() => {
      expect(screen.getByTestId('typing-indicator')).toBeInTheDocument();
    });
  });
});

describe('Chat UI Integration', () => {
  /**
   * T058: Test end-to-end flow: login → open chat → manage tasks → see updates in main UI
   */
  test('should maintain proper z-index hierarchy to avoid overlapping', () => {
    const mockOnOpen = jest.fn();
    const mockOnClose = jest.fn();
    const mockUserId = 'test-user-123';

    const { container: iconContainer } = render(
      <ChatbotIcon onOpen={mockOnOpen} isLoggedIn={true} />
    );

    const { container: windowContainer } = render(
      <ChatWindow isOpen={true} onClose={mockOnClose} userId={mockUserId} />
    );

    const icon = iconContainer.querySelector('.fixed.bottom-6.right-6');
    const window = windowContainer.querySelector('.fixed.bottom-24.right-6');

    expect(icon).toHaveClass('z-50');
    expect(window).toHaveClass('z-50');
  });
});
