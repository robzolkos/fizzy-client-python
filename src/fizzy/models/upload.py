"""Upload model for the Fizzy API."""

from typing import Any

from pydantic import BaseModel


class DirectUpload(BaseModel):
    """Represents a direct upload response from Fizzy."""

    id: str
    key: str
    filename: str
    content_type: str
    byte_size: int
    checksum: str
    signed_id: str
    direct_upload: dict[str, Any]

    @property
    def upload_url(self) -> str:
        """Get the URL to upload the file to."""
        url: str = self.direct_upload.get("url", "")
        return url

    @property
    def upload_headers(self) -> dict[str, str]:
        """Get the headers required for the upload."""
        headers: dict[str, str] = self.direct_upload.get("headers", {})
        return headers

    @staticmethod
    def build_attachment_tag(signed_id: str) -> str:
        """Build an ActionText attachment tag for use in rich text.

        Args:
            signed_id: The signed_id from DirectUpload.

        Returns:
            HTML string for an action-text-attachment tag.
        """
        return f'<action-text-attachment sgid="{signed_id}"></action-text-attachment>'
