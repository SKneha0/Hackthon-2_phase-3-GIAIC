from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
import os
from dotenv import load_dotenv
from typing import Dict, Optional
from pydantic import BaseModel

# Load environment variables
load_dotenv()

# Initialize JWT settings
JWT_ALGORITHM = "HS256"
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET", "secret")

# Initialize security scheme
security = HTTPBearer()

class CurrentUser(BaseModel):
    """Model for current user data extracted from JWT"""
    user_id: int
    email: Optional[str] = None
    name: Optional[str] = None

def get_current_user(token: HTTPAuthorizationCredentials = Depends(security)) -> CurrentUser:
    """
    Dependency to get current user from JWT token
    Extracts user_id from JWT token using BETTER_AUTH_SECRET
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Decode the JWT token
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[JWT_ALGORITHM])

        # Extract user_id from the token
        user_id: int = payload.get("userId") or payload.get("sub") or payload.get("id")

        if user_id is None:
            raise credentials_exception

        # Additional claims that might be present
        email = payload.get("email", None)
        name = payload.get("name", None)

        # Return user data
        return CurrentUser(user_id=user_id, email=email, name=name)

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception:
        raise credentials_exception