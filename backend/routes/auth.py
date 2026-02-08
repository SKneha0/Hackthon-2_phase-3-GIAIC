from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from datetime import datetime, timedelta
import jwt
import os
import bcrypt
from dotenv import load_dotenv

from models import User, UserBase
from schemas.auth_schemas import SignupRequest, SigninRequest, AuthResponse, UserResponse, UserProfileResponse
from db import get_session
from auth import get_current_user

# Load environment variables
load_dotenv()

# Initialize JWT settings
JWT_ALGORITHM = "HS256"
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET", "secret")

# Bcrypt configuration
BCRYPT_ROUNDS = 12

router = APIRouter(prefix="/auth", tags=["auth"])

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password"""
    # Ensure the plain password doesn't exceed bcrypt's 72-byte limit
    if len(plain_password.encode('utf-8')) > 72:
        plain_password = plain_password.encode('utf-8')[:72].decode('utf-8', errors='ignore')

    # Encode both passwords to bytes for comparison
    plain_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    
    return bcrypt.checkpw(plain_bytes, hashed_bytes)

def get_password_hash(password: str) -> str:
    """Hash a plain password, truncating if longer than 72 bytes (bcrypt limit)"""
    # Bcrypt has a maximum password length of 72 bytes
    # Truncate if necessary to prevent ValueError
    if len(password.encode('utf-8')) > 72:
        # Safely truncate to 72 bytes while preserving UTF-8 character integrity
        password = password.encode('utf-8')[:72].decode('utf-8', errors='ignore')

    # Encode password to bytes for bcrypt
    password_bytes = password.encode('utf-8')
    
    # Generate the hash
    salt = bcrypt.gensalt(rounds=BCRYPT_ROUNDS)
    hashed = bcrypt.hashpw(password_bytes, salt)
    
    # Return as string
    return hashed.decode('utf-8')

def create_access_token(data: dict, expires_delta: timedelta = None):
    """Create a JWT access token"""
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=7)  # Default 7 days

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt

@router.post("/signup", response_model=AuthResponse)
def signup(signup_data: SignupRequest, session: Session = Depends(get_session)):
    """
    Create a new user account.
    Creates user in the 'users' table with hashed password.
    """
    # Check if user already exists
    existing_user = session.exec(select(User).where(User.email == signup_data.email)).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists"
        )

    # Hash the password
    password_hash = get_password_hash(signup_data.password)

    # Create new user
    user = User(
        email=signup_data.email,
        name=signup_data.name,
        password_hash=password_hash
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    # Create user response object
    user_response = UserResponse(
        id=user.id,
        email=user.email,
        name=user.name
    )

    # Return success response (no token here - Better Auth handles client-side JWT)
    return AuthResponse(
        success=True,
        message="User created successfully",
        user=user_response,
        token=None  # No token on signup, frontend should handle login after
    )


@router.post("/signin", response_model=AuthResponse)
def signin(signin_data: SigninRequest, session: Session = Depends(get_session)):
    """
    Authenticate user and return JWT token.
    Verifies password against hashed value in DB.
    Returns JWT token signed with BETTER_AUTH_SECRET.
    """
    # Find user by email
    user = session.exec(select(User).where(User.email == signin_data.email)).first()

    if not user or not verify_password(signin_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create JWT token with user data
    access_token_expires = timedelta(days=7)  # 7 days expiration
    token_data = {
        "sub": str(user.id),  # Subject: user ID
        "email": user.email,
        "name": user.name,
        "iat": datetime.utcnow(),  # Issued at
    }

    access_token = create_access_token(
        data=token_data,
        expires_delta=access_token_expires
    )

    # Update user's last login time
    user.update_timestamp()
    session.add(user)
    session.commit()

    # Create user response object
    user_response = UserResponse(
        id=user.id,
        email=user.email,
        name=user.name
    )

    # Return success response with token - match frontend expectation
    return AuthResponse(
        success=True,
        message="Login successful",
        user=user_response,
        token=access_token
    )


@router.get("/me", response_model=UserProfileResponse)
def get_current_user_profile(current_user = Depends(get_current_user), session: Session = Depends(get_session)):
    """
    Protected endpoint to get current user's profile information.
    Requires valid JWT token via get_current_user dependency.
    Returns basic profile data for the authenticated user.
    """
    # Query the user from the database using the user_id from the JWT token
    user = session.exec(select(User).where(User.id == current_user.user_id)).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Return the user profile data in the required format
    return UserProfileResponse(
        id=user.id,
        email=user.email,
        name=user.name,
        createdAt=user.created_at.isoformat()
    )