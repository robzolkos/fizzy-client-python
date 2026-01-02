"""Pytest fixtures for the Fizzy API client tests."""

import pytest
import respx

from fizzy import AsyncFizzyClient, FizzyClient


@pytest.fixture
def client():
    """Create a sync Fizzy client for testing."""
    return FizzyClient(
        token="test-token",
        account_slug="123456",
        cache=False,
    )


@pytest.fixture
async def async_client():
    """Create an async Fizzy client for testing."""
    client = AsyncFizzyClient(
        token="test-token",
        account_slug="123456",
        cache=False,
    )
    yield client
    await client.close()


@pytest.fixture
def mock_api():
    """Create a respx mock for API requests."""
    with respx.mock(base_url="https://app.fizzy.do") as respx_mock:
        yield respx_mock


# Sample fixtures for common API responses
@pytest.fixture
def sample_board():
    """Sample board data matching actual API response."""
    return {
        "id": "abc123",
        "name": "Test Board",
        "public_description": "<p>A test board</p>",
        "position": 1,
        "cards_count": 10,
        "all_access": True,
        "auto_postpone_period": 7,
        "url": "https://app.fizzy.do/123456/boards/abc123",
        "created_at": "2025-01-01T00:00:00Z",
        "updated_at": "2025-01-01T00:00:00Z",
    }


@pytest.fixture
def sample_card():
    """Sample card data matching actual API response."""
    return {
        "id": "card123",
        "number": 42,
        "title": "Test Card",
        "description": "<p>Test description</p>",
        "status": "open",
        "golden": False,
        "position": 1,
        "steps_count": 3,
        "completed_steps_count": 1,
        "comments_count": 5,
        "deferred_until": None,
        "url": "https://app.fizzy.do/123456/cards/42",
        "image_url": None,
        "board": {"id": "board123", "name": "Test Board"},
        "board_id": "board123",
        "column": {"id": "col123", "name": "To Do"},
        "column_id": "col123",
        "creator": {"id": "user123", "name": "Test User"},
        "creator_id": "user123",
        "assignees": [{"id": "user123", "name": "Test User"}],
        "assignee_ids": ["user123"],
        "tags": [{"id": "tag123", "name": "Bug", "color": "#ff0000"}],
        "tag_ids": ["tag123"],
        "steps": [],
        "created_at": "2025-01-01T00:00:00Z",
        "updated_at": "2025-01-01T00:00:00Z",
        "closed_at": None,
    }


@pytest.fixture
def sample_comment():
    """Sample comment data matching actual API response."""
    return {
        "id": "comment123",
        "body": {
            "plain_text": "Test comment",
            "html": "<p>Test comment</p>",
        },
        "card": {"id": "card123"},
        "card_id": "card123",
        "creator": {"id": "user123", "name": "Test User"},
        "creator_id": "user123",
        "reactions_count": 2,
        "reactions_url": "https://app.fizzy.do/123456/cards/42/comments/comment123/reactions",
        "url": "https://app.fizzy.do/123456/cards/42/comments/comment123",
        "created_at": "2025-01-01T00:00:00Z",
        "updated_at": "2025-01-01T00:00:00Z",
    }


@pytest.fixture
def sample_reaction():
    """Sample reaction data matching actual API response."""
    return {
        "id": "reaction123",
        "content": "thumbs_up",
        "comment_id": "comment123",
        "user": {"id": "user123", "name": "Test User"},
        "user_id": "user123",
        "created_at": "2025-01-01T00:00:00Z",
    }


@pytest.fixture
def sample_step():
    """Sample step data matching actual API response."""
    return {
        "id": "step123",
        "content": "Test step",
        "completed": False,
        "position": 1,
        "completed_at": None,
        "created_at": "2025-01-01T00:00:00Z",
        "updated_at": "2025-01-01T00:00:00Z",
    }


@pytest.fixture
def sample_tag():
    """Sample tag data matching actual API response."""
    return {
        "id": "tag123",
        "title": "Bug",
        "color": "#ff0000",
    }


@pytest.fixture
def sample_column():
    """Sample column data matching actual API response."""
    return {
        "id": "col123",
        "name": "To Do",
        "color": "#0000ff",
        "position": 1,
        "cards_count": 5,
        "url": "https://app.fizzy.do/123456/boards/board123/columns/col123",
        "created_at": "2025-01-01T00:00:00Z",
        "updated_at": "2025-01-01T00:00:00Z",
    }


@pytest.fixture
def sample_user():
    """Sample user data matching actual API response."""
    return {
        "id": "user123",
        "name": "Test User",
        "email_address": "test@example.com",
        "role": "member",
        "active": True,
        "avatar_url": "https://example.com/avatar.jpg",
        "url": "https://app.fizzy.do/123456/users/user123",
        "created_at": "2025-01-01T00:00:00Z",
        "updated_at": "2025-01-01T00:00:00Z",
    }


@pytest.fixture
def sample_notification():
    """Sample notification data matching actual API response."""
    return {
        "id": "notif123",
        "kind": "card_assigned",
        "read": False,
        "card": {"id": "card123", "number": 42, "title": "Test Card"},
        "card_id": "card123",
        "comment_id": None,
        "actor": {"id": "user456", "name": "Other User"},
        "actor_id": "user456",
        "url": "https://app.fizzy.do/123456/notifications/notif123",
        "created_at": "2025-01-01T00:00:00Z",
    }


@pytest.fixture
def sample_identity():
    """Sample identity data matching actual API response."""
    return {
        "accounts": [
            {
                "id": "acc123",
                "name": "Test Account",
                "url": "https://app.fizzy.do/123456",
                "user": {
                    "id": "user123",
                    "name": "Test User",
                    "role": "admin",
                    "active": True,
                    "email_address": "test@example.com",
                },
            },
            {
                "id": "acc456",
                "name": "Other Account",
                "url": "https://app.fizzy.do/789012",
                "user": {
                    "id": "user123",
                    "name": "Test User",
                    "role": "member",
                    "active": True,
                    "email_address": "test@example.com",
                },
            },
        ],
    }


@pytest.fixture
def sample_direct_upload():
    """Sample direct upload data matching actual API response."""
    return {
        "id": "upload123",
        "key": "uploads/abc123",
        "filename": "test.png",
        "content_type": "image/png",
        "byte_size": 12345,
        "checksum": "abc123==",
        "signed_id": "eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaHBBZ0...",
        "direct_upload": {
            "url": "https://storage.example.com/upload",
            "headers": {
                "Content-Type": "image/png",
                "Content-MD5": "abc123==",
            },
        },
    }
