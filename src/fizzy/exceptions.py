"""Custom exceptions for the Fizzy API client."""

from typing import Any


class FizzyError(Exception):
    """Base exception for all Fizzy API errors."""

    def __init__(
        self,
        message: str,
        status_code: int | None = None,
        response_body: dict[str, Any] | None = None,
    ) -> None:
        self.message = message
        self.status_code = status_code
        self.response_body = response_body or {}
        super().__init__(message)

    def __str__(self) -> str:
        if self.status_code:
            return f"[{self.status_code}] {self.message}"
        return self.message


class AuthenticationError(FizzyError):
    """Raised when authentication fails (401)."""

    def __init__(
        self,
        message: str = "Authentication failed",
        response_body: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message, status_code=401, response_body=response_body)


class ForbiddenError(FizzyError):
    """Raised when access is forbidden (403)."""

    def __init__(
        self,
        message: str = "Access forbidden",
        response_body: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message, status_code=403, response_body=response_body)


class NotFoundError(FizzyError):
    """Raised when a resource is not found (404)."""

    def __init__(
        self,
        message: str = "Resource not found",
        response_body: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message, status_code=404, response_body=response_body)


class ValidationError(FizzyError):
    """Raised when request validation fails (422)."""

    def __init__(
        self,
        message: str = "Validation failed",
        errors: dict[str, list[str]] | None = None,
        response_body: dict[str, Any] | None = None,
    ) -> None:
        self.errors = errors or {}
        super().__init__(message, status_code=422, response_body=response_body)

    def __str__(self) -> str:
        if self.errors:
            error_details = "; ".join(
                f"{field}: {', '.join(msgs)}" for field, msgs in self.errors.items()
            )
            return f"[422] {self.message}: {error_details}"
        return super().__str__()


class RateLimitError(FizzyError):
    """Raised when rate limit is exceeded (429)."""

    def __init__(
        self,
        message: str = "Rate limit exceeded",
        retry_after: int | None = None,
        response_body: dict[str, Any] | None = None,
    ) -> None:
        self.retry_after = retry_after
        super().__init__(message, status_code=429, response_body=response_body)


class ServerError(FizzyError):
    """Raised when the server returns a 5xx error."""

    def __init__(
        self,
        message: str = "Server error",
        status_code: int = 500,
        response_body: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message, status_code=status_code, response_body=response_body)


class BadRequestError(FizzyError):
    """Raised when the request is malformed (400)."""

    def __init__(
        self,
        message: str = "Bad request",
        response_body: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message, status_code=400, response_body=response_body)
