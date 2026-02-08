# Quickstart Guide: Backend Todo Application API

**Date**: 2026-02-06
**Feature**: 1-backend-fastapi-todo
**Status**: Complete

## Overview
This guide provides the essential steps to set up and run the backend todo application API. The backend implements secure RESTful endpoints with JWT authentication and user-isolated task management.

## Prerequisites
- Python 3.13 or higher
- pip package manager
- Access to Neon Serverless PostgreSQL database
- Better Auth secret for JWT verification

## Setup Instructions

### 1. Clone or Navigate to Project Directory
```bash
cd /path/to/hackathon-project/backend
```

### 2. Install Dependencies
```bash
pip install fastapi uvicorn sqlmodel python-dotenv pyjwt psycopg2-binary
```

### 3. Create Environment File
Create a `.env` file in the backend directory with the following content:

```env
BETTER_AUTH_SECRET=secret
BETTER_AUTH_URL=http://localhost:3000
NEON_DB_URL=postgresql://neonpg_5xMPfhq9XgaS@ep-bitter-cloud-adk6f8ds-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require
```

### 4. Initialize Project Structure
Create the following directory structure:

```
backend/
├── main.py
├── models.py
├── db.py
├── auth.py
├── routes/
│   └── tasks.py
└── schemas/
    └── __init__.py
```

### 5. Start the Application
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Key Features

### Authentication
- All API endpoints require a valid JWT token from Better Auth
- Tokens are verified using the shared BETTER_AUTH_SECRET
- Access is restricted to authenticated users

### User Isolation
- Each user can only access, modify, and delete their own tasks
- Database queries automatically filter by the authenticated user's ID
- Cross-user data access is prevented

### API Endpoints
- `GET /api/tasks` - Retrieve user's tasks with optional filtering
- `POST /api/tasks` - Create a new task for the user
- `GET /api/tasks/{id}` - Retrieve a specific task
- `PUT /api/tasks/{id}` - Update a specific task
- `DELETE /api/tasks/{id}` - Delete a specific task
- `PATCH /api/tasks/{id}/complete` - Toggle task completion status

### Filtering and Sorting
- Filter tasks by status (all, pending, completed)
- Sort tasks by creation date or title

## API Documentation
Once the application is running, visit:
- http://localhost:8000/docs - Interactive API documentation (Swagger UI)
- http://localhost:8000/redoc - Alternative API documentation (ReDoc)

## Environment Variables
- `BETTER_AUTH_SECRET`: Secret used to verify JWT tokens from Better Auth
- `BETTER_AUTH_URL`: Base URL of the frontend application
- `NEON_DB_URL`: Connection string for Neon Serverless PostgreSQL database

## Troubleshooting
- If you get a database connection error, verify the NEON_DB_URL in your .env file
- If authentication fails, ensure the BETTER_AUTH_SECRET matches the frontend
- If endpoints return 401 errors, verify your JWT token is valid and properly formatted