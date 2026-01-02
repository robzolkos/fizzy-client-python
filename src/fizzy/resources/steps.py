"""Steps resource for the Fizzy API."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from fizzy.models.card import Card
from fizzy.models.step import Step
from fizzy.resources.base import AsyncBaseResource, BaseResource

if TYPE_CHECKING:
    from fizzy.utils.http import AsyncHTTPClient, HTTPClient


class StepsResource(BaseResource[Step]):
    """Resource for managing steps (checklist items) on cards."""

    def __init__(self, http_client: HTTPClient) -> None:
        super().__init__(http_client)

    def list(self, card_number: int) -> list[Step]:
        """List all steps on a card.

        Note: Steps are fetched via the card endpoint since there's no
        dedicated steps list endpoint.

        Args:
            card_number: The card number.

        Returns:
            A list of steps.
        """
        data, _ = self._http.get(f"/cards/{card_number}")
        card = Card.model_validate(data)
        # Convert CardStep objects to Step objects
        return [
            Step(
                id=s.id,
                content=s.content,
                completed=s.completed,
                position=s.position,
                completed_at=s.completed_at,
            )
            for s in card.steps
        ]

    def get(self, card_number: int, step_id: str | int) -> Step:
        """Get a specific step.

        Args:
            card_number: The card number.
            step_id: The step ID.

        Returns:
            The requested step.
        """
        data, _ = self._http.get(f"/cards/{card_number}/steps/{step_id}")
        return self._parse_model(data, Step)

    def create(self, card_number: int, content: str, completed: bool | None = None) -> Step:
        """Create a new step on a card.

        Args:
            card_number: The card number.
            content: The content/description of the step.
            completed: Optional completion status.

        Returns:
            The created step.
        """
        payload: dict[str, Any] = {"content": content}
        if completed is not None:
            payload["completed"] = completed

        data = self._http.post(
            f"/cards/{card_number}/steps",
            data={"step": payload},
        )
        return self._parse_model(data, Step)

    def update(
        self,
        card_number: int,
        step_id: str | int,
        content: str | None = None,
        completed: bool | None = None,
    ) -> Step:
        """Update a step.

        Args:
            card_number: The card number.
            step_id: The step ID.
            content: Optional new content/description.
            completed: Optional completion status.

        Returns:
            The updated step.
        """
        payload: dict[str, Any] = {}
        if content is not None:
            payload["content"] = content
        if completed is not None:
            payload["completed"] = completed

        data = self._http.put(
            f"/cards/{card_number}/steps/{step_id}",
            data={"step": payload},
        )
        return self._parse_model(data, Step)

    def delete(self, card_number: int, step_id: str | int) -> None:
        """Delete a step.

        Args:
            card_number: The card number.
            step_id: The step ID.
        """
        self._http.delete(f"/cards/{card_number}/steps/{step_id}")


class AsyncStepsResource(AsyncBaseResource[Step]):
    """Async resource for managing steps (checklist items) on cards."""

    def __init__(self, http_client: AsyncHTTPClient) -> None:
        super().__init__(http_client)

    async def list(self, card_number: int) -> list[Step]:
        """List all steps on a card.

        Note: Steps are fetched via the card endpoint since there's no
        dedicated steps list endpoint.

        Args:
            card_number: The card number.

        Returns:
            A list of steps.
        """
        data, _ = await self._http.get(f"/cards/{card_number}")
        card = Card.model_validate(data)
        # Convert CardStep objects to Step objects
        return [
            Step(
                id=s.id,
                content=s.content,
                completed=s.completed,
                position=s.position,
                completed_at=s.completed_at,
            )
            for s in card.steps
        ]

    async def get(self, card_number: int, step_id: str | int) -> Step:
        """Get a specific step.

        Args:
            card_number: The card number.
            step_id: The step ID.

        Returns:
            The requested step.
        """
        data, _ = await self._http.get(f"/cards/{card_number}/steps/{step_id}")
        return self._parse_model(data, Step)

    async def create(self, card_number: int, content: str, completed: bool | None = None) -> Step:
        """Create a new step on a card.

        Args:
            card_number: The card number.
            content: The content/description of the step.
            completed: Optional completion status.

        Returns:
            The created step.
        """
        payload: dict[str, Any] = {"content": content}
        if completed is not None:
            payload["completed"] = completed

        data = await self._http.post(
            f"/cards/{card_number}/steps",
            data={"step": payload},
        )
        return self._parse_model(data, Step)

    async def update(
        self,
        card_number: int,
        step_id: str | int,
        content: str | None = None,
        completed: bool | None = None,
    ) -> Step:
        """Update a step.

        Args:
            card_number: The card number.
            step_id: The step ID.
            content: Optional new content/description.
            completed: Optional completion status.

        Returns:
            The updated step.
        """
        payload: dict[str, Any] = {}
        if content is not None:
            payload["content"] = content
        if completed is not None:
            payload["completed"] = completed

        data = await self._http.put(
            f"/cards/{card_number}/steps/{step_id}",
            data={"step": payload},
        )
        return self._parse_model(data, Step)

    async def delete(self, card_number: int, step_id: str | int) -> None:
        """Delete a step.

        Args:
            card_number: The card number.
            step_id: The step ID.
        """
        await self._http.delete(f"/cards/{card_number}/steps/{step_id}")
