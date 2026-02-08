# Data Model: AI Todo Chatbot Integration

## Entities

### Conversation
Represents a persistent chat session containing multiple exchanges between user and AI; linked to a specific user

**Fields**:
- `id` (UUID/int): Primary key, unique identifier for the conversation
- `user_id` (UUID/string): Foreign key linking to the user who owns this conversation
- `title` (string, optional): Auto-generated short title from first user message
- `created_at` (datetime): Timestamp when conversation was created
- `updated_at` (datetime): Timestamp when conversation was last updated

**Relationships**:
- Belongs to one User (via user_id foreign key)
- Has many Messages (one-to-many relationship)

**Validation Rules**:
- user_id must exist in users table
- title max length 100 characters if provided
- created_at and updated_at are automatically set by database

### Message
Represents individual exchanges within a conversation; contains role (user/assistant), content, timestamp; belongs to a Conversation

**Fields**:
- `id` (UUID/int): Primary key, unique identifier for the message
- `conversation_id` (UUID/int): Foreign key linking to the conversation
- `role` (string): Role of the message sender ('user' or 'assistant')
- `content` (text): The actual content of the message
- `tool_calls` (JSON, optional): Any tool calls made by the AI (as JSON object)
- `created_at` (datetime): Timestamp when message was created

**Relationships**:
- Belongs to one Conversation (via conversation_id foreign key)

**Validation Rules**:
- conversation_id must exist in conversations table
- role must be either 'user' or 'assistant'
- content is required (not empty)
- tool_calls must be valid JSON if present

### Task (Existing from Phase II, extended)
Represents user tasks with additional fields for enhanced functionality

**Fields**:
- `id` (UUID/int): Primary key
- `user_id` (UUID/string): Foreign key to user who owns this task
- `title` (string): Task title
- `description` (text, optional): Detailed description of the task
- `due_date` (datetime, optional): When the task is due
- `completed` (boolean): Whether the task is completed
- `completed_at` (datetime, optional): When the task was marked as completed
- `created_at` (datetime): Timestamp when task was created
- `updated_at` (datetime): Timestamp when task was last updated

**Relationships**:
- Belongs to one User (via user_id foreign key)

### UserProfile (Reference to existing user data)
Represents user account information accessible via natural language queries

**Fields**:
- `id` (UUID/string): Primary key from Better Auth
- `email` (string): User's email address
- `name` (string): User's name
- `created_at` (datetime): Account creation timestamp

**Note**: This represents existing user data from Better Auth system

## Relationships Diagram

```
Users (1) <---> (Many) Conversations (1) <---> (Many) Messages
Users (1) <---> (Many) Tasks
```

## State Transitions

### Task States
- **Active** → **Completed**: When user marks task as complete
  - `completed` field changes from false to true
  - `completed_at` field is set to current timestamp
- **Completed** → **Active**: When user unmarks task as complete
  - `completed` field changes from true to false
  - `completed_at` field is set to null

### Message States
- Messages are immutable once created
- No state transitions for messages, only creation and deletion

## Indexing Strategy

### Database Indexes
- `conversations.user_id`: For efficient user-based conversation retrieval
- `messages.conversation_id`: For efficient conversation-based message retrieval
- `messages.created_at`: For chronological message ordering
- `tasks.user_id`: For efficient user-based task filtering
- `tasks.completed`: For efficient task status filtering
- `tasks.created_at`: For chronological task ordering