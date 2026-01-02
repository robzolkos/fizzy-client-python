"""Tests for authentication helpers."""

import pytest
import respx
from httpx import Response

from fizzy import ValidationError
from fizzy.auth import (
    async_request_magic_link,
    async_submit_magic_code,
    request_magic_link,
    submit_magic_code,
)
from fizzy.exceptions import AuthenticationError


class TestMagicLinkAuth:
    """Tests for magic link authentication."""

    @respx.mock
    def test_request_magic_link_success(self):
        """Test successful magic link request."""
        respx.post("https://app.fizzy.do/session").mock(
            return_value=Response(200, json={"status": "ok", "message": "Magic link sent"})
        )

        result = request_magic_link("test@example.com")

        assert result["status"] == "ok"

    @respx.mock
    def test_request_magic_link_invalid_email(self):
        """Test magic link request with invalid email."""
        respx.post("https://app.fizzy.do/session").mock(
            return_value=Response(
                422, json={"error": "Invalid email", "errors": {"email": ["is invalid"]}}
            )
        )

        with pytest.raises(ValidationError) as exc_info:
            request_magic_link("invalid-email")

        assert exc_info.value.status_code == 422

    @respx.mock
    def test_submit_magic_code_success(self):
        """Test successful magic code submission."""
        respx.post("https://app.fizzy.do/session/magic_link").mock(
            return_value=Response(200, json={"token": "session-token-123"})
        )

        token = submit_magic_code("ABC123")

        assert token == "session-token-123"

    @respx.mock
    def test_submit_magic_code_invalid(self):
        """Test magic code submission with invalid code."""
        respx.post("https://app.fizzy.do/session/magic_link").mock(
            return_value=Response(401, json={"error": "Invalid or expired code"})
        )

        with pytest.raises(AuthenticationError) as exc_info:
            submit_magic_code("INVALID")

        assert exc_info.value.status_code == 401


class TestAsyncMagicLinkAuth:
    """Tests for async magic link authentication."""

    @pytest.mark.asyncio
    @respx.mock
    async def test_async_request_magic_link_success(self):
        """Test successful async magic link request."""
        respx.post("https://app.fizzy.do/session").mock(
            return_value=Response(200, json={"status": "ok", "message": "Magic link sent"})
        )

        result = await async_request_magic_link("test@example.com")

        assert result["status"] == "ok"

    @pytest.mark.asyncio
    @respx.mock
    async def test_async_submit_magic_code_success(self):
        """Test successful async magic code submission."""
        respx.post("https://app.fizzy.do/session/magic_link").mock(
            return_value=Response(200, json={"token": "session-token-123"})
        )

        token = await async_submit_magic_code("ABC123")

        assert token == "session-token-123"
