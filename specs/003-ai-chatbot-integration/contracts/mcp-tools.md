# MCP Tool Definitions for AI Todo Chatbot

This document defines the Model Context Protocol (MCP) compatible tool definitions for the Cohere-powered AI chatbot.

## Task Management Tools

### add_task
Adds a new task to the user's task list.

```json
{
  "name": "add_task",
  "description": "Add a new task to the user's todo list",
  "parameters": {
    "type": "object",
    "properties": {
      "title": {
        "type": "string",
        "description": "The title of the task to add"
      },
      "description": {
        "type": "string",
        "description": "Optional description for the task"
      },
      "due_date": {
        "type": "string",
        "format": "date-time",
        "description": "Optional due date for the task in ISO 8601 format"
      }
    },
    "required": ["title"]
  }
}
```

### list_tasks
Retrieves tasks from the user's task list with optional filtering.

```json
{
  "name": "list_tasks",
  "description": "Retrieve the user's tasks with optional filtering",
  "parameters": {
    "type": "object",
    "properties": {
      "status": {
        "type": "string",
        "enum": ["all", "pending", "completed"],
        "description": "Filter tasks by completion status. Default is 'all'"
      }
    }
  }
}
```

### complete_task
Marks a specific task as completed.

```json
{
  "name": "complete_task",
  "description": "Mark a specific task as completed",
  "parameters": {
    "type": "object",
    "properties": {
      "task_id": {
        "type": "string",
        "description": "The ID of the task to mark as completed"
      }
    },
    "required": ["task_id"]
  }
}
```

### delete_task
Removes a specific task from the user's task list.

```json
{
  "name": "delete_task",
  "description": "Delete a specific task from the user's list",
  "parameters": {
    "type": "object",
    "properties": {
      "task_id": {
        "type": "string",
        "description": "The ID of the task to delete"
      }
    },
    "required": ["task_id"]
  }
}
```

### update_task
Updates properties of an existing task.

```json
{
  "name": "update_task",
  "description": "Update an existing task's properties",
  "parameters": {
    "type": "object",
    "properties": {
      "task_id": {
        "type": "string",
        "description": "The ID of the task to update"
      },
      "title": {
        "type": "string",
        "description": "New title for the task (optional)"
      },
      "description": {
        "type": "string",
        "description": "New description for the task (optional)"
      },
      "due_date": {
        "type": "string",
        "format": "date-time",
        "description": "New due date for the task (optional)"
      },
      "completed": {
        "type": "boolean",
        "description": "Whether the task is completed (optional)"
      }
    },
    "required": ["task_id"]
  }
}
```

## User Profile Tools

### get_user_profile
Retrieves the current user's profile information.

```json
{
  "name": "get_user_profile",
  "description": "Get the current user's profile information",
  "parameters": {
    "type": "object",
    "properties": {}
  }
}
```

## Tool Calling Process

The Cohere AI model will recognize when to call these tools based on user input. When tools are called:

1. The AI returns a response indicating which tools to call and with what parameters
2. The system executes the appropriate tool functions with the user's context (user_id)
3. The results of tool execution are fed back to the AI
4. The AI generates a natural language response incorporating the tool results
5. Both user message and AI response are stored in the conversation history