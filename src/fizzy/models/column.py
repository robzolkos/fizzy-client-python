"""Column model for the Fizzy API."""

from datetime import datetime

from pydantic import BaseModel


class Column(BaseModel):
    """Represents a column on a Fizzy board."""

    id: str
    name: str
    position: int | None = None
    board_id: str | None = None
    cards_count: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
