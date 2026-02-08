from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from sqlmodel import Session, select
from datetime import datetime

from models import Task, TaskBase
from schemas.task_schemas import TaskCreate, TaskUpdate, TaskResponse, TaskListQuery
from auth import get_current_user, CurrentUser
from db import get_session

router = APIRouter()

@router.get("/tasks", response_model=List[TaskResponse])
def get_tasks(
    status_filter: str = Query("all", description="Filter by completion status"),
    sort_by: str = Query("created", description="Sort by creation date or title"),
    current_user: CurrentUser = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get user's tasks with filtering and sorting options.
    Filters tasks by current_user.id to ensure user isolation.
    """
    # Build query with user filter
    query = select(Task).where(Task.user_id == current_user.user_id)

    # Apply status filter
    if status_filter == "pending":
        query = query.where(Task.completed == False)
    elif status_filter == "completed":
        query = query.where(Task.completed == True)
    # "all" includes both completed and pending

    # Apply sorting
    if sort_by == "title":
        query = query.order_by(Task.title)
    else:  # Default or "created"
        query = query.order_by(Task.created_at.desc())

    tasks = session.exec(query).all()
    return tasks


@router.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    task_data: TaskCreate,
    current_user: CurrentUser = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Create a new task for the user.
    Associates the new task with current_user.id.
    """
    # Create new task instance with user association
    task = Task(
        title=task_data.title,
        description=task_data.description,
        completed=task_data.completed,
        user_id=current_user.user_id  # Associate with current user
    )

    session.add(task)
    session.commit()
    session.refresh(task)

    return task


@router.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    current_user: CurrentUser = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get a specific task.
    Validates that the task belongs to the current_user.
    Returns 403 if task doesn't belong to the user.
    """
    # Query for the task with user filter
    task = session.exec(
        select(Task).where(Task.id == task_id).where(Task.user_id == current_user.user_id)
    ).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied or task not found"
        )

    return task


@router.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_update: TaskUpdate,
    current_user: CurrentUser = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Update a specific task.
    Validates that the task belongs to the current_user.
    Returns 403 if task doesn't belong to the user.
    """
    # Get the existing task with user filter
    task = session.exec(
        select(Task).where(Task.id == task_id).where(Task.user_id == current_user.user_id)
    ).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied or task not found"
        )

    # Update the task fields
    if task_update.title is not None:
        task.title = task_update.title
    if task_update.description is not None:
        task.description = task_update.description
    if task_update.completed is not None:
        task.completed = task_update.completed

    # Update the updated_at timestamp
    task.update_timestamp()

    session.add(task)
    session.commit()
    session.refresh(task)

    return task


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    current_user: CurrentUser = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Delete a specific task.
    Validates that the task belongs to the current_user.
    Returns 403 if task doesn't belong to the user.
    """
    # Get the task with user filter
    task = session.exec(
        select(Task).where(Task.id == task_id).where(Task.user_id == current_user.user_id)
    ).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied or task not found"
        )

    session.delete(task)
    session.commit()

    return


@router.patch("/tasks/{task_id}/complete", response_model=TaskResponse)
def toggle_task_completion(
    task_id: int,
    current_user: CurrentUser = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Toggle task completion status.
    Validates that the task belongs to the current_user.
    """
    # Get the task with user filter
    task = session.exec(
        select(Task).where(Task.id == task_id).where(Task.user_id == current_user.user_id)
    ).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied or task not found"
        )

    # Toggle the completion status
    task.completed = not task.completed
    # Update the updated_at timestamp
    task.update_timestamp()

    session.add(task)
    session.commit()
    session.refresh(task)

    return task