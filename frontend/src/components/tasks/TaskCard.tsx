import React from 'react';
import { Card, CardContent } from '@/components/ui/Card';
import { Checkbox } from '@/components/ui/Checkbox';
import { Button } from '@/components/ui/Button';
import { Trash2, Edit3 } from 'lucide-react';
import { cn } from '@/lib/utils';

type Task = {
  id: string;
  title: string;
  description?: string;
  completed: boolean;
  dueDate?: string;
  createdAt: string;
  updatedAt: string;
};

type TaskCardProps = {
  task: Task;
  onToggleComplete: (id: string) => void;
  onEdit: (id: string) => void;
  onDelete: (id: string) => void;
};

const TaskCard: React.FC<TaskCardProps> = ({ task, onToggleComplete, onEdit, onDelete }) => {
  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
  };

  return (
    <Card
      className={cn(
        'transition-all duration-300 hover:shadow-lg hover:translate-y-[-2px] motion-reduce:transition-none',
        {
          'opacity-70': task.completed,
          'bg-secondary/20': task.completed,
        }
      )}
      role="listitem"
      aria-label={`Task: ${task.title}, ${task.completed ? 'completed' : 'pending'}`}
    >
      <CardContent className="p-4 flex items-start gap-3">
        <div className="pt-1">
          <Checkbox
            id={`task-${task.id}`}
            checked={task.completed}
            onCheckedChange={() => onToggleComplete(task.id)}
            aria-label={`Mark task "${task.title}" as ${task.completed ? 'incomplete' : 'complete'}`}
          />
        </div>

        <div className="flex-1 min-w-0">
          <div className="flex items-start justify-between">
            <h3
              className={cn(
                'font-medium text-lg break-words transition-colors duration-300',
                {
                  'line-through text-muted-foreground': task.completed,
                }
              )}
            >
              {task.title}
            </h3>

            <div className="flex gap-1 ml-2" role="group" aria-label="Task actions">
              <Button
                variant="ghost"
                size="sm"
                onClick={() => onEdit(task.id)}
                aria-label={`Edit task: ${task.title}`}
                className="transition-colors duration-200"
              >
                <Edit3 className="h-4 w-4" aria-hidden="true" />
              </Button>
              <Button
                variant="ghost"
                size="sm"
                onClick={() => onDelete(task.id)}
                aria-label={`Delete task: ${task.title}`}
                className="transition-colors duration-200"
              >
                <Trash2 className="h-4 w-4" aria-hidden="true" />
              </Button>
            </div>
          </div>

          {task.description && (
            <p
              className={cn(
                'text-sm text-muted-foreground mt-1 transition-colors duration-300',
                {
                  'line-through': task.completed,
                }
              )}
            >
              {task.description}
            </p>
          )}

          {task.dueDate && (
            <div className="mt-2 text-xs">
              <span
                className={cn(
                  'px-2 py-1 rounded-full transition-colors duration-300',
                  {
                    'bg-destructive/20 text-destructive':
                      new Date(task.dueDate) < new Date(),
                    'bg-secondary text-secondary-foreground':
                      new Date(task.dueDate) >= new Date(),
                  }
                )}
                aria-label={`Due date: ${formatDate(task.dueDate)}${
                  new Date(task.dueDate) < new Date() ? ', overdue' : ''
                }`}
              >
                Due: {formatDate(task.dueDate)}
              </span>
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );
};

const MemoizedTaskCard = React.memo(TaskCard);
export { MemoizedTaskCard as TaskCard, type Task };