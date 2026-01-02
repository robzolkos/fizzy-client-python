"""Columns resource for the Fizzy API."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from fizzy.models.column import Column
from fizzy.resources.base import AsyncBaseResource, BaseResource

if TYPE_CHECKING:
    from fizzy.utils.http import AsyncHTTPClient, HTTPClient


class ColumnsResource(BaseResource[Column]):
    """Resource for managing columns on boards."""

    def __init__(self, http_client: HTTPClient) -> None:
        super().__init__(http_client)

    def list(self, board_id: str | int) -> list[Column]:
        """List all columns on a board.

        Args:
            board_id: The board ID.

        Returns:
            A list of columns.
        """
        data, _ = self._http.get(f"/boards/{board_id}/columns")
        return self._parse_list(data, Column)

    def get(self, board_id: str | int, column_id: str | int) -> Column:
        """Get a specific column.

        Args:
            board_id: The board ID.
            column_id: The column ID.

        Returns:
            The requested column.
        """
        data, _ = self._http.get(f"/boards/{board_id}/columns/{column_id}")
        return self._parse_model(data, Column)

    def create(self, board_id: str | int, name: str, color: str | None = None) -> Column:
        """Create a new column on a board.

        Args:
            board_id: The board ID.
            name: The name of the column.
            color: Optional color for the column.

        Returns:
            The created column.
        """
        payload: dict[str, Any] = {"name": name}
        if color is not None:
            payload["color"] = color

        data = self._http.post(f"/boards/{board_id}/columns", data={"column": payload})
        return self._parse_model(data, Column)

    def update(
        self,
        board_id: str | int,
        column_id: str | int,
        name: str | None = None,
        color: str | None = None,
    ) -> Column:
        """Update a column.

        Args:
            board_id: The board ID.
            column_id: The column ID.
            name: Optional new name.
            color: Optional new color.

        Returns:
            The updated column.
        """
        payload: dict[str, Any] = {}
        if name is not None:
            payload["name"] = name
        if color is not None:
            payload["color"] = color

        self._http.put(f"/boards/{board_id}/columns/{column_id}", data={"column": payload})
        # API returns 204 No Content, so fetch the updated column
        return self.get(board_id, column_id)

    def delete(self, board_id: str | int, column_id: str | int) -> None:
        """Delete a column.

        Args:
            board_id: The board ID.
            column_id: The column ID.
        """
        self._http.delete(f"/boards/{board_id}/columns/{column_id}")


class AsyncColumnsResource(AsyncBaseResource[Column]):
    """Async resource for managing columns on boards."""

    def __init__(self, http_client: AsyncHTTPClient) -> None:
        super().__init__(http_client)

    async def list(self, board_id: str | int) -> list[Column]:
        """List all columns on a board.

        Args:
            board_id: The board ID.

        Returns:
            A list of columns.
        """
        data, _ = await self._http.get(f"/boards/{board_id}/columns")
        return self._parse_list(data, Column)

    async def get(self, board_id: str | int, column_id: str | int) -> Column:
        """Get a specific column.

        Args:
            board_id: The board ID.
            column_id: The column ID.

        Returns:
            The requested column.
        """
        data, _ = await self._http.get(f"/boards/{board_id}/columns/{column_id}")
        return self._parse_model(data, Column)

    async def create(self, board_id: str | int, name: str, color: str | None = None) -> Column:
        """Create a new column on a board.

        Args:
            board_id: The board ID.
            name: The name of the column.
            color: Optional color for the column.

        Returns:
            The created column.
        """
        payload: dict[str, Any] = {"name": name}
        if color is not None:
            payload["color"] = color

        data = await self._http.post(f"/boards/{board_id}/columns", data={"column": payload})
        return self._parse_model(data, Column)

    async def update(
        self,
        board_id: str | int,
        column_id: str | int,
        name: str | None = None,
        color: str | None = None,
    ) -> Column:
        """Update a column.

        Args:
            board_id: The board ID.
            column_id: The column ID.
            name: Optional new name.
            color: Optional new color.

        Returns:
            The updated column.
        """
        payload: dict[str, Any] = {}
        if name is not None:
            payload["name"] = name
        if color is not None:
            payload["color"] = color

        await self._http.put(f"/boards/{board_id}/columns/{column_id}", data={"column": payload})
        # API returns 204 No Content, so fetch the updated column
        return await self.get(board_id, column_id)

    async def delete(self, board_id: str | int, column_id: str | int) -> None:
        """Delete a column.

        Args:
            board_id: The board ID.
            column_id: The column ID.
        """
        await self._http.delete(f"/boards/{board_id}/columns/{column_id}")
