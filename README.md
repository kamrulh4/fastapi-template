# FastAPI Boilerplate with Tortoise ORM, JWT Auth, and Docker

A production-ready FastAPI template with async Tortoise ORM, PostgreSQL, JWT authentication, Docker support, and database migrations.

## 🚀 Features

- **FastAPI** - Modern, fast web framework for building APIs
- **Tortoise ORM** - Async ORM with PostgreSQL support
- **JWT Authentication** - Access & refresh tokens with OAuth2 password flow
- **Abstract Base Model** - Common fields (`id`, `uid`, `created_at`, `updated_at`, `is_deleted`)
- **Soft Delete Support** - Built-in soft deletion functionality
- **User Management** - Complete user model with role-based access
- **Database Migrations** - Aerich integration for schema management
- **Docker Ready** - Multi-stage Dockerfile with docker-compose
- **Auto Superuser** - Automatic admin creation on first run
- **Production Ready** - Environment configs, health checks, and restart policies
- **Test Suite** - Pytest with async support

## 📋 Quick Start

### 1. Clone and Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd fastapi-template

# Copy environment template
cp .env.example .env

# Edit .env with your settings (especially JWT secrets!)
nano .env
```

### 2. Run with Docker (Recommended)

```bash
# Build and start services
docker-compose up --build

# The API will be available at:
# - API: http://localhost:8000
# - Docs: http://localhost:8000/docs
# - ReDoc: http://localhost:8000/redoc
```

On first run, the application will:
1. ✅ Run database migrations
2. ✅ Create superuser from environment variables
3. ✅ Start the FastAPI server

### 3. Login with Default Superuser

Default credentials (configured in `.env`):
- **Email**: `admin@example.com`
- **Password**: `changeme123`

**⚠️ IMPORTANT**: Change these credentials in production!

## 🔧 Development Setup

### Local Development (without Docker)

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your local database URL

# Initialize database migrations (first time only)
aerich init -t app.core.db.TORTOISE_ORM
aerich init-db

# Run migrations
aerich upgrade

# Create superuser
python scripts/create_superuser.py

# Start development server
uvicorn app.main:app --reload
```

Visit `http://localhost:8000/docs` for interactive API documentation.

## 📚 API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/login` | Login with email/password, returns access & refresh tokens |
| POST | `/auth/refresh` | Refresh access token using refresh token |
| GET | `/auth/me` | Get current authenticated user details |

### Users (Admin Only)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/users/` | List all users (paginated) |
| POST | `/users/` | Create a new user |
| GET | `/users/{uid}` | Get user by UID |

## 🗄️ Database Migrations

This template uses **Aerich** for database migrations. See [MIGRATIONS.md](file:///Users/kamrul/Desktop/PythonWS/fastapi-template/MIGRATIONS.md) for detailed guide.

### Quick Reference

```bash
# Create a migration after model changes
aerich migrate --name describe_your_changes

# Apply migrations
aerich upgrade

# Rollback last migration
aerich downgrade

# View migration history
aerich history
```

### When to Use Migrations vs generate_schemas

**Current Setup (Development):**
- `generate_schemas=True` is enabled
- ✅ New tables created automatically
- ❌ Changes to existing tables NOT applied

**Production:**
- Set `generate_schemas=False`
- Always use `aerich migrate` and `aerich upgrade`
- Safer and trackable schema changes

## 🔐 Security

### Environment Variables

**CRITICAL**: Set strong secrets in production!

```bash
# Generate secure random secrets
openssl rand -hex 32  # For JWT_SECRET_KEY
openssl rand -hex 32  # For JWT_REFRESH_SECRET_KEY
```

Update your `.env`:
```env
JWT_SECRET_KEY=your-generated-secret-here
JWT_REFRESH_SECRET_KEY=your-other-generated-secret-here
```

### Production Checklist

- [ ] Change JWT secret keys
- [ ] Update superuser credentials
- [ ] Set `ENVIRONMENT=production`
- [ ] Configure CORS origins properly
- [ ] Use strong database password
- [ ] Enable HTTPS
- [ ] Set `generate_schemas=False` and use migrations

## 🐳 Docker Configuration

### Services

**PostgreSQL Database:**
- Image: `postgres:18`
- Port: `5432`
- Volume: Persistent storage for data
- Health checks enabled

**FastAPI Web Application:**
- Multi-stage build for optimization
- Runs as non-root user
- Auto-runs migrations on startup
- Auto-creates superuser
- Restart policy: `unless-stopped`

### Docker Commands

```bash
# Start services
docker-compose up

# Start in background
docker-compose up -d

# View logs
docker-compose logs -f web

# Rebuild after code changes
docker-compose up --build

# Stop services
docker-compose down

# Stop and remove volumes (⚠️ deletes data!)
docker-compose down -v

# Access shell in web container
docker-compose exec web bash

# Run migrations manually
docker-compose exec web aerich upgrade
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_auth.py

# Run with coverage
pytest --cov=app
```

The test suite uses:
- `pytest-asyncio` for async test support
- `httpx` for async HTTP client
- `aiosqlite` for in-memory test database

## 📁 Project Structure

```
fastapi-template/
├── app/
│   ├── core/               # Core configurations
│   │   ├── config.py       # Settings and environment variables
│   │   ├── db.py          # Database configuration
│   │   └── security.py    # JWT and password utilities
│   ├── crud/              # Database CRUD operations
│   ├── dependencies/      # FastAPI dependencies (auth, pagination)
│   ├── models/            # Tortoise ORM models
│   │   ├── base.py       # Abstract base model
│   │   └── user.py       # User model
│   ├── routers/          # API route handlers
│   │   ├── auth.py      # Authentication endpoints
│   │   └── users.py     # User management endpoints
│   ├── schemas/         # Pydantic schemas (request/response)
│   ├── services/        # Business logic layer
│   └── main.py          # FastAPI application entry point
├── migrations/          # Aerich database migrations
├── scripts/            # Utility scripts
│   ├── create_superuser.py  # Superuser creation
│   └── init.sh             # Docker initialization
├── tests/              # Test suite
├── .env.example       # Environment variables template
├── docker-compose.yml # Docker services configuration
├── Dockerfile         # Multi-stage Docker build
├── pyproject.toml    # Aerich configuration
├── requirements.txt  # Python dependencies
├── MIGRATIONS.md    # Database migrations guide
└── README.md       # This file
```

## 🔄 Common Workflows

### Adding a New Model

1. **Create the model file** (e.g., `app/models/post.py`)
2. **Register in [`db.py`](file:///Users/kamrul/Desktop/PythonWS/fastapi-template/app/core/db.py)** - Add to `TORTOISE_ORM` and `init_tortoise()`
3. **Generate migration**: `aerich migrate --name create_post_model`
4. **Apply migration**: `aerich upgrade`
5. **Create CRUD operations** in `app/crud/`
6. **Add schemas** in `app/schemas/`
7. **Create router** in `app/routers/`

See [MIGRATIONS.md](file:///Users/kamrul/Desktop/PythonWS/fastapi-template/MIGRATIONS.md) for detailed examples.

### Updating an Existing Model

1. **Modify the model** (e.g., add/remove/change fields)
2. **Generate migration**: `aerich migrate --name add_phone_to_user`
3. **Review migration** in `migrations/models/`
4. **Apply migration**: `aerich upgrade`

## 🌐 Environment Variables

See [`.env.example`](file:///Users/kamrul/Desktop/PythonWS/fastapi-template/.env.example) for all available configuration options.

### Key Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `ENVIRONMENT` | Environment mode | `development` |
| `DATABASE_URL` | PostgreSQL connection string | `postgres://...` |
| `JWT_SECRET_KEY` | Secret for access tokens | **CHANGE IN PRODUCTION** |
| `JWT_REFRESH_SECRET_KEY` | Secret for refresh tokens | **CHANGE IN PRODUCTION** |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Access token expiry | `30` |
| `REFRESH_TOKEN_EXPIRE_DAYS` | Refresh token expiry | `7` |
| `FIRST_SUPERUSER_EMAIL` | Initial admin email | `admin@example.com` |
| `FIRST_SUPERUSER_PASSWORD` | Initial admin password | **CHANGE IN PRODUCTION** |

## 🐛 Troubleshooting

### Database Connection Errors

```bash
# Check if PostgreSQL is running
docker-compose ps

# Check logs
docker-compose logs db

# Restart database
docker-compose restart db
```

### Migration Issues

```bash
# Check migration status
aerich history

# Reset migrations (⚠️ development only!)
docker-compose down -v
docker-compose up --build
```

### Port Already in Use

```bash
# Change port in docker-compose.yml
ports:
  - "8001:8000"  # Use 8001 instead
```

## 📖 Learn More

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Tortoise ORM Documentation](https://tortoise.github.io/)
- [Aerich Migrations](https://github.com/tortoise/aerich)
- [Pydantic Settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)

## 📝 License

This template is MIT licensed. Feel free to use it for your projects!

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

**Built with ❤️ using FastAPI, Tortoise ORM, and Docker**
