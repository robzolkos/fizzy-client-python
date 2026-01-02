"""Comments resource for the Fizzy API."""

from __future__ import annotations

from typing import TYPE_CHECKING

from fizzy.models.comment import Comment
from fizzy.resources.base import AsyncBaseResource, BaseResource
from fizzy.utils.pagination import (
    AsyncPaginatedResponse,
    AsyncPaginationIterator,
    PaginatedResponse,
    PaginationIterator,
)

if TYPE_CHECKING:
    from fizzy.utils.http import AsyncHTTPClient, HTTPClient


class CommentsResource(BaseResource[Comment]):
    """Resource for managing comments on cards."""

    def __init__(self, http_client: HTTPClient) -> None:
        super().__init__(http_client)

    def list(self, card_number: int) -> list[Comment]:
        """List all comments on a card.

        Args:
            card_number: The card number.

        Returns:
            A list of comments.
        """
        data, _ = self._http.get(f"/cards/{card_number}/comments")
        return self._parse_list(data, Comment)

    def list_paginated(self, card_number: int) -> PaginatedResponse[Comment]:
        """List comments with pagination support.

        Args:
            card_number: The card number.

        Returns:
            A paginated response containing comments.
        """
        data, response = self._http.get(f"/cards/{card_number}/comments")
        return PaginatedResponse(
            items=self._parse_list(data, Comment),
            response=response,
            http_client=self._http,
            path=f"/cards/{card_number}/comments",
        )

    def list_all(self, card_number: int) -> PaginationIterator[Comment]:
        """Iterate over all comments, automatically handling pagination.

        Args:
            card_number: The card number.

        Returns:
            An iterator that yields all comments across all pages.
        """
        return PaginationIterator(
            http_client=self._http,
            path=f"/cards/{card_number}/comments",
        )

    def get(self, card_number: int, comment_id: str | int) -> Comment:
        """Get a specific comment.

        Args:
            card_number: The card number.
            comment_id: The comment ID.

        Returns:
            The requested comment.
        """
        data, _ = self._http.get(f"/cards/{card_number}/comments/{comment_id}")
        return self._parse_model(data, Comment)

    def create(self, card_number: int, body: str) -> Comment:
        """Create a new comment on a card.

        Args:
            card_number: The card number.
            body: The HTML body/content of the comment.

        Returns:
            The created comment.
        """
        data = self._http.post(
            f"/cards/{card_number}/comments",
            data={"comment": {"body": body}},
        )
        return self._parse_model(data, Comment)

    def update(self, card_number: int, comment_id: str | int, body: str) -> Comment:
        """Update a comment.

        Args:
            card_number: The card number.
            comment_id: The comment ID.
            body: The new HTML body/content of the comment.

        Returns:
            The updated comment.
        """
        self._http.put(
            f"/cards/{card_number}/comments/{comment_id}",
            data={"comment": {"body": body}},
        )
        # API returns 204 No Content, so fetch the updated comment
        return self.get(card_number, comment_id)

    def delete(self, card_number: int, comment_id: str | int) -> None:
        """Delete a comment.

        Args:
            card_number: The card number.
            comment_id: The comment ID.
        """
        self._http.delete(f"/cards/{card_number}/comments/{comment_id}")


class AsyncCommentsResource(AsyncBaseResource[Comment]):
    """Async resource for managing comments on cards."""

    def __init__(self, http_client: AsyncHTTPClient) -> None:
        super().__init__(http_client)

    async def list(self, card_number: int) -> list[Comment]:
        """List all comments on a card.

        Args:
            card_number: The card number.

        Returns:
            A list of comments.
        """
        data, _ = await self._http.get(f"/cards/{card_number}/comments")
        return self._parse_list(data, Comment)

    async def list_paginated(self, card_number: int) -> AsyncPaginatedResponse[Comment]:
        """List comments with pagination support.

        Args:
            card_number: The card number.

        Returns:
            A paginated response containing comments.
        """
        data, response = await self._http.get(f"/cards/{card_number}/comments")
        return AsyncPaginatedResponse(
            items=self._parse_list(data, Comment),
            response=response,
            http_client=self._http,
            path=f"/cards/{card_number}/comments",
        )

    def list_all(self, card_number: int) -> AsyncPaginationIterator[Comment]:
        """Iterate over all comments, automatically handling pagination.

        Args:
            card_number: The card number.

        Returns:
            An async iterator that yields all comments across all pages.
        """
        return AsyncPaginationIterator(
            http_client=self._http,
            path=f"/cards/{card_number}/comments",
        )

    async def get(self, card_number: int, comment_id: str | int) -> Comment:
        """Get a specific comment.

        Args:
            card_number: The card number.
            comment_id: The comment ID.

        Returns:
            The requested comment.
        """
        data, _ = await self._http.get(f"/cards/{card_number}/comments/{comment_id}")
        return self._parse_model(data, Comment)

    async def create(self, card_number: int, body: str) -> Comment:
        """Create a new comment on a card.

        Args:
            card_number: The card number.
            body: The HTML body/content of the comment.

        Returns:
            The created comment.
        """
        data = await self._http.post(
            f"/cards/{card_number}/comments",
            data={"comment": {"body": body}},
        )
        return self._parse_model(data, Comment)

    async def update(self, card_number: int, comment_id: str | int, body: str) -> Comment:
        """Update a comment.

        Args:
            card_number: The card number.
            comment_id: The comment ID.
            body: The new HTML body/content of the comment.

        Returns:
            The updated comment.
        """
        await self._http.put(
            f"/cards/{card_number}/comments/{comment_id}",
            data={"comment": {"body": body}},
        )
        # API returns 204 No Content, so fetch the updated comment
        return await self.get(card_number, comment_id)

    async def delete(self, card_number: int, comment_id: str | int) -> None:
        """Delete a comment.

        Args:
            card_number: The card number.
            comment_id: The comment ID.
        """
        await self._http.delete(f"/cards/{card_number}/comments/{comment_id}")
