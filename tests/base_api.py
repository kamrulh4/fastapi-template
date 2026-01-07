import os
from typing import AsyncGenerator

import pytest
from httpx import AsyncClient, ASGITransport
from asgi_lifespan import LifespanManager

# Ensure tests use an in-memory SQLite database by default
os.environ.setdefault("DATABASE_URL", "sqlite://:memory:")

from app.main import app  # noqa: E402


class BaseAPITest:
    """Base API test class providing an async HTTP client.

    Other test classes can inherit from this to reuse the `client` fixture.
    """

    @pytest.fixture(autouse=True)
    async def _client_fixture(self) -> AsyncGenerator[AsyncClient, None]:
        async with LifespanManager(app):
            async with AsyncClient(
                transport=ASGITransport(app=app), base_url="http://test"
            ) as client:
                self.client = client
                yield client
