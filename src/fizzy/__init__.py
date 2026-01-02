"""Fizzy API Client for Python.

A Python client library for the Fizzy API.

Example usage:
    from fizzy import FizzyClient

    client = FizzyClient(
        token="your-api-token",
        account_slug="your-account-slug"
    )

    # List boards
    boards = client.boards.list()

    # Create a card
    card = client.cards.create(
        board_id=123,
        title="My new card"
    )

For async usage:
    from fizzy import AsyncFizzyClient
    import asyncio

    async def main():
        async with AsyncFizzyClient(
            token="your-api-token",
            account_slug="your-account-slug"
        ) as client:
            boards = await client.boards.list()

    asyncio.run(main())
"""

from fizzy.auth import (
    async_request_magic_link,
    async_submit_magic_code,
    request_magic_link,
    submit_magic_code,
)
from fizzy.client import AsyncFizzyClient, FizzyClient
from fizzy.exceptions import (
    AuthenticationError,
    BadRequestError,
    FizzyError,
    ForbiddenError,
    NotFoundError,
    RateLimitError,
    ServerError,
    ValidationError,
)
from fizzy.models import (
    Account,
    Board,
    Card,
    Column,
    Comment,
    DirectUpload,
    Identity,
    Notification,
    Reaction,
    Step,
    Tag,
    User,
)

__version__ = "1.0.0"

__all__ = [
    # Clients
    "AsyncFizzyClient",
    "FizzyClient",
    # Auth
    "async_request_magic_link",
    "async_submit_magic_code",
    "request_magic_link",
    "submit_magic_code",
    # Exceptions
    "AuthenticationError",
    "BadRequestError",
    "FizzyError",
    "ForbiddenError",
    "NotFoundError",
    "RateLimitError",
    "ServerError",
    "ValidationError",
    # Models
    "Account",
    "Board",
    "Card",
    "Column",
    "Comment",
    "DirectUpload",
    "Identity",
    "Notification",
    "Reaction",
    "Step",
    "Tag",
    "User",
]
