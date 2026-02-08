"""
MCP-compatible tools for user information operations
"""

from typing import Dict, Any
from pydantic import BaseModel
from sqlmodel import Session, select
from ..models.user_model import User
from db import engine


class UserProfileSchema(BaseModel):
    user_id: str
    email: str
    name: str
    created_at: str


async def get_user_profile(user_id: str) -> Dict[str, Any]:
    """
    Get user profile information

    Args:
        user_id: The ID of the user whose profile to retrieve

    Returns:
        Dictionary containing the user profile information
    """
    from ..models.user_model import User  # Import the User model
    from sqlalchemy.exc import SQLAlchemyError

    try:
        # Create a new database session
        with Session(engine) as session:
            # Convert user_id to int, handling both string and numeric formats
            if isinstance(user_id, str) and user_id.isdigit():
                actual_user_id = int(user_id)
            elif isinstance(user_id, int):
                actual_user_id = user_id
            else:
                actual_user_id = 0  # Default fallback
                
            # Find the user by ID
            statement = select(User).where(User.id == actual_user_id)
            user = session.exec(statement).first()

            if not user:
                return {
                    "success": False,
                    "error": "User not found"
                }

            # Create and return user profile
            user_profile = UserProfileSchema(
                user_id=str(user.id),
                email=user.email,
                name=user.name or "",
                created_at=str(user.created_at)
            )

            return {
                "success": True,
                "profile": user_profile.dict()
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }