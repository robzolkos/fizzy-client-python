"""Tests for the Steps resource."""

import pytest
import respx
from httpx import Response

from fizzy import Step


class TestStepsResource:
    """Tests for the sync Steps resource."""

    @respx.mock
    def test_list_steps(self, client, sample_card, sample_step):
        """Test listing steps on a card.

        Steps are retrieved by fetching the card and returning its steps.
        """
        # The list() method fetches the card and extracts steps
        card_with_steps = {**sample_card, "steps": [sample_step]}
        respx.get("https://app.fizzy.do/123456/cards/42").mock(
            return_value=Response(200, json=card_with_steps)
        )

        steps = client.steps.list(42)

        assert len(steps) == 1
        assert steps[0].content == "Test step"
        assert isinstance(steps[0], Step)

    @respx.mock
    def test_get_step(self, client, sample_step):
        """Test getting a specific step."""
        respx.get("https://app.fizzy.do/123456/cards/42/steps/step123").mock(
            return_value=Response(200, json=sample_step)
        )

        step = client.steps.get(42, "step123")

        assert step.id == "step123"
        assert step.content == "Test step"
        assert step.completed is False

    @respx.mock
    def test_create_step(self, client, sample_step):
        """Test creating a step."""
        respx.post("https://app.fizzy.do/123456/cards/42/steps").mock(
            return_value=Response(201, json=sample_step)
        )

        step = client.steps.create(42, content="Test step")

        assert step.content == "Test step"

    @respx.mock
    def test_create_step_with_location_header(self, client, sample_step):
        """Test creating a step when API returns 201 with Location header."""
        respx.post("https://app.fizzy.do/123456/cards/42/steps").mock(
            return_value=Response(
                201,
                headers={"Location": "https://app.fizzy.do/123456/cards/42/steps/step123.json"},
            )
        )
        respx.get("https://app.fizzy.do/123456/cards/42/steps/step123").mock(
            return_value=Response(200, json=sample_step)
        )

        step = client.steps.create(42, content="Test step")

        assert step.id == "step123"

    @respx.mock
    def test_update_step_complete(self, client, sample_step):
        """Test marking a step as complete."""
        completed = {
            **sample_step,
            "completed": True,
            "completed_at": "2025-01-02T00:00:00Z",
            "completed_by_id": "user123",
        }
        # PUT returns the updated step
        respx.put("https://app.fizzy.do/123456/cards/42/steps/step123").mock(
            return_value=Response(200, json=completed)
        )

        step = client.steps.update(42, "step123", completed=True)

        assert step.completed is True

    @respx.mock
    def test_delete_step(self, client):
        """Test deleting a step."""
        respx.delete("https://app.fizzy.do/123456/cards/42/steps/step123").mock(
            return_value=Response(204)
        )

        client.steps.delete(42, "step123")


class TestAsyncStepsResource:
    """Tests for the async Steps resource."""

    @pytest.mark.asyncio
    @respx.mock
    async def test_list_steps(self, async_client, sample_card, sample_step):
        """Test listing steps asynchronously."""
        card_with_steps = {**sample_card, "steps": [sample_step]}
        respx.get("https://app.fizzy.do/123456/cards/42").mock(
            return_value=Response(200, json=card_with_steps)
        )

        steps = await async_client.steps.list(42)

        assert len(steps) == 1

    @pytest.mark.asyncio
    @respx.mock
    async def test_create_step(self, async_client, sample_step):
        """Test creating a step asynchronously."""
        respx.post("https://app.fizzy.do/123456/cards/42/steps").mock(
            return_value=Response(201, json=sample_step)
        )

        step = await async_client.steps.create(42, content="Test step")

        assert step.content == "Test step"

    @pytest.mark.asyncio
    @respx.mock
    async def test_update_step(self, async_client, sample_step):
        """Test updating a step asynchronously."""
        completed = {**sample_step, "completed": True}
        respx.put("https://app.fizzy.do/123456/cards/42/steps/step123").mock(
            return_value=Response(200, json=completed)
        )

        step = await async_client.steps.update(42, "step123", completed=True)

        assert step.completed is True
