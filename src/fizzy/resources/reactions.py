"""Reactions resource for the Fizzy API."""

from __future__ import annotations

from typing import TYPE_CHECKING

from fizzy.models.reaction import Reaction
from fizzy.resources.base import AsyncBaseResource, BaseResource

if TYPE_CHECKING:
    from fizzy.utils.http import AsyncHTTPClient, HTTPClient


class ReactionsResource(BaseResource[Reaction]):
    """Resource for managing reactions on comments."""

    def __init__(self, http_client: HTTPClient) -> None:
        super().__init__(http_client)

    def list(self, card_number: int, comment_id: str | int) -> list[Reaction]:
        """List all reactions on a comment.

        Args:
            card_number: The card number.
            comment_id: The comment ID.

        Returns:
            A list of reactions.
        """
        data, _ = self._http.get(f"/cards/{card_number}/comments/{comment_id}/reactions")
        return self._parse_list(data, Reaction)

    def create(self, card_number: int, comment_id: str | int, content: str) -> Reaction:
        """Add a reaction to a comment.

        Args:
            card_number: The card number.
            comment_id: The comment ID.
            content: The emoji content to add as a reaction.

        Returns:
            The created reaction.
        """
        data = self._http.post(
            f"/cards/{card_number}/comments/{comment_id}/reactions",
            data={"reaction": {"content": content}},
        )
        if data:
            return self._parse_model(data, Reaction)
        # API returns 201 with no body, list reactions and find by content
        reactions = self.list(card_number, comment_id)
        for reaction in reactions:
            if reaction.content == content:
                return reaction
        # Fallback: return a minimal reaction
        return Reaction(id="", content=content)

    def delete(self, card_number: int, comment_id: str | int, reaction_id: str | int) -> None:
        """Remove a reaction from a comment.

        Args:
            card_number: The card number.
            comment_id: The comment ID.
            reaction_id: The reaction ID.
        """
        self._http.delete(f"/cards/{card_number}/comments/{comment_id}/reactions/{reaction_id}")


class AsyncReactionsResource(AsyncBaseResource[Reaction]):
    """Async resource for managing reactions on comments."""

    def __init__(self, http_client: AsyncHTTPClient) -> None:
        super().__init__(http_client)

    async def list(self, card_number: int, comment_id: str | int) -> list[Reaction]:
        """List all reactions on a comment.

        Args:
            card_number: The card number.
            comment_id: The comment ID.

        Returns:
            A list of reactions.
        """
        data, _ = await self._http.get(f"/cards/{card_number}/comments/{comment_id}/reactions")
        return self._parse_list(data, Reaction)

    async def create(self, card_number: int, comment_id: str | int, content: str) -> Reaction:
        """Add a reaction to a comment.

        Args:
            card_number: The card number.
            comment_id: The comment ID.
            content: The emoji content to add as a reaction.

        Returns:
            The created reaction.
        """
        data = await self._http.post(
            f"/cards/{card_number}/comments/{comment_id}/reactions",
            data={"reaction": {"content": content}},
        )
        if data:
            return self._parse_model(data, Reaction)
        # API returns 201 with no body, list reactions and find by content
        reactions = await self.list(card_number, comment_id)
        for reaction in reactions:
            if reaction.content == content:
                return reaction
        # Fallback: return a minimal reaction
        return Reaction(id="", content=content)

    async def delete(self, card_number: int, comment_id: str | int, reaction_id: str | int) -> None:
        """Remove a reaction from a comment.

        Args:
            card_number: The card number.
            comment_id: The comment ID.
            reaction_id: The reaction ID.
        """
        await self._http.delete(
            f"/cards/{card_number}/comments/{comment_id}/reactions/{reaction_id}"
        )
