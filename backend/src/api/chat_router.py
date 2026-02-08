"""
API router for chat endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from typing import Dict, Any, Optional
from pydantic import BaseModel
from ..services.auth_service import extract_user_id_from_token
from ..services.cohere_runner import CohereRunner
from ..services.tool_executor import ToolExecutor
from db import get_session
from sqlmodel import Session
from ..models.conversation_model import Conversation, Message, MessageRole
import os
from datetime import datetime
import logging


# Set up logging
logger = logging.getLogger(__name__)


router = APIRouter(prefix="/api", tags=["chat"])


class ChatRequest(BaseModel):
    """Request model for chat endpoint"""
    message: str
    conversation_id: Optional[int] = None

    class Config:
        schema_extra = {
            "example": {
                "message": "Add task: Buy groceries",
                "conversation_id": 1
            }
        }


class ChatResponse(BaseModel):
    """Response model for chat endpoint"""
    response: str
    conversation_id: int
    message_id: int

    class Config:
        schema_extra = {
            "example": {
                "response": "I've added the task 'Buy groceries' to your list.",
                "conversation_id": 1,
                "message_id": 123
            }
        }


@router.post(
    "/{user_id}/chat",
    response_model=ChatResponse,
    summary="Send a chat message to the AI assistant",
    description="""
    Send a message to the AI chatbot and receive a response with tool execution capabilities.

    The chatbot can:
    - Create, list, complete, delete, and update tasks using natural language
    - Retrieve user profile information
    - Support multilingual queries (English and Urdu)
    - Maintain conversation history across sessions

    **Authentication**: Requires valid JWT token in Authorization header

    **Rate Limiting**: Maximum 10 requests per minute per user

    **Example Requests**:
    - "Add task: Buy groceries"
    - "Show my pending tasks"
    - "Complete the first task"
    - "Who am I?"
    - "Mera email kya hai?" (Urdu)
    """,
    responses={
        200: {
            "description": "Successful response with AI-generated message",
            "content": {
                "application/json": {
                    "example": {
                        "response": "I've added the task 'Buy groceries' to your list.",
                        "conversation_id": 1,
                        "message_id": 123
                    }
                }
            }
        },
        404: {
            "description": "Conversation not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Conversation not found"}
                }
            }
        },
        429: {
            "description": "Rate limit exceeded",
            "content": {
                "application/json": {
                    "example": {"detail": "Too many requests. Please wait before sending another message."}
                }
            }
        },
        500: {
            "description": "Internal server error",
            "content": {
                "application/json": {
                    "example": {"detail": "Error processing chat request"}
                }
            }
        }
    }
)
async def chat_endpoint(
    user_id: str,
    request: ChatRequest,
    db: Session = Depends(get_session)
):
    """
    Chat endpoint that handles user messages and returns AI responses
    with tool calling capabilities.
    """
    logger.info(f"Received chat request from user {user_id} with message: {request.message[:50]}...")
    
    # Validate that the user_id in the path matches the authenticated user
    # In a real implementation, we would extract the user_id from JWT
    # For now, we'll assume it's validated at the middleware level

    try:
        # Load conversation history if provided
        conversation = None
        conversation_history = []

        if request.conversation_id:
            # Try to load existing conversation
            conversation = db.query(Conversation).filter(
                Conversation.id == request.conversation_id,
                Conversation.user_id == user_id
            ).first()

            if not conversation:
                logger.warning(f"Conversation {request.conversation_id} not found for user {user_id}")
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Conversation not found"
                )

            # Load messages for this conversation
            messages = db.query(Message).filter(
                Message.conversation_id == request.conversation_id
            ).order_by(Message.timestamp).all()

            for msg in messages:
                conversation_history.append({
                    "role": msg.role.value,
                    "content": msg.content
                })
                
            logger.info(f"Loaded {len(conversation_history)} messages from conversation {request.conversation_id}")
        else:
            # Create new conversation
            conversation = Conversation(user_id=user_id)
            # Generate title from the first message
            conversation.generate_title_from_first_message(request.message)
            db.add(conversation)
            db.commit()
            db.refresh(conversation)
            
            logger.info(f"Created new conversation {conversation.id} for user {user_id}")

        # Create Cohere runner and process the message
        cohere_runner = CohereRunner()
        response_data = await cohere_runner.chat_with_tools(
            user_message=request.message,
            user_id=user_id,
            conversation_id=conversation.id,
            conversation_history=conversation_history
        )

        # Extract the response text
        response_text = response_data.get("text", "I couldn't process that request.")
        
        # Log the response
        logger.info(f"Processed chat request for user {user_id}, response length: {len(response_text)}")

        # Since the messages are now saved in cohere_runner, we need to get the latest message ID
        # Get the most recent message from the conversation to return its ID
        latest_message = db.query(Message).filter(
            Message.conversation_id == conversation.id
        ).order_by(Message.timestamp.desc()).first()
        
        message_id = latest_message.id if latest_message else 0

        return ChatResponse(
            response=response_text,
            conversation_id=conversation.id,
            message_id=message_id
        )

    except HTTPException as e:
        logger.error(f"HTTP error in chat endpoint for user {user_id}: {str(e)}")
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Unexpected error in chat endpoint for user {user_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing chat request: {str(e)}"
        )


@router.get(
    "/{user_id}/conversations",
    summary="Get user's conversation list",
    description="Retrieve all conversations for the authenticated user, ordered by most recent first.",
    responses={
        200: {
            "description": "List of conversations",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": 1,
                            "title": "Task Management",
                            "created_at": "2026-02-07T10:00:00",
                            "updated_at": "2026-02-07T10:30:00"
                        }
                    ]
                }
            }
        }
    }
)
async def get_conversations(
    user_id: str,
    db: Session = Depends(get_session)
):
    """
    Get list of user's conversations
    """
    logger.info(f"Getting conversations for user {user_id}")
    
    try:
        conversations = db.query(Conversation).filter(
            Conversation.user_id == user_id
        ).order_by(Conversation.updated_at.desc()).all()

        logger.info(f"Retrieved {len(conversations)} conversations for user {user_id}")
        
        return [
            {
                "id": conv.id,
                "title": conv.title,
                "created_at": conv.created_at,
                "updated_at": conv.updated_at
            }
            for conv in conversations
        ]
    except Exception as e:
        logger.error(f"Error retrieving conversations for user {user_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving conversations: {str(e)}"
        )


@router.get(
    "/{user_id}/conversations/{conversation_id}/messages",
    summary="Get conversation messages",
    description="Retrieve all messages for a specific conversation, ordered chronologically.",
    responses={
        200: {
            "description": "List of messages",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": 1,
                            "role": "user",
                            "content": "Add task: Buy milk",
                            "timestamp": "2026-02-07T10:00:00"
                        },
                        {
                            "id": 2,
                            "role": "assistant",
                            "content": "I've added the task 'Buy milk' to your list.",
                            "timestamp": "2026-02-07T10:00:05"
                        }
                    ]
                }
            }
        },
        404: {
            "description": "Conversation not found"
        }
    }
)
async def get_conversation_messages(
    user_id: str,
    conversation_id: int,
    db: Session = Depends(get_session)
):
    """
    Get messages for a specific conversation
    """
    logger.info(f"Getting messages for conversation {conversation_id} for user {user_id}")
    
    try:
        # Verify user owns this conversation
        conversation = db.query(Conversation).filter(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id
        ).first()

        if not conversation:
            logger.warning(f"Conversation {conversation_id} not found for user {user_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found"
            )

        messages = db.query(Message).filter(
            Message.conversation_id == conversation_id
        ).order_by(Message.timestamp).all()

        logger.info(f"Retrieved {len(messages)} messages from conversation {conversation_id}")
        
        return [
            {
                "id": msg.id,
                "role": msg.role.value,
                "content": msg.content,
                "timestamp": msg.timestamp
            }
            for msg in messages
        ]
    except HTTPException as e:
        logger.error(f"HTTP error retrieving messages for conversation {conversation_id}, user {user_id}: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Error retrieving messages for conversation {conversation_id}, user {user_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving messages: {str(e)}"
        )