"""Tests for the Comments resource."""

import pytest
import respx
from httpx import Response

from fizzy import Comment


class TestCommentsResource:
    """Tests for the sync Comments resource."""

    @respx.mock
    def test_list_comments(self, client, sample_comment):
        """Test listing comments on a card."""
        respx.get("https://app.fizzy.do/123456/cards/42/comments").mock(
            return_value=Response(200, json=[sample_comment])
        )

        comments = client.comments.list(42)

        assert len(comments) == 1
        assert comments[0].body.plain_text == "Test comment"
        assert comments[0].body.html == "<p>Test comment</p>"
        assert isinstance(comments[0], Comment)

    @respx.mock
    def test_get_comment(self, client, sample_comment):
        """Test getting a specific comment."""
        respx.get("https://app.fizzy.do/123456/cards/42/comments/comment123").mock(
            return_value=Response(200, json=sample_comment)
        )

        comment = client.comments.get(42, "comment123")

        assert comment.id == "comment123"
        assert comment.body.plain_text == "Test comment"

    @respx.mock
    def test_create_comment(self, client, sample_comment):
        """Test creating a comment."""
        respx.post("https://app.fizzy.do/123456/cards/42/comments").mock(
            return_value=Response(201, json=sample_comment)
        )

        # The resource method parameter is 'body' not 'content'
        comment = client.comments.create(42, body="<p>Test comment</p>")

        assert comment.body.html == "<p>Test comment</p>"

    @respx.mock
    def test_create_comment_with_location_header(self, client, sample_comment):
        """Test creating a comment when API returns 201 with Location header."""
        respx.post("https://app.fizzy.do/123456/cards/42/comments").mock(
            return_value=Response(
                201,
                headers={
                    "Location": "https://app.fizzy.do/123456/cards/42/comments/comment123.json"
                },
            )
        )
        respx.get("https://app.fizzy.do/123456/cards/42/comments/comment123").mock(
            return_value=Response(200, json=sample_comment)
        )

        comment = client.comments.create(42, body="<p>Test comment</p>")

        assert comment.id == "comment123"

    @respx.mock
    def test_update_comment(self, client, sample_comment):
        """Test updating a comment."""
        updated = {
            **sample_comment,
            "body": {"plain_text": "Updated comment", "html": "<p>Updated comment</p>"},
        }
        # PUT returns 204, then we GET the updated comment
        respx.put("https://app.fizzy.do/123456/cards/42/comments/comment123").mock(
            return_value=Response(204)
        )
        respx.get("https://app.fizzy.do/123456/cards/42/comments/comment123").mock(
            return_value=Response(200, json=updated)
        )

        comment = client.comments.update(42, "comment123", body="<p>Updated comment</p>")

        assert comment.body.html == "<p>Updated comment</p>"

    @respx.mock
    def test_delete_comment(self, client):
        """Test deleting a comment."""
        respx.delete("https://app.fizzy.do/123456/cards/42/comments/comment123").mock(
            return_value=Response(204)
        )

        client.comments.delete(42, "comment123")


class TestAsyncCommentsResource:
    """Tests for the async Comments resource."""

    @pytest.mark.asyncio
    @respx.mock
    async def test_list_comments(self, async_client, sample_comment):
        """Test listing comments asynchronously."""
        respx.get("https://app.fizzy.do/123456/cards/42/comments").mock(
            return_value=Response(200, json=[sample_comment])
        )

        comments = await async_client.comments.list(42)

        assert len(comments) == 1

    @pytest.mark.asyncio
    @respx.mock
    async def test_create_comment(self, async_client, sample_comment):
        """Test creating a comment asynchronously."""
        respx.post("https://app.fizzy.do/123456/cards/42/comments").mock(
            return_value=Response(201, json=sample_comment)
        )

        comment = await async_client.comments.create(42, body="<p>Test</p>")

        assert comment.id == "comment123"
