"""Card model for the Fizzy API."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel

if TYPE_CHECKING:
    pass


class CardCreator(BaseModel):
    """Represents the creator of a card."""

    id: str
    name: str
    url: str | None = None


class CardAssignee(BaseModel):
    """Represents an assignee on a card."""

    id: str
    name: str
    url: str | None = None


class CardTag(BaseModel):
    """Represents a tag on a card."""

    id: str
    name: str
    color: str | None = None


class CardColumn(BaseModel):
    """Represents the column a card belongs to."""

    id: str
    name: str


class CardBoard(BaseModel):
    """Represents the board a card belongs to."""

    id: str
    name: str
    url: str | None = None


class CardStep(BaseModel):
    """Represents a step embedded in a card response."""

    id: str
    content: str
    completed: bool
    position: int | None = None
    completed_at: datetime | None = None


class Card(BaseModel):
    """Represents a Fizzy card."""

    id: str
    number: int
    title: str
    description: str | None = None
    status: str
    golden: bool | None = None
    position: int | None = None
    steps_count: int | None = None
    completed_steps_count: int | None = None
    comments_count: int | None = None
    deferred_until: datetime | str | None = None
    url: str | None = None
    image_url: str | None = None
    board: CardBoard | None = None
    board_id: str | None = None
    column: CardColumn | None = None
    column_id: str | None = None
    creator: CardCreator | None = None
    creator_id: str | None = None
    assignees: list[CardAssignee] = []
    assignee_ids: list[str] = []
    tags: list[CardTag] = []
    tag_ids: list[str] = []
    steps: list[CardStep] = []
    created_at: datetime | None = None
    updated_at: datetime | None = None
    closed_at: datetime | None = None
