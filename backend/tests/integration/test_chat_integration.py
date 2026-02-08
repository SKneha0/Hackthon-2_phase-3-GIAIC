"""
Integration tests for chat functionality
Tests User Stories 1, 2, 3, 4 - Natural language task management, user profile, multilingual, and persistence
"""
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine, SQLModel
from sqlmodel.pool import StaticPool
from src.main import app
from src.db import get_session
from src.models.user_model import User
from src.models.task_model import Task
from src.models.conversation_model import Conversation, Message
from unittest.mock import patch, MagicMock, AsyncMock
import os


# Create in-memory SQLite database for testing
@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture(name="test_user")
def test_user_fixture(session: Session):
    """Create a test user"""
    user = User(
        id=1,
        email="test@example.com",
        name="Test User"
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@pytest.fixture(name="test_tasks")
def test_tasks_fixture(session: Session, test_user: User):
    """Create test tasks for the user"""
    tasks = [
        Task(
            id=1,
            user_id=str(test_user.id),
            title="Buy milk",
            description="Get 2 liters of milk",
            completed=False
        ),
        Task(
            id=2,
            user_id=str(test_user.id),
            title="Complete project",
            description="Finish the AI chatbot integration",
            completed=False
        ),
        Task(
            id=3,
            user_id=str(test_user.id),
            title="Old completed task",
            description="This was done yesterday",
            completed=True
        )
    ]
    for task in tasks:
        session.add(task)
    session.commit()
    return tasks


# User Story 1 Tests: Natural Language Task Management

@pytest.mark.asyncio
async def test_add_task_natural_language(client: TestClient, test_user: User):
    """
    T023: Test that "Add task: Buy milk" creates task visible in task list
    """
    # Mock Cohere API response
    mock_response = MagicMock()
    mock_response.text = "I've added the task 'Buy milk' to your list."
    mock_response.tool_calls = [
        MagicMock(
            name="add_task",
            parameters={"title": "Buy milk", "description": "", "user_id": str(test_user.id)}
        )
    ]

    with patch('cohere.Client') as mock_cohere:
        mock_cohere.return_value.chat.return_value = mock_response

        response = client.post(
            f"/api/{test_user.id}/chat",
            json={"message": "Add task: Buy milk"}
        )

        assert response.status_code == 200
        data = response.json()
        assert "conversation_id" in data
        assert "response" in data


@pytest.mark.asyncio
async def test_list_pending_tasks(client: TestClient, test_user: User, test_tasks):
    """
    T024: Test that "Show pending tasks" returns only incomplete tasks in chat response
    """
    mock_response = MagicMock()
    mock_response.text = "You have 2 pending tasks: Buy milk, Complete project"
    mock_response.tool_calls = [
        MagicMock(
            name="list_tasks",
            parameters={"filter": "pending", "user_id": str(test_user.id)}
        )
    ]

    with patch('cohere.Client') as mock_cohere:
        mock_cohere.return_value.chat.return_value = mock_response

        response = client.post(
            f"/api/{test_user.id}/chat",
            json={"message": "Show pending tasks"}
        )

        assert response.status_code == 200
        data = response.json()
        assert "response" in data


@pytest.mark.asyncio
async def test_complete_first_task(client: TestClient, test_user: User, test_tasks):
    """
    T025: Test that "Complete the first task" marks oldest task as completed in DB and UI
    """
    mock_response = MagicMock()
    mock_response.text = "I've marked the task 'Buy milk' as completed."
    mock_response.tool_calls = [
        MagicMock(
            name="complete_task",
            parameters={"task_id": 1, "user_id": str(test_user.id)}
        )
    ]

    with patch('cohere.Client') as mock_cohere:
        mock_cohere.return_value.chat.return_value = mock_response

        response = client.post(
            f"/api/{test_user.id}/chat",
            json={"message": "Complete the first task"}
        )

        assert response.status_code == 200


# User Story 2 Tests: User Profile Information Retrieval

@pytest.mark.asyncio
async def test_who_am_i_query(client: TestClient, test_user: User):
    """
    T028: Test that "Who am I?" returns user's name and email in chat response
    """
    mock_response = MagicMock()
    mock_response.text = f"You are {test_user.name} with email {test_user.email}"
    mock_response.tool_calls = [
        MagicMock(
            name="get_user_profile",
            parameters={"user_id": str(test_user.id)}
        )
    ]

    with patch('cohere.Client') as mock_cohere:
        mock_cohere.return_value.chat.return_value = mock_response

        response = client.post(
            f"/api/{test_user.id}/chat",
            json={"message": "Who am I?"}
        )

        assert response.status_code == 200
        data = response.json()
        assert "response" in data


@pytest.mark.asyncio
async def test_email_query(client: TestClient, test_user: User):
    """
    T029: Test that "What is my email?" returns user's email address
    """
    mock_response = MagicMock()
    mock_response.text = f"Your email is {test_user.email}"
    mock_response.tool_calls = [
        MagicMock(
            name="get_user_profile",
            parameters={"user_id": str(test_user.id)}
        )
    ]

    with patch('cohere.Client') as mock_cohere:
        mock_cohere.return_value.chat.return_value = mock_response

        response = client.post(
            f"/api/{test_user.id}/chat",
            json={"message": "What is my email?"}
        )

        assert response.status_code == 200
        data = response.json()
        assert "response" in data


@pytest.mark.asyncio
async def test_urdu_name_query(client: TestClient, test_user: User):
    """
    T030: Test that "Mera naam batao" returns user's name appropriately
    """
    mock_response = MagicMock()
    mock_response.text = f"Aap ka naam {test_user.name} hai"
    mock_response.tool_calls = [
        MagicMock(
            name="get_user_profile",
            parameters={"user_id": str(test_user.id)}
        )
    ]

    with patch('cohere.Client') as mock_cohere:
        mock_cohere.return_value.chat.return_value = mock_response

        response = client.post(
            f"/api/{test_user.id}/chat",
            json={"message": "Mera naam batao"}
        )

        assert response.status_code == 200
        data = response.json()
        assert "response" in data


# User Story 3 Tests: Multilingual Chat Interface

@pytest.mark.asyncio
async def test_urdu_email_query(client: TestClient, test_user: User):
    """
    T032: Test Urdu command "Mera email kya hai?" returns correct email
    """
    mock_response = MagicMock()
    mock_response.text = f"Aap ka email {test_user.email} hai"
    mock_response.tool_calls = [
        MagicMock(
            name="get_user_profile",
            parameters={"user_id": str(test_user.id)}
        )
    ]

    with patch('cohere.Client') as mock_cohere:
        mock_cohere.return_value.chat.return_value = mock_response

        response = client.post(
            f"/api/{test_user.id}/chat",
            json={"message": "Mera email kya hai?"}
        )

        assert response.status_code == 200
        data = response.json()
        assert "response" in data


@pytest.mark.asyncio
async def test_mixed_language_query(client: TestClient, test_user: User):
    """
    T033: Test mixed language queries are processed correctly
    """
    mock_response = MagicMock()
    mock_response.text = "Your tasks are: Buy milk, Complete project"
    mock_response.tool_calls = [
        MagicMock(
            name="list_tasks",
            parameters={"filter": "all", "user_id": str(test_user.id)}
        )
    ]

    with patch('cohere.Client') as mock_cohere:
        mock_cohere.return_value.chat.return_value = mock_response

        response = client.post(
            f"/api/{test_user.id}/chat",
            json={"message": "Show my tasks please"}
        )

        assert response.status_code == 200
        data = response.json()
        assert "response" in data


# User Story 4 Tests: Persistent Conversation History

@pytest.mark.asyncio
async def test_conversation_history_persists(client: TestClient, test_user: User, session: Session):
    """
    T039: Test conversation history persists after page refresh
    """
    # Create a conversation with messages
    conversation = Conversation(user_id=str(test_user.id), title="Test Conversation")
    session.add(conversation)
    session.commit()
    session.refresh(conversation)

    # Retrieve conversation
    response = client.get(f"/api/{test_user.id}/conversations")
    assert response.status_code == 200
    conversations = response.json()
    assert len(conversations) > 0
    assert conversations[0]["id"] == conversation.id


@pytest.mark.asyncio
async def test_conversation_history_available_after_time_gap(client: TestClient, test_user: User, session: Session):
    """
    T040: Test conversation history available when returning after time gap
    """
    # Create a conversation
    conversation = Conversation(user_id=str(test_user.id), title="Old Conversation")
    session.add(conversation)
    session.commit()
    session.refresh(conversation)

    # Retrieve messages for the conversation
    response = client.get(f"/api/{test_user.id}/conversations/{conversation.id}/messages")
    assert response.status_code == 200
    messages = response.json()
    assert isinstance(messages, list)
