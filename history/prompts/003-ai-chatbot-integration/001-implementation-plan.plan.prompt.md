---
id: 1
title: "Implementation Plan for Phase III – AI Todo Chatbot"
stage: plan
date_iso: "2026-02-07"
surface: "agent"
model: "Claude Sonnet 4.5"
feature: "003-ai-chatbot-integration"
branch: "003-ai-chatbot-integration"
user: "Neha Shahzad"
command: "/sp.plan Implementation Plan for Phase III – AI Todo Chatbot (Cohere-Powered Integration)"
labels:
  - "ai-chatbot"
  - "cohere"
  - "planning"
  - "spec-driven"
links:
  spec: "./spec.md"
  ticket: "null"
  adr: "null"
  pr: "null"
files_yaml:
  - "specs/003-ai-chatbot-integration/plan.md"
  - "specs/003-ai-chatbot-integration/research.md"
  - "specs/003-ai-chatbot-integration/data-model.md"
  - "specs/003-ai-chatbot-integration/quickstart.md"
  - "specs/003-ai-chatbot-integration/contracts/chat-api.yaml"
  - "specs/003-ai-chatbot-integration/contracts/mcp-tools.md"
tests_yaml:
  - "N/A (Planning phase)"
prompt_text: |
  Implementation Plan for Phase III – AI Todo Chatbot (Cohere-Powered Integration)
  Create:

  Updated backend architecture diagram showing how Cohere + custom agent runner fits into existing FastAPI server
  New database schema extensions (Conversation and Message models) with relationships to users
  MCP-compatible tool definitions in Cohere format (JSON schema for tool calling)
  Custom Cohere Runner class / function that mimics OpenAI Agents SDK behavior (chat → tool call detection → execution → final response)
  Chat endpoint logic flow: auth → load history → call Cohere → execute tools → save messages → return response
  Frontend chatbot UI integration plan: floating icon, modal/chat window, message streaming simulation, typing indicator
  Environment variable & security checklist (COHERE_API_KEY, domain allowlist prep)
  Error & fallback strategy document (tool failure, rate limit, invalid JWT)

  Decisions needing documentation:

  Cohere model choice: command-r-plus (better reasoning/tool use) vs command-r (faster, cheaper) → Choose command-r-plus for best tool-calling accuracy in hackathon demo
  Tool calling implementation: Use Cohere native tool calling vs force JSON mode → Native tool calling (more reliable, supports parallel calls)
  Chat UI technology: Hosted OpenAI ChatKit vs custom React + Tailwind component → Hybrid: Try hosted ChatKit first (configure domain allowlist), fallback to custom lightweight modal if setup fails
  Floating icon style: Circular FAB vs chat bubble icon → Modern circular FAB with subtle pulse animation on new messages (inspired by WhatsApp/Telegram)
  Message history limit: Unlimited vs truncate after N messages → Truncate to last 20 messages per conversation (prevents token blowup)
  Tool execution order: Sequential vs parallel when multiple tools called → Parallel execution when possible (Cohere supports it)
  Response streaming: Full response vs simulate typing → Simulate typing effect in frontend (no real streaming from Cohere in basic setup)
  Conversation naming: Auto-generate from first message vs manual → Auto-generate short title from first user message

  Testing strategy (validation against success criteria):

  Natural language task commands: Test 10+ variations ("Add task buy milk", "Show all tasks", "Mark task 3 done", "Delete the first one", "Change task 2 to call mom")
  Profile queries: "Mera email kya hai?", "Who am I logged in as?", "Mera naam batao" → correct data returned
  Context preservation: Send 5 messages, restart backend, continue same conversation_id → history intact
  Security: Try accessing chat without JWT → 401; try task operations for wrong user_id → 403 or no data
  Tool calls visibility: Check response.tool_calls array shows correct tools invoked
  UI integration: Floating icon appears only when logged in; chat window opens/closes smoothly; messages display correctly
  Multilingual: Test Urdu commands ("Ek task add karo grocery khareedne ka") → understood and executed
  Edge cases: Empty message, very long input, task not found, duplicate task title, rate limit simulation
  End-to-end: Signup → login → open chat → manage tasks → see updates in main task list UI

  Technical details:

  Use spec-concurrent approach: Implement backend chatbot logic first, then frontend UI, iterate with @specs references
  Cohere integration: cohere.Client with api_key from env, tools defined as list of dicts (name, description, parameters schema)
  Custom runner: Function that takes history + new message → calls cohere.chat() → if tool_calls → execute via existing FastAPI route logic or direct DB calls → feed results back → final response
  DB: Use SQLModel to define Conversation(user_id, id, title?, created_at) and Message(conversation_id, role, content, created_at)
  Frontend: Add /components/ChatbotIcon.tsx, /components/ChatWindow.tsx; use existing api.ts to call /api/{user_id}/chat
  JWT: Reuse get_current_user dependency → pass user_id to tools automatically

  Organize by phases:

  Foundation
  → Add COHERE_API_KEY to .env
  → Extend DB schema: Conversation + Message models
  → Create tools list in Cohere-compatible format (add_task, list_tasks, ..., get_user_profile)
  Backend – Chat Endpoint & Agent Runner
  → Implement POST /api/{user_id}/chat (protected)
  → Build custom CohereRunner: load history, call Cohere, handle tool calls, save messages
  → Integrate existing task & user logic as tool executors
  MCP Tools Implementation
  → Code each tool function (add_task → DB insert, list_tasks → query with filter, etc.)
  → Ensure every tool enforces user_id ownership
  Frontend – Chatbot UI
  → Add floating chatbot icon (visible only logged-in)
  → Create chat modal/window with message list, input, send button
  → Implement message sending to backend + display responses
  → Add typing indicator + auto-scroll
  Polish & Optimizations
  → Friendly response formatting (action confirmations, emojis)
  → Error handling in UI (connection lost, invalid response)
  → Dark mode consistency with main app
  → Performance: Limit history sent to Cohere (last 15–20 messages)
  Final Integration & Review
  → Full end-to-end testing: chat controls tasks → main UI reflects changes
  → Verify no regressions in Phase II CRUD
  → Document domain allowlist setup for ChatKit (if used)
  → Judges-ready demo flow: login → chat → manage tasks conversationally

  This plan ensures a clean, powerful, Cohere-powered AI chatbot that feels like a natural 2026 upgrade to your existing premium Todo app – fully integrated, secure, delightful, and spec-driven from start to finish.
response_text: |
  Successfully created the implementation plan for the AI Todo Chatbot Integration with Cohere. The following artifacts were generated:

  1. Updated `plan.md` with comprehensive implementation strategy
  2. Created `research.md` with architecture decisions and technology choices
  3. Created `data-model.md` with entity definitions for Conversation and Message models
  4. Created `quickstart.md` with setup and usage instructions
  5. Created API contracts in YAML format for the chat endpoint
  6. Defined MCP-compatible tool contracts for task and user operations

  The plan addresses all the key aspects requested:
  - Cohere model choice (command-r-plus for best tool-calling accuracy)
  - Database schema extensions (Conversation and Message models)
  - MCP-compatible tool definitions
  - Custom Cohere runner architecture
  - Security and authentication considerations
  - Frontend integration strategy

  All constitutional principles were verified to be compliant during both initial check and post-design review.
outcome: "Successfully completed implementation planning for AI Todo Chatbot Integration with Cohere"
evaluation: "Plan is comprehensive, covers all required aspects, and maintains alignment with constitutional principles"
---

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

**Post-Design Constitution Check**: All design decisions comply with constitutional principles established in .specify/memory/constitution.md

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