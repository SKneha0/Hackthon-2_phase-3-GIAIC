# Research: AI Todo Chatbot Integration (Cohere-Powered)

## Overview
This research document captures findings and decisions for implementing the Cohere-powered AI chatbot in the existing full-stack todo application.

## Architecture Research

### Cohere Model Selection
- **Decision**: Use `command-r-plus` model for Phase III implementation
- **Rationale**: Better reasoning and tool-calling accuracy compared to `command-r`, which is important for the hackathon demo to ensure reliable task management operations
- **Alternatives considered**:
  - `command-r`: Faster and cheaper but lower accuracy for complex tool calling
  - Other Cohere models: Not optimized for tool-calling patterns needed for task management

### Tool Calling Implementation
- **Decision**: Use Cohere native tool calling instead of forcing JSON mode
- **Rationale**: Native tool calling is more reliable and supports parallel tool execution when multiple tools are called simultaneously
- **Alternatives considered**:
  - JSON mode parsing: More error-prone and doesn't leverage Cohere's native capabilities
  - Function calling pattern: Less standardized than native tool calling

### Chat UI Technology Choice
- **Decision**: Hybrid approach - try OpenAI ChatKit first with domain allowlist configuration, fallback to custom lightweight modal
- **Rationale**: Leverages existing UI framework while providing fallback option if domain configuration fails
- **Alternatives considered**:
  - Pure custom React component: More control but requires more development time
  - Third-party chat widget: Potential security concerns and customization limitations

### Floating Icon Style
- **Decision**: Modern circular FAB (Floating Action Button) with subtle pulse animation for new messages
- **Rationale**: Inspired by WhatsApp/Telegram, provides familiar UX while being unobtrusive
- **Alternatives considered**:
  - Traditional chat bubble: Can be visually intrusive on modern designs
  - Menu item: Less discoverable and accessible

### Message History Management
- **Decision**: Truncate to last 20 messages per conversation to prevent token blowup
- **Rationale**: Balances context preservation with cost management and performance
- **Alternatives considered**:
  - Unlimited history: Could lead to excessive token usage and slow responses
  - Shorter history (e.g., 5 messages): Might lose important context

### Tool Execution Order
- **Decision**: Parallel execution when possible since Cohere supports it
- **Rationale**: More efficient execution when multiple tools are called simultaneously
- **Alternatives considered**:
  - Sequential execution: Slower but simpler to implement and debug

### Response Streaming
- **Decision**: Simulate typing effect in frontend instead of real streaming from Cohere
- **Rationale**: Simpler initial implementation, no need for complex streaming infrastructure
- **Alternatives considered**:
  - Real streaming: Better UX but more complex implementation

### Conversation Naming
- **Decision**: Auto-generate short title from first user message
- **Rationale**: Provides useful context without burdening users with manual naming
- **Alternatives considered**:
  - Manual naming: More user control but adds friction to conversation initiation

## Technical Implementation Research

### Database Schema Extensions
- **Conversation Model**:
  - Fields: id, user_id (FK to users), title (optional, auto-generated), created_at, updated_at
  - Relationships: One-to-many with Message model, belongs to User
- **Message Model**:
  - Fields: id, conversation_id (FK), role ('user'/'assistant'), content (text), created_at
  - Relationships: Belongs to Conversation

### MCP-Compatible Tool Definitions
Each tool follows the JSON schema format required by Cohere's tool calling:

- **add_task**: Creates new task with title, description, due_date
- **list_tasks**: Retrieves tasks with filters (completed, pending, all)
- **complete_task**: Marks specific task as completed
- **delete_task**: Removes specific task
- **update_task**: Modifies existing task properties
- **get_user_profile**: Returns user's id, email, name, createdAt

### Security and Authentication
- JWT authentication reused from existing Better Auth implementation
- All database queries filtered by authenticated user_id
- Conversation access restricted to owning user
- Rate limiting considerations for Cohere API calls

## Best Practices Research

### Error Handling Strategy
- Graceful degradation when Cohere API is unavailable
- Helpful error messages for tool execution failures
- Proper validation of tool parameters before execution
- Clear distinction between LLM errors and application errors

### Performance Optimization
- Limit history sent to Cohere (last 15-20 messages)
- Caching for frequently accessed user data
- Efficient database queries with proper indexing
- Client-side optimizations for chat UI responsiveness

### Internationalization
- English primary language support
- Urdu language support for common commands
- Culturally appropriate responses for multilingual users
- Mixed-language query handling capability

## Dependencies and Integrations

### Primary Dependencies
- Cohere Python SDK for LLM interactions
- SQLModel for database models and queries
- FastAPI for backend API development
- Better Auth for authentication and JWT handling
- Next.js for frontend development

### Environment Variables
- COHERE_API_KEY: Required for Cohere API access
- BETTER_AUTH_SECRET: Shared secret for JWT validation
- NEON_DB_URL: Database connection string
- ALLOWED_ORIGINS: For CORS configuration if using ChatKit

## Conclusion
This research provides a solid foundation for implementing the Cohere-powered AI chatbot with proper architecture decisions, security measures, and performance considerations in place.