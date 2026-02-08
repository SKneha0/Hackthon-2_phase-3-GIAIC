# Quickstart Guide: AI Todo Chatbot Integration

## Prerequisites

- Python 3.11+
- Node.js 18+
- Poetry (for Python dependency management)
- npm/yarn/pnpm (for frontend dependencies)
- Cohere API Key
- Database (Neon Serverless PostgreSQL instance)

## Environment Setup

### Backend Setup

1. **Install Python dependencies**:
```bash
cd backend
poetry install
poetry shell
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

## Key Features & Usage

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

## Architecture Overview

### Backend Components

- `src/models/conversation_model.py`: Conversation and Message SQLModel definitions
- `src/services/cohere_runner.py`: Custom Cohere runner with tool calling capabilities
- `src/api/chat_router.py`: Handles POST /api/{user_id}/chat endpoint
- `src/tools/task_tools.py`: MCP-compatible task management tools
- `src/tools/user_tools.py`: User profile information tools

### Frontend Components

- `src/components/ChatbotIcon.tsx`: Floating chat icon component
- `src/components/ChatWindow.tsx`: Main chat interface
- `src/components/MessageList.tsx`: Displays conversation history
- `src/components/MessageInput.tsx`: Handles user input submission

## Development Commands

### Backend
- **Run tests**: `pytest`
- **Format code**: `black src/ && ruff check src/ --fix`
- **Lint**: `ruff check src/`

### Frontend
- **Run tests**: `npm test`
- **Lint**: `npm run lint`
- **Format**: `npm run format`

## API Endpoints

### Chat Endpoint
- **Endpoint**: `POST /api/{user_id}/chat`
- **Headers**: Authorization: Bearer {jwt_token}
- **Body**: `{ "message": "user's message", "conversation_id": "optional" }`
- **Response**: `{ "conversation_id": "...", "response": "...", "tool_calls": [...] }`

## Troubleshooting

### Common Issues

1. **Authentication failures**:
   - Verify JWT token is properly set in frontend requests
   - Check BETTER_AUTH_SECRET matches between frontend and backend

2. **Cohere API errors**:
   - Confirm COHERE_API_KEY is set correctly
   - Check internet connectivity to Cohere API endpoints

3. **Database connection issues**:
   - Verify NEON_DB_URL is properly configured
   - Ensure database migration ran successfully

4. **Chat UI not appearing**:
   - Check if user is properly authenticated
   - Verify frontend environment variables are set correctly

## Production Deployment

### Backend
```bash
# Build and run in production mode
gunicorn src.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Frontend
```bash
# Build and serve
npm run build && npm start
```