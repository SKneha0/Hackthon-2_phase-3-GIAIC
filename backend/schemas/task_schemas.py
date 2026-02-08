from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class TaskCreate(BaseModel):
    """Schema for creating a new task"""
    title: str = Field(..., min_length=1, max_length=255, description="Title of the new task")
    description: Optional[str] = Field(default=None, max_length=1000, description="Description of the new task")
    completed: bool = Field(default=False, description="Initial completion status of the task")

class TaskUpdate(BaseModel):
    """Schema for updating an existing task"""
    title: Optional[str] = Field(default=None, min_length=1, max_length=255, description="New title (if changing)")
    description: Optional[str] = Field(default=None, max_length=1000, description="New description (if changing)")
    completed: Optional[bool] = Field(default=None, description="New completion status")

class TaskResponse(BaseModel):
    """Schema for returning task data"""
    id: int
    title: str
    description: Optional[str]
    completed: bool
    user_id: int
    created_at: datetime
    updated_at: datetime

class TaskListQuery(BaseModel):
    """Schema for query parameters when listing tasks"""
    status: str = Field(default="all", description="Filter by completion status", pattern=r"^(all|pending|completed)$")
    sort: str = Field(default="created", description="Sort order", pattern=r"^(created|title)$")