# Database Migrations Guide

This guide covers everything you need to know about managing database schema changes using Aerich with Tortoise ORM.

## Overview

**Aerich** is the migration tool for Tortoise ORM (similar to Alembic for SQLAlchemy). It helps you:
- Track database schema changes over time
- Apply changes safely without losing data
- Roll back changes if needed
- Keep your team's databases in sync

## Initial Setup

### First-Time Initialization

If you're starting fresh, initialize Aerich:

```bash
# 1. Initialize aerich (creates migrations directory structure)
aerich init -t app.core.db.TORTOISE_ORM

# 2. Create initial migration from current models
aerich init-db
```

This creates the `migrations/` directory with your baseline schema.

### Already Initialized?

If `migrations/` directory already exists (like in this template), you can skip the initialization and just run:

```bash
# Apply existing migrations to your database
aerich upgrade
```

## Common Workflows

### Creating a New Migration

When you add or modify models:

**1. Make your model changes**

Example - adding a field to an existing model:
```python
# app/models/user.py
class User(BaseModel):
    email: str = fields.CharField(max_length=255, unique=True, index=True)
    hashed_password: str = fields.CharField(max_length=255)
    phone: str = fields.CharField(max_length=20, null=True)  # NEW FIELD
    # ... rest of fields
```

**2. Generate the migration**

```bash
aerich migrate --name add_phone_to_user
```

This creates a new migration file in `migrations/models/`.

**3. Review the generated migration**

Check `migrations/models/` to see what SQL will be executed.

**4. Apply the migration**

```bash
aerich upgrade
```

### Creating a New Model

**1. Create the model file**

```python
# app/models/post.py
from tortoise import fields
from app.models.base import BaseModel

class Post(BaseModel):
    title: str = fields.CharField(max_length=255)
    content: str = fields.TextField()
    
    class Meta:
        table = "posts"
```

**2. Register in TORTOISE_ORM**

```python
# app/core/db.py
TORTOISE_ORM = {
    "connections": {"default": get_settings().DATABASE_URL},
    "apps": {
        "models": {
            "models": [
                "app.models.user",
                "app.models.post",  # ADD THIS
                "aerich.models",
            ],
            "default_connection": "default",
        },
    },
}
```

**3. Update init_tortoise function**

```python
# app/core/db.py
def init_tortoise(app):
    settings = get_settings()
    register_tortoise(
        app,
        db_url=settings.DATABASE_URL,
        modules={"models": ["app.models.user", "app.models.post", "aerich.models"]},  # ADD HERE
        generate_schemas=True,
        add_exception_handlers=True,
    )
```

**4. Generate and apply migration**

```bash
aerich migrate --name create_post_model
aerich upgrade
```

## Migration Commands Reference

### Core Commands

```bash
# Apply all pending migrations
aerich upgrade

# Rollback last migration
aerich downgrade

# Rollback to specific version (0 = rollback all)
aerich downgrade -v 3

# Show migration history
aerich history

# Show current database version
aerich heads

# Generate new migration
aerich migrate --name description_of_change
```

### Inspecting Migrations

```bash
# View generated SQL without applying
cat migrations/models/1_*.py

# Check migration status
aerich history
```

## Development vs Production

### Development Mode (Current Setup)

The template uses `generate_schemas=True` in [`db.py`](file:///Users/kamrul/Desktop/PythonWS/fastapi-template/app/core/db.py):

```python
register_tortoise(
    app,
    # ...
    generate_schemas=True,  # Auto-creates tables on startup
)
```

**Pros:**
- ✅ New tables are created automatically
- ✅ Fast prototyping

**Cons:**
- ❌ Changes to existing tables are NOT applied
- ❌ No migration history
- ❌ Data loss risk

### Production Mode (Recommended)

For production, set `generate_schemas=False` and use migrations:

```python
register_tortoise(
    app,
    # ...
    generate_schemas=False,  # Use migrations only
)
```

Then always use Aerich:

```bash
# Local development
aerich migrate --name my_changes
aerich upgrade

# In production (via Docker or CI/CD)
aerich upgrade
```

## Docker Integration

The template is configured to run migrations automatically on startup.

In [`docker-compose.yml`](file:///Users/kamrul/Desktop/PythonWS/fastapi-template/docker-compose.yml):

```yaml
command: >
  sh -c "aerich upgrade 2>/dev/null || echo 'No migrations to run' &&
         python scripts/create_superuser.py &&
         uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"
```

This ensures:
1. Migrations are applied before the app starts
2. Superuser is created (idempotent)
3. App starts normally

## Common Scenarios

### Scenario 1: Renaming a Field

```python
# BEFORE
class User(BaseModel):
    full_name: str = fields.CharField(max_length=200)

# AFTER
class User(BaseModel):
    name: str = fields.CharField(max_length=200)
```

```bash
aerich migrate --name rename_full_name_to_name
aerich upgrade
```

### Scenario 2: Adding a Foreign Key

```python
class Post(BaseModel):
    title: str = fields.CharField(max_length=255)
    author: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User", related_name="posts"
    )
```

```bash
aerich migrate --name add_author_to_post
aerich upgrade
```

### Scenario 3: Making a Field Required

```python
# BEFORE
phone: str | None = fields.CharField(max_length=20, null=True)

# AFTER - requires existing data to be updated first!
phone: str = fields.CharField(max_length=20)
```

**⚠️ Important:** Provide a default or update existing records before making a nullable field required.

## Troubleshooting

### "No changes detected"

If `aerich migrate` doesn't detect your changes:
- Ensure the model is registered in `TORTOISE_ORM`
- Check that you're in the correct directory
- Verify `pyproject.toml` has correct Aerich config

### Migration Conflicts

If you have conflicting migrations:
```bash
# Rollback to a safe point
aerich downgrade -v 3

# Delete problematic migration files
rm migrations/models/X_*.py

# Regenerate
aerich migrate --name fixed_migration
```

### Fresh Start (Development Only)

To reset and start over:
```bash
# ⚠️ WARNING: This deletes all data!
docker-compose down -v
docker-compose up --build
```

## Best Practices

1. **Always review migrations** before applying to production
2. **Use descriptive names**: `aerich migrate --name add_user_profile_fields`
3. **Test rollbacks**: Ensure `aerich downgrade` works
4. **Commit migrations** to version control
5. **Don't edit applied migrations** - create new ones instead
6. **Backup production data** before major schema changes

## Learn More

- [Tortoise ORM Documentation](https://tortoise.github.io/)
- [Aerich Documentation](https://github.com/tortoise/aerich)
