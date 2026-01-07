## FastAPI Boilerplate with Tortoise ORM, JWT Auth, and Docker

**Features**
- Tortoise ORM with Postgres and async driver
- Abstract base model with `id`, `uid`, `created_at`, `updated_at`, `is_deleted`
- User model with basic profile and auth fields
- JWT-based auth with access and refresh tokens
- `/auth/login`, `/auth/refresh`, `/auth/me` endpoints
- Admin-only user creation and listing
- Dockerfile and docker-compose with Postgres

**Running locally with Docker**

```bash
docker-compose up --build
```

The API will be available at `http://localhost:8000` and docs at `http://localhost:8000/docs`.

**Environment variables**

Main vars (see `app/core/config.py`):
- `DATABASE_URL`
- `JWT_SECRET_KEY`
- `JWT_REFRESH_SECRET_KEY`
- `ACCESS_TOKEN_EXPIRE_MINUTES`
- `REFRESH_TOKEN_EXPIRE_DAYS`
