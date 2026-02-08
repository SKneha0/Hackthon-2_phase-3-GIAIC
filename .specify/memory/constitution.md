<!-- SYNC IMPACT REPORT
Version change: 1.1.0 → 2.0.0
Modified principles:
- Principle I: Spec-Driven Development → Enhanced Spec-Driven Development with Agentic Patterns
- Principle II: Zero Manual Coding → Full Agentic Development with Claude Code + Spec-Kit
- Principle III: Modular Architecture → Expanded Modular Architecture (includes MCP tools, Cohere integration)
- Principle IV: Complete User Isolation → Enhanced User Isolation (secure chatbot operations)
- Principle V: Technology Stack Compliance → Extended Tech Stack (Cohere + MCP + AI chatbot)
- Principle VI: Stateless Authentication → Enhanced Authentication (JWT for chat operations)
Added sections: New principles for stateless architecture, LLM integration, MCP tools, multilingual support, frontend integration
Removed sections: None
Templates requiring updates:
- .specify/templates/plan-template.md ✅ updated
- .specify/templates/spec-template.md ✅ updated
- .specify/templates/tasks-template.md ✅ updated
- .specify/templates/commands/*.md ✅ reviewed
Follow-up TODOs: None
-->

# Hackathon Phase III – AI Todo Chatbot Integration into Existing Full-Stack Todo Application Constitution

## Core Principles

### I. Enhanced Spec-Driven Development with Agentic Patterns
Full agentic, spec-driven development with zero manual coding – all implementation via Claude Code + Spec-Kit references; All features and functionality must be defined in spec documents before implementation begins; Every code change must be traceable to a specific requirement in the specifications; All development follows Model Context Protocol (MCP) tool patterns for agent integration.

### II. Full Agentic Development with Claude Code + Spec-Kit
All implementation must be generated via Claude Code using Spec-Kit references; No manual coding is allowed unless explicitly through automated generation tools; All changes must be reproducible through spec-driven processes; Agentic workflows must seamlessly integrate with existing Phase II functionality without disruption.

### III. Expanded Modular Architecture with MCP Tools and Cohere Integration
Modular architecture through agents and skills with clear separation of concerns including MCP tools, Cohere agents, and stateless chat services; Defined roles for Main Agent, Task Agent, Auth Agent, UI Agent, and AI Chat Agent; Clean interfaces between components with well-defined responsibilities; MCP tools remain standardized interface for agent-tool interaction exposing all task and user operations.

### IV. Enhanced User Isolation and Secure Chat Operations
Every API endpoint must filter data by authenticated user_id; Users can only access their own tasks and data; No data leakage between users under any circumstances; Strict enforcement of task ownership through user_id foreign keys; All chat operations protected by JWT (user_id from token), strict task/user isolation, no data leakage; Conversation state persisted only in database with user_id enforcement.

### V. Extended Technology Stack with Cohere and MCP
Strict adherence to extended technology stack: Next.js 16+, FastAPI, SQLModel, Neon Serverless PostgreSQL, Better Auth with JWT, Tailwind CSS, Cohere API for LLM backend, MCP SDK for agent tools; No external libraries beyond specified stack (Cohere SDK and Official MCP SDK only); Monorepo structure must follow documented layout exactly with added conversation/message tables.

### VI. Enhanced Stateless Authentication for Chat Operations
Better Auth configured with JWT plugin and shared BETTER_AUTH_SECRET between frontend and backend; No session storage on backend - authentication must be stateless (JWT only); All CRUD operations must enforce task ownership through verified authentication; Chat endpoint (POST /api/{user_id}/chat) requires valid JWT and enforces user_id ownership; All tools require user_id (from JWT) and enforce ownership.

### VII. Stateless Architecture for Scalability
Stateless architecture for scalability: conversation state persisted only in database (conversations + messages tables); No in-memory session – all state in DB; Stateless server design ensures scalability and resilience; Conversation context preserved across requests via DB persistence – resumes after server restart.

### VIII. Cohere API Integration and LLM Reasoning
Natural language chatbot that fully controls task management (add, list, complete, delete, update) and provides user profile information (id, email, name, createdAt); Use Cohere API as the primary LLM backend for agent reasoning, tool calling, and response generation; Adapt OpenAI Agents SDK patterns and code structure to work with Cohere API (use Cohere's tool-calling capabilities, structured outputs, and chat completions); Use Cohere API key via environment variable COHERE_API_KEY.

### IX. MCP Standardized Interface for Agent Tools
MCP (Model Context Protocol) tools remain the standardized interface for agent-tool interaction – expose all task and user operations as MCP-compatible tools; MCP Tools must exactly match spec: add_task, list_tasks, complete_task, delete_task, update_task + new get_user_profile; All tools follow MCP standards and work seamlessly with Cohere's tool-calling capabilities; Conversation history fetched from DB on every request, user/assistant messages stored after processing.

### X. Multilingual Support and User Experience
Friendly, contextual, and multilingual responses (English + Urdu support when relevant) with action confirmations and graceful error handling; Agent behavior: Understand natural language intents (e.g., "Add task buy milk", "Show pending tasks", "Mera profile batao", "Mark task 4 complete", "Delete the old one"); Responses must be culturally sensitive and support mixed-language queries where appropriate; Error handling returns helpful messages for task not found, invalid input, auth failure (401).

## Technical Standards

### API Endpoints and Contract
Chat endpoint: POST /api/{user_id}/chat (accepts conversation_id optional, message required) – returns conversation_id, response, tool_calls; Agent uses Cohere for reasoning/tool selection – successful tool calls visible in response (tool_calls array); Endpoint returns correct response format: {conversation_id, response, tool_calls}; All queries filtered by authenticated user_id from JWT middleware (reuse existing get_current_user).

### Database Schema Extensions
DB schema extensions: Conversation and Message tables with proper foreign key relationships to users table; All database queries must be filtered by authenticated user_id; Proper indexing for efficient conversation retrieval and message history access; Schema must support stateless architecture with complete conversation persistence.

### Frontend Integration Standards
Frontend: Integrate OpenAI ChatKit (or compatible Cohere-compatible chat UI) in existing Next.js app – call backend /api/{user_id}/chat; Domain allowlist prepared for OpenAI ChatKit hosted mode (even if using Cohere backend) – documented setup in README; ChatKit integration in Next.js (new page/route) with JWT attachment; Existing frontend maintains all Phase II functionality while adding new chat interface.

## Security and Access Control Standards

All API endpoints must require valid JWT token for access; Database schema must match specifications exactly with users table managed by Better Auth and tasks table with user_id foreign key; All database queries filtered by authenticated user_id; No direct database access from frontend - all operations via protected FastAPI endpoints; Public auth routes (signup/signin) remain unchanged; chat endpoint fully protected; No cross-user access to conversations or tasks.

## Development Workflow

All references in prompts must use @specs/path/to/file.md format; Code structure must follow guidelines in root CLAUDE.md, frontend/CLAUDE.md, and backend/CLAUDE.md; Responsive, clean UI using Tailwind CSS and Next.js App Router (server components by default); Every change must be specifiable and traceable; Swagger docs updated to include /api/{user_id}/chat endpoint; Environment variables: Add COHERE_API_KEY; reuse BETTER_AUTH_SECRET, NEON_DB_URL.

## Quality Assurance

Chatbot fully manages tasks via natural language: add, list (with filters), complete, delete, update – with friendly confirmations; User profile queries work: "Mera email kya hai?" → returns id, email, name, createdAt; Conversation context preserved across requests via DB persistence – resumes after server restart; All operations secure: JWT required, user_id enforced, no cross-user access; Agent uses Cohere for reasoning/tool selection – successful tool calls visible in response (tool_calls array); Endpoint returns correct response format: {conversation_id, response, tool_calls}; Full integration: Existing frontend can add ChatKit UI tab/page calling backend chat endpoint; Zero regressions in Phase II functionality (task CRUD, auth).

## Governance

Constitution supersedes all other development practices and must be strictly followed; All amendments to this constitution require formal documentation and approval; All pull requests and reviews must verify compliance with these principles; Code changes must be accompanied by corresponding spec updates; All implementations must be fully testable and verifiable against acceptance criteria; Success criteria: Judges confirm "Seamless Phase III upgrade – agentic, secure, scalable, Cohere-powered, fully spec-driven"; Runs locally with docker-compose (frontend + backend + Neon).

**Version**: 2.0.0 | **Ratified**: 2026-02-06 | **Last Amended**: 2026-02-06