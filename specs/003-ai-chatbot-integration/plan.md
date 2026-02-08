# Implementation Plan: AI Todo Chatbot Integration (Cohere-Powered)

**Branch**: `003-ai-chatbot-integration` | **Date**: 2026-02-07 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/003-ai-chatbot-integration/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

This plan integrates a Cohere-powered AI chatbot into the existing Next.js + FastAPI full-stack todo application. The chatbot provides natural language task management (add, list, complete, delete, update) and user profile information retrieval. It implements a stateless architecture with conversation history persisted in the database and MCP-compatible tools for secure user-isolated operations. The frontend includes a floating chat icon that opens a modern chat interface for conversational task management.

## Technical Context

**Language/Version**: Python 3.11, TypeScript/JavaScript, Next.js 16+, FastAPI 0.104+
**Primary Dependencies**: FastAPI, Next.js, SQLModel, Neon PostgreSQL, Better Auth, Cohere SDK, Tailwind CSS, MCP SDK
**Storage**: Neon Serverless PostgreSQL database with Conversation and Message models
**Testing**: pytest for backend, Jest/Vitest for frontend, contract testing for API endpoints
**Target Platform**: Linux server deployment with web application frontend
**Project Type**: Web application (frontend + backend)
**Performance Goals**: <5 second response time for 90% of chat requests, 95% accuracy for natural language task commands
**Constraints**: <200ms p95 for internal API calls, JWT-based authentication, strict user data isolation, token limits to prevent LLM costs explosion
**Scale/Scope**: Up to 10k concurrent users, stateless design for horizontal scaling, conversation history retention policy

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Spec-Driven Development**: ✓ All features defined in spec before implementation
- **Agentic Development**: ✓ Using Claude Code + Spec-Kit, no manual coding
- **Modular Architecture**: ✓ MCP tools with clear separation of concerns
- **User Isolation**: ✓ All operations filtered by user_id from JWT, strict ownership enforcement
- **Technology Stack**: ✓ Using approved stack: Next.js, FastAPI, SQLModel, Neon, Better Auth, Cohere
- **Stateless Authentication**: ✓ JWT-based authentication without session storage
- **Cohere Integration**: ✓ Using Cohere API as primary LLM backend with proper tool calling
- **MCP Tools**: ✓ MCP-compatible tool definitions for all task/user operations
- **Multilingual Support**: ✓ Supporting English + Urdu as per spec

## Project Structure

### Documentation (this feature)

```text
specs/003-ai-chatbot-integration/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/
│   │   ├── __init__.py
│   │   ├── conversation_model.py      # Conversation and Message SQLModel classes
│   │   ├── user_model.py              # User model with relationships
│   │   └── task_model.py              # Task model with user_id foreign key
│   ├── services/
│   │   ├── __init__.py
│   │   ├── cohere_runner.py           # Custom Cohere runner with tool calling
│   │   ├── chat_service.py            # Chat endpoint business logic
│   │   ├── tool_executor.py           # MCP-compatible tool executor functions
│   │   └── auth_service.py            # JWT validation and user extraction
│   ├── api/
│   │   ├── __init__.py
│   │   ├── chat_router.py             # POST /api/{user_id}/chat endpoint
│   │   └── routers/                   # Other API routers
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── task_tools.py              # add_task, list_tasks, complete_task, etc.
│   │   └── user_tools.py              # get_user_profile tool
│   └── main.py                        # FastAPI app entry point
└── tests/
    ├── unit/
    ├── integration/
    └── contract/

frontend/
├── src/
│   ├── components/
│   │   ├── ChatbotIcon.tsx            # Floating chat icon component
│   │   ├── ChatWindow.tsx             # Main chat interface component
│   │   ├── MessageList.tsx            # Component for displaying messages
│   │   └── MessageInput.tsx           # Component for message input
│   ├── pages/
│   │   └── dashboard/
│   │       └── index.tsx              # Dashboard page with chat integration
│   ├── services/
│   │   └── api.ts                     # API service with JWT headers
│   └── styles/
│       └── globals.css                # Global styles including chat components
└── tests/
    ├── unit/
    └── integration/
```

**Structure Decision**: Web application with separate frontend and backend directories to maintain clear separation of concerns while enabling tight integration between the Cohere-powered chatbot backend and the Next.js frontend UI components.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Additional DB Models | Need Conversation and Message tables for chat persistence | Existing task/user models insufficient for chat state management |
| Cohere-specific Tool Calling | Need to adapt OpenAI patterns to Cohere's tool-calling API | Generic LLM approach would lack proper tool execution capabilities |
| MCP Tool Definitions | Need standardized tool interfaces for agentic operations | Direct API calls would violate agentic development principles |
