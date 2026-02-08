# API Contract: Modern Frontend UI for Todo Application

## Overview

This document outlines the API contracts that the frontend UI will consume. These endpoints will be implemented by the backend and consumed by the frontend application.

## Authentication Endpoints

### POST /api/auth/login
Authenticate user and return JWT token

**Request:**
```json
{
  "email": "user@example.com",
  "password": "securePassword123"
}
```

**Response (200):**
```json
{
  "user": {
    "id": "uuid-string",
    "email": "user@example.com",
    "name": "John Doe"
  },
  "token": "jwt-token-string"
}
```

**Response (401):**
```json
{
  "error": "Invalid credentials"
}
```

### POST /api/auth/register
Register a new user

**Request:**
```json
{
  "email": "user@example.com",
  "password": "securePassword123",
  "name": "John Doe"
}
```

**Response (201):**
```json
{
  "user": {
    "id": "uuid-string",
    "email": "user@example.com",
    "name": "John Doe"
  },
  "token": "jwt-token-string"
}
```

**Response (400):**
```json
{
  "error": "Validation error or user already exists"
}
```

## Task Management Endpoints

### GET /api/tasks
Retrieve authenticated user's tasks with optional filtering

**Headers:**
```
Authorization: Bearer {jwt-token}
```

**Query Parameters:**
- `completed`: boolean (optional) - Filter by completion status
- `priority`: string (optional) - Filter by priority level
- `limit`: number (optional) - Number of results to return
- `offset`: number (optional) - Offset for pagination

**Response (200):**
```json
{
  "tasks": [
    {
      "id": "uuid-string",
      "title": "Task title",
      "description": "Task description (optional)",
      "completed": false,
      "dueDate": "2023-12-31T23:59:59Z",
      "createdAt": "2023-01-01T00:00:00Z",
      "updatedAt": "2023-01-01T00:00:00Z",
      "userId": "user-uuid"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 100
  }
}
```

### POST /api/tasks
Create a new task for the authenticated user

**Headers:**
```
Authorization: Bearer {jwt-token}
```

**Request:**
```json
{
  "title": "New task title",
  "description": "Task description (optional)",
  "dueDate": "2023-12-31T23:59:59Z"
}
```

**Response (201):**
```json
{
  "task": {
    "id": "new-uuid-string",
    "title": "New task title",
    "description": "Task description (optional)",
    "completed": false,
    "dueDate": "2023-12-31T23:59:59Z",
    "createdAt": "2023-01-01T00:00:00Z",
    "updatedAt": "2023-01-01T00:00:00Z",
    "userId": "authenticated-user-uuid"
  }
}
```

**Response (400):**
```json
{
  "error": "Validation error"
}
```

### PUT /api/tasks/{id}
Update an existing task

**Headers:**
```
Authorization: Bearer {jwt-token}
```

**Request:**
```json
{
  "title": "Updated task title",
  "description": "Updated description",
  "dueDate": "2023-12-31T23:59:59Z"
}
```

**Response (200):**
```json
{
  "task": {
    "id": "existing-uuid-string",
    "title": "Updated task title",
    "description": "Updated description",
    "completed": false,
    "dueDate": "2023-12-31T23:59:59Z",
    "createdAt": "2023-01-01T00:00:00Z",
    "updatedAt": "2023-01-02T00:00:00Z",
    "userId": "authenticated-user-uuid"
  }
}
```

### DELETE /api/tasks/{id}
Delete a task

**Headers:**
```
Authorization: Bearer {jwt-token}
```

**Response (204):**
```
No content
```

**Response (404):**
```json
{
  "error": "Task not found"
}
```

### PATCH /api/tasks/{id}/toggle-complete
Toggle the completion status of a task

**Headers:**
```
Authorization: Bearer {jwt-token}
```

**Response (200):**
```json
{
  "task": {
    "id": "existing-uuid-string",
    "title": "Task title",
    "description": "Task description",
    "completed": true, // Status flipped
    "dueDate": "2023-12-31T23:59:59Z",
    "createdAt": "2023-01-01T00:00:00Z",
    "updatedAt": "2023-01-02T00:00:00Z",
    "userId": "authenticated-user-uuid"
  }
}
```

## Common Error Responses

### 401 Unauthorized
```json
{
  "error": "Authentication required"
}
```

### 403 Forbidden
```json
{
  "error": "Insufficient permissions"
}
```

### 404 Not Found
```json
{
  "error": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal server error"
}
```

## Headers

### Request Headers
- `Authorization: Bearer {jwt-token}` - Required for authenticated endpoints
- `Content-Type: application/json` - For POST/PUT/PATCH requests
- `Accept: application/json` - Expected response format

### Response Headers
- `Content-Type: application/json` - Response content type
- `X-Request-ID: uuid-string` - Unique request identifier for debugging

## Rate Limiting

All authenticated endpoints are subject to rate limiting:
- 100 requests per minute per user
- Response headers include rate limit information:
  - `X-RateLimit-Limit`: Total requests allowed per window
  - `X-RateLimit-Remaining`: Remaining requests in current window
  - `X-RateLimit-Reset`: Time when counter resets