"""Board model for the Fizzy API."""

from datetime import datetime

from pydantic import BaseModel


class BoardCreator(BaseModel):
    """Represents the creator of a board."""

    id: str
    name: str
    url: str | None = None


class Board(BaseModel):
    """Represents a Fizzy board."""

    id: str
    name: str
    public_description: str | None = None
    all_access: bool | None = None
    auto_postpone_period: int | None = None
    position: int | None = None
    cards_count: int | None = None
    url: str | None = None
    creator: BoardCreator | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
