# Customer Support Assistant Backend

A FastAPI-based customer support system with AI integration using Groq API for generating responses.

## Features

- User authentication with JWT
- Support ticket management
- Real-time AI response streaming
- Role-based access control
- PostgreSQL database integration
- Docker containerization

## Architecture

The application follows a service-oriented architecture with the following components:

### Design Patterns Used

1. **Repository Pattern**: Implemented in the base service class to abstract database operations
2. **Dependency Injection**: Used throughout the application for better testability and loose coupling
3. **Factory Pattern**: Used in the service layer for creating service instances

### Project Structure

```
src/
├── api/
│   └── v1/
│       ├── endpoints/
│       │   ├── auth.py
│       │   └── tickets.py
│       └── api.py
├── core/
│   ├── config.py
│   └── security.py
├── db/
│   └── session.py
├── models/
│   ├── base.py
│   └── models.py
├── schemas/
│   ├── ticket.py
│   └── user.py
├── services/
│   ├── ai.py
│   ├── base.py
│   ├── ticket.py
│   └── user.py
└── main.py
```

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd customer-support-assistant
   ```

2. Install Poetry (if not already installed):
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

3. Install dependencies:
   ```bash
   poetry install
   ```

4. Create a `.env` file:
   ```bash
   cp .env.example .env
   ```
   Edit the `.env` file with your configuration values.

5. Initialize the database:
   ```bash
   # Make the database script executable
   chmod +x scripts/db.sh
   
   # Initialize the database
   ./scripts/db.sh init
   ```

6. Run with Docker:
   ```bash
   docker-compose up --build
   ```

   Or run locally:
   ```bash
   poetry run uvicorn src.main:app --reload
   ```

## Database Management

The project uses Alembic for database migrations. Here are some common commands:

```bash
# Create a new migration
./scripts/db.sh migrate "description of changes"

# Apply all pending migrations
./scripts/db.sh upgrade

# Rollback the last migration
./scripts/db.sh downgrade

# Reset the database (drop all tables and recreate)
./scripts/db.sh reset
```

## API Documentation

Once the application is running, you can access the API documentation at:
- Swagger UI: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc

### Available Endpoints

#### Authentication
- `POST /api/v1/auth/signup` - Create a new user
- `POST /api/v1/auth/login` - Login and receive JWT

#### Tickets
- `GET /api/v1/tickets` - List user's tickets
- `POST /api/v1/tickets` - Create a new support ticket
- `GET /api/v1/tickets/{ticket_id}` - Get a specific ticket
- `POST /api/v1/tickets/{ticket_id}/messages` - Add a message to a ticket
- `GET /api/v1/tickets/{ticket_id}/ai-response` - Stream AI response (SSE)

## Development

### Running Tests
```bash
poetry run pytest
```

### Code Formatting
```bash
poetry run black .
poetry run isort .
```

### Type Checking
```bash
poetry run mypy .
```

## Challenges and Solutions

1. **Real-time AI Response Streaming**
   - Challenge: Implementing server-sent events (SSE) for streaming AI responses
   - Solution: Used FastAPI's StreamingResponse with async generators

2. **Database Schema Design**
   - Challenge: Designing a flexible schema for tickets and messages
   - Solution: Implemented a normalized schema with proper relationships

3. **Authentication and Authorization**
   - Challenge: Implementing secure JWT-based auth with role-based access
   - Solution: Used FastAPI's dependency injection system with custom dependencies

## Future Improvements

1. Add rate limiting for API endpoints
2. Implement caching for frequently accessed data
3. Add more comprehensive error handling
4. Implement WebSocket support for real-time updates
5. Add monitoring and logging
6. Implement unit and integration tests
7. Add CI/CD pipeline

## License

This project is licensed under the MIT License - see the LICENSE file for details. 