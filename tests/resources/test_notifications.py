"""Tests for the Notifications resource."""

import pytest
import respx
from httpx import Response

from fizzy import Notification


class TestNotificationsResource:
    """Tests for the sync Notifications resource."""

    @respx.mock
    def test_list_notifications(self, client, sample_notification):
        """Test listing notifications."""
        respx.get("https://app.fizzy.do/123456/notifications").mock(
            return_value=Response(200, json=[sample_notification])
        )

        notifications = client.notifications.list()

        assert len(notifications) == 1
        assert notifications[0].kind == "card_assigned"
        assert notifications[0].read is False
        assert isinstance(notifications[0], Notification)

    @respx.mock
    def test_list_notifications_filtered(self, client, sample_notification):
        """Test listing notifications with read filter."""
        respx.get("https://app.fizzy.do/123456/notifications").mock(
            return_value=Response(200, json=[sample_notification])
        )

        notifications = client.notifications.list(read=False)

        assert len(notifications) == 1

    @respx.mock
    def test_mark_read(self, client, sample_notification):
        """Test marking a notification as read."""
        read = {**sample_notification, "read": True}
        respx.post("https://app.fizzy.do/123456/notifications/notif123/read").mock(
            return_value=Response(200, json=read)
        )

        notification = client.notifications.mark_read("notif123")

        assert notification.read is True

    @respx.mock
    def test_mark_unread(self, client, sample_notification):
        """Test marking a notification as unread."""
        respx.post("https://app.fizzy.do/123456/notifications/notif123/unread").mock(
            return_value=Response(200, json=sample_notification)
        )

        notification = client.notifications.mark_unread("notif123")

        assert notification.read is False

    @respx.mock
    def test_bulk_mark_read(self, client, sample_notification):
        """Test marking multiple notifications as read."""
        read1 = {**sample_notification, "id": "notif123", "read": True}
        read2 = {**sample_notification, "id": "notif456", "read": True}
        respx.post("https://app.fizzy.do/123456/notifications/read").mock(
            return_value=Response(200, json=[read1, read2])
        )

        notifications = client.notifications.bulk_mark_read(["notif123", "notif456"])

        assert len(notifications) == 2
        assert all(n.read for n in notifications)


class TestAsyncNotificationsResource:
    """Tests for the async Notifications resource."""

    @pytest.mark.asyncio
    @respx.mock
    async def test_list_notifications(self, async_client, sample_notification):
        """Test listing notifications asynchronously."""
        respx.get("https://app.fizzy.do/123456/notifications").mock(
            return_value=Response(200, json=[sample_notification])
        )

        notifications = await async_client.notifications.list()

        assert len(notifications) == 1

    @pytest.mark.asyncio
    @respx.mock
    async def test_mark_read(self, async_client, sample_notification):
        """Test marking a notification as read asynchronously."""
        read = {**sample_notification, "read": True}
        respx.post("https://app.fizzy.do/123456/notifications/notif123/read").mock(
            return_value=Response(200, json=read)
        )

        notification = await async_client.notifications.mark_read("notif123")

        assert notification.read is True
