"""Tests for the Boards resource."""

import pytest
import respx
from httpx import Response

from fizzy import NotFoundError
from fizzy.models.board import Board


class TestBoardsResource:
    """Tests for the sync Boards resource."""

    @respx.mock
    def test_list_boards(self, client, sample_board):
        """Test listing boards."""
        respx.get("https://app.fizzy.do/123456/boards").mock(
            return_value=Response(200, json=[sample_board])
        )

        boards = client.boards.list()

        assert len(boards) == 1
        assert boards[0].id == "abc123"
        assert boards[0].name == "Test Board"
        assert isinstance(boards[0], Board)

    @respx.mock
    def test_get_board(self, client, sample_board):
        """Test getting a specific board."""
        respx.get("https://app.fizzy.do/123456/boards/abc123").mock(
            return_value=Response(200, json=sample_board)
        )

        board = client.boards.get("abc123")

        assert board.id == "abc123"
        assert board.name == "Test Board"
        assert board.public_description == "<p>A test board</p>"

    @respx.mock
    def test_get_board_not_found(self, client):
        """Test getting a non-existent board."""
        respx.get("https://app.fizzy.do/123456/boards/nonexistent").mock(
            return_value=Response(404, json={"error": "Board not found"})
        )

        with pytest.raises(NotFoundError) as exc_info:
            client.boards.get("nonexistent")

        assert exc_info.value.status_code == 404

    @respx.mock
    def test_create_board(self, client, sample_board):
        """Test creating a board."""
        respx.post("https://app.fizzy.do/123456/boards").mock(
            return_value=Response(201, json=sample_board)
        )

        board = client.boards.create(name="Test Board", public_description="<p>A test board</p>")

        assert board.name == "Test Board"
        assert board.id == "abc123"

    @respx.mock
    def test_create_board_with_location_header(self, client, sample_board):
        """Test creating a board when API returns 201 with Location header."""
        # First request returns 201 with empty body and Location header
        respx.post("https://app.fizzy.do/123456/boards").mock(
            return_value=Response(
                201,
                headers={"Location": "https://app.fizzy.do/123456/boards/abc123.json"},
            )
        )
        # Follow-up GET to the Location
        respx.get("https://app.fizzy.do/123456/boards/abc123").mock(
            return_value=Response(200, json=sample_board)
        )

        board = client.boards.create(name="Test Board")

        assert board.name == "Test Board"

    @respx.mock
    def test_update_board(self, client, sample_board):
        """Test updating a board."""
        # PUT returns 204, then we GET the updated board
        respx.put("https://app.fizzy.do/123456/boards/abc123").mock(return_value=Response(204))
        updated_board = {**sample_board, "name": "Updated Board"}
        respx.get("https://app.fizzy.do/123456/boards/abc123").mock(
            return_value=Response(200, json=updated_board)
        )

        board = client.boards.update("abc123", name="Updated Board")

        assert board.name == "Updated Board"

    @respx.mock
    def test_delete_board(self, client):
        """Test deleting a board."""
        respx.delete("https://app.fizzy.do/123456/boards/abc123").mock(return_value=Response(204))

        # Should not raise
        client.boards.delete("abc123")


class TestAsyncBoardsResource:
    """Tests for the async Boards resource."""

    @pytest.mark.asyncio
    @respx.mock
    async def test_list_boards(self, async_client, sample_board):
        """Test listing boards asynchronously."""
        respx.get("https://app.fizzy.do/123456/boards").mock(
            return_value=Response(200, json=[sample_board])
        )

        boards = await async_client.boards.list()

        assert len(boards) == 1
        assert boards[0].name == "Test Board"

    @pytest.mark.asyncio
    @respx.mock
    async def test_get_board(self, async_client, sample_board):
        """Test getting a board asynchronously."""
        respx.get("https://app.fizzy.do/123456/boards/abc123").mock(
            return_value=Response(200, json=sample_board)
        )

        board = await async_client.boards.get("abc123")

        assert board.id == "abc123"
        assert board.name == "Test Board"

    @pytest.mark.asyncio
    @respx.mock
    async def test_create_board(self, async_client, sample_board):
        """Test creating a board asynchronously."""
        respx.post("https://app.fizzy.do/123456/boards").mock(
            return_value=Response(201, json=sample_board)
        )

        board = await async_client.boards.create(name="Test Board")

        assert board.name == "Test Board"

    @pytest.mark.asyncio
    @respx.mock
    async def test_delete_board(self, async_client):
        """Test deleting a board asynchronously."""
        respx.delete("https://app.fizzy.do/123456/boards/abc123").mock(return_value=Response(204))

        await async_client.boards.delete("abc123")
