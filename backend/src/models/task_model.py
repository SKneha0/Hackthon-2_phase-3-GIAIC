"""
Task model for the todo application
Re-exports the Task model from the main models module to avoid duplication
"""
from models import Task, TaskBase

__all__ = ['Task', 'TaskBase']
