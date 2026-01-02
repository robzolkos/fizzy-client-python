"""Tags resource for the Fizzy API."""

from __future__ import annotations

from typing import TYPE_CHECKING

from fizzy.models.tag import Tag
from fizzy.resources.base import AsyncBaseResource, BaseResource

if TYPE_CHECKING:
    from fizzy.utils.http import AsyncHTTPClient, HTTPClient


class TagsResource(BaseResource[Tag]):
    """Resource for accessing tags."""

    def __init__(self, http_client: HTTPClient) -> None:
        super().__init__(http_client)

    def list(self) -> list[Tag]:
        """List all tags in the account.

        Returns:
            A list of tags.
        """
        data, _ = self._http.get("/tags")
        return self._parse_list(data, Tag)


class AsyncTagsResource(AsyncBaseResource[Tag]):
    """Async resource for accessing tags."""

    def __init__(self, http_client: AsyncHTTPClient) -> None:
        super().__init__(http_client)

    async def list(self) -> list[Tag]:
        """List all tags in the account.

        Returns:
            A list of tags.
        """
        data, _ = await self._http.get("/tags")
        return self._parse_list(data, Tag)
