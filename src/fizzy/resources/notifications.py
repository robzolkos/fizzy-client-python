"""Notifications resource for the Fizzy API."""

from __future__ import annotations

import builtins
from typing import TYPE_CHECKING

from fizzy.models.notification import Notification
from fizzy.resources.base import AsyncBaseResource, BaseResource
from fizzy.utils.pagination import (
    AsyncPaginatedResponse,
    AsyncPaginationIterator,
    PaginatedResponse,
    PaginationIterator,
)

if TYPE_CHECKING:
    from fizzy.utils.http import AsyncHTTPClient, HTTPClient


class NotificationsResource(BaseResource[Notification]):
    """Resource for managing notifications."""

    def __init__(self, http_client: HTTPClient) -> None:
        super().__init__(http_client)

    def list(self, read: bool | None = None) -> builtins.list[Notification]:
        """List notifications.

        Args:
            read: Optional filter by read status.

        Returns:
            A list of notifications.
        """
        params = {}
        if read is not None:
            params["read"] = read

        data, _ = self._http.get("/notifications", params=params if params else None)
        return self._parse_list(data, Notification)

    def list_paginated(self, read: bool | None = None) -> PaginatedResponse[Notification]:
        """List notifications with pagination support.

        Args:
            read: Optional filter by read status.

        Returns:
            A paginated response containing notifications.
        """
        params = {}
        if read is not None:
            params["read"] = read

        data, response = self._http.get("/notifications", params=params if params else None)
        return PaginatedResponse(
            items=self._parse_list(data, Notification),
            response=response,
            http_client=self._http,
            path="/notifications",
            params=params,
        )

    def list_all(self, read: bool | None = None) -> PaginationIterator[Notification]:
        """Iterate over all notifications, automatically handling pagination.

        Args:
            read: Optional filter by read status.

        Returns:
            An iterator that yields all notifications across all pages.
        """
        params = {}
        if read is not None:
            params["read"] = read

        return PaginationIterator(
            http_client=self._http,
            path="/notifications",
            params=params if params else None,
        )

    def mark_read(self, notification_id: str | int) -> Notification:
        """Mark a notification as read.

        Args:
            notification_id: The notification ID.

        Returns:
            The updated notification.
        """
        data = self._http.post(f"/notifications/{notification_id}/read")
        return self._parse_model(data, Notification)

    def mark_unread(self, notification_id: str | int) -> Notification:
        """Mark a notification as unread.

        Args:
            notification_id: The notification ID.

        Returns:
            The updated notification.
        """
        data = self._http.post(f"/notifications/{notification_id}/unread")
        return self._parse_model(data, Notification)

    def bulk_mark_read(self, notification_ids: builtins.list[str]) -> builtins.list[Notification]:
        """Mark multiple notifications as read.

        Args:
            notification_ids: List of notification IDs.

        Returns:
            The updated notifications.
        """
        data = self._http.post("/notifications/read", data={"notification_ids": notification_ids})
        return self._parse_list(data, Notification)


class AsyncNotificationsResource(AsyncBaseResource[Notification]):
    """Async resource for managing notifications."""

    def __init__(self, http_client: AsyncHTTPClient) -> None:
        super().__init__(http_client)

    async def list(self, read: bool | None = None) -> builtins.list[Notification]:
        """List notifications.

        Args:
            read: Optional filter by read status.

        Returns:
            A list of notifications.
        """
        params = {}
        if read is not None:
            params["read"] = read

        data, _ = await self._http.get("/notifications", params=params if params else None)
        return self._parse_list(data, Notification)

    async def list_paginated(
        self, read: bool | None = None
    ) -> AsyncPaginatedResponse[Notification]:
        """List notifications with pagination support.

        Args:
            read: Optional filter by read status.

        Returns:
            A paginated response containing notifications.
        """
        params = {}
        if read is not None:
            params["read"] = read

        data, response = await self._http.get("/notifications", params=params if params else None)
        return AsyncPaginatedResponse(
            items=self._parse_list(data, Notification),
            response=response,
            http_client=self._http,
            path="/notifications",
            params=params,
        )

    def list_all(self, read: bool | None = None) -> AsyncPaginationIterator[Notification]:
        """Iterate over all notifications, automatically handling pagination.

        Args:
            read: Optional filter by read status.

        Returns:
            An async iterator that yields all notifications across all pages.
        """
        params = {}
        if read is not None:
            params["read"] = read

        return AsyncPaginationIterator(
            http_client=self._http,
            path="/notifications",
            params=params if params else None,
        )

    async def mark_read(self, notification_id: str | int) -> Notification:
        """Mark a notification as read.

        Args:
            notification_id: The notification ID.

        Returns:
            The updated notification.
        """
        data = await self._http.post(f"/notifications/{notification_id}/read")
        return self._parse_model(data, Notification)

    async def mark_unread(self, notification_id: str | int) -> Notification:
        """Mark a notification as unread.

        Args:
            notification_id: The notification ID.

        Returns:
            The updated notification.
        """
        data = await self._http.post(f"/notifications/{notification_id}/unread")
        return self._parse_model(data, Notification)

    async def bulk_mark_read(
        self, notification_ids: builtins.list[str]
    ) -> builtins.list[Notification]:
        """Mark multiple notifications as read.

        Args:
            notification_ids: List of notification IDs.

        Returns:
            The updated notifications.
        """
        data = await self._http.post(
            "/notifications/read", data={"notification_ids": notification_ids}
        )
        return self._parse_list(data, Notification)
