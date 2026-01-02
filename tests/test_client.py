"""Tests for the FizzyClient class."""

import pytest

from fizzy import AsyncFizzyClient, FizzyClient


class TestFizzyClient:
    """Tests for the sync FizzyClient."""

    def test_client_requires_token_or_session_token(self):
        """Test that client requires authentication."""
        with pytest.raises(ValueError, match="Either token or session_token must be provided"):
            FizzyClient(account_slug="123456")

    def test_client_with_token(self):
        """Test client initialization with token."""
        client = FizzyClient(token="test-token", account_slug="123456")
        assert client._http is not None
        client.close()

    def test_client_with_session_token(self):
        """Test client initialization with session token."""
        client = FizzyClient(session_token="test-session", account_slug="123456")
        assert client._http is not None
        client.close()

    def test_client_resources_available(self):
        """Test that all resources are available."""
        client = FizzyClient(token="test-token", account_slug="123456")

        assert client.identity is not None
        assert client.boards is not None
        assert client.cards is not None
        assert client.comments is not None
        assert client.reactions is not None
        assert client.steps is not None
        assert client.tags is not None
        assert client.columns is not None
        assert client.users is not None
        assert client.notifications is not None
        assert client.uploads is not None

        client.close()

    def test_client_context_manager(self):
        """Test client as context manager."""
        with FizzyClient(token="test-token", account_slug="123456") as client:
            assert client._http is not None


class TestAsyncFizzyClient:
    """Tests for the async FizzyClient."""

    def test_async_client_requires_token_or_session_token(self):
        """Test that async client requires authentication."""
        with pytest.raises(ValueError, match="Either token or session_token must be provided"):
            AsyncFizzyClient(account_slug="123456")

    def test_async_client_with_token(self):
        """Test async client initialization with token."""
        client = AsyncFizzyClient(token="test-token", account_slug="123456")
        assert client._http is not None

    def test_async_client_resources_available(self):
        """Test that all resources are available on async client."""
        client = AsyncFizzyClient(token="test-token", account_slug="123456")

        assert client.identity is not None
        assert client.boards is not None
        assert client.cards is not None
        assert client.comments is not None
        assert client.reactions is not None
        assert client.steps is not None
        assert client.tags is not None
        assert client.columns is not None
        assert client.users is not None
        assert client.notifications is not None
        assert client.uploads is not None

    @pytest.mark.asyncio
    async def test_async_client_context_manager(self):
        """Test async client as context manager."""
        async with AsyncFizzyClient(token="test-token", account_slug="123456") as client:
            assert client._http is not None
