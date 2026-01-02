"""Tests for the Cards resource."""

import pytest
import respx
from httpx import Response

from fizzy import Card


class TestCardsResource:
    """Tests for the sync Cards resource."""

    @respx.mock
    def test_list_cards(self, client, sample_card):
        """Test listing cards."""
        respx.get("https://app.fizzy.do/123456/cards").mock(
            return_value=Response(200, json=[sample_card])
        )

        cards = client.cards.list()

        assert len(cards) == 1
        assert cards[0].number == 42
        assert cards[0].title == "Test Card"
        assert isinstance(cards[0], Card)

    @respx.mock
    def test_list_cards_with_filters(self, client, sample_card):
        """Test listing cards with filters."""
        respx.get("https://app.fizzy.do/123456/cards").mock(
            return_value=Response(200, json=[sample_card])
        )

        cards = client.cards.list(board_id="board123", status="open", tag_ids=["tag123"])

        assert len(cards) == 1

    @respx.mock
    def test_get_card(self, client, sample_card):
        """Test getting a specific card."""
        respx.get("https://app.fizzy.do/123456/cards/42").mock(
            return_value=Response(200, json=sample_card)
        )

        card = client.cards.get(42)

        assert card.number == 42
        assert card.title == "Test Card"
        assert card.status == "open"
        assert card.assignee_ids == ["user123"]

    @respx.mock
    def test_create_card(self, client, sample_card):
        """Test creating a card."""
        # Card creation goes to /boards/{board_id}/cards
        respx.post("https://app.fizzy.do/123456/boards/board123/cards").mock(
            return_value=Response(201, json=sample_card)
        )

        card = client.cards.create(
            board_id="board123",
            title="Test Card",
            description="<p>Test description</p>",
        )

        assert card.title == "Test Card"

    @respx.mock
    def test_create_card_with_location_header(self, client, sample_card):
        """Test creating a card when API returns 201 with Location header."""
        respx.post("https://app.fizzy.do/123456/boards/board123/cards").mock(
            return_value=Response(
                201,
                headers={"Location": "https://app.fizzy.do/123456/cards/42.json"},
            )
        )
        respx.get("https://app.fizzy.do/123456/cards/42").mock(
            return_value=Response(200, json=sample_card)
        )

        card = client.cards.create(board_id="board123", title="Test Card")

        assert card.title == "Test Card"

    @respx.mock
    def test_update_card(self, client, sample_card):
        """Test updating a card."""
        updated = {**sample_card, "title": "Updated Card"}
        # PUT returns the updated card
        respx.put("https://app.fizzy.do/123456/cards/42").mock(
            return_value=Response(200, json=updated)
        )

        card = client.cards.update(42, title="Updated Card")

        assert card.title == "Updated Card"

    @respx.mock
    def test_delete_card(self, client):
        """Test deleting a card."""
        respx.delete("https://app.fizzy.do/123456/cards/42").mock(return_value=Response(204))

        client.cards.delete(42)

    @respx.mock
    def test_close_card(self, client, sample_card):
        """Test closing a card."""
        closed = {**sample_card, "status": "closed", "closed_at": "2025-01-02T00:00:00Z"}
        # Actual endpoint is /cards/{number}/closure
        respx.post("https://app.fizzy.do/123456/cards/42/closure").mock(
            return_value=Response(200, json=closed)
        )

        card = client.cards.close(42)

        assert card.status == "closed"

    @respx.mock
    def test_reopen_card(self, client):
        """Test reopening a card."""
        # Reopen uses DELETE /cards/{number}/closure
        respx.delete("https://app.fizzy.do/123456/cards/42/closure").mock(
            return_value=Response(204)
        )

        result = client.cards.reopen(42)

        # reopen() returns None per the implementation
        assert result is None

    @respx.mock
    def test_postpone_card(self, client, sample_card):
        """Test postponing a card (moving to 'not now')."""
        postponed = {**sample_card, "status": "deferred", "deferred_until": "2025-02-01"}
        # Actual endpoint is /cards/{number}/not_now
        respx.post("https://app.fizzy.do/123456/cards/42/not_now").mock(
            return_value=Response(200, json=postponed)
        )

        card = client.cards.postpone(42)

        assert card.status == "deferred"

    @respx.mock
    def test_toggle_tag(self, client, sample_card):
        """Test toggling a tag on a card."""
        tagged = {**sample_card, "tag_ids": ["tag123", "tag456"]}
        # Actual endpoint is /cards/{number}/taggings
        respx.post("https://app.fizzy.do/123456/cards/42/taggings").mock(
            return_value=Response(200, json=tagged)
        )

        card = client.cards.toggle_tag(42, tag_title="NewTag")

        assert "tag456" in card.tag_ids

    @respx.mock
    def test_toggle_assignment(self, client, sample_card):
        """Test toggling assignment of a user to a card."""
        assigned = {**sample_card, "assignee_ids": ["user123", "user456"]}
        # Actual endpoint is /cards/{number}/assignments
        respx.post("https://app.fizzy.do/123456/cards/42/assignments").mock(
            return_value=Response(200, json=assigned)
        )

        card = client.cards.toggle_assignment(42, assignee_id="user456")

        assert "user456" in card.assignee_ids

    @respx.mock
    def test_watch_card(self, client, sample_card):
        """Test watching a card."""
        respx.post("https://app.fizzy.do/123456/cards/42/watch").mock(
            return_value=Response(200, json=sample_card)
        )

        card = client.cards.watch(42)

        assert card.number == 42

    @respx.mock
    def test_triage_card(self, client, sample_card):
        """Test triaging a card to a column."""
        respx.post("https://app.fizzy.do/123456/cards/42/triage").mock(
            return_value=Response(200, json=sample_card)
        )

        card = client.cards.triage(42, column_id="col123")

        assert card.number == 42

    @respx.mock
    def test_gild_card(self, client, sample_card):
        """Test making a card a golden ticket."""
        gilded = {**sample_card, "golden": True}
        respx.post("https://app.fizzy.do/123456/cards/42/goldness").mock(
            return_value=Response(200, json=gilded)
        )

        card = client.cards.gild(42)

        assert card.golden is True


class TestAsyncCardsResource:
    """Tests for the async Cards resource."""

    @pytest.mark.asyncio
    @respx.mock
    async def test_list_cards(self, async_client, sample_card):
        """Test listing cards asynchronously."""
        respx.get("https://app.fizzy.do/123456/cards").mock(
            return_value=Response(200, json=[sample_card])
        )

        cards = await async_client.cards.list()

        assert len(cards) == 1
        assert cards[0].title == "Test Card"

    @pytest.mark.asyncio
    @respx.mock
    async def test_get_card(self, async_client, sample_card):
        """Test getting a card asynchronously."""
        respx.get("https://app.fizzy.do/123456/cards/42").mock(
            return_value=Response(200, json=sample_card)
        )

        card = await async_client.cards.get(42)

        assert card.number == 42

    @pytest.mark.asyncio
    @respx.mock
    async def test_create_card(self, async_client, sample_card):
        """Test creating a card asynchronously."""
        respx.post("https://app.fizzy.do/123456/boards/board123/cards").mock(
            return_value=Response(201, json=sample_card)
        )

        card = await async_client.cards.create(board_id="board123", title="Test Card")

        assert card.title == "Test Card"

    @pytest.mark.asyncio
    @respx.mock
    async def test_close_card(self, async_client, sample_card):
        """Test closing a card asynchronously."""
        closed = {**sample_card, "status": "closed"}
        respx.post("https://app.fizzy.do/123456/cards/42/closure").mock(
            return_value=Response(200, json=closed)
        )

        card = await async_client.cards.close(42)

        assert card.status == "closed"
