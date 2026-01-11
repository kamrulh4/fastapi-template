#!/bin/sh
set -e

echo "🚀 Starting FastAPI application initialization..."

# Run database migrations
echo "📦 Running database migrations..."
aerich upgrade 2>/dev/null || echo "⚠️  No migrations to run (using generate_schemas=True)"

# Create initial superuser
echo "👤 Creating superuser..."
python scripts/create_superuser.py

# Start the application
echo "✅ Initialization complete! Starting server..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
