"""File uploads resource for the Fizzy API.

This module provides support for ActionText direct uploads, which are used
to attach files (images, documents) to rich text fields in cards and comments.
"""

from __future__ import annotations

import base64
import hashlib
from pathlib import Path
from typing import TYPE_CHECKING

import httpx

from fizzy.models.upload import DirectUpload
from fizzy.resources.base import AsyncBaseResource, BaseResource

if TYPE_CHECKING:
    from fizzy.utils.http import AsyncHTTPClient, HTTPClient


class UploadsResource(BaseResource[DirectUpload]):
    """Resource for managing file uploads.

    This is used to attach files to rich text fields (card descriptions, comments).
    The process is:
    1. Create a direct upload with file metadata
    2. Upload the file to the returned URL with the specified headers
    3. Use the signed_id in an <action-text-attachment> tag in rich text
    """

    def __init__(self, http_client: HTTPClient) -> None:
        super().__init__(http_client)

    def create_direct_upload(
        self,
        filename: str,
        content_type: str,
        byte_size: int,
        checksum: str,
    ) -> DirectUpload:
        """Create a direct upload for a file.

        This creates a presigned URL for uploading a file directly to storage.
        After uploading, use the signed_id in card descriptions or comments.

        Args:
            filename: The name of the file.
            content_type: The MIME type of the file.
            byte_size: The size of the file in bytes.
            checksum: The MD5 checksum of the file (base64 encoded).

        Returns:
            The direct upload information including the upload URL.
        """
        data = self._http.post(
            "/rails/active_storage/direct_uploads",
            data={
                "blob": {
                    "filename": filename,
                    "content_type": content_type,
                    "byte_size": byte_size,
                    "checksum": checksum,
                }
            },
        )
        return self._parse_model(data, DirectUpload)

    def upload_file(
        self,
        file_path: Path | str,
        content_type: str | None = None,
    ) -> DirectUpload:
        """Upload a file and return the direct upload info.

        This is a convenience method that handles the full upload flow:
        1. Calculates the checksum
        2. Creates the direct upload
        3. Uploads the file to the storage service
        4. Returns the DirectUpload with the signed_id

        Args:
            file_path: Path to the file to upload.
            content_type: Optional MIME type. If not provided, guessed from extension.

        Returns:
            DirectUpload with signed_id to use in rich text.
        """
        path = Path(file_path)

        # Calculate checksum and size
        with open(path, "rb") as f:
            content = f.read()
            checksum = base64.b64encode(hashlib.md5(content).digest()).decode()
            byte_size = len(content)

        # Guess content type if not provided
        if content_type is None:
            content_type = self._guess_content_type(path.name)

        # Create the direct upload
        upload_info = self.create_direct_upload(
            filename=path.name,
            byte_size=byte_size,
            checksum=checksum,
            content_type=content_type,
        )

        # Upload the file to the storage service
        with open(path, "rb") as f:
            response = httpx.put(
                upload_info.upload_url,
                content=f,
                headers=upload_info.upload_headers,
            )
            response.raise_for_status()

        return upload_info

    def upload_bytes(
        self,
        content: bytes,
        filename: str,
        content_type: str,
    ) -> DirectUpload:
        """Upload bytes and return the direct upload info.

        Args:
            content: The file content as bytes.
            filename: The filename to use.
            content_type: The MIME type of the content.

        Returns:
            DirectUpload with signed_id to use in rich text.
        """
        checksum = base64.b64encode(hashlib.md5(content).digest()).decode()
        byte_size = len(content)

        upload_info = self.create_direct_upload(
            filename=filename,
            byte_size=byte_size,
            checksum=checksum,
            content_type=content_type,
        )

        response = httpx.put(
            upload_info.upload_url,
            content=content,
            headers=upload_info.upload_headers,
        )
        response.raise_for_status()

        return upload_info

    def _guess_content_type(self, filename: str) -> str:
        """Guess content type from filename."""
        ext = filename.lower().rsplit(".", 1)[-1] if "." in filename else ""
        content_types = {
            "jpg": "image/jpeg",
            "jpeg": "image/jpeg",
            "png": "image/png",
            "gif": "image/gif",
            "webp": "image/webp",
            "svg": "image/svg+xml",
            "pdf": "application/pdf",
        }
        return content_types.get(ext, "application/octet-stream")


class AsyncUploadsResource(AsyncBaseResource[DirectUpload]):
    """Async resource for managing file uploads."""

    def __init__(self, http_client: AsyncHTTPClient) -> None:
        super().__init__(http_client)

    async def create_direct_upload(
        self,
        filename: str,
        content_type: str,
        byte_size: int,
        checksum: str,
    ) -> DirectUpload:
        """Create a direct upload for a file.

        This creates a presigned URL for uploading a file directly to storage.
        After uploading, use the signed_id in card descriptions or comments.

        Args:
            filename: The name of the file.
            content_type: The MIME type of the file.
            byte_size: The size of the file in bytes.
            checksum: The MD5 checksum of the file (base64 encoded).

        Returns:
            The direct upload information including the upload URL.
        """
        data = await self._http.post(
            "/rails/active_storage/direct_uploads",
            data={
                "blob": {
                    "filename": filename,
                    "content_type": content_type,
                    "byte_size": byte_size,
                    "checksum": checksum,
                }
            },
        )
        return self._parse_model(data, DirectUpload)

    async def upload_file(
        self,
        file_path: Path | str,
        content_type: str | None = None,
    ) -> DirectUpload:
        """Upload a file and return the direct upload info.

        Args:
            file_path: Path to the file to upload.
            content_type: Optional MIME type. If not provided, guessed from extension.

        Returns:
            DirectUpload with signed_id to use in rich text.
        """
        path = Path(file_path)

        with open(path, "rb") as f:
            content = f.read()
            checksum = base64.b64encode(hashlib.md5(content).digest()).decode()
            byte_size = len(content)

        if content_type is None:
            content_type = self._guess_content_type(path.name)

        upload_info = await self.create_direct_upload(
            filename=path.name,
            byte_size=byte_size,
            checksum=checksum,
            content_type=content_type,
        )

        async with httpx.AsyncClient() as client:
            with open(path, "rb") as f:
                response = await client.put(
                    upload_info.upload_url,
                    content=f.read(),
                    headers=upload_info.upload_headers,
                )
                response.raise_for_status()

        return upload_info

    async def upload_bytes(
        self,
        content: bytes,
        filename: str,
        content_type: str,
    ) -> DirectUpload:
        """Upload bytes and return the direct upload info.

        Args:
            content: The file content as bytes.
            filename: The filename to use.
            content_type: The MIME type of the content.

        Returns:
            DirectUpload with signed_id to use in rich text.
        """
        checksum = base64.b64encode(hashlib.md5(content).digest()).decode()
        byte_size = len(content)

        upload_info = await self.create_direct_upload(
            filename=filename,
            byte_size=byte_size,
            checksum=checksum,
            content_type=content_type,
        )

        async with httpx.AsyncClient() as client:
            response = await client.put(
                upload_info.upload_url,
                content=content,
                headers=upload_info.upload_headers,
            )
            response.raise_for_status()

        return upload_info

    def _guess_content_type(self, filename: str) -> str:
        """Guess content type from filename."""
        ext = filename.lower().rsplit(".", 1)[-1] if "." in filename else ""
        content_types = {
            "jpg": "image/jpeg",
            "jpeg": "image/jpeg",
            "png": "image/png",
            "gif": "image/gif",
            "webp": "image/webp",
            "svg": "image/svg+xml",
            "pdf": "application/pdf",
        }
        return content_types.get(ext, "application/octet-stream")
