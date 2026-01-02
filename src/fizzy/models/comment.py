"""Comment model for the Fizzy API."""

from datetime import datetime

from pydantic import BaseModel


class CommentCreator(BaseModel):
    """Represents the creator of a comment."""

    id: str
    name: str
    url: str | None = None


class CommentBody(BaseModel):
    """Represents the body content of a comment."""

    plain_text: str
    html: str


class CommentCard(BaseModel):
    """Represents the card reference in a comment."""

    id: str
    url: str | None = None


class Comment(BaseModel):
    """Represents a comment on a Fizzy card."""

    id: str
    body: CommentBody | None = None
    card: CommentCard | None = None
    card_id: str | None = None
    creator: CommentCreator | None = None
    creator_id: str | None = None
    reactions_count: int | None = None
    reactions_url: str | None = None
    url: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
