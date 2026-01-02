"""Identity resource for the Fizzy API."""

from __future__ import annotations

from typing import TYPE_CHECKING

from fizzy.models.identity import Account, Identity
from fizzy.resources.base import AsyncBaseResource, BaseResource

if TYPE_CHECKING:
    from fizzy.utils.http import AsyncHTTPClient, HTTPClient


class IdentityResource(BaseResource[Identity]):
    """Resource for accessing the authenticated user's identity."""

    def __init__(self, http_client: HTTPClient) -> None:
        super().__init__(http_client)

    def get(self) -> Identity:
        """Get the authenticated user's identity.

        Returns:
            The authenticated user's identity with account information.
        """
        data, _ = self._http.get("/my/identity", include_account=False)
        # The API returns a list of accounts directly
        if isinstance(data, list):
            accounts = [Account.model_validate(acc) for acc in data]
            return Identity(accounts=accounts)
        return self._parse_model(data, Identity)


class AsyncIdentityResource(AsyncBaseResource[Identity]):
    """Async resource for accessing the authenticated user's identity."""

    def __init__(self, http_client: AsyncHTTPClient) -> None:
        super().__init__(http_client)

    async def get(self) -> Identity:
        """Get the authenticated user's identity.

        Returns:
            The authenticated user's identity with account information.
        """
        data, _ = await self._http.get("/my/identity", include_account=False)
        # The API returns a list of accounts directly
        if isinstance(data, list):
            accounts = [Account.model_validate(acc) for acc in data]
            return Identity(accounts=accounts)
        return self._parse_model(data, Identity)
