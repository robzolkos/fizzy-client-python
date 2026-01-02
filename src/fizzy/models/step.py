"""Step model for the Fizzy API."""

from datetime import datetime

from pydantic import BaseModel


class StepCompletedBy(BaseModel):
    """Represents the user who completed the step."""

    id: str
    name: str
    url: str | None = None


class Step(BaseModel):
    """Represents a step (checklist item) on a Fizzy card."""

    id: str
    content: str
    completed: bool
    position: int | None = None
    card_id: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    completed_at: datetime | None = None
    completed_by: StepCompletedBy | None = None
    completed_by_id: str | None = None
