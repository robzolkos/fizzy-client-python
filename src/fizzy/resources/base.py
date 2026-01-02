"""Base resource class for the Fizzy API."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Generic, TypeVar

from pydantic import BaseModel

if TYPE_CHECKING:
    from fizzy.utils.http import AsyncHTTPClient, HTTPClient

T = TypeVar("T", bound=BaseModel)


class BaseResource(Generic[T]):
    """Base class for API resources."""

    def __init__(self, http_client: HTTPClient) -> None:
        self._http = http_client

    def _parse_model(self, data: dict[str, Any], model_class: type[T]) -> T:
        """Parse API response data into a Pydantic model."""
        return model_class.model_validate(data)

    def _parse_list(self, data: list[dict[str, Any]], model_class: type[T]) -> list[T]:
        """Parse a list of API response data into Pydantic models."""
        return [model_class.model_validate(item) for item in data]


class AsyncBaseResource(Generic[T]):
    """Base class for async API resources."""

    def __init__(self, http_client: AsyncHTTPClient) -> None:
        self._http = http_client

    def _parse_model(self, data: dict[str, Any], model_class: type[T]) -> T:
        """Parse API response data into a Pydantic model."""
        return model_class.model_validate(data)

    def _parse_list(self, data: list[dict[str, Any]], model_class: type[T]) -> list[T]:
        """Parse a list of API response data into Pydantic models."""
        return [model_class.model_validate(item) for item in data]
