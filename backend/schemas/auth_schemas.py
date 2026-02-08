from pydantic import BaseModel, Field
from pydantic.networks import EmailStr
from typing import Optional

class SignupRequest(BaseModel):
    """Schema for signup request"""
    email: EmailStr
    password: str = Field(..., min_length=8, description="Password must be at least 8 characters")
    name: Optional[str] = Field(default=None, max_length=100)


class SigninRequest(BaseModel):
    """Schema for signin request"""
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """Schema for user response"""
    id: int
    email: EmailStr
    name: Optional[str] = None


class AuthResponse(BaseModel):
    """Schema for authentication response"""
    success: bool
    message: str
    user: Optional[UserResponse] = None
    token: Optional[str] = None


class UserProfileResponse(BaseModel):
    """Schema for user profile response"""
    id: int
    email: EmailStr
    name: Optional[str] = None
    createdAt: str