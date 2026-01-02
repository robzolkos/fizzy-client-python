"""Tests for the Tags resource."""

import pytest
import respx
from httpx import Response

from fizzy import Tag


class TestTagsResource:
    """Tests for the sync Tags resource."""

    @respx.mock
    def test_list_tags(self, client, sample_tag):
        """Test listing tags."""
        respx.get("https://app.fizzy.do/123456/tags").mock(
            return_value=Response(200, json=[sample_tag])
        )

        tags = client.tags.list()

        assert len(tags) == 1
        assert tags[0].name == "Bug"
        assert tags[0].color == "#ff0000"
        assert isinstance(tags[0], Tag)


class TestAsyncTagsResource:
    """Tests for the async Tags resource."""

    @pytest.mark.asyncio
    @respx.mock
    async def test_list_tags(self, async_client, sample_tag):
        """Test listing tags asynchronously."""
        respx.get("https://app.fizzy.do/123456/tags").mock(
            return_value=Response(200, json=[sample_tag])
        )

        tags = await async_client.tags.list()

        assert len(tags) == 1
        assert tags[0].name == "Bug"
