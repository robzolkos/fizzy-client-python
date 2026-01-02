"""User model for the Fizzy API."""

from datetime import datetime

from pydantic import BaseModel


class User(BaseModel):
    """Represents a user in a Fizzy account."""

    id: str
    name: str
    role: str | None = None
    active: bool | None = None
    email_address: str | None = None
    avatar_url: str | None = None
    url: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
