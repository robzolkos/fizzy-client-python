# Fizzy API Client

Python client for the [Fizzy](https://fizzy.do) API.

[![Tests](https://github.com/robzolkos/fizzy-client-python/actions/workflows/test.yml/badge.svg)](https://github.com/robzolkos/fizzy-client-python/actions/workflows/test.yml)
[![PyPI version](https://badge.fury.io/py/fizzy-api-client.svg)](https://badge.fury.io/py/fizzy-api-client)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Installation

```bash
pip install fizzy-api-client
```

## Quick Start

```python
from fizzy import FizzyClient

client = FizzyClient(
    token="your-api-token",
    account_slug="your-account-slug"
)

# List boards
boards = client.boards.list()

# Create a card
card = client.cards.create(
    board_id="board-123",
    title="My new card"
)

# List cards with filtering
cards = client.cards.list(
    board_id="board-123",
    tag_ids=["tag-1", "tag-2"],
    status="open"
)
```

## Authentication

### Personal Access Token

The recommended authentication method for scripts and integrations:

```python
from fizzy import FizzyClient

client = FizzyClient(
    token="your-personal-access-token",
    account_slug="your-account-slug"
)
```

### Magic Link Session

For native applications that need user authentication:

```python
from fizzy import FizzyClient
from fizzy.auth import request_magic_link, submit_magic_code

# Request a magic link
request_magic_link("user@example.com")

# User receives email with 6-character code
session_token = submit_magic_code("ABC123")

# Use the session token
client = FizzyClient(
    session_token=session_token,
    account_slug="your-account-slug"
)
```

## Resources

### Identity

```python
# Get authenticated user info (list of accounts)
identity = client.identity.get()
for account in identity.accounts:
    print(f"Account: {account.name} ({account.id})")
    print(f"  User: {account.user.name} - Role: {account.user.role}")
```

### Boards

```python
# List all boards
boards = client.boards.list()

# Get a specific board
board = client.boards.get("board-id")

# Create a board
board = client.boards.create(
    name="My Board",
    public_description="<p>Optional rich text description</p>"
)

# Update a board
board = client.boards.update("board-id", name="New Name")

# Delete a board
client.boards.delete("board-id")
```

### Cards

```python
# List cards with optional filters
cards = client.cards.list(
    board_id="board-123",     # Optional: filter by board
    column_id="col-456",      # Optional: filter by column
    tag_ids=["tag-1"],        # Optional: filter by tags
    assignee_ids=["user-1"],  # Optional: filter by assignees
    status="open"             # Optional: "open", "closed", "deferred"
)

# Get a specific card by number
card = client.cards.get(42)  # Cards are accessed by number, not ID

# Create a card
card = client.cards.create(
    board_id="board-123",
    title="New Card",
    description="<p>Rich text description</p>"  # HTML supported
)

# Create a card with header image
card = client.cards.create(
    board_id="board-123",
    title="Card with Image",
    image="/path/to/image.png"  # File path or tuple (filename, file_obj, content_type)
)

# Update a card
card = client.cards.update(42, title="Updated Title")

# Update card with new header image
card = client.cards.update(42, image="/path/to/new-image.png")

# Delete card header image
client.cards.delete_image(42)

# Delete a card
client.cards.delete(42)

# Card operations
client.cards.close(42)                          # Close the card
client.cards.reopen(42)                         # Reopen a closed card
client.cards.postpone(42)                       # Move to "not now"
client.cards.triage(42, column_id="col-123")    # Move to a column
client.cards.untriage(42)                       # Remove from triage
client.cards.toggle_tag(42, tag_title="Bug")    # Toggle a tag on/off
client.cards.toggle_assignment(42, assignee_id="user-123")  # Toggle assignment
client.cards.watch(42)                          # Start watching
client.cards.unwatch(42)                        # Stop watching
client.cards.gild(42)                           # Make a "golden ticket"
client.cards.ungild(42)                         # Remove golden status
```

### Comments

```python
# List comments on a card
comments = client.comments.list(42)  # card_number

# Get a specific comment
comment = client.comments.get(42, "comment-id")

# Create a comment
comment = client.comments.create(
    42,  # card_number
    body="<p>Hello, world!</p>"  # HTML supported
)

# Update a comment
comment = client.comments.update(42, "comment-id", body="<p>Updated</p>")

# Delete a comment
client.comments.delete(42, "comment-id")
```

### Reactions

```python
# List reactions on a comment
reactions = client.reactions.list(42, "comment-id")

# Add a reaction
reaction = client.reactions.create(42, "comment-id", content="thumbs_up")

# Remove a reaction
client.reactions.delete(42, "comment-id", "reaction-id")
```

### Steps (Checklist Items)

```python
# List steps (retrieved from the card)
steps = client.steps.list(42)  # card_number

# Get a specific step
step = client.steps.get(42, "step-id")

# Create a step
step = client.steps.create(42, content="Do this thing")

# Update a step (mark complete)
client.steps.update(42, "step-id", completed=True)

# Delete a step
client.steps.delete(42, "step-id")
```

### Columns

```python
# List columns on a board
columns = client.columns.list("board-id")

# Get a specific column
column = client.columns.get("board-id", "column-id")

# Create a column
column = client.columns.create("board-id", name="In Progress")

# Update a column
column = client.columns.update("board-id", "column-id", name="Done")

# Delete a column
client.columns.delete("board-id", "column-id")
```

### Users

```python
# List users in account
users = client.users.list()

# Get a specific user
user = client.users.get("user-id")

# Update a user (name or avatar)
user = client.users.update("user-id", name="New Name")
user = client.users.update("user-id", avatar="/path/to/avatar.png")

# Deactivate a user
client.users.delete("user-id")
```

### Tags

```python
# List all tags in account
tags = client.tags.list()
```

### Notifications

```python
# List notifications
notifications = client.notifications.list()

# Filter by read status
unread = client.notifications.list(read=False)

# Mark as read
client.notifications.mark_read("notification-id")

# Mark as unread
client.notifications.mark_unread("notification-id")

# Bulk mark as read
client.notifications.bulk_mark_read(["notif-1", "notif-2", "notif-3"])
```

### File Uploads (Direct Uploads for Rich Text)

For embedding images in card descriptions or comments:

```python
import hashlib
import base64

# Calculate MD5 checksum
with open("image.png", "rb") as f:
    content = f.read()
    checksum = base64.b64encode(hashlib.md5(content).digest()).decode()

# Create a direct upload
upload = client.uploads.create_direct_upload(
    filename="image.png",
    content_type="image/png",
    byte_size=len(content),
    checksum=checksum
)

# Upload to storage using the provided URL and headers
import httpx
httpx.put(
    upload.upload_url,
    content=content,
    headers=upload.upload_headers
)

# Build an ActionText attachment tag
from fizzy import DirectUpload
tag = DirectUpload.build_attachment_tag(upload.signed_id)

# Use in card description or comment
client.cards.update(42, description=f"<p>Check this out: {tag}</p>")
client.comments.create(42, body=f"<p>Here's an image: {tag}</p>")
```

## Pagination

```python
# Auto-pagination iterator
for card in client.cards.list_all(board_id="board-123"):
    print(card.title)

# Manual pagination
page = client.cards.list_paginated(board_id="board-123")
while page.has_next:
    for card in page.items:
        print(card.title)
    page = page.next_page()
```

## Async Usage

```python
from fizzy import AsyncFizzyClient
import asyncio

async def main():
    async with AsyncFizzyClient(
        token="your-token",
        account_slug="your-account-slug"
    ) as client:
        # All methods are async
        boards = await client.boards.list()

        # Async iteration
        async for card in client.cards.list_all():
            print(card.title)

asyncio.run(main())
```

## Error Handling

```python
from fizzy.exceptions import (
    FizzyError,           # Base exception
    AuthenticationError,  # 401
    ForbiddenError,       # 403
    NotFoundError,        # 404
    BadRequestError,      # 400
    RateLimitError,       # 429
    ServerError,          # 5xx
)

try:
    card = client.cards.get(99999)
except NotFoundError as e:
    print(f"Card not found: {e.message}")
except BadRequestError as e:
    print(f"Bad request: {e.message}")
except FizzyError as e:
    print(f"API error: {e.status_code} - {e.message}")
```

## Caching

ETag caching is enabled by default for GET requests:

```python
# First request stores the ETag
card = client.cards.get(123)

# Subsequent requests use If-None-Match header
# Returns cached response if server returns 304
card = client.cards.get(123)

# Disable caching
client = FizzyClient(
    token="...",
    account_slug="...",
    cache=False
)
```

## Configuration

```python
client = FizzyClient(
    token="your-token",
    account_slug="your-account-slug",
    base_url="https://app.fizzy.do",  # Default
    cache=True,                        # Enable ETag caching (default)
    timeout=30.0,                      # Request timeout in seconds
)
```

## Development

```bash
# Clone the repository
git clone https://github.com/robzolkos/fizzy-client-python.git
cd fizzy-client-python

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run tests with coverage
pytest --cov=src/fizzy --cov-report=html

# Run linting
ruff check src tests
ruff format --check src tests

# Run type checking
mypy src
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT License - see the [LICENSE](LICENSE) file for details.

---

Fizzy is a product and trademark of [37signals](https://37signals.com).
