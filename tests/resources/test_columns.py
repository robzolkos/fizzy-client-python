"""Tests for the Columns resource."""

import pytest
import respx
from httpx import Response

from fizzy import Column


class TestColumnsResource:
    """Tests for the sync Columns resource."""

    @respx.mock
    def test_list_columns(self, client, sample_column):
        """Test listing columns on a board."""
        respx.get("https://app.fizzy.do/123456/boards/board123/columns").mock(
            return_value=Response(200, json=[sample_column])
        )

        columns = client.columns.list("board123")

        assert len(columns) == 1
        assert columns[0].name == "To Do"
        assert isinstance(columns[0], Column)

    @respx.mock
    def test_get_column(self, client, sample_column):
        """Test getting a specific column."""
        respx.get("https://app.fizzy.do/123456/boards/board123/columns/col123").mock(
            return_value=Response(200, json=sample_column)
        )

        column = client.columns.get("board123", "col123")

        assert column.id == "col123"
        assert column.name == "To Do"

    @respx.mock
    def test_create_column(self, client, sample_column):
        """Test creating a column."""
        respx.post("https://app.fizzy.do/123456/boards/board123/columns").mock(
            return_value=Response(201, json=sample_column)
        )

        column = client.columns.create("board123", name="To Do")

        assert column.name == "To Do"

    @respx.mock
    def test_create_column_with_location_header(self, client, sample_column):
        """Test creating a column when API returns 201 with Location header."""
        respx.post("https://app.fizzy.do/123456/boards/board123/columns").mock(
            return_value=Response(
                201,
                headers={
                    "Location": "https://app.fizzy.do/123456/boards/board123/columns/col123.json"
                },
            )
        )
        respx.get("https://app.fizzy.do/123456/boards/board123/columns/col123").mock(
            return_value=Response(200, json=sample_column)
        )

        column = client.columns.create("board123", name="To Do")

        assert column.name == "To Do"

    @respx.mock
    def test_update_column(self, client, sample_column):
        """Test updating a column."""
        # PUT returns 204, then we GET the updated column
        respx.put("https://app.fizzy.do/123456/boards/board123/columns/col123").mock(
            return_value=Response(204)
        )
        updated = {**sample_column, "name": "In Progress"}
        respx.get("https://app.fizzy.do/123456/boards/board123/columns/col123").mock(
            return_value=Response(200, json=updated)
        )

        column = client.columns.update("board123", "col123", name="In Progress")

        assert column.name == "In Progress"

    @respx.mock
    def test_delete_column(self, client):
        """Test deleting a column."""
        respx.delete("https://app.fizzy.do/123456/boards/board123/columns/col123").mock(
            return_value=Response(204)
        )

        client.columns.delete("board123", "col123")


class TestAsyncColumnsResource:
    """Tests for the async Columns resource."""

    @pytest.mark.asyncio
    @respx.mock
    async def test_list_columns(self, async_client, sample_column):
        """Test listing columns asynchronously."""
        respx.get("https://app.fizzy.do/123456/boards/board123/columns").mock(
            return_value=Response(200, json=[sample_column])
        )

        columns = await async_client.columns.list("board123")

        assert len(columns) == 1

    @pytest.mark.asyncio
    @respx.mock
    async def test_create_column(self, async_client, sample_column):
        """Test creating a column asynchronously."""
        respx.post("https://app.fizzy.do/123456/boards/board123/columns").mock(
            return_value=Response(201, json=sample_column)
        )

        column = await async_client.columns.create("board123", name="To Do")

        assert column.name == "To Do"
