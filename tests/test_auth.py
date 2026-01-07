import pytest

from app.schemas.user import UserCreate
from app.services.user import create_user

from .base_api import BaseAPITest


@pytest.mark.asyncio
class TestAuth(BaseAPITest):
    async def _create_superuser(self):
        user_in = UserCreate(
            email="admin@example.com",
            password="secret123",
            first_name="Admin",
            last_name="User",
        )
        user = await create_user(user_in, is_superuser=True)
        return user

    async def test_login_returns_tokens(self):
        await self._create_superuser()

        response = await self.client.post(
            "/auth/login",
            data={"username": "admin@example.com", "password": "secret123"},
        )

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"

    async def test_me_requires_auth(self):
        response = await self.client.get("/auth/me")
        assert response.status_code == 401

    async def test_me_returns_current_user(self):
        await self._create_superuser()

        login_resp = await self.client.post(
            "/auth/login",
            data={"username": "admin@example.com", "password": "secret123"},
        )
        access_token = login_resp.json()["access_token"]

        me_resp = await self.client.get(
            "/auth/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert me_resp.status_code == 200
        data = me_resp.json()
        assert data["status_code"] == 200
        assert data["result"]["email"] == "admin@example.com"
        assert data["result"]["is_superuser"] is True
