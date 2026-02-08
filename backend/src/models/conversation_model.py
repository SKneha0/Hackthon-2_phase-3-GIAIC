from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional
from enum import Enum


class Conversation(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: str = Field()  # Store user_id as string from JWT
    title: str = Field(max_length=100)  # Limit title length
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to messages
    messages: list["Message"] = Relationship(back_populates="conversation")

    def generate_title_from_first_message(self, first_message_content: str):
        """
        Generate a title for the conversation based on the first message
        
        Args:
            first_message_content: The content of the first message in the conversation
        """
        # Take the first 50 characters of the first message and add "..." if longer
        if len(first_message_content) <= 50:
            self.title = first_message_content.strip()
        else:
            self.title = first_message_content[:47].strip() + "..."
        
        # Ensure title isn't empty
        if not self.title.strip():
            self.title = "New Conversation"


class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"


class Message(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversation.id")
    role: MessageRole
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to conversation
    conversation: Conversation = Relationship(back_populates="messages")