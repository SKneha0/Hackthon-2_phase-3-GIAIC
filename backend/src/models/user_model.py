"""
User model for the todo application
Re-exports the User model from the main models module to avoid duplication
"""
from models import User, UserBase

__all__ = ['User', 'UserBase']
