'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuthContext } from '@/providers/AuthProvider';
import { Button } from '@/components/ui/Button';
import { TaskList, type Task } from '@/components/tasks/TaskList';
import { EmptyState } from '@/components/tasks/EmptyState';
import { Modal } from '@/components/ui/Modal';
import { TaskForm } from '@/components/tasks/TaskForm';
import { Sidebar } from '@/components/navigation/Sidebar';
import { MobileNav } from '@/components/navigation/MobileNav';
import { Plus, Sun, Moon, RefreshCw } from 'lucide-react';
import { useTheme } from 'next-themes';
import { apiClient } from '@/lib/api';

// Chat components
import ChatbotIcon from '@/components/chat/ChatbotIcon';
import ChatWindow from '@/components/chat/ChatWindow';
import { useChat } from '@/hooks/useChat';

const DashboardPage = () => {
  const { user, logout, isAuthenticated, isLoading: authIsLoading } = useAuthContext();
  const router = useRouter();
  const { theme, setTheme } = useTheme();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showAddTaskModal, setShowAddTaskModal] = useState(false);
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [isChatOpen, setIsChatOpen] = useState(false);

  // Initialize chat hook
  const {
    messages,
    isLoading: isChatLoading,
    isError: isChatError,
    sendMessage: sendChatMessage,
    resetConversation
  } = useChat({ userId: user?.id || '' });

  useEffect(() => {
    if (!authIsLoading && !isAuthenticated) {
      router.push('/login');
    }
  }, [isAuthenticated, authIsLoading, router]);

  // Fetch tasks from API
  const fetchTasks = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await apiClient.get('/tasks');
      setTasks(response.data.tasks || response.data);
    } catch (err) {
      console.error('Failed to fetch tasks:', err);
      setError('Failed to load tasks. Please try again later.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (isAuthenticated) {
      fetchTasks();
    }
  }, [isAuthenticated]);

  const handleAddTask = () => {
    setEditingTask(null);
    setShowAddTaskModal(true);
  };

  // Show loading state while auth status is being determined
  if (authIsLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900"></div>
      </div>
    );
  }

  // If not authenticated, we're redirecting via useEffect, so return nothing
  if (!isAuthenticated) {
    return null;
  }

  const handleEditTask = (id: string) => {
    const task = tasks.find(t => t.id === id);
    if (task) {
      setEditingTask(task);
      setShowAddTaskModal(true);
    }
  };

  const handleDeleteTask = async (id: string) => {
    try {
      await apiClient.delete(`/tasks/${id}`);
      setTasks(tasks.filter(task => task.id !== id));
    } catch (err) {
      console.error('Failed to delete task:', err);
      alert('Failed to delete task. Please try again.');
    }
  };

  const handleToggleComplete = async (id: string) => {
    try {
      const task = tasks.find(t => t.id === id);
      if (task) {
        const updatedTask = { ...task, completed: !task.completed };
        await apiClient.put(`/tasks/${id}`, updatedTask);
        setTasks(tasks.map(task =>
          task.id === id ? { ...task, completed: !task.completed } : task
        ));
      }
    } catch (err) {
      console.error('Failed to update task:', err);
      alert('Failed to update task. Please try again.');
    }
  };

  const handleSubmitTask = async (formData: { title: string; description: string; dueDate: string }) => {
    try {
      if (editingTask) {
        // Update existing task
        const response = await apiClient.put(`/tasks/${editingTask.id}`, {
          ...formData,
          completed: editingTask.completed
        });
        setTasks(tasks.map(task =>
          task.id === editingTask.id ? response.data : task
        ));
      } else {
        // Add new task
        const response = await apiClient.post('/tasks', formData);
        setTasks([...tasks, response.data]);
      }
      setShowAddTaskModal(false);
    } catch (err) {
      console.error('Failed to save task:', err);
      alert('Failed to save task. Please try again.');
    }
  };

  const navItems = [
    { label: 'Dashboard', href: '/dashboard' },
  ];

  return (
    <div className="flex min-h-screen">
      <Sidebar
        navItems={navItems}
        isLoggedIn={!!isAuthenticated}
        onLogout={logout}
      />

      <div className="flex-1 flex flex-col">
        {/* Top Navigation */}
        <header className="border-b p-4 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <MobileNav
              navItems={navItems}
              isLoggedIn={!!isAuthenticated}
              onLogout={logout}
            />
            <h1 className="text-xl font-bold hidden md:block">Dashboard</h1>
          </div>

          <div className="flex items-center gap-2">
            <Button
              variant="outline"
              size="icon"
              onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
              aria-label="Toggle theme"
            >
              {theme === 'dark' ? <Sun className="h-5 w-5" /> : <Moon className="h-5 w-5" />}
            </Button>

            <div className="hidden md:block">
              <p className="text-sm font-medium">{user?.name || 'User'}</p>
              <p className="text-xs text-muted-foreground">{user?.email}</p>
            </div>
          </div>
        </header>

        {/* Main Content */}
        <main className="flex-1 p-4 md:p-6">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-2xl font-bold">My Tasks</h2>
            <div className="flex gap-2">
              <Button
                variant="outline"
                onClick={fetchTasks}
                disabled={loading}
              >
                <RefreshCw className={`mr-2 h-4 w-4 ${loading ? 'animate-spin' : ''}`} />
                Refresh
              </Button>
              <Button onClick={handleAddTask}>
                <Plus className="mr-2 h-4 w-4" /> Add Task
              </Button>
            </div>
          </div>

          {tasks.length === 0 && !loading ? (
            <EmptyState
              title="No tasks yet"
              description="Get started by creating your first task"
              onButtonClick={handleAddTask}
              buttonText="Add Task"
            />
          ) : (
            <TaskList
              tasks={tasks}
              loading={loading}
              onToggleComplete={handleToggleComplete}
              onEdit={handleEditTask}
              onDelete={handleDeleteTask}
            />
          )}
        </main>

        {/* Chat Window */}
        <ChatWindow
          isOpen={isChatOpen}
          onClose={() => setIsChatOpen(false)}
          messages={messages}
          onSendMessage={sendChatMessage}
          isLoading={isChatLoading}
        />

        {/* Chat Icon - Only show when user is logged in */}
        {isAuthenticated && (
          <ChatbotIcon onClick={() => setIsChatOpen(true)} />
        )}
      </div>

      {/* Add/Edit Task Modal */}
      <Modal
        isOpen={showAddTaskModal}
        onClose={() => setShowAddTaskModal(false)}
        title={editingTask ? 'Edit Task' : 'Add New Task'}
      >
        <TaskForm
          task={editingTask || undefined}
          onSubmit={handleSubmitTask}
          onCancel={() => setShowAddTaskModal(false)}
          submitButtonText={editingTask ? 'Update Task' : 'Create Task'}
          autoFocusTitle={!editingTask}
        />
      </Modal>
    </div>
  );
};

export default DashboardPage;