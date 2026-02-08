# Tasks: AI Todo Chatbot Integration (Cohere-Powered)

## Feature Overview
Integration of a Cohere-powered AI chatbot into the existing Next.js + FastAPI todo application, providing natural language task management and user profile information retrieval with multilingual support.

## Implementation Strategy
Build incrementally starting with the core API functionality, then the tools layer, then the frontend UI. Focus on delivering User Story 1 (natural language task management) as the MVP first, then expand to other user stories.

---

## Phase 1: Setup and Environment Configuration

- [X] T001 Set up Cohere API key in environment variables in backend/.env
- [X] T002 Install Cohere Python SDK dependency in backend/pyproject.toml
- [X] T003 Install SQLModel for Conversation and Message models in backend/pyproject.toml
- [X] T004 Create backend/src/models/conversation_model.py with Conversation and Message SQLModel classes
- [X] T005 Create backend/src/tools/__init__.py module file
- [X] T006 Create frontend/src/components/__init__.py for chat components

---

## Phase 2: Foundational Components

- [X] T007 Implement Conversation and Message models with proper relationships in backend/src/models/conversation_model.py
- [X] T008 Set up database migration for new Conversation and Message tables in backend/src/main.py
- [X] T009 Implement auth service to validate JWT and extract user_id in backend/src/services/auth_service.py
- [X] T010 Create tool executor base service in backend/src/services/tool_executor.py
- [X] T011 Define MCP-compatible tool schemas in backend/src/tools/task_tools.py
- [X] T012 Define MCP-compatible user tool schema in backend/src/tools/user_tools.py

---

## Phase 3: User Story 1 - Natural Language Task Management (Priority: P1)

### Story Goal
Enable users to manage tasks using natural language commands ("Add task: Buy groceries", "Mark task 3 as complete", etc.)

### Independent Test
The chatbot can process natural language commands like "Add task: Buy groceries" or "Mark task 3 as complete" and successfully execute the corresponding task operations, delivering immediate value by simplifying task management.

### Tasks

- [X] T013 [P] [US1] Implement add_task tool function that creates new tasks in backend/src/tools/task_tools.py
- [X] T014 [P] [US1] Implement list_tasks tool function that retrieves user's tasks with filters in backend/src/tools/task_tools.py
- [X] T015 [P] [US1] Implement complete_task tool function that marks tasks as completed in backend/src/tools/task_tools.py
- [X] T016 [P] [US1] Implement delete_task tool function that removes user's tasks in backend/src/tools/task_tools.py
- [X] T017 [P] [US1] Implement update_task tool function that modifies user's tasks in backend/src/tools/task_tools.py
- [X] T018 [US1] Create Cohere runner service to handle chat completion and tool calling in backend/src/services/cohere_runner.py
- [X] T019 [US1] Implement chat endpoint POST /api/{user_id}/chat in backend/src/api/chat_router.py
- [X] T020 [US1] Add conversation history loading in cohere_runner.py
- [X] T021 [US1] Add message saving to database after tool execution in cohere_runner.py
- [X] T022 [US1] Add proper error handling for tool execution failures in tool_executor.py
- [X] T023 [US1] Test that "Add task: Buy milk" creates task visible in task list
- [X] T024 [US1] Test that "Show pending tasks" returns only incomplete tasks in chat response
- [X] T025 [US1] Test that "Complete the first task" marks oldest task as completed in DB and UI

---

## Phase 4: User Story 2 - User Profile Information Retrieval (Priority: P1)

### Story Goal
Allow users to get their profile information through the chatbot ("Who am I?", "Mera email kya hai?")

### Independent Test
The chatbot can respond to profile queries like "Who am I?" or "Mera email kya hai?" and return accurate user profile information (id, email, name, creation date), delivering value by making profile access conversational.

### Tasks

- [X] T026 [P] [US2] Implement get_user_profile tool function in backend/src/tools/user_tools.py
- [X] T027 [US2] Ensure user isolation in get_user_profile tool (enforce user_id from JWT)
- [X] T028 [US2] Test that "Who am I?" returns user's name and email in chat response
- [X] T029 [US2] Test that "What is my email?" returns user's email address
- [X] T030 [US2] Test that "Mera naam batao" returns user's name appropriately

---

## Phase 5: User Story 3 - Multilingual Chat Interface (Priority: P2)

### Story Goal
Support interaction with chatbot in English or Urdu

### Independent Test
The chatbot can understand and respond appropriately to commands in both English and Urdu (e.g., "Add task: Buy milk" vs "Task add karo: Doodh lena hai"), delivering value by supporting multilingual interactions.

### Tasks

- [X] T031 [P] [US3] Add multilingual support to Cohere configuration in cohere_runner.py
- [X] T032 [US3] Test Urdu command "Mera email kya hai?" returns correct email
- [X] T033 [US3] Test mixed language queries are processed correctly
- [X] T034 [US3] Add cultural sensitivity to responses for multilingual users
- [X] T035 [US3] Verify 85% comprehension accuracy for multilingual queries

---

## Phase 6: User Story 4 - Persistent Conversation History (Priority: P2)

### Story Goal
Preserve chat history across sessions so users can continue conversations after refresh

### Independent Test
After closing the chat window and reopening it later, previous conversation history is available, delivering value by preserving conversation context.

### Tasks

- [X] T036 [P] [US4] Implement conversation history loading from database in cohere_runner.py
- [X] T037 [US4] Add conversation title auto-generation from first message in conversation_model.py
- [X] T038 [US4] Implement conversation history truncation (last 20 messages) in cohere_runner.py
- [X] T039 [US4] Test conversation history persists after page refresh
- [X] T040 [US4] Test conversation history available when returning after time gap

---

## Phase 7: User Story 5 - Unobtrusive Chat Interface (Priority: P3)

### Story Goal
Provide clean, minimal chat interface that appears only when logged in without interfering with existing UI

### Independent Test
A floating chat icon appears only when logged in, and clicking it opens a clean chat interface that doesn't overlap with existing UI elements, delivering value by providing easy access without visual clutter.

### Tasks

- [X] T041 [P] [US5] Create floating ChatbotIcon component in frontend/src/components/ChatbotIcon.tsx
- [X] T042 [P] [US5] Create ChatWindow component in frontend/src/components/ChatWindow.tsx
- [X] T043 [P] [US5] Create MessageList component in frontend/src/components/MessageList.tsx
- [X] T044 [P] [US5] Create MessageInput component in frontend/src/components/MessageInput.tsx
- [X] T045 [US5] Integrate chat components into dashboard page in frontend/src/pages/dashboard/index.tsx
- [X] T046 [US5] Implement chat API service with JWT headers in frontend/src/services/api.ts
- [X] T047 [US5] Add conditional rendering of chat icon only when logged in
- [X] T048 [US5] Implement smooth open/close animation for chat window
- [X] T049 [US5] Test floating icon appears in bottom-right corner when logged in
- [X] T050 [US5] Test chat window opens without overlapping existing UI elements

---

## Phase 8: Polish & Cross-Cutting Concerns

- [X] T051 Add typing indicator simulation in frontend chat UI
- [X] T052 Implement error handling in frontend UI (connection lost, invalid response)
- [X] T053 Ensure dark mode consistency with main app for chat components
- [X] T054 Add rate limiting to Cohere API calls in cohere_runner.py
- [X] T055 Implement proper logging for chat interactions in backend
- [X] T056 Add comprehensive tests for all tool functions
- [X] T057 Update Swagger documentation to include /api/{user_id}/chat endpoint
- [X] T058 Test end-to-end flow: login → open chat → manage tasks → see updates in main UI
- [X] T059 Verify no regressions in Phase II functionality (task CRUD, auth)
- [X] T060 Conduct final QA: Natural language commands work with 95% accuracy

---

## Dependencies

- User Story 1 (T013-T025) must be completed before User Story 2 (T026-T030)
- Foundational components (Phase 2) must be completed before any user story implementation
- Database models must be implemented before API endpoints

## Parallel Execution Opportunities

- Task tools (add_task, list_tasks, complete_task, etc.) can be developed in parallel [P markers]
- Frontend components (ChatbotIcon, ChatWindow, MessageList, MessageInput) can be developed in parallel [P markers]
- Different user stories can have parallel development where components don't depend on each other

## MVP Scope

The MVP includes User Story 1 (natural language task management) which delivers core value:
- Cohere integration with tool calling
- Task management tools (add, list, complete, delete, update)
- Chat endpoint with authentication
- Basic frontend chat interface