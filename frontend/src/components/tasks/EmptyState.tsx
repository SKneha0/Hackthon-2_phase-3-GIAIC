import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Plus } from 'lucide-react';

type EmptyStateProps = {
  title: string;
  description: string;
  buttonText?: string;
  onButtonClick?: () => void;
};

const EmptyState: React.FC<EmptyStateProps> = ({
  title,
  description,
  buttonText = 'Add Task',
  onButtonClick
}) => {
  return (
    <Card className="text-center">
      <CardHeader>
        <CardTitle className="text-2xl font-light">{title}</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="max-w-md mx-auto">
          <div className="mx-auto bg-muted rounded-full w-16 h-16 flex items-center justify-center mb-4">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-8 h-8 text-muted-foreground">
              <path strokeLinecap="round" strokeLinejoin="round" d="M9 12.75L11.25 15 15 9.75m-3-7.036A11.959 11.959 0 013.598 6 11.99 11.99 0 003 9.749c0 5.592 3.824 10.29 9 11.623 5.176-1.332 9-6.03 9-11.622 0-1.31-.21-2.571-.598-3.751h-.152c-3.196 0-6.1-1.248-8.25-3.285z" />
            </svg>
          </div>
          <p className="text-muted-foreground mb-6">{description}</p>
          {onButtonClick && (
            <Button onClick={onButtonClick}>
              <Plus className="mr-2 h-4 w-4" /> {buttonText}
            </Button>
          )}
        </div>
      </CardContent>
    </Card>
  );
};

export { EmptyState };