"""Boards resource for the Fizzy API."""

from __future__ import annotations

import builtins
from typing import TYPE_CHECKING, Any

from fizzy.models.board import Board
from fizzy.resources.base import AsyncBaseResource, BaseResource
from fizzy.utils.pagination import (
    AsyncPaginatedResponse,
    AsyncPaginationIterator,
    PaginatedResponse,
    PaginationIterator,
)

if TYPE_CHECKING:
    from fizzy.utils.http import AsyncHTTPClient, HTTPClient


class BoardsResource(BaseResource[Board]):
    """Resource for managing boards."""

    def __init__(self, http_client: HTTPClient) -> None:
        super().__init__(http_client)

    def list(self) -> list[Board]:
        """List all boards in the account.

        Returns:
            A list of boards.
        """
        data, _ = self._http.get("/boards")
        return self._parse_list(data, Board)

    def list_paginated(self) -> PaginatedResponse[Board]:
        """List boards with pagination support.

        Returns:
            A paginated response containing boards.
        """
        data, response = self._http.get("/boards")
        return PaginatedResponse(
            items=self._parse_list(data, Board),
            response=response,
            http_client=self._http,
            path="/boards",
        )

    def list_all(self) -> PaginationIterator[Board]:
        """Iterate over all boards, automatically handling pagination.

        Returns:
            An iterator that yields all boards across all pages.
        """
        return PaginationIterator(
            http_client=self._http,
            path="/boards",
        )

    def get(self, board_id: str | int) -> Board:
        """Get a specific board.

        Args:
            board_id: The ID of the board to retrieve.

        Returns:
            The requested board.
        """
        data, _ = self._http.get(f"/boards/{board_id}")
        return self._parse_model(data, Board)

    def create(
        self,
        name: str,
        public_description: str | None = None,
        all_access: bool | None = None,
        auto_postpone_period: int | None = None,
    ) -> Board:
        """Create a new board.

        Args:
            name: The name of the board.
            public_description: Rich text description shown on the public board page.
            all_access: Whether any user in the account can access this board.
            auto_postpone_period: Number of days of inactivity before cards are postponed.

        Returns:
            The created board.
        """
        payload: dict[str, Any] = {"name": name}
        if public_description is not None:
            payload["public_description"] = public_description
        if all_access is not None:
            payload["all_access"] = all_access
        if auto_postpone_period is not None:
            payload["auto_postpone_period"] = auto_postpone_period

        data = self._http.post("/boards", data={"board": payload})
        return self._parse_model(data, Board)

    def update(
        self,
        board_id: str | int,
        name: str | None = None,
        public_description: str | None = None,
        all_access: bool | None = None,
        auto_postpone_period: int | None = None,
        user_ids: builtins.list[str] | None = None,
    ) -> Board:
        """Update a board.

        Args:
            board_id: The ID of the board to update.
            name: Optional new name for the board.
            public_description: Rich text description shown on the public board page.
            all_access: Whether any user in the account can access this board.
            auto_postpone_period: Number of days of inactivity before cards are postponed.
            user_ids: Array of user IDs who should have access (only when all_access is False).

        Returns:
            The updated board (fetched after update since API returns 204).
        """
        payload: dict[str, Any] = {}
        if name is not None:
            payload["name"] = name
        if public_description is not None:
            payload["public_description"] = public_description
        if all_access is not None:
            payload["all_access"] = all_access
        if auto_postpone_period is not None:
            payload["auto_postpone_period"] = auto_postpone_period
        if user_ids is not None:
            payload["user_ids"] = user_ids

        self._http.put(f"/boards/{board_id}", data={"board": payload})
        # API returns 204 No Content, so fetch the updated board
        return self.get(board_id)

    def delete(self, board_id: str | int) -> None:
        """Delete a board.

        Args:
            board_id: The ID of the board to delete.
        """
        self._http.delete(f"/boards/{board_id}")


class AsyncBoardsResource(AsyncBaseResource[Board]):
    """Async resource for managing boards."""

    def __init__(self, http_client: AsyncHTTPClient) -> None:
        super().__init__(http_client)

    async def list(self) -> list[Board]:
        """List all boards in the account.

        Returns:
            A list of boards.
        """
        data, _ = await self._http.get("/boards")
        return self._parse_list(data, Board)

    async def list_paginated(self) -> AsyncPaginatedResponse[Board]:
        """List boards with pagination support.

        Returns:
            A paginated response containing boards.
        """
        data, response = await self._http.get("/boards")
        return AsyncPaginatedResponse(
            items=self._parse_list(data, Board),
            response=response,
            http_client=self._http,
            path="/boards",
        )

    def list_all(self) -> AsyncPaginationIterator[Board]:
        """Iterate over all boards, automatically handling pagination.

        Returns:
            An async iterator that yields all boards across all pages.
        """
        return AsyncPaginationIterator(
            http_client=self._http,
            path="/boards",
        )

    async def get(self, board_id: str | int) -> Board:
        """Get a specific board.

        Args:
            board_id: The ID of the board to retrieve.

        Returns:
            The requested board.
        """
        data, _ = await self._http.get(f"/boards/{board_id}")
        return self._parse_model(data, Board)

    async def create(
        self,
        name: str,
        public_description: str | None = None,
        all_access: bool | None = None,
        auto_postpone_period: int | None = None,
    ) -> Board:
        """Create a new board.

        Args:
            name: The name of the board.
            public_description: Rich text description shown on the public board page.
            all_access: Whether any user in the account can access this board.
            auto_postpone_period: Number of days of inactivity before cards are postponed.

        Returns:
            The created board.
        """
        payload: dict[str, Any] = {"name": name}
        if public_description is not None:
            payload["public_description"] = public_description
        if all_access is not None:
            payload["all_access"] = all_access
        if auto_postpone_period is not None:
            payload["auto_postpone_period"] = auto_postpone_period

        data = await self._http.post("/boards", data={"board": payload})
        return self._parse_model(data, Board)

    async def update(
        self,
        board_id: str | int,
        name: str | None = None,
        public_description: str | None = None,
        all_access: bool | None = None,
        auto_postpone_period: int | None = None,
        user_ids: builtins.list[str] | None = None,
    ) -> Board:
        """Update a board.

        Args:
            board_id: The ID of the board to update.
            name: Optional new name for the board.
            public_description: Rich text description shown on the public board page.
            all_access: Whether any user in the account can access this board.
            auto_postpone_period: Number of days of inactivity before cards are postponed.
            user_ids: Array of user IDs who should have access (only when all_access is False).

        Returns:
            The updated board (fetched after update since API returns 204).
        """
        payload: dict[str, Any] = {}
        if name is not None:
            payload["name"] = name
        if public_description is not None:
            payload["public_description"] = public_description
        if all_access is not None:
            payload["all_access"] = all_access
        if auto_postpone_period is not None:
            payload["auto_postpone_period"] = auto_postpone_period
        if user_ids is not None:
            payload["user_ids"] = user_ids

        await self._http.put(f"/boards/{board_id}", data={"board": payload})
        # API returns 204 No Content, so fetch the updated board
        return await self.get(board_id)

    async def delete(self, board_id: str | int) -> None:
        """Delete a board.

        Args:
            board_id: The ID of the board to delete.
        """
        await self._http.delete(f"/boards/{board_id}")
