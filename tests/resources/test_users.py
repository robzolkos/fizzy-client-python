"""Tests for the Users resource."""

import pytest
import respx
from httpx import Response

from fizzy import User


class TestUsersResource:
    """Tests for the sync Users resource."""

    @respx.mock
    def test_list_users(self, client, sample_user):
        """Test listing users."""
        respx.get("https://app.fizzy.do/123456/users").mock(
            return_value=Response(200, json=[sample_user])
        )

        users = client.users.list()

        assert len(users) == 1
        assert users[0].name == "Test User"
        assert isinstance(users[0], User)

    @respx.mock
    def test_get_user(self, client, sample_user):
        """Test getting a specific user."""
        respx.get("https://app.fizzy.do/123456/users/user123").mock(
            return_value=Response(200, json=sample_user)
        )

        user = client.users.get("user123")

        assert user.id == "user123"
        assert user.email_address == "test@example.com"
        assert user.role == "member"

    @respx.mock
    def test_update_user(self, client, sample_user):
        """Test updating a user."""
        updated = {**sample_user, "name": "Updated Name"}
        # PUT returns 204, then we GET the updated user
        respx.put("https://app.fizzy.do/123456/users/user123").mock(return_value=Response(204))
        respx.get("https://app.fizzy.do/123456/users/user123").mock(
            return_value=Response(200, json=updated)
        )

        user = client.users.update("user123", name="Updated Name")

        assert user.name == "Updated Name"

    @respx.mock
    def test_delete_user(self, client):
        """Test removing a user from account."""
        respx.delete("https://app.fizzy.do/123456/users/user123").mock(return_value=Response(204))

        client.users.delete("user123")


class TestAsyncUsersResource:
    """Tests for the async Users resource."""

    @pytest.mark.asyncio
    @respx.mock
    async def test_list_users(self, async_client, sample_user):
        """Test listing users asynchronously."""
        respx.get("https://app.fizzy.do/123456/users").mock(
            return_value=Response(200, json=[sample_user])
        )

        users = await async_client.users.list()

        assert len(users) == 1

    @pytest.mark.asyncio
    @respx.mock
    async def test_get_user(self, async_client, sample_user):
        """Test getting a user asynchronously."""
        respx.get("https://app.fizzy.do/123456/users/user123").mock(
            return_value=Response(200, json=sample_user)
        )

        user = await async_client.users.get("user123")

        assert user.id == "user123"
