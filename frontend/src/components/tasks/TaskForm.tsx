import React, { useState, useEffect } from 'react';
import { Input } from '@/components/ui/Input';
import { Button } from '@/components/ui/Button';
import { Textarea } from '@/components/ui/Textarea';
import { Label } from '@/components/ui/Label';

type TaskFormData = {
  title: string;
  description: string;
  dueDate: string;
};

// Define a type for the task prop that matches what TaskForm expects
type FormTask = {
  title: string;
  description?: string;
  dueDate?: string;
};

type TaskFormProps = {
  task?: FormTask;
  onSubmit: (data: TaskFormData) => void;
  onCancel: () => void;
  submitButtonText?: string;
  autoFocusTitle?: boolean; // Whether to autofocus the title field
};

const TaskForm: React.FC<TaskFormProps> = ({
  task,
  onSubmit,
  onCancel,
  submitButtonText = 'Save Task',
  autoFocusTitle = false
}) => {
  const [formData, setFormData] = useState<TaskFormData>({
    title: task?.title || '',
    description: task?.description || '',
    dueDate: task?.dueDate || ''
  });

  const [errors, setErrors] = useState<Record<string, string>>({});

  useEffect(() => {
    if (task) {
      setFormData({
        title: task.title || '',
        description: task.description || '',
        dueDate: task.dueDate || ''
      });
    } else {
      setFormData({
        title: '',
        description: '',
        dueDate: ''
      });
    }
  }, [task]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { id, value } = e.target;
    setFormData(prev => ({ ...prev, [id]: value }));

    // Clear error when user starts typing
    if (errors[id]) {
      setErrors(prev => {
        const newErrors = { ...prev };
        delete newErrors[id];
        return newErrors;
      });
    }
  };

  const validateForm = (): boolean => {
    const newErrors: Record<string, string> = {};

    if (!formData.title.trim()) {
      newErrors.title = 'Title is required';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (!validateForm()) return;

    onSubmit(formData);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4" role="form" aria-label="Task form">
      <div className="space-y-2">
        <Label htmlFor="title">Title *</Label>
        <Input
          id="title"
          value={formData.title}
          onChange={handleChange}
          placeholder="Task title"
          className={errors.title ? 'border-red-500' : ''}
          required
          aria-invalid={!!errors.title}
          aria-describedby={errors.title ? "title-error" : undefined}
          autoFocus={autoFocusTitle}
        />
        {errors.title && (
          <p id="title-error" className="text-sm text-red-500">
            {errors.title}
          </p>
        )}
      </div>

      <div className="space-y-2">
        <Label htmlFor="description">Description</Label>
        <Textarea
          id="description"
          value={formData.description}
          onChange={handleChange}
          placeholder="Task description"
          rows={3}
          aria-describedby="description-help"
        />
        <p id="description-help" className="text-sm text-muted-foreground">
          Optional task description
        </p>
      </div>

      <div className="space-y-2">
        <Label htmlFor="dueDate">Due Date</Label>
        <Input
          id="dueDate"
          type="date"
          value={formData.dueDate}
          onChange={handleChange}
        />
      </div>

      <div className="flex justify-end gap-2 pt-2">
        <Button type="button" variant="outline" onClick={onCancel}>
          Cancel
        </Button>
        <Button type="submit">
          {submitButtonText}
        </Button>
      </div>
    </form>
  );
};

export { TaskForm };