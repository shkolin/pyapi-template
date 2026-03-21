# Python API Template

A production-ready Python API template built with modern tools and best practices.

## Tech Stack

- **Framework**: FastAPI
- **Database**: SQLAlchemy with PostgreSQL
- **DI**: dependency-injector
- **Auth**: JWT
- **Migrations**: Alembic
- **Testing**: pytest
- **Code Quality**: ruff, mypy, black

## Architecture

```
app/
├── command/         # Command pattern implementation
├── domain/          # Domain models and business logic
├── endpoint/        # FastAPI routes and handlers
├── event/           # Event-driven architecture
├── handler/         # Command handlers
├── mapping/         # SQLAlchemy table mappings
├── repository/      # Data access layer
├── service/         # Business services
└── uow.py          # Unit of Work pattern
```

## Features

- Dependency injection container
- Unit of Work pattern for transaction management
- Event-driven architecture with domain events
- JWT authentication
- SMTP email sending
- Clean architecture with separation of concerns

## Getting Started

```bash
# Install dependencies
pip install -r requirements/dev.txt

# Copy config
cp config-dist.yml config.yml

# Run migrations
alembic upgrade head

# Start server
uvicorn app.main:app --reload
```

## Testing

```bash
pytest tests/
```
