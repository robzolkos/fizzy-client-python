"""Reaction model for the Fizzy API."""

from datetime import datetime

from pydantic import BaseModel


class ReactionUser(BaseModel):
    """Represents the user who created the reaction."""

    id: str
    name: str
    url: str | None = None


class Reaction(BaseModel):
    """Represents a reaction on a comment."""

    id: str
    content: str
    comment_id: str | None = None
    user: ReactionUser | None = None
    user_id: str | None = None
    created_at: datetime | None = None
