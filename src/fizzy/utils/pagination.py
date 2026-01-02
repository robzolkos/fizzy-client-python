"""Pagination utilities for the Fizzy API client."""

from __future__ import annotations

from collections.abc import AsyncIterator, Iterator
from typing import TYPE_CHECKING, Any, Generic, TypeVar

from fizzy.utils.http import parse_link_header

if TYPE_CHECKING:
    import httpx

    from fizzy.utils.http import AsyncHTTPClient, HTTPClient

T = TypeVar("T")


class PaginatedResponse(Generic[T]):
    """A paginated response from the API."""

    def __init__(
        self,
        items: list[T],
        response: httpx.Response,
        http_client: HTTPClient,
        path: str,
        params: dict[str, Any] | None = None,
    ) -> None:
        self.items = items
        self._response = response
        self._http_client = http_client
        self._path = path
        self._params = params or {}
        self._links = parse_link_header(response.headers.get("Link"))

    @property
    def has_next(self) -> bool:
        """Check if there is a next page."""
        return "next" in self._links

    @property
    def next_url(self) -> str | None:
        """Get the URL for the next page."""
        return self._links.get("next")

    def next_page(self) -> PaginatedResponse[T]:
        """Fetch the next page of results."""
        if not self.has_next:
            raise StopIteration("No more pages")

        # Extract the path from the next URL
        next_url = self._links["next"]
        # The URL is relative to the base URL
        data, response = self._http_client.get(next_url, include_account=False)

        return PaginatedResponse(
            items=data,
            response=response,
            http_client=self._http_client,
            path=self._path,
            params=self._params,
        )

    def __iter__(self) -> Iterator[T]:
        """Iterate over items in this page."""
        return iter(self.items)

    def __len__(self) -> int:
        """Return the number of items in this page."""
        return len(self.items)


class AsyncPaginatedResponse(Generic[T]):
    """An async paginated response from the API."""

    def __init__(
        self,
        items: list[T],
        response: httpx.Response,
        http_client: AsyncHTTPClient,
        path: str,
        params: dict[str, Any] | None = None,
    ) -> None:
        self.items = items
        self._response = response
        self._http_client = http_client
        self._path = path
        self._params = params or {}
        self._links = parse_link_header(response.headers.get("Link"))

    @property
    def has_next(self) -> bool:
        """Check if there is a next page."""
        return "next" in self._links

    @property
    def next_url(self) -> str | None:
        """Get the URL for the next page."""
        return self._links.get("next")

    async def next_page(self) -> AsyncPaginatedResponse[T]:
        """Fetch the next page of results."""
        if not self.has_next:
            raise StopAsyncIteration("No more pages")

        next_url = self._links["next"]
        data, response = await self._http_client.get(next_url, include_account=False)

        return AsyncPaginatedResponse(
            items=data,
            response=response,
            http_client=self._http_client,
            path=self._path,
            params=self._params,
        )

    def __iter__(self) -> Iterator[T]:
        """Iterate over items in this page."""
        return iter(self.items)

    def __len__(self) -> int:
        """Return the number of items in this page."""
        return len(self.items)


class PaginationIterator(Generic[T]):
    """Iterator that automatically fetches all pages."""

    def __init__(
        self,
        http_client: HTTPClient,
        path: str,
        params: dict[str, Any] | None = None,
    ) -> None:
        self._http_client = http_client
        self._path = path
        self._params = params or {}
        self._current_page: PaginatedResponse[T] | None = None
        self._index = 0

    def __iter__(self) -> Iterator[T]:
        return self

    def __next__(self) -> T:
        # Fetch the first page if not yet fetched
        if self._current_page is None:
            data, response = self._http_client.get(self._path, params=self._params)
            self._current_page = PaginatedResponse(
                items=data,
                response=response,
                http_client=self._http_client,
                path=self._path,
                params=self._params,
            )
            self._index = 0

        # Return next item from current page
        if self._index < len(self._current_page.items):
            item = self._current_page.items[self._index]
            self._index += 1
            return item

        # Fetch next page if available
        if self._current_page.has_next:
            self._current_page = self._current_page.next_page()
            self._index = 0
            return self.__next__()

        raise StopIteration


class AsyncPaginationIterator(Generic[T]):
    """Async iterator that automatically fetches all pages."""

    def __init__(
        self,
        http_client: AsyncHTTPClient,
        path: str,
        params: dict[str, Any] | None = None,
    ) -> None:
        self._http_client = http_client
        self._path = path
        self._params = params or {}
        self._current_page: AsyncPaginatedResponse[T] | None = None
        self._index = 0

    def __aiter__(self) -> AsyncIterator[T]:
        return self

    async def __anext__(self) -> T:
        # Fetch the first page if not yet fetched
        if self._current_page is None:
            data, response = await self._http_client.get(self._path, params=self._params)
            self._current_page = AsyncPaginatedResponse(
                items=data,
                response=response,
                http_client=self._http_client,
                path=self._path,
                params=self._params,
            )
            self._index = 0

        # Return next item from current page
        if self._index < len(self._current_page.items):
            item = self._current_page.items[self._index]
            self._index += 1
            return item

        # Fetch next page if available
        if self._current_page.has_next:
            self._current_page = await self._current_page.next_page()
            self._index = 0
            return await self.__anext__()

        raise StopAsyncIteration
