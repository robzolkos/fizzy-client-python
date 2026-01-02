"""Users resource for the Fizzy API."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any, BinaryIO

from fizzy.models.user import User
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


class UsersResource(BaseResource[User]):
    """Resource for managing users in an account."""

    def __init__(self, http_client: HTTPClient) -> None:
        super().__init__(http_client)

    def list(self) -> list[User]:
        """List all users in the account.

        Returns:
            A list of users.
        """
        data, _ = self._http.get("/users")
        return self._parse_list(data, User)

    def list_paginated(self) -> PaginatedResponse[User]:
        """List users with pagination support.

        Returns:
            A paginated response containing users.
        """
        data, response = self._http.get("/users")
        return PaginatedResponse(
            items=self._parse_list(data, User),
            response=response,
            http_client=self._http,
            path="/users",
        )

    def list_all(self) -> PaginationIterator[User]:
        """Iterate over all users, automatically handling pagination.

        Returns:
            An iterator that yields all users across all pages.
        """
        return PaginationIterator(
            http_client=self._http,
            path="/users",
        )

    def get(self, user_id: str | int) -> User:
        """Get a specific user.

        Args:
            user_id: The user ID.

        Returns:
            The requested user.
        """
        data, _ = self._http.get(f"/users/{user_id}")
        return self._parse_model(data, User)

    def update(
        self,
        user_id: str | int,
        name: str | None = None,
        avatar: FileInput | None = None,
    ) -> User:
        """Update a user.

        Args:
            user_id: The user ID.
            name: Optional new name.
            avatar: Optional avatar image. Can be a file path (str or Path),
                    or a tuple of (filename, file_obj, content_type).

        Returns:
            The updated user.
        """
        payload: dict[str, Any] = {}
        if name is not None:
            payload["name"] = name

        if avatar is not None:
            files = {"user[avatar]": avatar}
            self._http.put_multipart(f"/users/{user_id}", data={"user": payload}, files=files)
        else:
            self._http.put(f"/users/{user_id}", data={"user": payload})
        # API returns 204 No Content, so fetch the updated user
        return self.get(user_id)

    def delete(self, user_id: str | int) -> None:
        """Deactivate a user.

        Args:
            user_id: The user ID.
        """
        self._http.delete(f"/users/{user_id}")


class AsyncUsersResource(AsyncBaseResource[User]):
    """Async resource for managing users in an account."""

    def __init__(self, http_client: AsyncHTTPClient) -> None:
        super().__init__(http_client)

    async def list(self) -> list[User]:
        """List all users in the account.

        Returns:
            A list of users.
        """
        data, _ = await self._http.get("/users")
        return self._parse_list(data, User)

    async def list_paginated(self) -> AsyncPaginatedResponse[User]:
        """List users with pagination support.

        Returns:
            A paginated response containing users.
        """
        data, response = await self._http.get("/users")
        return AsyncPaginatedResponse(
            items=self._parse_list(data, User),
            response=response,
            http_client=self._http,
            path="/users",
        )

    def list_all(self) -> AsyncPaginationIterator[User]:
        """Iterate over all users, automatically handling pagination.

        Returns:
            An async iterator that yields all users across all pages.
        """
        return AsyncPaginationIterator(
            http_client=self._http,
            path="/users",
        )

    async def get(self, user_id: str | int) -> User:
        """Get a specific user.

        Args:
            user_id: The user ID.

        Returns:
            The requested user.
        """
        data, _ = await self._http.get(f"/users/{user_id}")
        return self._parse_model(data, User)

    async def update(
        self,
        user_id: str | int,
        name: str | None = None,
        avatar: FileInput | None = None,
    ) -> User:
        """Update a user.

        Args:
            user_id: The user ID.
            name: Optional new name.
            avatar: Optional avatar image. Can be a file path (str or Path),
                    or a tuple of (filename, file_obj, content_type).

        Returns:
            The updated user.
        """
        payload: dict[str, Any] = {}
        if name is not None:
            payload["name"] = name

        if avatar is not None:
            files = {"user[avatar]": avatar}
            await self._http.put_multipart(f"/users/{user_id}", data={"user": payload}, files=files)
        else:
            await self._http.put(f"/users/{user_id}", data={"user": payload})
        # API returns 204 No Content, so fetch the updated user
        return await self.get(user_id)

    async def delete(self, user_id: str | int) -> None:
        """Deactivate a user.

        Args:
            user_id: The user ID.
        """
        await self._http.delete(f"/users/{user_id}")
