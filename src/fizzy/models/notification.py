"""Notification model for the Fizzy API."""

from datetime import datetime

from pydantic import BaseModel


class NotificationActor(BaseModel):
    """Represents the actor who triggered the notification."""

    id: str
    name: str
    url: str | None = None


class NotificationCard(BaseModel):
    """Represents the card associated with the notification."""

    id: str
    number: int
    title: str
    url: str | None = None


class Notification(BaseModel):
    """Represents a notification in Fizzy."""

    id: str
    kind: str
    read: bool
    card: NotificationCard | None = None
    card_id: str | None = None
    card_number: int | None = None
    card_title: str | None = None
    comment_id: str | None = None
    actor: NotificationActor | None = None
    actor_id: str | None = None
    actor_name: str | None = None
    url: str | None = None
    created_at: datetime | None = None
