"""Tests for the Reactions resource."""

import pytest
import respx
from httpx import Response

from fizzy import Reaction


class TestReactionsResource:
    """Tests for the sync Reactions resource."""

    @respx.mock
    def test_list_reactions(self, client, sample_reaction):
        """Test listing reactions on a comment."""
        respx.get("https://app.fizzy.do/123456/cards/42/comments/comment123/reactions").mock(
            return_value=Response(200, json=[sample_reaction])
        )

        reactions = client.reactions.list(42, "comment123")

        assert len(reactions) == 1
        assert reactions[0].content == "thumbs_up"
        assert isinstance(reactions[0], Reaction)

    @respx.mock
    def test_create_reaction(self, client, sample_reaction):
        """Test creating a reaction."""
        respx.post("https://app.fizzy.do/123456/cards/42/comments/comment123/reactions").mock(
            return_value=Response(201, json=sample_reaction)
        )

        reaction = client.reactions.create(42, "comment123", content="thumbs_up")

        assert reaction.content == "thumbs_up"

    @respx.mock
    def test_create_reaction_with_location_header(self, client, sample_reaction):
        """Test creating a reaction when API returns 201 with Location header."""
        respx.post("https://app.fizzy.do/123456/cards/42/comments/comment123/reactions").mock(
            return_value=Response(
                201,
                headers={
                    "Location": "https://app.fizzy.do/123456/cards/42/comments/comment123/reactions/reaction123.json"
                },
            )
        )
        respx.get(
            "https://app.fizzy.do/123456/cards/42/comments/comment123/reactions/reaction123"
        ).mock(return_value=Response(200, json=sample_reaction))

        reaction = client.reactions.create(42, "comment123", content="thumbs_up")

        assert reaction.id == "reaction123"

    @respx.mock
    def test_delete_reaction(self, client):
        """Test deleting a reaction."""
        respx.delete(
            "https://app.fizzy.do/123456/cards/42/comments/comment123/reactions/reaction123"
        ).mock(return_value=Response(204))

        client.reactions.delete(42, "comment123", "reaction123")


class TestAsyncReactionsResource:
    """Tests for the async Reactions resource."""

    @pytest.mark.asyncio
    @respx.mock
    async def test_list_reactions(self, async_client, sample_reaction):
        """Test listing reactions asynchronously."""
        respx.get("https://app.fizzy.do/123456/cards/42/comments/comment123/reactions").mock(
            return_value=Response(200, json=[sample_reaction])
        )

        reactions = await async_client.reactions.list(42, "comment123")

        assert len(reactions) == 1

    @pytest.mark.asyncio
    @respx.mock
    async def test_create_reaction(self, async_client, sample_reaction):
        """Test creating a reaction asynchronously."""
        respx.post("https://app.fizzy.do/123456/cards/42/comments/comment123/reactions").mock(
            return_value=Response(201, json=sample_reaction)
        )

        reaction = await async_client.reactions.create(42, "comment123", content="thumbs_up")

        assert reaction.content == "thumbs_up"
