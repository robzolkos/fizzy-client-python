"""Main client classes for the Fizzy API."""

from __future__ import annotations

from typing import Any

from fizzy.resources.boards import AsyncBoardsResource, BoardsResource
from fizzy.resources.cards import AsyncCardsResource, CardsResource
from fizzy.resources.columns import AsyncColumnsResource, ColumnsResource
from fizzy.resources.comments import AsyncCommentsResource, CommentsResource
from fizzy.resources.identity import AsyncIdentityResource, IdentityResource
from fizzy.resources.notifications import AsyncNotificationsResource, NotificationsResource
from fizzy.resources.reactions import AsyncReactionsResource, ReactionsResource
from fizzy.resources.steps import AsyncStepsResource, StepsResource
from fizzy.resources.tags import AsyncTagsResource, TagsResource
from fizzy.resources.uploads import AsyncUploadsResource, UploadsResource
from fizzy.resources.users import AsyncUsersResource, UsersResource
from fizzy.utils.http import AsyncHTTPClient, HTTPClient


class FizzyClient:
    """Synchronous client for the Fizzy API.

    Example usage:
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
    """

    DEFAULT_BASE_URL = "https://app.fizzy.do"

    def __init__(
        self,
        token: str | None = None,
        session_token: str | None = None,
        account_slug: str | None = None,
        base_url: str = DEFAULT_BASE_URL,
        cache: bool = True,
        timeout: float = 30.0,
    ) -> None:
        """Initialize the Fizzy client.

        Args:
            token: Personal access token for authentication.
            session_token: Session token from magic link authentication.
            account_slug: The account slug to use for API requests.
            base_url: The base URL for the Fizzy API.
            cache: Whether to enable ETag caching.
            timeout: Request timeout in seconds.

        Raises:
            ValueError: If neither token nor session_token is provided.
        """
        self._http = HTTPClient(
            token=token,
            session_token=session_token,
            account_slug=account_slug,
            base_url=base_url,
            cache=cache,
            timeout=timeout,
        )

        # Initialize resources
        self._identity = IdentityResource(self._http)
        self._boards = BoardsResource(self._http)
        self._cards = CardsResource(self._http)
        self._comments = CommentsResource(self._http)
        self._reactions = ReactionsResource(self._http)
        self._steps = StepsResource(self._http)
        self._tags = TagsResource(self._http)
        self._columns = ColumnsResource(self._http)
        self._users = UsersResource(self._http)
        self._notifications = NotificationsResource(self._http)
        self._uploads = UploadsResource(self._http)

    @property
    def identity(self) -> IdentityResource:
        """Access the identity resource."""
        return self._identity

    @property
    def boards(self) -> BoardsResource:
        """Access the boards resource."""
        return self._boards

    @property
    def cards(self) -> CardsResource:
        """Access the cards resource."""
        return self._cards

    @property
    def comments(self) -> CommentsResource:
        """Access the comments resource."""
        return self._comments

    @property
    def reactions(self) -> ReactionsResource:
        """Access the reactions resource."""
        return self._reactions

    @property
    def steps(self) -> StepsResource:
        """Access the steps resource."""
        return self._steps

    @property
    def tags(self) -> TagsResource:
        """Access the tags resource."""
        return self._tags

    @property
    def columns(self) -> ColumnsResource:
        """Access the columns resource."""
        return self._columns

    @property
    def users(self) -> UsersResource:
        """Access the users resource."""
        return self._users

    @property
    def notifications(self) -> NotificationsResource:
        """Access the notifications resource."""
        return self._notifications

    @property
    def uploads(self) -> UploadsResource:
        """Access the uploads resource."""
        return self._uploads

    def close(self) -> None:
        """Close the HTTP client."""
        self._http.close()

    def __enter__(self) -> FizzyClient:
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()


class AsyncFizzyClient:
    """Asynchronous client for the Fizzy API.

    Example usage:
        async with AsyncFizzyClient(
            token="your-api-token",
            account_slug="your-account-slug"
        ) as client:
            # List boards
            boards = await client.boards.list()

            # Create a card
            card = await client.cards.create(
                board_id=123,
                title="My new card"
            )
    """

    DEFAULT_BASE_URL = "https://app.fizzy.do"

    def __init__(
        self,
        token: str | None = None,
        session_token: str | None = None,
        account_slug: str | None = None,
        base_url: str = DEFAULT_BASE_URL,
        cache: bool = True,
        timeout: float = 30.0,
    ) -> None:
        """Initialize the async Fizzy client.

        Args:
            token: Personal access token for authentication.
            session_token: Session token from magic link authentication.
            account_slug: The account slug to use for API requests.
            base_url: The base URL for the Fizzy API.
            cache: Whether to enable ETag caching.
            timeout: Request timeout in seconds.

        Raises:
            ValueError: If neither token nor session_token is provided.
        """
        self._http = AsyncHTTPClient(
            token=token,
            session_token=session_token,
            account_slug=account_slug,
            base_url=base_url,
            cache=cache,
            timeout=timeout,
        )

        # Initialize resources
        self._identity = AsyncIdentityResource(self._http)
        self._boards = AsyncBoardsResource(self._http)
        self._cards = AsyncCardsResource(self._http)
        self._comments = AsyncCommentsResource(self._http)
        self._reactions = AsyncReactionsResource(self._http)
        self._steps = AsyncStepsResource(self._http)
        self._tags = AsyncTagsResource(self._http)
        self._columns = AsyncColumnsResource(self._http)
        self._users = AsyncUsersResource(self._http)
        self._notifications = AsyncNotificationsResource(self._http)
        self._uploads = AsyncUploadsResource(self._http)

    @property
    def identity(self) -> AsyncIdentityResource:
        """Access the identity resource."""
        return self._identity

    @property
    def boards(self) -> AsyncBoardsResource:
        """Access the boards resource."""
        return self._boards

    @property
    def cards(self) -> AsyncCardsResource:
        """Access the cards resource."""
        return self._cards

    @property
    def comments(self) -> AsyncCommentsResource:
        """Access the comments resource."""
        return self._comments

    @property
    def reactions(self) -> AsyncReactionsResource:
        """Access the reactions resource."""
        return self._reactions

    @property
    def steps(self) -> AsyncStepsResource:
        """Access the steps resource."""
        return self._steps

    @property
    def tags(self) -> AsyncTagsResource:
        """Access the tags resource."""
        return self._tags

    @property
    def columns(self) -> AsyncColumnsResource:
        """Access the columns resource."""
        return self._columns

    @property
    def users(self) -> AsyncUsersResource:
        """Access the users resource."""
        return self._users

    @property
    def notifications(self) -> AsyncNotificationsResource:
        """Access the notifications resource."""
        return self._notifications

    @property
    def uploads(self) -> AsyncUploadsResource:
        """Access the uploads resource."""
        return self._uploads

    async def close(self) -> None:
        """Close the HTTP client."""
        await self._http.close()

    async def __aenter__(self) -> AsyncFizzyClient:
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.close()
