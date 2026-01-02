"""Tag model for the Fizzy API."""

from pydantic import BaseModel, Field


class Tag(BaseModel):
    """Represents a tag in Fizzy."""

    id: str
    name: str | None = Field(default=None, alias="title")
    color: str | None = None

    model_config = {"populate_by_name": True}
