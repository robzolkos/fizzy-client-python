"""Tests for the Identity resource."""

import pytest
import respx
from httpx import Response

from fizzy import Identity


class TestIdentityResource:
    """Tests for the sync Identity resource."""

    @respx.mock
    def test_get_identity(self, client, sample_identity):
        """Test getting the authenticated user's identity."""
        respx.get("https://app.fizzy.do/my/identity").mock(
            return_value=Response(200, json=sample_identity)
        )

        identity = client.identity.get()

        assert len(identity.accounts) == 2
        assert identity.accounts[0].id == "acc123"
        assert identity.accounts[0].name == "Test Account"
        assert identity.accounts[0].user.name == "Test User"
        assert identity.accounts[1].id == "acc456"
        assert isinstance(identity, Identity)


class TestAsyncIdentityResource:
    """Tests for the async Identity resource."""

    @pytest.mark.asyncio
    @respx.mock
    async def test_get_identity(self, async_client, sample_identity):
        """Test getting identity asynchronously."""
        respx.get("https://app.fizzy.do/my/identity").mock(
            return_value=Response(200, json=sample_identity)
        )

        identity = await async_client.identity.get()

        assert len(identity.accounts) == 2
        assert identity.accounts[0].name == "Test Account"
