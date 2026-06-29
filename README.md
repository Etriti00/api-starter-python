# FastAPI Starter Template 🐍

Production-ready FastAPI backend with SQLAlchemy, Alembic, JWT auth, Docker Compose, and PostgreSQL.

## Quick Start

```bash
cp .env.example .env
docker compose up -d    # Start PostgreSQL + Redis
alembic upgrade head    # Run migrations
python -m app.seed      # Seed database
uvicorn app.main:app --reload  # Start dev server
```

## What's Included

### Authentication & Security 🔐
- JWT access + refresh tokens
- Password hashing with bcrypt
- Role-based access control (RBAC)
- Rate limiting middleware
- CORS configuration
- Input validation with Pydantic v2

### Database & Migrations 🗄️
- SQLAlchemy 2.0 with async sessions
- Alembic migrations
- PostgreSQL with connection pooling
- Redis for caching & rate limiting
- Database seed script

### API Structure 📁
- RESTful endpoints with versioning
- Dependency injection pattern
- Request/response schemas (Pydantic)
- Pagination helpers
- Error handling middleware
- OpenAPI/Swagger docs

### DevOps & Deployment 🐳
- Docker Compose (PostgreSQL, Redis, API)
- GitHub Actions CI/CD
- Pre-commit hooks
- Health check endpoints
- Structured logging

### Project Structure

```
app/
├── main.py              # FastAPI app + middleware
├── config.py            # Settings with Pydantic
├── database.py          # SQLAlchemy session
├── dependencies.py      # Shared dependencies
├── models.py            # SQLAlchemy models
├── schemas.py           # Pydantic schemas
├── auth/
│   ├── router.py        # Auth endpoints
│   ├── jwt.py           # JWT utilities
│   └── password.py      # Password hashing
├── users/
│   ├── router.py        # User CRUD
│   └── service.py       # Business logic
├── middleware/
│   ├── rate_limit.py    # Rate limiting
│   └── logging.py       # Request logging
└── seed.py              # Database seeder
alembic/
├── env.py
└── versions/
docker-compose.yml
Dockerfile
requirements.txt
```

## API Endpoints

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/api/v1/auth/register` | No | Register new user |
| POST | `/api/v1/auth/login` | No | Login, get tokens |
| POST | `/api/v1/auth/refresh` | Refresh | Refresh access token |
| GET | `/api/v1/users/me` | Bearer | Get current user |
| PATCH | `/api/v1/users/me` | Bearer | Update current user |
| GET | `/api/v1/users` | Admin | List all users |
| GET | `/api/v1/users/{id}` | Admin | Get user by ID |
| DELETE | `/api/v1/users/{id}` | Admin | Delete user |
| GET | `/api/v1/health` | No | Health check |
| GET | `/docs` | No | Swagger UI |

## License

MIT — use for any personal or commercial project.
