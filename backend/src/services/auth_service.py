"""
Authentication service to validate JWT and extract user_id
"""
from typing import Optional
from datetime import datetime, timezone
import jwt
from fastapi import HTTPException, status
from ..models.user_model import User
from pydantic import BaseModel


class TokenData(BaseModel):
    user_id: str
    username: Optional[str] = None


def validate_jwt_token(token: str, secret: str) -> TokenData:
    """
    Validate JWT token and extract user information

    Args:
        token: The JWT token to validate
        secret: The secret used to decode the token

    Returns:
        TokenData containing user information

    Raises:
        HTTPException: If token is invalid or expired
    """
    try:
        payload = jwt.decode(token, secret, algorithms=["HS256"])
        user_id: str = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials"
            )

        token_data = TokenData(user_id=user_id)
        return token_data

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )


def extract_user_id_from_token(token: str, secret: str) -> str:
    """
    Extract user_id from JWT token

    Args:
        token: The JWT token
        secret: The secret used to decode the token

    Returns:
        The user_id extracted from the token
    """
    token_data = validate_jwt_token(token, secret)
    return token_data.user_id