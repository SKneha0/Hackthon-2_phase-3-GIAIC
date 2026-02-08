from sqlmodel import create_engine, Session
from typing import Generator
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv("NEON_DB_URL", "sqlite:///./test.db")

# Create the database engine
engine = create_engine(DATABASE_URL, echo=False)

def get_session() -> Generator[Session, None, None]:
    """Dependency to get database session"""
    with Session(engine) as session:
        yield session

def create_db_and_tables():
    """Create database tables on startup"""
    # Import all models to ensure they are registered
    from models import SQLModel, User, Task
    from src.models.conversation_model import Conversation, Message

    SQLModel.metadata.create_all(engine)