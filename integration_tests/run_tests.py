#!/usr/bin/env python3
"""Integration test harness for the Fizzy API client.

This script runs integration tests against the real Fizzy API.
"""

import os
import sys
import tempfile
from datetime import datetime

# Add the src directory to the path for development
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from fizzy import FizzyClient, NotFoundError
from fizzy.models.upload import DirectUpload


def create_test_image() -> str:
    """Create a minimal valid PNG image for testing."""
    png_data = bytes([
        0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A,
        0x00, 0x00, 0x00, 0x0D, 0x49, 0x48, 0x44, 0x52,
        0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x01,
        0x08, 0x02, 0x00, 0x00, 0x00, 0x90, 0x77, 0x53,
        0xDE, 0x00, 0x00, 0x00, 0x0C, 0x49, 0x44, 0x41,
        0x54, 0x08, 0xD7, 0x63, 0xF8, 0xCF, 0xC0, 0x00,
        0x00, 0x00, 0x03, 0x00, 0x01, 0x00, 0x18, 0xDD,
        0x8D, 0xB4, 0x00, 0x00, 0x00, 0x00, 0x49, 0x45,
        0x4E, 0x44, 0xAE, 0x42, 0x60, 0x82
    ])
    fd, path = tempfile.mkstemp(suffix='.png')
    os.write(fd, png_data)
    os.close(fd)
    return path


def test_identity(client: FizzyClient) -> None:
    """Test the identity endpoint."""
    print("Testing identity...")
    identity = client.identity.get()
    # Identity returns a list of accounts the user has access to
    if identity.accounts:
        first_account = identity.accounts[0]
        user_info = first_account.user
        if user_info:
            print(f"  ✓ Authenticated as {user_info.name} ({user_info.email_address})")
        else:
            print(f"  ✓ Authenticated with account '{first_account.name}'")
    print(f"  ✓ Access to {len(identity.accounts)} accounts")


def test_boards_crud(client: FizzyClient, board_name: str) -> str:
    """Test board CRUD operations and return the created board ID."""
    print("Testing boards CRUD...")

    # List existing boards
    boards = client.boards.list()
    print(f"  ✓ Found {len(boards)} existing boards")

    # Create a test board
    board = client.boards.create(
        name=board_name,
        public_description="<p>Integration test board - will be deleted after tests</p>",
    )
    print(f"  ✓ Created board '{board.name}' (ID: {board.id})")

    # Get the board
    fetched = client.boards.get(board.id)
    assert fetched.name == board_name
    print(f"  ✓ Retrieved board '{fetched.name}'")

    # Update the board - Note: API accepts public_description but may not return it
    updated = client.boards.update(board.id, public_description="<p>Updated description</p>")
    # Just verify the update call succeeded (board was returned)
    assert updated.id == board.id
    print(f"  ✓ Updated board")

    return board.id


def test_columns_crud(client: FizzyClient, board_id: str) -> str:
    """Test column CRUD operations and return a column ID."""
    print("Testing columns CRUD...")

    # List columns (new board should have none or default)
    columns = client.columns.list(board_id)
    print(f"  ✓ Found {len(columns)} existing columns")

    # Create columns
    col1 = client.columns.create(board_id, name="To Do")
    print(f"  ✓ Created column '{col1.name}' (ID: {col1.id})")

    col2 = client.columns.create(board_id, name="In Progress")
    print(f"  ✓ Created column '{col2.name}' (ID: {col2.id})")

    col3 = client.columns.create(board_id, name="Done")
    print(f"  ✓ Created column '{col3.name}' (ID: {col3.id})")

    # Update a column
    updated = client.columns.update(board_id, col2.id, name="Working On")
    assert updated.name == "Working On"
    print(f"  ✓ Updated column name to '{updated.name}'")

    # Delete a column
    client.columns.delete(board_id, col3.id)
    print(f"  ✓ Deleted 'Done' column")

    return col1.id


def test_tags(client: FizzyClient) -> list[str]:
    """Test tags listing and return available tag IDs."""
    print("Testing tags...")
    tags = client.tags.list()
    print(f"  ✓ Found {len(tags)} tags")
    for tag in tags[:3]:  # Show first 3 tags
        print(f"    - {tag.name} (ID: {tag.id})")
    return [tag.id for tag in tags[:2]] if tags else []


def test_users(client: FizzyClient) -> list[str]:
    """Test users listing and return user IDs."""
    print("Testing users...")
    users = client.users.list()
    print(f"  ✓ Found {len(users)} users")
    for user in users[:3]:  # Show first 3 users
        print(f"    - {user.name} ({user.email_address}) - {user.role}")
    return [user.id for user in users[:2]] if users else []


def test_cards_crud(
    client: FizzyClient,
    board_id: str,
    column_id: str,
    tag_ids: list[str],
    user_ids: list[str],
) -> int:
    """Test card CRUD operations and return a card number."""
    print("Testing cards CRUD...")

    # Create a card
    card = client.cards.create(
        board_id=board_id,
        title="Test Card 1 - Basic",
        description="<p>This is a <strong>test card</strong> with rich text.</p>",
        column_id=column_id,
    )
    print(f"  ✓ Created card #{card.number}: '{card.title}'")

    # Get the card
    fetched = client.cards.get(card.number)
    assert fetched.title == "Test Card 1 - Basic"
    print(f"  ✓ Retrieved card #{card.number}")

    # Update the card
    updated = client.cards.update(
        card.number,
        title="Test Card 1 - Updated",
        description="<p>Updated description with <em>formatting</em>.</p>",
    )
    assert "Updated" in updated.title
    print(f"  ✓ Updated card title to '{updated.title}'")

    # Create more cards for testing operations
    card2 = client.cards.create(
        board_id=board_id,
        title="Test Card 2 - For Operations",
        column_id=column_id,
    )
    print(f"  ✓ Created card #{card2.number}: '{card2.title}'")

    card3 = client.cards.create(
        board_id=board_id,
        title="Test Card 3 - For Closing",
        column_id=column_id,
    )
    print(f"  ✓ Created card #{card3.number}: '{card3.title}'")

    return card.number


def test_card_operations(
    client: FizzyClient,
    card_number: int,
    column_id: str,
    tag_ids: list[str],
    user_ids: list[str],
) -> None:
    """Test card operations like close, reopen, tags, assignees."""
    print("Testing card operations...")

    # Close and reopen
    client.cards.close(card_number)
    print(f"  ✓ Closed card #{card_number}")

    client.cards.reopen(card_number)
    print(f"  ✓ Reopened card #{card_number}")

    # Postpone (not now)
    client.cards.postpone(card_number)
    print(f"  ✓ Postponed card #{card_number}")

    # Triage (bring back to a column)
    client.cards.triage(card_number, column_id=column_id)
    print(f"  ✓ Triaged card #{card_number} to column")

    # Toggle tag if available
    if tag_ids:
        client.cards.toggle_tag(card_number, tag_title="test-tag")
        print(f"  ✓ Toggled tag on card #{card_number}")

    # Toggle assignment if available
    if user_ids:
        client.cards.toggle_assignment(card_number, assignee_id=user_ids[0])
        print(f"  ✓ Toggled assignment on card #{card_number}")

    # Watch/unwatch
    client.cards.watch(card_number)
    print(f"  ✓ Started watching card #{card_number}")

    client.cards.unwatch(card_number)
    print(f"  ✓ Stopped watching card #{card_number}")

    # Gild/ungild
    client.cards.gild(card_number)
    print(f"  ✓ Gilded card #{card_number}")

    client.cards.ungild(card_number)
    print(f"  ✓ Ungilded card #{card_number}")


def test_steps_crud(client: FizzyClient, card_number: int) -> None:
    """Test step (checklist) CRUD operations."""
    print("Testing steps (checklist) CRUD...")

    # Create steps
    step1 = client.steps.create(card_number, content="Step 1: Setup environment")
    print(f"  ✓ Created step: '{step1.content}'")

    step2 = client.steps.create(card_number, content="Step 2: Write code")
    print(f"  ✓ Created step: '{step2.content}'")

    step3 = client.steps.create(card_number, content="Step 3: Run tests")
    print(f"  ✓ Created step: '{step3.content}'")

    # List steps
    steps = client.steps.list(card_number)
    print(f"  ✓ Listed {len(steps)} steps")

    # Complete a step
    completed = client.steps.update(card_number, step1.id, completed=True)
    assert completed.completed is True
    print(f"  ✓ Marked step 1 as complete")

    # Update step content
    updated = client.steps.update(
        card_number, step2.id, content="Step 2: Write awesome code"
    )
    assert "awesome" in updated.content
    print(f"  ✓ Updated step 2 content")

    # Delete a step
    client.steps.delete(card_number, step3.id)
    print(f"  ✓ Deleted step 3")


def test_comments_crud(client: FizzyClient, card_number: int) -> str:
    """Test comment CRUD operations and return a comment ID."""
    print("Testing comments CRUD...")

    # Create comments
    comment1 = client.comments.create(
        card_number,
        body="<p>This is the <strong>first</strong> comment!</p>",
    )
    print(f"  ✓ Created comment #{comment1.id}")

    comment2 = client.comments.create(
        card_number,
        body="<p>Another comment with some details:</p><ul><li>Item 1</li><li>Item 2</li></ul>",
    )
    print(f"  ✓ Created comment #{comment2.id}")

    # List comments
    comments = client.comments.list(card_number)
    print(f"  ✓ Listed {len(comments)} comments")

    # Get a comment
    fetched = client.comments.get(card_number, comment1.id)
    assert fetched.body and "first" in fetched.body.plain_text
    print(f"  ✓ Retrieved comment #{comment1.id}")

    # Update a comment
    updated = client.comments.update(
        card_number,
        comment1.id,
        body="<p>This is the <strong>updated first</strong> comment!</p>",
    )
    assert updated.body and "updated" in updated.body.plain_text
    print(f"  ✓ Updated comment #{comment1.id}")

    return comment1.id


def test_reactions_crud(client: FizzyClient, card_number: int, comment_id: str) -> None:
    """Test reaction CRUD operations."""
    print("Testing reactions CRUD...")

    # Create reactions
    reaction1 = client.reactions.create(card_number, comment_id, content="👍")
    print(f"  ✓ Added 👍 reaction")

    reaction2 = client.reactions.create(card_number, comment_id, content="🎉")
    print(f"  ✓ Added 🎉 reaction")

    # List reactions
    reactions = client.reactions.list(card_number, comment_id)
    print(f"  ✓ Listed {len(reactions)} reactions")

    # Delete a reaction
    client.reactions.delete(card_number, comment_id, reaction1.id)
    print(f"  ✓ Removed 👍 reaction")


def test_notifications(client: FizzyClient) -> None:
    """Test notification operations."""
    print("Testing notifications...")

    notifications = client.notifications.list()
    print(f"  ✓ Found {len(notifications)} notifications")

    unread = client.notifications.list(read=False)
    print(f"  ✓ Found {len(unread)} unread notifications")

    if unread:
        # Mark one as read
        marked = client.notifications.mark_read(unread[0].id)
        assert marked.read is True
        print(f"  ✓ Marked notification #{unread[0].id} as read")

        # Mark it back as unread
        unmarked = client.notifications.mark_unread(unread[0].id)
        assert unmarked.read is False
        print(f"  ✓ Marked notification #{unread[0].id} as unread")


def test_image_uploads(client: FizzyClient, board_id: str, card_number: int) -> None:
    """Test image upload functionality."""
    print("Testing image uploads...")

    test_image = create_test_image()
    try:
        # Test 1: Create card with header image
        card_with_image = client.cards.create(
            board_id=board_id,
            title="Card with Header Image",
            image=test_image
        )
        assert card_with_image.image_url is not None
        print(f"  ✓ Created card #{card_with_image.number} with header image")

        # Test 2: Update card header image
        updated = client.cards.update(card_with_image.number, image=test_image)
        assert updated.image_url is not None
        print(f"  ✓ Updated card header image")

        # Test 3: Delete card header image
        client.cards.delete_image(card_with_image.number)
        deleted = client.cards.get(card_with_image.number)
        assert deleted.image_url is None
        print(f"  ✓ Deleted card header image")

        # Test 4: Direct upload for inline image in description
        upload = client.uploads.upload_file(test_image)
        assert upload.signed_id
        print(f"  ✓ Uploaded file via direct upload")

        attachment_tag = DirectUpload.build_attachment_tag(upload.signed_id)
        description_with_image = f"<p>Inline image:</p>{attachment_tag}"
        card_with_inline = client.cards.create(
            board_id=board_id,
            title="Card with Inline Image",
            description=description_with_image
        )
        print(f"  ✓ Created card #{card_with_inline.number} with inline image in description")

        # Test 5: Comment with inline image
        upload2 = client.uploads.upload_file(test_image)
        attachment_tag2 = DirectUpload.build_attachment_tag(upload2.signed_id)
        comment_body = f"<p>Comment with image:</p>{attachment_tag2}"
        comment = client.comments.create(card_number, body=comment_body)
        print(f"  ✓ Created comment with inline image")

    finally:
        if os.path.exists(test_image):
            os.unlink(test_image)


def test_cards_list_filters(client: FizzyClient, board_id: str) -> None:
    """Test card listing with various filters."""
    print("Testing card list filters...")

    # List all cards in board
    all_cards = client.cards.list(board_id=board_id)
    print(f"  ✓ Found {len(all_cards)} cards in test board")

    # List open cards
    open_cards = client.cards.list(board_id=board_id, status="open")
    print(f"  ✓ Found {len(open_cards)} open cards")

    # Test pagination iterator (limit to first page to avoid timeout)
    count = 0
    for card in client.cards.list_all(board_id=board_id):
        count += 1
        if count >= 10:  # Limit for testing
            break
    print(f"  ✓ Iterated over {count}+ cards using list_all()")


def cleanup_board(client: FizzyClient, board_id: str) -> None:
    """Delete the test board."""
    print("Cleaning up...")
    client.boards.delete(board_id)
    print(f"  ✓ Deleted test board (ID: {board_id})")


def main():
    """Run all integration tests."""
    print("=" * 70)
    print("Fizzy API Client - Integration Tests")
    print("=" * 70)
    print()

    # Configuration
    token = os.environ.get("FIZZY_API_TOKEN", "sqjE7ZExG2kw4xrJF2CJVU1s")
    account_slug = os.environ.get("FIZZY_ACCOUNT_SLUG", "6102600")

    print(f"Account: {account_slug}")
    print()

    # Create client
    client = FizzyClient(
        token=token,
        account_slug=account_slug,
    )

    # Generate test board name with today's date
    today = datetime.now().strftime("%Y-%m-%d")
    board_name = f"test board python {today}"

    board_id = None
    passed = 0
    failed = 0

    try:
        # Test identity
        try:
            test_identity(client)
            passed += 1
        except Exception as e:
            print(f"  ✗ FAILED: {e}")
            failed += 1
            raise  # Can't continue without auth

        print()

        # Test users and tags (for later use)
        try:
            user_ids = test_users(client)
            passed += 1
        except Exception as e:
            print(f"  ✗ FAILED: {e}")
            failed += 1
            user_ids = []

        print()

        try:
            tag_ids = test_tags(client)
            passed += 1
        except Exception as e:
            print(f"  ✗ FAILED: {e}")
            failed += 1
            tag_ids = []

        print()

        # Test board CRUD
        try:
            board_id = test_boards_crud(client, board_name)
            passed += 1
        except Exception as e:
            print(f"  ✗ FAILED: {e}")
            failed += 1
            raise  # Can't continue without board

        print()

        # Test columns CRUD
        try:
            column_id = test_columns_crud(client, board_id)
            passed += 1
        except Exception as e:
            print(f"  ✗ FAILED: {e}")
            failed += 1
            column_id = None

        print()

        # Test cards CRUD
        try:
            card_number = test_cards_crud(client, board_id, column_id, tag_ids, user_ids)
            passed += 1
        except Exception as e:
            print(f"  ✗ FAILED: {e}")
            failed += 1
            card_number = None

        print()

        # Test card operations
        if card_number and column_id:
            try:
                test_card_operations(client, card_number, column_id, tag_ids, user_ids)
                passed += 1
            except Exception as e:
                print(f"  ✗ FAILED: {e}")
                failed += 1

            print()

            # Test steps
            try:
                test_steps_crud(client, card_number)
                passed += 1
            except Exception as e:
                print(f"  ✗ FAILED: {e}")
                failed += 1

            print()

            # Test comments
            try:
                comment_id = test_comments_crud(client, card_number)
                passed += 1
            except Exception as e:
                print(f"  ✗ FAILED: {e}")
                failed += 1
                comment_id = None

            print()

            # Test reactions
            if comment_id:
                try:
                    test_reactions_crud(client, card_number, comment_id)
                    passed += 1
                except Exception as e:
                    print(f"  ✗ FAILED: {e}")
                    failed += 1

                print()

            # Test image uploads
            try:
                test_image_uploads(client, board_id, card_number)
                passed += 1
            except Exception as e:
                print(f"  ✗ FAILED: {e}")
                failed += 1

            print()

        # Test card list filters
        try:
            test_cards_list_filters(client, board_id)
            passed += 1
        except Exception as e:
            print(f"  ✗ FAILED: {e}")
            failed += 1

        print()

        # Test notifications
        try:
            test_notifications(client)
            passed += 1
        except Exception as e:
            print(f"  ✗ FAILED: {e}")
            failed += 1

        print()

    finally:
        # Cleanup
        if board_id:
            try:
                cleanup_board(client, board_id)
                print()
            except Exception as e:
                print(f"  ✗ Cleanup failed: {e}")

        client.close()

    print("=" * 70)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 70)

    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
