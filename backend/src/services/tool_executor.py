"""
Service to execute tools with proper error handling and user isolation
"""
from typing import Dict, Any, Callable, Awaitable
import asyncio
import logging


logger = logging.getLogger(__name__)


class ToolExecutor:
    """
    Service to execute MCP-compatible tools with proper error handling and user isolation
    """

    def __init__(self):
        self.tools: Dict[str, Callable[..., Awaitable[Any]]] = {}
        self._register_default_tools()

    def _register_default_tools(self):
        """
        Register default tools available to the AI
        """
        # Import tools dynamically to avoid circular imports
        from ..tools.task_tools import (
            add_task, list_tasks, complete_task, delete_task, update_task
        )
        from ..tools.user_tools import get_user_profile

        self.tools = {
            "add_task": add_task,
            "list_tasks": list_tasks,
            "complete_task": complete_task,
            "delete_task": delete_task,
            "update_task": update_task,
            "get_user_profile": get_user_profile
        }

    async def execute_tool(self, tool_name: str, tool_args: Dict[str, Any], user_id: str) -> Any:
        """
        Execute a tool with the given arguments and user context

        Args:
            tool_name: Name of the tool to execute
            tool_args: Arguments to pass to the tool
            user_id: ID of the user requesting the tool execution

        Returns:
            Result of the tool execution

        Raises:
            ValueError: If the tool doesn't exist
            Exception: If the tool execution fails
        """
        if tool_name not in self.tools:
            error_msg = f"Tool '{tool_name}' not found. Available tools: {list(self.tools.keys())}"
            logger.error(error_msg)
            raise ValueError(error_msg)

        # Add user_id to arguments if not already present
        if 'user_id' not in tool_args:
            tool_args['user_id'] = user_id

        try:
            # Validate that user_id is properly set for isolation
            if 'user_id' in tool_args and str(tool_args['user_id']) != str(user_id):
                logger.warning(f"Attempt to use different user_id in tool call by user {user_id}. Expected: {user_id}, Got: {tool_args['user_id']}")
                # Override with actual user_id to enforce user isolation
                tool_args['user_id'] = user_id

            # Validate required parameters before execution
            tool_func = self.tools[tool_name]
            result = await tool_func(**tool_args)
            
            logger.info(f"Tool '{tool_name}' executed successfully for user {user_id}")
            return result

        except ValueError as ve:
            # Handle validation errors specifically
            error_msg = f"Validation error in tool '{tool_name}' for user {user_id}: {str(ve)}"
            logger.error(error_msg)
            raise ValueError(error_msg) from ve
            
        except PermissionError as pe:
            # Handle permission errors specifically
            error_msg = f"Permission error in tool '{tool_name}' for user {user_id}: {str(pe)}"
            logger.error(error_msg)
            raise PermissionError(error_msg) from pe
            
        except Exception as e:
            # Log the full error with context for debugging
            error_msg = f"Unexpected error in tool '{tool_name}' for user {user_id}: {str(e)}"
            logger.error(error_msg, exc_info=True)  # Include traceback info
            
            # Raise a generic error to avoid exposing internal details to the user
            raise Exception(f"Tool '{tool_name}' execution failed due to an internal error") from e

    def get_tool_schema(self, tool_name: str) -> Dict[str, Any]:
        """
        Get the schema for a specific tool (placeholder implementation)

        Args:
            tool_name: Name of the tool

        Returns:
            Schema for the tool
        """
        # This is a simplified implementation
        # In a real implementation, you'd generate proper schemas
        schemas = {
            "add_task": {
                "name": "add_task",
                "description": "Add a new task",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string", "description": "Title of the task"},
                        "description": {"type": "string", "description": "Description of the task"}
                    },
                    "required": ["title"]
                }
            },
            "list_tasks": {
                "name": "list_tasks",
                "description": "List tasks for the user. Use this when the user asks to see their tasks, show tasks, list tasks, view tasks, or similar requests. If the user specifies a status (completed, pending), use the status parameter to filter. If not specified, default to 'all'.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "status": {"type": "string", "enum": ["all", "pending", "completed"], "description": "Filter tasks by status: 'all' for all tasks, 'pending' for incomplete tasks, 'completed' for finished tasks. Use 'all' as default if user doesn't specify a status."}
                    }
                }
            },
            "complete_task": {
                "name": "complete_task",
                "description": "Mark a task as completed",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {"type": "integer", "description": "ID of the task to complete"}
                    },
                    "required": ["task_id"]
                }
            },
            "delete_task": {
                "name": "delete_task",
                "description": "Delete a task",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {"type": "integer", "description": "ID of the task to delete"}
                    },
                    "required": ["task_id"]
                }
            },
            "update_task": {
                "name": "update_task",
                "description": "Update a task with new information. Use this when the user wants to change the title, description, or completion status of a specific task. The user might say 'update task X', 'change task X to...', 'modify task X', or similar phrases.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {"type": "integer", "description": "ID of the task to update"},
                        "title": {"type": "string", "description": "New title of the task"},
                        "description": {"type": "string", "description": "New description of the task"},
                        "completed": {"type": "boolean", "description": "New completion status"}
                    },
                    "required": ["task_id"]
                }
            },
            "get_user_profile": {
                "name": "get_user_profile",
                "description": "Get user profile information",
                "parameters": {
                    "type": "object",
                    "properties": {}
                }
            }
        }

        return schemas.get(tool_name, {})