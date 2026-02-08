"""
MCP-compatible tools for task management operations
"""

from typing import List, Dict, Any
import json
from datetime import datetime
from pydantic import BaseModel, Field
from sqlmodel import Session, select
from ..models.task_model import Task as TaskModel  # Renamed to avoid conflict with Pydantic model
# Removed unused import


class TaskSchema(BaseModel):
    id: int
    title: str
    description: str
    completed: bool
    user_id: str
    created_at: str
    updated_at: str


def _serialize_task(task: TaskModel) -> TaskSchema:
    """Helper to convert SQLModel task to serializable format."""
    return TaskSchema(
        id=task.id,
        title=task.title,
        description=task.description,
        completed=task.completed,
        user_id=str(task.user_id),
        created_at=str(task.created_at),
        updated_at=str(task.updated_at)
    )


async def add_task(title: str, description: str = "", user_id: str = None) -> Dict[str, Any]:
    """
    Add a new task for the user

    Args:
        title: The title of the task
        description: The description of the task
        user_id: The ID of the user who owns the task

    Returns:
        Dictionary containing the created task
    """
    from db import get_session
    from sqlalchemy.exc import SQLAlchemyError

    try:
        # Use the dependency injection approach to get a session
        # We'll get the session from the global application context or as passed in
        from fastapi import Depends
        from db import engine

        # Create a new database session
        with Session(engine) as session:
            # Create new task instance
            # Convert user_id to int, handling both string and numeric formats
            # For testing purposes, we'll hash the string user_id to get a consistent integer
            if isinstance(user_id, str) and user_id.isdigit():
                actual_user_id = int(user_id)
            elif isinstance(user_id, int):
                actual_user_id = user_id
            elif isinstance(user_id, str):
                # For string user_ids (like "test_user"), create a consistent hash
                actual_user_id = abs(hash(user_id)) % (10**8)  # Use positive hash modulo large number
            else:
                actual_user_id = 0  # Default fallback

            new_task = TaskModel(
                title=title,
                description=description,
                user_id=actual_user_id,
                completed=False
            )

            # Add and commit the new task to the database
            session.add(new_task)
            session.commit()
            session.refresh(new_task)  # Refresh to get the auto-generated ID

            # Return the created task
            serialized_task = _serialize_task(new_task)
            return {
                "success": True,
                "task": serialized_task.dict()
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


async def list_tasks(status: str = "all", user_id: str = None) -> Dict[str, Any]:
    """
    List tasks for the user with optional filtering

    Args:
        status: Filter by status ('all', 'pending', 'completed')
        user_id: The ID of the user whose tasks to list

    Returns:
        Dictionary containing the list of tasks
    """
    from db import engine
    from sqlalchemy.exc import SQLAlchemyError

    try:
        # Create a new database session
        with Session(engine) as session:
            # Convert user_id to int, handling both string and numeric formats
            # For testing purposes, we'll hash the string user_id to get a consistent integer
            if isinstance(user_id, str) and user_id.isdigit():
                actual_user_id = int(user_id)
            elif isinstance(user_id, int):
                actual_user_id = user_id
            elif isinstance(user_id, str):
                # For string user_ids (like "test_user"), create a consistent hash
                actual_user_id = abs(hash(user_id)) % (10**8)  # Use positive hash modulo large number
            else:
                actual_user_id = 0  # Default fallback

            # Build query based on user_id and status filter
            query = select(TaskModel).where(TaskModel.user_id == actual_user_id)

            if status == "pending":
                query = query.where(TaskModel.completed == False)
            elif status == "completed":
                query = query.where(TaskModel.completed == True)

            # Execute query
            tasks = session.exec(query).all()

            # Serialize tasks
            serialized_tasks = [_serialize_task(task) for task in tasks]

            # Format response for chatbot
            if not tasks:
                if status == "pending":
                    formatted_response = "You have no pending tasks."
                elif status == "completed":
                    formatted_response = "You have no completed tasks."
                else:
                    formatted_response = "You have no tasks."
            else:
                task_list = []
                for i, task in enumerate(serialized_tasks, 1):
                    status_str = "✓ Completed" if task.completed else "○ Pending"
                    # Format with clear ID inclusion that the AI should preserve
                    task_list.append(f"{i}. {task.title} (ID: {task.id})")
                    if task.description:
                        task_list.append(f"   Description: {task.description}")

                formatted_response = f"You currently have {len(tasks)} task{'s' if len(tasks) != 1 else ''}:\n" + "\n".join(task_list)

            return {
                "success": True,
                "tasks": [task.dict() for task in serialized_tasks],
                "formatted_response": formatted_response
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


async def complete_task(task_id: int, user_id: str = None) -> Dict[str, Any]:
    """
    Mark a task as completed

    Args:
        task_id: The ID of the task to mark as completed
        user_id: The ID of the user who owns the task

    Returns:
        Dictionary indicating success status
    """
    from db import engine
    from sqlalchemy.exc import SQLAlchemyError

    try:
        # Create a new database session
        with Session(engine) as session:
            # Convert user_id to int, handling both string and numeric formats
            # For testing purposes, we'll hash the string user_id to get a consistent integer
            if isinstance(user_id, str) and user_id.isdigit():
                actual_user_id = int(user_id)
            elif isinstance(user_id, int):
                actual_user_id = user_id
            elif isinstance(user_id, str):
                # For string user_ids (like "test_user"), create a consistent hash
                actual_user_id = abs(hash(user_id)) % (10**8)  # Use positive hash modulo large number
            else:
                actual_user_id = 0  # Default fallback

            # Find the task belonging to the user
            statement = select(TaskModel).where(
                TaskModel.id == task_id,
                TaskModel.user_id == actual_user_id
            )
            task = session.exec(statement).first()

            if not task:
                return {
                    "success": False,
                    "error": "Task not found or does not belong to user"
                }

            # Update task completion status
            task.completed = True
            task.update_timestamp()
            session.add(task)
            session.commit()
            session.refresh(task)

            # Return the updated task
            serialized_task = _serialize_task(task)
            return {
                "success": True,
                "task": serialized_task.dict(),
                "message": f"Task {task_id} marked as completed"
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


async def delete_task(task_id: int, user_id: str = None) -> Dict[str, Any]:
    """
    Delete a task

    Args:
        task_id: The ID of the task to delete
        user_id: The ID of the user who owns the task

    Returns:
        Dictionary indicating success status
    """
    from db import engine
    from sqlalchemy.exc import SQLAlchemyError

    try:
        # Create a new database session
        with Session(engine) as session:
            # Convert user_id to int, handling both string and numeric formats
            # For testing purposes, we'll hash the string user_id to get a consistent integer
            if isinstance(user_id, str) and user_id.isdigit():
                actual_user_id = int(user_id)
            elif isinstance(user_id, int):
                actual_user_id = user_id
            elif isinstance(user_id, str):
                # For string user_ids (like "test_user"), create a consistent hash
                actual_user_id = abs(hash(user_id)) % (10**8)  # Use positive hash modulo large number
            else:
                actual_user_id = 0  # Default fallback

            # Find the task belonging to the user
            statement = select(TaskModel).where(
                TaskModel.id == task_id,
                TaskModel.user_id == actual_user_id
            )
            task = session.exec(statement).first()

            if not task:
                return {
                    "success": False,
                    "error": "Task not found or does not belong to user"
                }

            # Delete the task
            session.delete(task)
            session.commit()

            return {
                "success": True,
                "task_id": task_id,
                "message": f"Task {task_id} deleted"
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


async def update_task(task_id: int, title: str = None, description: str = None,
                      completed: bool = None, user_id: str = None) -> Dict[str, Any]:
    """
    Update a task

    Args:
        task_id: The ID of the task to update
        title: New title for the task
        description: New description for the task
        completed: New completion status for the task
        user_id: The ID of the user who owns the task

    Returns:
        Dictionary containing the updated task
    """
    from db import engine
    from sqlalchemy.exc import SQLAlchemyError

    try:
        # Create a new database session
        with Session(engine) as session:
            # Convert user_id to int, handling both string and numeric formats
            # For testing purposes, we'll hash the string user_id to get a consistent integer
            if isinstance(user_id, str) and user_id.isdigit():
                actual_user_id = int(user_id)
            elif isinstance(user_id, int):
                actual_user_id = user_id
            elif isinstance(user_id, str):
                # For string user_ids (like "test_user"), create a consistent hash
                actual_user_id = abs(hash(user_id)) % (10**8)  # Use positive hash modulo large number
            else:
                actual_user_id = 0  # Default fallback

            # Find the task belonging to the user
            statement = select(TaskModel).where(
                TaskModel.id == task_id,
                TaskModel.user_id == actual_user_id
            )
            task = session.exec(statement).first()

            if not task:
                return {
                    "success": False,
                    "error": "Task not found or does not belong to user"
                }

            # Update task properties if provided
            if title is not None:
                task.title = title
            if description is not None:
                task.description = description
            if completed is not None:
                task.completed = completed

            task.update_timestamp()
            session.add(task)
            session.commit()
            session.refresh(task)

            # Return the updated task
            serialized_task = _serialize_task(task)
            
            # Create formatted response for chatbot
            status_str = "✓ Completed" if task.completed else "○ Pending"
            formatted_response = f"Task updated successfully!\n[ID: {task.id}] [{status_str}] {task.title}"
            if task.description:
                formatted_response += f"\nDescription: {task.description}"
            
            return {
                "success": True,
                "task": serialized_task.dict(),
                "formatted_response": formatted_response
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }