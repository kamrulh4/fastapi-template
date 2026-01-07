import pytest

from app.schemas.user import UserCreate
from app.services.user import create_user

from .base_api import BaseAPITest


@pytest.mark.asyncio
class TestUsers(BaseAPITest):
    async def _create_superuser_and_login(self) -> str:
        user_in = UserCreate(
            email="admin2@example.com",
            password="secret123",
            first_name="Admin2",
            last_name="User",
        )
        await create_user(user_in, is_superuser=True)

        resp = await self.client.post(
            "/auth/login",
            data={"username": "admin2@example.com", "password": "secret123"},
        )
        assert resp.status_code == 200
        return resp.json()["access_token"]

    async def test_create_and_list_users(self):
        access_token = await self._create_superuser_and_login()

        # Create regular user
        create_resp = await self.client.post(
            "/users/",
            json={
                "email": "user@example.com",
                "password": "secret123",
                "first_name": "Reg",
                "last_name": "User",
            },
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert create_resp.status_code == 201
        user_data = create_resp.json()
        assert user_data["status_code"] == 201
        assert user_data["result"]["email"] == "user@example.com"
        assert user_data["result"]["is_superuser"] is False

        # List users
        list_resp = await self.client.get(
            "/users/", headers={"Authorization": f"Bearer {access_token}"}
        )

        assert list_resp.status_code == 200
        users_payload = list_resp.json()
        assert users_payload["status_code"] == 200
        assert "results" in users_payload
        assert "pagination" in users_payload
        assert any(u["email"] == "user@example.com" for u in users_payload["results"])
        assert users_payload["pagination"]["page"] == 1
        assert users_payload["pagination"]["page_size"] >= 1
