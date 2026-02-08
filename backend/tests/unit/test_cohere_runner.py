import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from src.services.cohere_runner import CohereRunner, rate_limiter


@pytest.fixture
def cohere_runner():
    """Create a CohereRunner instance for testing"""
    with patch('os.getenv', return_value='fake-api-key'):
        with patch('cohere.Client') as mock_client:
            runner = CohereRunner()
            runner.client = mock_client.return_value
            runner.tool_executor = AsyncMock()
            return runner


@pytest.mark.asyncio
async def test_chat_with_tools_success(cohere_runner):
    """Test successful chat with tools execution"""
    # Mock the Cohere client response
    mock_response = MagicMock()
    mock_response.text = "This is a test response"
    mock_response.tool_calls = []
    cohere_runner.client.chat.return_value = mock_response
    
    # Mock the save_message_to_db method
    with patch.object(cohere_runner, 'save_message_to_db', new_callable=AsyncMock) as mock_save:
        # Call the method
        result = await cohere_runner.chat_with_tools(
            user_message="Test message",
            user_id="test-user-id",
            conversation_id=1,
            conversation_history=[]
        )
        
        # Assertions
        assert result["text"] == "This is a test response"
        assert mock_save.call_count == 2  # Called twice: once for user message, once for AI response
        cohere_runner.client.chat.assert_called_once()


@pytest.mark.asyncio
async def test_rate_limiting():
    """Test rate limiting functionality"""
    # Temporarily modify rate limiter for testing
    original_max_requests = rate_limiter.max_requests
    rate_limiter.max_requests = 2  # Allow only 2 requests
    
    try:
        # Test that first 2 requests are allowed
        assert rate_limiter.is_allowed("user1") == True
        assert rate_limiter.is_allowed("user1") == True
        
        # Test that 3rd request is denied
        assert rate_limiter.is_allowed("user1") == False
        
        # Test that other user is still allowed
        assert rate_limiter.is_allowed("user2") == True
    finally:
        # Restore original value
        rate_limiter.max_requests = original_max_requests


@pytest.mark.asyncio
async def test_detect_language_english(cohere_runner):
    """Test language detection for English text"""
    text = "This is an English sentence."
    result = cohere_runner.detect_language(text)
    assert result == "en"


@pytest.mark.asyncio
async def test_detect_language_urdu(cohere_runner):
    """Test language detection for Urdu text"""
    # Using Arabic script characters for Urdu
    text = "یہ اردو کا جملہ ہے"
    result = cohere_runner.detect_language(text)
    assert result == "ur"


@pytest.mark.asyncio
async def test_detect_language_mixed(cohere_runner):
    """Test language detection for mixed text"""
    text = "This is English and یہ اردو ہے"
    result = cohere_runner.detect_language(text)
    assert result == "mixed"