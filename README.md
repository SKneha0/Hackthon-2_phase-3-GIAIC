# AI Todo Chatbot Integration

This project integrates a Cohere-powered AI chatbot into the existing Next.js + FastAPI todo application, providing natural language task management and user profile information retrieval with multilingual support.

## Features

- **Natural Language Task Management**: Add, list, complete, delete, and update tasks using natural language commands
- **User Profile Information**: Retrieve user profile information through the chatbot
- **Multilingual Support**: Support for English and Urdu languages
- **Persistent Conversation History**: Chat history preserved across sessions
- **Unobtrusive UI**: Floating chat icon that appears only when logged in

## Architecture

### Backend Components

- `src/models/conversation_model.py`: Conversation and Message SQLModel classes
- `src/services/cohere_runner.py`: Custom Cohere runner with tool calling capabilities
- `src/api/chat_router.py`: Handles POST /api/{user_id}/chat endpoint
- `src/tools/task_tools.py`: MCP-compatible task management tools
- `src/tools/user_tools.py`: User profile information tools
- `src/services/tool_executor.py`: MCP-compatible tool executor functions

### Frontend Components

- `src/components/ChatbotIcon.tsx`: Floating chat icon component
- `src/components/ChatWindow.tsx`: Main chat interface component
- `src/components/MessageList.tsx`: Component for displaying messages
- `src/components/MessageInput.tsx`: Component for message input
- `src/pages/dashboard/index.tsx`: Dashboard page with chat integration
- `src/services/api.ts`: API service with JWT headers

## Setup

### Backend Setup

1. **Install Python dependencies**:
```bash
cd backend
pip install -r requirements.txt
```

2. **Set up environment variables** in `.env` file:
```bash
# Cohere API
COHERE_API_KEY=your_cohere_api_key_here

# Auth
BETTER_AUTH_SECRET=your_secret_key
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:8000

# Database
NEON_DB_URL=your_neon_db_connection_string

# Optional - for production
ALLOWED_ORIGINS=http://localhost:3000
```

3. **Run database migrations**:
```bash
python -m src.main init-db
```

4. **Start the backend server**:
```bash
python -m src.main dev
```

### Frontend Setup

1. **Install dependencies**:
```bash
cd frontend
npm install
```

2. **Copy environment template**:
```bash
cp .env.example .env.local
```

3. **Update environment variables** in `.env.local`:
```bash
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:8000
```

4. **Start the frontend server**:
```bash
npm run dev
```

## Usage

### Starting a Chat Session

1. **Login to the application** at `http://localhost:3000`
2. **Click the floating chat icon** in the bottom-right corner
3. **Begin typing natural language commands** such as:
   - "Add task: Buy groceries"
   - "Show my pending tasks"
   - "Mark task 3 as complete"
   - "What is my email?"
   - "Mera email kya hai?"

### Supported Commands

#### Task Management
- **Adding tasks**: "Add task: [task title]", "Create task: [task description]"
- **Listing tasks**: "Show my tasks", "List pending tasks", "Show completed tasks"
- **Completing tasks**: "Complete task 3", "Mark task as done", "Finish the first task"
- **Deleting tasks**: "Delete task 2", "Remove the third task"
- **Updating tasks**: "Update task 1 to [new description]"

#### Profile Information
- **User details**: "Who am I?", "What is my email?", "Mera naam batao", "Mera email kya hai?"

## Testing

Run the backend tests:
```bash
cd backend
pytest
```

## API Endpoints

### Chat Endpoint
- **Endpoint**: `POST /api/{user_id}/chat`
- **Headers**: Authorization: Bearer {jwt_token}
- **Body**: `{ "message": "user's message", "conversation_id": "optional" }`
- **Response**: `{ "conversation_id": "...", "response": "...", "message_id": "..." }`

## Security

- JWT-based authentication with user isolation
- All database queries filtered by authenticated user_id
- Conversation access restricted to owning user
- Rate limiting to prevent API abuse

## Technologies Used

- **Backend**: Python, FastAPI, SQLModel, Neon PostgreSQL
- **Frontend**: Next.js, React, TypeScript, Tailwind CSS
- **AI/ML**: Cohere API for natural language processing
- **Authentication**: Better Auth
- **Testing**: pytest