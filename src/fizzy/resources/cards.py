"""Cards resource for the Fizzy API."""

from __future__ import annotations

import builtins
from pathlib import Path
from typing import TYPE_CHECKING, Any, BinaryIO

from fizzy.models.card import Card
from fizzy.resources.base import AsyncBaseResource, BaseResource
from fizzy.utils.pagination import (
    AsyncPaginatedResponse,
    AsyncPaginationIterator,
    PaginatedResponse,
    PaginationIterator,
)

if TYPE_CHECKING:
    from fizzy.utils.http import AsyncHTTPClient, HTTPClient

# Type alias for file uploads
FileInput = Path | str | tuple[str, BinaryIO, str]


class CardsResource(BaseResource[Card]):
    """Resource for managing cards."""

    def __init__(self, http_client: HTTPClient) -> None:
        super().__init__(http_client)

    def list(
        self,
        board_id: str | int | None = None,
        column_id: str | int | None = None,
        tag_ids: builtins.list[str] | None = None,
        assignee_ids: builtins.list[str] | None = None,
        status: str | None = None,
    ) -> list[Card]:
        """List cards with optional filters.

        Args:
            board_id: Filter by board ID.
            column_id: Filter by column ID.
            tag_ids: Filter by tag IDs.
            assignee_ids: Filter by assignee IDs.
            status: Filter by status (open, closed, deferred).

        Returns:
            A list of cards.
        """
        params: dict[str, Any] = {}
        if board_id is not None:
            params["board_id"] = board_id
        if column_id is not None:
            params["column_id"] = column_id
        if tag_ids is not None:
            params["tag_ids"] = tag_ids
        if assignee_ids is not None:
            params["assignee_ids"] = assignee_ids
        if status is not None:
            params["status"] = status

        data, _ = self._http.get("/cards", params=params)
        return self._parse_list(data, Card)

    def list_paginated(
        self,
        board_id: str | int | None = None,
        column_id: str | int | None = None,
        tag_ids: builtins.list[str] | None = None,
        assignee_ids: builtins.list[str] | None = None,
        status: str | None = None,
    ) -> PaginatedResponse[Card]:
        """List cards with pagination support.

        Args:
            board_id: Filter by board ID.
            column_id: Filter by column ID.
            tag_ids: Filter by tag IDs.
            assignee_ids: Filter by assignee IDs.
            status: Filter by status (open, closed, deferred).

        Returns:
            A paginated response containing cards.
        """
        params: dict[str, Any] = {}
        if board_id is not None:
            params["board_id"] = board_id
        if column_id is not None:
            params["column_id"] = column_id
        if tag_ids is not None:
            params["tag_ids"] = tag_ids
        if assignee_ids is not None:
            params["assignee_ids"] = assignee_ids
        if status is not None:
            params["status"] = status

        data, response = self._http.get("/cards", params=params)
        return PaginatedResponse(
            items=self._parse_list(data, Card),
            response=response,
            http_client=self._http,
            path="/cards",
            params=params,
        )

    def list_all(
        self,
        board_id: str | int | None = None,
        column_id: str | int | None = None,
        tag_ids: builtins.list[str] | None = None,
        assignee_ids: builtins.list[str] | None = None,
        status: str | None = None,
    ) -> PaginationIterator[Card]:
        """Iterate over all cards, automatically handling pagination.

        Args:
            board_id: Filter by board ID.
            column_id: Filter by column ID.
            tag_ids: Filter by tag IDs.
            assignee_ids: Filter by assignee IDs.
            status: Filter by status (open, closed, deferred).

        Returns:
            An iterator that yields all cards across all pages.
        """
        params: dict[str, Any] = {}
        if board_id is not None:
            params["board_id"] = board_id
        if column_id is not None:
            params["column_id"] = column_id
        if tag_ids is not None:
            params["tag_ids"] = tag_ids
        if assignee_ids is not None:
            params["assignee_ids"] = assignee_ids
        if status is not None:
            params["status"] = status

        return PaginationIterator(
            http_client=self._http,
            path="/cards",
            params=params,
        )

    def get(self, card_number: int) -> Card:
        """Get a specific card by its number.

        Args:
            card_number: The card number (not ID).

        Returns:
            The requested card.
        """
        data, _ = self._http.get(f"/cards/{card_number}")
        return self._parse_model(data, Card)

    def create(
        self,
        board_id: str | int,
        title: str,
        description: str | None = None,
        column_id: str | int | None = None,
        tag_ids: builtins.list[str] | None = None,
        assignee_ids: builtins.list[str] | None = None,
        image: FileInput | None = None,
    ) -> Card:
        """Create a new card.

        Args:
            board_id: The ID of the board to create the card in.
            title: The title of the card.
            description: Optional HTML description of the card.
            column_id: Optional column ID to place the card in.
            tag_ids: Optional list of tag IDs to apply.
            assignee_ids: Optional list of user IDs to assign.
            image: Optional header image. Can be a file path (str or Path),
                   or a tuple of (filename, file_obj, content_type).

        Returns:
            The created card.
        """
        payload: dict[str, Any] = {
            "title": title,
        }
        if description is not None:
            payload["description"] = description
        if column_id is not None:
            payload["column_id"] = column_id
        if tag_ids is not None:
            payload["tag_ids"] = tag_ids
        if assignee_ids is not None:
            payload["assignee_ids"] = assignee_ids

        if image is not None:
            # Use multipart upload when image is provided
            files = {"card[image]": image}
            data = self._http.post_multipart(
                f"/boards/{board_id}/cards",
                data={"card": payload},
                files=files,
            )
        else:
            data = self._http.post(f"/boards/{board_id}/cards", data={"card": payload})
        return self._parse_model(data, Card)

    def update(
        self,
        card_number: int,
        title: str | None = None,
        description: str | None = None,
        column_id: str | int | None = None,
        board_id: str | int | None = None,
        image: FileInput | None = None,
    ) -> Card:
        """Update a card.

        Args:
            card_number: The card number.
            title: Optional new title.
            description: Optional new HTML description.
            column_id: Optional new column ID.
            board_id: Optional new board ID.
            image: Optional header image. Can be a file path (str or Path),
                   or a tuple of (filename, file_obj, content_type).

        Returns:
            The updated card.
        """
        payload: dict[str, Any] = {}
        if title is not None:
            payload["title"] = title
        if description is not None:
            payload["description"] = description
        if column_id is not None:
            payload["column_id"] = column_id
        if board_id is not None:
            payload["board_id"] = board_id

        if image is not None:
            # Use multipart upload when image is provided
            files = {"card[image]": image}
            data = self._http.put_multipart(
                f"/cards/{card_number}",
                data={"card": payload},
                files=files,
            )
        else:
            data = self._http.put(f"/cards/{card_number}", data={"card": payload})
        return self._parse_model(data, Card)

    def delete_image(self, card_number: int) -> None:
        """Delete the header image from a card.

        Args:
            card_number: The card number.
        """
        self._http.delete(f"/cards/{card_number}/image")

    def delete(self, card_number: int) -> None:
        """Delete a card.

        Args:
            card_number: The card number.
        """
        self._http.delete(f"/cards/{card_number}")

    def close(self, card_number: int) -> Card | None:
        """Close a card.

        Args:
            card_number: The card number.

        Returns:
            The closed card or None.
        """
        data = self._http.post(f"/cards/{card_number}/closure")
        return self._parse_model(data, Card) if data else None

    def reopen(self, card_number: int) -> Card | None:
        """Reopen a closed card.

        Args:
            card_number: The card number.

        Returns:
            The reopened card or None.
        """
        self._http.delete(f"/cards/{card_number}/closure")
        return None

    def postpone(self, card_number: int) -> Card | None:
        """Postpone a card (move to 'not now').

        Args:
            card_number: The card number.

        Returns:
            The postponed card or None.
        """
        data = self._http.post(f"/cards/{card_number}/not_now")
        return self._parse_model(data, Card) if data else None

    # Alias for backwards compatibility
    defer = postpone

    def triage(self, card_number: int, column_id: str | int) -> Card | None:
        """Move a card to a column (triage).

        Args:
            card_number: The card number.
            column_id: The column ID to move the card to.

        Returns:
            The triaged card or None.
        """
        data = self._http.post(f"/cards/{card_number}/triage", data={"column_id": column_id})
        return self._parse_model(data, Card) if data else None

    def untriage(self, card_number: int) -> Card | None:
        """Remove a card from triage.

        Args:
            card_number: The card number.

        Returns:
            The card or None.
        """
        self._http.delete(f"/cards/{card_number}/triage")
        return None

    def toggle_tag(self, card_number: int, tag_title: str) -> Card | None:
        """Toggle a tag on a card.

        Args:
            card_number: The card number.
            tag_title: The tag title to toggle.

        Returns:
            The updated card or None.
        """
        data = self._http.post(f"/cards/{card_number}/taggings", data={"tag_title": tag_title})
        return self._parse_model(data, Card) if data else None

    def toggle_assignment(self, card_number: int, assignee_id: str | int) -> Card | None:
        """Toggle assignment of a user to a card.

        Args:
            card_number: The card number.
            assignee_id: The user ID to toggle assignment for.

        Returns:
            The updated card or None.
        """
        data = self._http.post(
            f"/cards/{card_number}/assignments", data={"assignee_id": assignee_id}
        )
        return self._parse_model(data, Card) if data else None

    def watch(self, card_number: int) -> Card | None:
        """Start watching a card.

        Args:
            card_number: The card number.

        Returns:
            The card or None.
        """
        data = self._http.post(f"/cards/{card_number}/watch")
        return self._parse_model(data, Card) if data else None

    def unwatch(self, card_number: int) -> None:
        """Stop watching a card.

        Args:
            card_number: The card number.
        """
        self._http.delete(f"/cards/{card_number}/watch")

    def gild(self, card_number: int) -> Card | None:
        """Make a card a 'golden ticket' (highlighted/pinned).

        Args:
            card_number: The card number.

        Returns:
            The card or None.
        """
        data = self._http.post(f"/cards/{card_number}/goldness")
        return self._parse_model(data, Card) if data else None

    def ungild(self, card_number: int) -> None:
        """Remove 'golden ticket' status from a card.

        Args:
            card_number: The card number.
        """
        self._http.delete(f"/cards/{card_number}/goldness")


class AsyncCardsResource(AsyncBaseResource[Card]):
    """Async resource for managing cards."""

    def __init__(self, http_client: AsyncHTTPClient) -> None:
        super().__init__(http_client)

    async def list(
        self,
        board_id: str | int | None = None,
        column_id: str | int | None = None,
        tag_ids: builtins.list[str] | None = None,
        assignee_ids: builtins.list[str] | None = None,
        status: str | None = None,
    ) -> list[Card]:
        """List cards with optional filters.

        Args:
            board_id: Filter by board ID.
            column_id: Filter by column ID.
            tag_ids: Filter by tag IDs.
            assignee_ids: Filter by assignee IDs.
            status: Filter by status (open, closed, deferred).

        Returns:
            A list of cards.
        """
        params: dict[str, Any] = {}
        if board_id is not None:
            params["board_id"] = board_id
        if column_id is not None:
            params["column_id"] = column_id
        if tag_ids is not None:
            params["tag_ids"] = tag_ids
        if assignee_ids is not None:
            params["assignee_ids"] = assignee_ids
        if status is not None:
            params["status"] = status

        data, _ = await self._http.get("/cards", params=params)
        return self._parse_list(data, Card)

    async def list_paginated(
        self,
        board_id: str | int | None = None,
        column_id: str | int | None = None,
        tag_ids: builtins.list[str] | None = None,
        assignee_ids: builtins.list[str] | None = None,
        status: str | None = None,
    ) -> AsyncPaginatedResponse[Card]:
        """List cards with pagination support.

        Args:
            board_id: Filter by board ID.
            column_id: Filter by column ID.
            tag_ids: Filter by tag IDs.
            assignee_ids: Filter by assignee IDs.
            status: Filter by status (open, closed, deferred).

        Returns:
            A paginated response containing cards.
        """
        params: dict[str, Any] = {}
        if board_id is not None:
            params["board_id"] = board_id
        if column_id is not None:
            params["column_id"] = column_id
        if tag_ids is not None:
            params["tag_ids"] = tag_ids
        if assignee_ids is not None:
            params["assignee_ids"] = assignee_ids
        if status is not None:
            params["status"] = status

        data, response = await self._http.get("/cards", params=params)
        return AsyncPaginatedResponse(
            items=self._parse_list(data, Card),
            response=response,
            http_client=self._http,
            path="/cards",
            params=params,
        )

    def list_all(
        self,
        board_id: str | int | None = None,
        column_id: str | int | None = None,
        tag_ids: builtins.list[str] | None = None,
        assignee_ids: builtins.list[str] | None = None,
        status: str | None = None,
    ) -> AsyncPaginationIterator[Card]:
        """Iterate over all cards, automatically handling pagination.

        Args:
            board_id: Filter by board ID.
            column_id: Filter by column ID.
            tag_ids: Filter by tag IDs.
            assignee_ids: Filter by assignee IDs.
            status: Filter by status (open, closed, deferred).

        Returns:
            An async iterator that yields all cards across all pages.
        """
        params: dict[str, Any] = {}
        if board_id is not None:
            params["board_id"] = board_id
        if column_id is not None:
            params["column_id"] = column_id
        if tag_ids is not None:
            params["tag_ids"] = tag_ids
        if assignee_ids is not None:
            params["assignee_ids"] = assignee_ids
        if status is not None:
            params["status"] = status

        return AsyncPaginationIterator(
            http_client=self._http,
            path="/cards",
            params=params,
        )

    async def get(self, card_number: int) -> Card:
        """Get a specific card by its number.

        Args:
            card_number: The card number (not ID).

        Returns:
            The requested card.
        """
        data, _ = await self._http.get(f"/cards/{card_number}")
        return self._parse_model(data, Card)

    async def create(
        self,
        board_id: str | int,
        title: str,
        description: str | None = None,
        column_id: str | int | None = None,
        tag_ids: builtins.list[str] | None = None,
        assignee_ids: builtins.list[str] | None = None,
        image: FileInput | None = None,
    ) -> Card:
        """Create a new card.

        Args:
            board_id: The ID of the board to create the card in.
            title: The title of the card.
            description: Optional HTML description of the card.
            column_id: Optional column ID to place the card in.
            tag_ids: Optional list of tag IDs to apply.
            assignee_ids: Optional list of user IDs to assign.
            image: Optional header image. Can be a file path (str or Path),
                   or a tuple of (filename, file_obj, content_type).

        Returns:
            The created card.
        """
        payload: dict[str, Any] = {"title": title}
        if description is not None:
            payload["description"] = description
        if column_id is not None:
            payload["column_id"] = column_id
        if tag_ids is not None:
            payload["tag_ids"] = tag_ids
        if assignee_ids is not None:
            payload["assignee_ids"] = assignee_ids

        if image is not None:
            files = {"card[image]": image}
            data = await self._http.post_multipart(
                f"/boards/{board_id}/cards",
                data={"card": payload},
                files=files,
            )
        else:
            data = await self._http.post(f"/boards/{board_id}/cards", data={"card": payload})
        return self._parse_model(data, Card)

    async def update(
        self,
        card_number: int,
        title: str | None = None,
        description: str | None = None,
        column_id: str | int | None = None,
        board_id: str | int | None = None,
        image: FileInput | None = None,
    ) -> Card:
        """Update a card.

        Args:
            card_number: The card number.
            title: Optional new title.
            description: Optional new HTML description.
            column_id: Optional new column ID.
            board_id: Optional new board ID.
            image: Optional header image. Can be a file path (str or Path),
                   or a tuple of (filename, file_obj, content_type).

        Returns:
            The updated card.
        """
        payload: dict[str, Any] = {}
        if title is not None:
            payload["title"] = title
        if description is not None:
            payload["description"] = description
        if column_id is not None:
            payload["column_id"] = column_id
        if board_id is not None:
            payload["board_id"] = board_id

        if image is not None:
            files = {"card[image]": image}
            data = await self._http.put_multipart(
                f"/cards/{card_number}",
                data={"card": payload},
                files=files,
            )
        else:
            data = await self._http.put(f"/cards/{card_number}", data={"card": payload})
        return self._parse_model(data, Card)

    async def delete_image(self, card_number: int) -> None:
        """Delete the header image from a card.

        Args:
            card_number: The card number.
        """
        await self._http.delete(f"/cards/{card_number}/image")

    async def delete(self, card_number: int) -> None:
        """Delete a card.

        Args:
            card_number: The card number.
        """
        await self._http.delete(f"/cards/{card_number}")

    async def close(self, card_number: int) -> Card | None:
        """Close a card.

        Args:
            card_number: The card number.

        Returns:
            The closed card or None.
        """
        data = await self._http.post(f"/cards/{card_number}/closure")
        return self._parse_model(data, Card) if data else None

    async def reopen(self, card_number: int) -> Card | None:
        """Reopen a closed card.

        Args:
            card_number: The card number.

        Returns:
            The reopened card or None.
        """
        await self._http.delete(f"/cards/{card_number}/closure")
        return None

    async def postpone(self, card_number: int) -> Card | None:
        """Postpone a card (move to 'not now').

        Args:
            card_number: The card number.

        Returns:
            The postponed card or None.
        """
        data = await self._http.post(f"/cards/{card_number}/not_now")
        return self._parse_model(data, Card) if data else None

    # Alias for backwards compatibility
    defer = postpone

    async def triage(self, card_number: int, column_id: str | int) -> Card | None:
        """Move a card to a column (triage).

        Args:
            card_number: The card number.
            column_id: The column ID to move the card to.

        Returns:
            The triaged card or None.
        """
        data = await self._http.post(f"/cards/{card_number}/triage", data={"column_id": column_id})
        return self._parse_model(data, Card) if data else None

    async def untriage(self, card_number: int) -> Card | None:
        """Remove a card from triage.

        Args:
            card_number: The card number.

        Returns:
            The card or None.
        """
        await self._http.delete(f"/cards/{card_number}/triage")
        return None

    async def toggle_tag(self, card_number: int, tag_title: str) -> Card | None:
        """Toggle a tag on a card.

        Args:
            card_number: The card number.
            tag_title: The tag title to toggle.

        Returns:
            The updated card or None.
        """
        data = await self._http.post(
            f"/cards/{card_number}/taggings", data={"tag_title": tag_title}
        )
        return self._parse_model(data, Card) if data else None

    async def toggle_assignment(self, card_number: int, assignee_id: str | int) -> Card | None:
        """Toggle assignment of a user to a card.

        Args:
            card_number: The card number.
            assignee_id: The user ID to toggle assignment for.

        Returns:
            The updated card or None.
        """
        data = await self._http.post(
            f"/cards/{card_number}/assignments", data={"assignee_id": assignee_id}
        )
        return self._parse_model(data, Card) if data else None

    async def watch(self, card_number: int) -> Card | None:
        """Start watching a card.

        Args:
            card_number: The card number.

        Returns:
            The card or None.
        """
        data = await self._http.post(f"/cards/{card_number}/watch")
        return self._parse_model(data, Card) if data else None

    async def unwatch(self, card_number: int) -> None:
        """Stop watching a card.

        Args:
            card_number: The card number.
        """
        await self._http.delete(f"/cards/{card_number}/watch")

    async def gild(self, card_number: int) -> Card | None:
        """Make a card a 'golden ticket' (highlighted/pinned).

        Args:
            card_number: The card number.

        Returns:
            The card or None.
        """
        data = await self._http.post(f"/cards/{card_number}/goldness")
        return self._parse_model(data, Card) if data else None

    async def ungild(self, card_number: int) -> None:
        """Remove 'golden ticket' status from a card.

        Args:
            card_number: The card number.
        """
        await self._http.delete(f"/cards/{card_number}/goldness")
