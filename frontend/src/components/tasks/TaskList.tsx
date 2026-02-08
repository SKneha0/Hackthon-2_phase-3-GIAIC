import React, { memo } from 'react';
import { Task, TaskCard } from '@/components/tasks/TaskCard';
import { Skeleton } from '@/components/ui/Skeleton';

export type { Task };

type TaskListProps = {
  tasks: Task[];
  loading?: boolean;
  onToggleComplete: (id: string) => void;
  onEdit: (id: string) => void;
  onDelete: (id: string) => void;
};

const TaskListComponent: React.FC<TaskListProps> = ({
  tasks,
  loading = false,
  onToggleComplete,
  onEdit,
  onDelete
}) => {
  if (loading) {
    return (
      <div className="space-y-4">
        {[...Array(3)].map((_, idx) => (
          <div key={idx} className="flex gap-3 p-4">
            <Skeleton className="h-5 w-5 rounded-sm mt-1" />
            <div className="flex-1 space-y-2">
              <Skeleton className="h-5 w-3/4" />
              <Skeleton className="h-4 w-1/2" />
            </div>
          </div>
        ))}
      </div>
    );
  }

  if (tasks.length === 0) {
    return (
      <div className="text-center py-10 text-muted-foreground">
        <p>No tasks yet. Create your first task!</p>
      </div>
    );
  }

  return (
    <div className="space-y-3" role="list" aria-label="Task list">
      {tasks.map((task) => (
        <TaskCard
          key={task.id}
          task={task}
          onToggleComplete={onToggleComplete}
          onEdit={onEdit}
          onDelete={onDelete}
        />
      ))}
    </div>
  );
};

const TaskList = memo(TaskListComponent);
export { TaskList };