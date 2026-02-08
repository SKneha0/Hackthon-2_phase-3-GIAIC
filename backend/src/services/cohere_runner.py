"""
Custom Cohere runner with tool calling capabilities
"""
import os
import asyncio
import logging
from typing import Dict, Any, List
import cohere
from ..services.tool_executor import ToolExecutor
from sqlmodel import Session
from ..models.conversation_model import Message, MessageRole
from db import engine
from collections import defaultdict
from datetime import datetime, timedelta
import threading


logger = logging.getLogger(__name__)


class RateLimiter:
    """
    Simple rate limiter to prevent excessive API calls to Cohere
    """
    def __init__(self, max_requests: int = 10, time_window: int = 60):  # 10 requests per minute
        self.max_requests = max_requests
        self.time_window = time_window  # in seconds
        self.requests = defaultdict(list)  # user_id -> list of timestamps
        self.lock = threading.Lock()

    def is_allowed(self, user_id: str) -> bool:
        """
        Check if the user is allowed to make a request
        """
        with self.lock:
            now = datetime.now()
            # Clean old requests outside the time window
            self.requests[user_id] = [
                req_time for req_time in self.requests[user_id]
                if (now - req_time).seconds < self.time_window
            ]
            
            # Check if user has exceeded the limit
            if len(self.requests[user_id]) >= self.max_requests:
                return False
            
            # Add current request
            self.requests[user_id].append(now)
            return True


# Global rate limiter instance
rate_limiter = RateLimiter()


class CohereRunner:
    """
    Service to handle chat completion and tool calling with Cohere API
    """

    def __init__(self):
        self.api_key = os.getenv("COHERE_API_KEY")
        if not self.api_key:
            raise ValueError("COHERE_API_KEY environment variable is not set")

        # Initialize Cohere client with multilingual support
        self.client = cohere.Client(self.api_key)
        
        # Set up multilingual configuration
        self.supported_languages = ["en", "ur"]  # English and Urdu support
        
        self.tool_executor = ToolExecutor()

    async def chat_with_tools(
        self,
        user_message: str,
        user_id: str,
        conversation_id: int,
        conversation_history: List[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Process a chat message with tool calling capabilities

        Args:
            user_message: The user's message
            user_id: The ID of the user sending the message
            conversation_id: The ID of the conversation
            conversation_history: Previous messages in the conversation

        Returns:
            Response from Cohere including any tool call results
        """
        # Check rate limit before processing
        if not rate_limiter.is_allowed(user_id):
            logger.warning(f"Rate limit exceeded for user {user_id}")
            return {
                "text": "Rate limit exceeded. Please wait before sending another message.",
                "error": "Rate limit exceeded",
                "language": "unknown"
            }
        
        try:
            # Detect language in the user message for multilingual support
            detected_language = self.detect_language(user_message)
            
            # Prepare message history for Cohere
            chat_history = []
            if conversation_history:
                # Limit conversation history to last 20 messages to prevent token overflow
                limited_history = conversation_history[-20:] if len(conversation_history) > 20 else conversation_history
                
                for msg in limited_history:
                    role = "USER" if msg["role"] == "user" else "CHATBOT"
                    chat_history.append({
                        "role": role,
                        "message": msg["content"]
                    })

            # Get available tools
            tools = []
            for tool_name in self.tool_executor.tools.keys():
                tool_schema = self.tool_executor.get_tool_schema(tool_name)
                if tool_schema:
                    tools.append(tool_schema)

            # Call Cohere chat with tools
            # Using the command-r-08-2024 model which supports tool calling
            response = self.client.chat(
                message=user_message,
                chat_history=chat_history,
                tools=tools,
                model="command-r-08-2024",  # Updated model (command-r-plus was deprecated)
                temperature=0.3,  # Lower temperature for more consistent responses
            )

            # Process tool calls if any
            final_response = {
                "text": response.text,
                "finish_reason": getattr(response, 'finish_reason', 'COMPLETE'),
                "tool_calls": [],
                "tool_results": [],
                "language": detected_language  # Include detected language in response
            }

            if hasattr(response, 'tool_calls') and response.tool_calls:
                for tool_call in response.tool_calls:
                    tool_name = tool_call.name
                    tool_parameters = tool_call.parameters

                    try:
                        # Execute the tool
                        tool_result = await self.tool_executor.execute_tool(
                            tool_name, tool_parameters, user_id
                        )

                        # Store the raw tool result
                        logger.debug(f"Tool '{tool_name}' executed, result: {tool_result}")

                        # Special handling for tools with formatted responses
                        if (isinstance(tool_result, dict) and 
                            "formatted_response" in tool_result):
                            # Use the formatted response for tools that have it
                            output_data = [{"result": tool_result["formatted_response"]}]
                        else:
                            output_data = [tool_result]

                        final_response["tool_calls"].append({
                            "name": tool_name,
                            "parameters": tool_parameters
                        })

                        final_response["tool_results"].append({
                            "call": {"name": tool_name, "parameters": tool_parameters},
                            "outputs": output_data
                        })

                        logger.info(f"Tool '{tool_name}' executed successfully for user {user_id}")

                    except Exception as e:
                        logger.error(f"Tool '{tool_name}' execution failed: {str(e)}")
                        final_response["tool_results"].append({
                            "call": {"name": tool_name, "parameters": tool_parameters},
                            "error": str(e)
                        })

                # Make a second call to Cohere with tool results to get final response
                if final_response["tool_results"]:
                    try:
                        # Check if any of the tool results have formatted responses for special tools
                        formatted_response_used = False
                        
                        for result in final_response["tool_results"]:
                            outputs = result.get("outputs", [{"error": result.get("error", "Unknown error")}])

                            # Special handling for tools with formatted responses
                            if (result.get("call", {}).get("name") in ["list_tasks", "update_task"] and
                                len(outputs) > 0 and
                                isinstance(outputs[0], dict) and
                                "formatted_response" in outputs[0]):
                                # Use the formatted response directly for these tools
                                final_response["text"] = outputs[0]["formatted_response"]
                                logger.info(f"Used formatted response for {result.get('call', {}).get('name')} for user {user_id}")
                                formatted_response_used = True
                                break  # Exit after using the first formatted response

                        if not formatted_response_used:
                            # Prepare tool results for Cohere if no formatted response was used
                            tool_results_for_cohere = []
                            for result in final_response["tool_results"]:
                                outputs = result.get("outputs", [{"error": result.get("error", "Unknown error")}])
                                tool_results_for_cohere.append({
                                    "call": result["call"],
                                    "outputs": outputs
                                })

                            # Make second call with tool results
                            # According to the error, we need to use the correct parameter for single step mode
                            # Different versions of the API might use different parameter names
                            try:
                                # Try with force_single_step first
                                final_cohere_response = self.client.chat(
                                    message="Based on the tool results, provide a clear response to the user's original request.",
                                    chat_history=chat_history,
                                    tool_results=tool_results_for_cohere,
                                    model="command-r-08-2024",
                                    temperature=0.3,
                                    force_single_step=True
                                )
                            except TypeError:
                                # If force_single_step is not supported, try with call_multi_rag_sources_only=False
                                # Or just call without the parameter if it's not supported
                                final_cohere_response = self.client.chat(
                                    message="Based on the tool results, provide a clear response to the user's original request.",
                                    chat_history=chat_history,
                                    tool_results=tool_results_for_cohere,
                                    model="command-r-08-2024",
                                    temperature=0.3
                                )

                            # Update the response text with the final answer
                            final_response["text"] = final_cohere_response.text
                            logger.info(f"Generated final response after tool execution for user {user_id}")
                        else:
                            logger.info(f"Using formatted response directly for user {user_id}")

                    except Exception as e:
                        logger.error(f"Failed to generate final response with tool results: {str(e)}")
                        # Keep the original response if second call fails

            # Save user message to database
            await self.save_message_to_db(conversation_id, "user", user_message)

            # Save AI response to database (use final_response text after tool execution)
            await self.save_message_to_db(conversation_id, "assistant", final_response["text"])

            return final_response

        except Exception as e:
            logger.error(f"Cohere chat error for user {user_id}: {str(e)}")
            return {
                "text": "Sorry, I encountered an error processing your request.",
                "error": str(e),
                "language": "unknown"
            }

    def detect_language(self, text: str) -> str:
        """
        Simple language detection based on character sets and common words
        This is a basic implementation - in production, use a proper NLP library
        
        Args:
            text: The text to analyze for language detection
            
        Returns:
            Detected language code (e.g., 'en', 'ur', 'mixed', 'unknown')
        """
        # Check for Urdu characters (Arabic script)
        urdu_chars = 0
        english_chars = 0
        
        for char in text:
            # Urdu/Arabic Unicode range
            if '\u0600' <= char <= '\u06FF':
                urdu_chars += 1
            # English letters
            elif char.isalpha() and ord(char) < 128:
                english_chars += 1
        
        total_alpha = urdu_chars + english_chars
        
        if total_alpha == 0:
            return "unknown"
        elif urdu_chars / total_alpha > 0.3:  # If more than 30% are Urdu chars
            return "ur"
        elif english_chars / total_alpha > 0.3:  # If more than 30% are English chars
            return "en"
        else:
            return "mixed"

    async def save_message_to_db(self, conversation_id: int, role: str, content: str):
        """
        Save a message to the database
        
        Args:
            conversation_id: The ID of the conversation
            role: The role of the message sender ('user' or 'assistant')
            content: The content of the message
        """
        try:
            # Create a new database session
            with Session(engine) as session:
                # Create new message instance
                new_message = Message(
                    conversation_id=conversation_id,
                    role=MessageRole.ASSISTANT if role == "assistant" else MessageRole.USER,
                    content=content
                )

                # Add and commit the new message to the database
                session.add(new_message)
                session.commit()
                
        except Exception as e:
            logger.error(f"Failed to save message to database: {str(e)}")
            # Don't raise the exception as it shouldn't break the chat flow

    async def stream_chat_with_tools(
        self,
        user_message: str,
        user_id: str,
        conversation_history: List[Dict[str, str]] = None
    ) -> Any:
        """
        Stream chat response with tool calling capabilities

        Args:
            user_message: The user's message
            user_id: The ID of the user sending the message
            conversation_history: Previous messages in the conversation

        Returns:
            Streaming response from Cohere
        """
        # Prepare message history for Cohere
        chat_history = []
        if conversation_history:
            for msg in conversation_history:
                role = "USER" if msg["role"] == "user" else "CHATBOT"
                chat_history.append({
                    "role": role,
                    "message": msg["content"]
                })

        # Get available tools
        tools = []
        for tool_name in self.tool_executor.tools.keys():
            tool_schema = self.tool_executor.get_tool_schema(tool_name)
            if tool_schema:
                tools.append(tool_schema)

        # Start streaming chat with Cohere
        response = self.client.chat_stream(
            message=user_message,
            chat_history=chat_history,
            tools=tools,
            connectors=[{"id": "web-search"}] if not tools else []  # Use web search as fallback
        )

        return response