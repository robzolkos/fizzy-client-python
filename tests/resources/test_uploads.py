"""Tests for the Uploads resource."""

import pytest
import respx
from httpx import Response

from fizzy import DirectUpload


class TestUploadsResource:
    """Tests for the sync Uploads resource."""

    @respx.mock
    def test_create_direct_upload(self, client, sample_direct_upload):
        """Test creating a direct upload."""
        respx.post("https://app.fizzy.do/123456/rails/active_storage/direct_uploads").mock(
            return_value=Response(201, json=sample_direct_upload)
        )

        upload = client.uploads.create_direct_upload(
            filename="image.png",
            content_type="image/png",
            byte_size=12345,
            checksum="abc123==",
        )

        assert upload.signed_id == "eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaHBBZ0..."
        assert upload.upload_url == "https://storage.example.com/upload"
        assert isinstance(upload, DirectUpload)

    @respx.mock
    def test_direct_upload_headers(self, client, sample_direct_upload):
        """Test that direct upload headers are accessible."""
        respx.post("https://app.fizzy.do/123456/rails/active_storage/direct_uploads").mock(
            return_value=Response(201, json=sample_direct_upload)
        )

        upload = client.uploads.create_direct_upload(
            filename="image.png",
            content_type="image/png",
            byte_size=12345,
            checksum="abc123==",
        )

        assert upload.upload_headers["Content-Type"] == "image/png"
        assert upload.upload_headers["Content-MD5"] == "abc123=="


class TestAsyncUploadsResource:
    """Tests for the async Uploads resource."""

    @pytest.mark.asyncio
    @respx.mock
    async def test_create_direct_upload(self, async_client, sample_direct_upload):
        """Test creating a direct upload asynchronously."""
        respx.post("https://app.fizzy.do/123456/rails/active_storage/direct_uploads").mock(
            return_value=Response(201, json=sample_direct_upload)
        )

        upload = await async_client.uploads.create_direct_upload(
            filename="image.png",
            content_type="image/png",
            byte_size=12345,
            checksum="abc123==",
        )

        assert upload.signed_id == "eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaHBBZ0..."


class TestDirectUploadHelpers:
    """Tests for DirectUpload helper methods."""

    def test_build_attachment_tag(self):
        """Test building an ActionText attachment tag."""
        signed_id = "eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaHBBZ0..."
        tag = DirectUpload.build_attachment_tag(signed_id)

        assert tag == f'<action-text-attachment sgid="{signed_id}"></action-text-attachment>'
