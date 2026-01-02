"""Authentication helpers for the Fizzy API."""

from __future__ import annotations

from typing import Any, cast

import httpx

from fizzy.exceptions import AuthenticationError, ValidationError

DEFAULT_BASE_URL = "https://app.fizzy.do"


def request_magic_link(
    email: str,
    base_url: str = DEFAULT_BASE_URL,
) -> dict[str, Any]:
    """Request a magic link to be sent to the user's email.

    Args:
        email: The user's email address.
        base_url: The base URL for the Fizzy API.

    Returns:
        A dict with status information.

    Raises:
        ValidationError: If the email is invalid.
    """
    response = httpx.post(
        f"{base_url}/session",
        json={"email": email},
        headers={"Content-Type": "application/json"},
    )

    if response.status_code == 422:
        body = response.json()
        raise ValidationError(
            message="Invalid email",
            errors=body.get("errors", {}),
            response_body=body,
        )

    response.raise_for_status()
    return cast(dict[str, Any], response.json())


def submit_magic_code(
    code: str,
    base_url: str = DEFAULT_BASE_URL,
) -> str:
    """Submit the 6-character magic link code to authenticate.

    Args:
        code: The 6-character code from the magic link email.
        base_url: The base URL for the Fizzy API.

    Returns:
        The session token for authenticated requests.

    Raises:
        AuthenticationError: If the code is invalid or expired.
    """
    response = httpx.post(
        f"{base_url}/session/magic_link",
        json={"code": code},
        headers={"Content-Type": "application/json"},
    )

    if response.status_code == 401:
        body = response.json()
        raise AuthenticationError(
            message=body.get("error", "Invalid or expired code"),
            response_body=body,
        )

    response.raise_for_status()
    data = response.json()
    return cast(str, data["token"])


async def async_request_magic_link(
    email: str,
    base_url: str = DEFAULT_BASE_URL,
) -> dict[str, Any]:
    """Async version of request_magic_link.

    Args:
        email: The user's email address.
        base_url: The base URL for the Fizzy API.

    Returns:
        A dict with status information.

    Raises:
        ValidationError: If the email is invalid.
    """
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{base_url}/session",
            json={"email": email},
            headers={"Content-Type": "application/json"},
        )

        if response.status_code == 422:
            body = response.json()
            raise ValidationError(
                message="Invalid email",
                errors=body.get("errors", {}),
                response_body=body,
            )

        response.raise_for_status()
        return cast(dict[str, Any], response.json())


async def async_submit_magic_code(
    code: str,
    base_url: str = DEFAULT_BASE_URL,
) -> str:
    """Async version of submit_magic_code.

    Args:
        code: The 6-character code from the magic link email.
        base_url: The base URL for the Fizzy API.

    Returns:
        The session token for authenticated requests.

    Raises:
        AuthenticationError: If the code is invalid or expired.
    """
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{base_url}/session/magic_link",
            json={"code": code},
            headers={"Content-Type": "application/json"},
        )

        if response.status_code == 401:
            body = response.json()
            raise AuthenticationError(
                message=body.get("error", "Invalid or expired code"),
                response_body=body,
            )

        response.raise_for_status()
        data = response.json()
        return cast(str, data["token"])
