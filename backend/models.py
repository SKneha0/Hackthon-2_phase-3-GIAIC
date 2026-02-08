from sqlmodel import SQLModel, Field, create_engine
from typing import Optional
from datetime import datetime
from pydantic import validator
import uuid

class UserBase(SQLModel):
    """Base class for User with common fields"""
    email: str = Field(unique=True, index=True)
    name: Optional[str] = Field(default=None)

class User(UserBase, table=True):
    """User model for authentication"""
    id: Optional[int] = Field(default=None, primary_key=True)
    password_hash: str = Field(sa_column_kwargs={"nullable": False})
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    def update_timestamp(self):
        """Update the updated_at timestamp"""
        self.updated_at = datetime.utcnow()

class TaskBase(SQLModel):
    """Base class for Task with common fields"""
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)

class Task(TaskBase, table=True):
    """Task model representing a user's todo item"""
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(index=True)  # Foreign key to users table (will be linked in the database)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    # Add index for completed field to optimize queries
    __table_args__ = {'sqlite_autoincrement': True}

    def update_timestamp(self):
        """Update the updated_at timestamp"""
        self.updated_at = datetime.utcnow()