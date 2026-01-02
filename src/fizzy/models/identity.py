"""Identity model for the Fizzy API."""

from pydantic import BaseModel


class AccountUser(BaseModel):
    """Represents the user within an account."""

    id: str
    name: str
    role: str
    active: bool
    email_address: str | None = None
    created_at: str | None = None
    url: str | None = None


class Account(BaseModel):
    """Represents a Fizzy account the user belongs to."""

    id: str
    name: str
    url: str | None = None
    user: AccountUser | None = None


class Identity(BaseModel):
    """Represents the authenticated user's identity (list of accounts)."""

    accounts: list[Account] = []
