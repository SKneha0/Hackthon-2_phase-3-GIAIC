# Research: Backend Todo Application API

**Date**: 2026-02-06
**Feature**: 1-backend-fastapi-todo
**Status**: Complete

## Overview
This document captures all research and decisions made during the planning phase for the backend todo application API, focusing on technology choices, architecture patterns, and implementation strategies.

## Technology Stack Decisions

### Decision: FastAPI Framework
**Rationale**: FastAPI provides automatic API documentation (Swagger UI), excellent performance, built-in validation with Pydantic, and async support. It's ideal for building REST APIs with Python and has strong community support.

**Alternatives considered**:
- Flask: More manual work needed for validation and documentation
- Django: Too heavy for this simple API-only application
- Express.js: Would deviate from required Python stack

### Decision: SQLModel ORM
**Rationale**: SQLModel combines the power of SQLAlchemy with Pydantic validation, making it ideal for FastAPI applications. It allows using the same models for both database operations and API request/response validation.

**Alternatives considered**:
- Pure SQLAlchemy: More verbose, less integration with Pydantic
- Tortoise ORM: Async-first but less mature than SQLModel
- Peewee: Simpler but lacks Pydantic integration

### Decision: PyJWT for Token Verification
**Rationale**: Lightweight, widely-used library specifically for JWT handling. Perfect for verifying tokens issued by Better Auth without heavy dependencies.

**Alternatives considered**:
- Authlib: More comprehensive but heavier than needed for simple verification
- python-jose: Good alternative but PyJWT has broader adoption
- FastAPI's built-in OAuth2PasswordBearer: Designed for password-based auth, not pre-existing JWTs

### Decision: Per-Request Database Sessions
**Rationale**: Creating a new database session for each request is a FastAPI best practice. It ensures proper cleanup and avoids potential issues with async requests sharing connections.

**Alternatives considered**:
- Global session: Could lead to connection pooling issues and race conditions
- Request-scoped with manual management: More error-prone than using FastAPI dependencies

### Decision: Environment Variable Loading with python-dotenv
**Rationale**: Simple and effective for loading environment variables during development, matching the .env file pattern mentioned in the specification.

**Alternatives considered**:
- Pydantic Settings: More robust but overkill for this simple configuration
- Manual os.environ usage: Less clean and no automatic .env loading

### Decision: CORS Configuration for Specific Origins
**Rationale**: Restricting CORS to specific origins (likely localhost:3000 for the frontend) is more secure than wildcard access while still enabling the frontend integration.

**Alternatives considered**:
- Wildcard (*): Less secure, allows any origin to make requests
- Disabled: Would prevent frontend integration entirely

## Authentication Architecture

### Decision: JWT Token Verification Strategy
**Rationale**: The system will decode JWT tokens using the shared BETTER_AUTH_SECRET to extract the user_id. This aligns with the specification's requirement to work with Better Auth's frontend-issued tokens.

**Implementation approach**:
- Use FastAPI's Depends() to inject current user into route handlers
- Create reusable get_current_user dependency
- Handle token expiration and invalid signature gracefully
- Extract user_id from token claims for user isolation

### Decision: User Isolation Enforcement
**Rationale**: Every database query will be filtered by the authenticated user's ID to prevent cross-user data access. This is critical for meeting the specification's security requirements.

**Implementation approach**:
- All route handlers will have access to current_user via dependency injection
- All queries will include WHERE user_id = current_user.id (or equivalent)
- Access to specific records will be validated against current_user ownership

## Database Schema Design

### Decision: Task Model Structure
**Rationale**: The Task model will include essential fields (id, title, description, completed status) and crucial user_id foreign key for enforcing ownership.

**Fields planned**:
- id: Primary key, auto-generated
- title: String, required, indexed for performance
- description: String, optional
- completed: Boolean, default False, indexed for filtering
- user_id: Foreign key to users table (managed by Better Auth)
- created_at: Timestamp, auto-generated
- updated_at: Timestamp, auto-generated and updated

### Decision: Table Creation Strategy
**Rationale**: Using SQLModel's create_all() on application startup is appropriate for a hackathon project and development environment, allowing for easy setup.

**Considerations**:
- For production, proper migration tools like Alembic would be preferred
- Neon Serverless PostgreSQL handles schema changes gracefully
- This approach simplifies initial setup and development

## API Design Patterns

### Decision: RESTful Endpoint Design
**Rationale**: Following standard REST patterns makes the API intuitive and aligns with the specification's requirements.

**Endpoints planned**:
- GET /api/tasks - List user's tasks with filtering options
- POST /api/tasks - Create new task for user
- GET /api/tasks/{id} - Get specific task (owned by user)
- PUT /api/tasks/{id} - Update specific task (owned by user)
- DELETE /api/tasks/{id} - Delete specific task (owned by user)
- PATCH /api/tasks/{id}/complete - Toggle task completion status

### Decision: Query Parameter Support
**Rationale**: Supporting query parameters for filtering and sorting improves the user experience by allowing efficient task management.

**Parameters planned**:
- status: "all", "pending", "completed" to filter by completion status
- sort: Options for sorting (created, title, due_date if implemented)

## Error Handling Strategy

### Decision: Standard HTTP Status Codes
**Rationale**: Using standard HTTP status codes ensures predictable behavior and follows REST conventions.

**Codes planned**:
- 200: Successful requests
- 201: Resource created (POST)
- 400: Bad request (malformed request)
- 401: Unauthorized (invalid/expired JWT)
- 403: Forbidden (attempt to access other user's resource)
- 404: Not found (resource doesn't exist)
- 422: Validation error (request body doesn't match schema)

## Integration Points

### Decision: Frontend Integration Design
**Rationale**: The backend must work seamlessly with the existing frontend as specified in the requirements.

**Integration approach**:
- Use /api prefix for all endpoints to separate from frontend routes
- Support JWT token verification from Better Auth
- Provide proper CORS headers for frontend origin
- Follow API contract that frontend's /lib/api.ts expects