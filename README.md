# AI Todo Application - Backend

This is the backend for the AI-powered Todo application built with FastAPI and PostgreSQL.

## Features

- Task management with CRUD operations
- AI agent execution for natural language processing
- Skills-based architecture for business logic
- Authentication with Better Auth
- RESTful API design
- Async database operations

## Tech Stack

- FastAPI (Python 3.10+)
- PostgreSQL (with Neon)
- SQLAlchemy (async)
- Alembic (for migrations)
- Pydantic (for data validation)
- Better Auth (for authentication)

## Getting Started

### Prerequisites

- Python 3.10+
- PostgreSQL database (or Neon account)
- pip package manager

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your actual configuration
   ```

5. Run the application:
   ```bash
   uvicorn main:app --reload
   ```

The API will be available at `http://localhost:8000`.

## API Endpoints

### Task Management

- `POST /api/tasks` - Create a new task
- `GET /api/tasks` - Get all tasks with optional filtering
- `GET /api/tasks/{id}` - Get a specific task
- `PUT /api/tasks/{id}` - Update a specific task
- `DELETE /api/tasks/{id}` - Delete a specific task

### AI Agent

- `POST /api/agent/run` - Execute an AI agent with specified parameters

## Architecture

### Layers

- **Routers**: Handle API endpoints and request/response
- **Services**: Contain business logic and coordinate operations
- **Agents**: Orchestrate skills for complex operations
- **Skills**: Atomic operations that perform specific tasks
- **Models**: Database entity definitions
- **Schemas**: Pydantic models for request/response validation

### Agent Architecture

The application uses an agent-based architecture where agents coordinate skills to perform complex operations:

- **Task Agent**: Handles task-related operations
- **Natural Language Agent**: Processes natural language commands

### Skills Architecture

Skills are atomic operations that perform specific tasks:

- **Task Creation Skill**: Creates new tasks
- **Task Query Skill**: Retrieves tasks
- **Task Update Skill**: Updates tasks
- **Task Deletion Skill**: Deletes tasks

## Database Schema

The application uses PostgreSQL with the following tables:

- `users`: Stores user information
- `tasks`: Stores task information
- `agent_logs`: Stores logs of agent executions

## Environment Variables

- `DATABASE_URL`: PostgreSQL connection string
- `AUTH_SECRET`: Secret key for authentication
- `AUTH_FRONTEND_URL`: Frontend URL for auth redirects
- `SECRET_KEY`: Secret key for JWT tokens

## Running Tests

To run tests:
```bash
pytest
```

## Deployment

For production deployment:
1. Set up a production database
2. Configure environment variables
3. Run database migrations
4. Deploy the application

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request