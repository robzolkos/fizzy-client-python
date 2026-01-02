"""HTTP client wrapper for the Fizzy API."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any, BinaryIO

import httpx

from fizzy.exceptions import (
    AuthenticationError,
    BadRequestError,
    FizzyError,
    ForbiddenError,
    NotFoundError,
    RateLimitError,
    ServerError,
    ValidationError,
)


class ETagCache:
    """Simple in-memory cache for ETags and responses."""

    def __init__(self) -> None:
        self._cache: dict[str, tuple[str, Any]] = {}

    def get(self, url: str) -> tuple[str | None, Any | None]:
        """Get cached ETag and response for a URL."""
        if url in self._cache:
            return self._cache[url]
        return None, None

    def set(self, url: str, etag: str, response: Any) -> None:
        """Cache ETag and response for a URL."""
        self._cache[url] = (etag, response)

    def clear(self) -> None:
        """Clear the cache."""
        self._cache.clear()


class HTTPClient:
    """HTTP client wrapper with authentication and error handling."""

    DEFAULT_BASE_URL = "https://app.fizzy.do"

    def __init__(
        self,
        token: str | None = None,
        session_token: str | None = None,
        account_slug: str | None = None,
        base_url: str = DEFAULT_BASE_URL,
        cache: bool = True,
        timeout: float = 30.0,
    ) -> None:
        if not token and not session_token:
            raise ValueError("Either token or session_token must be provided")

        self.account_slug = account_slug
        self.base_url = base_url.rstrip("/")
        self._cache_enabled = cache
        self._etag_cache = ETagCache() if cache else None

        # Set up authentication headers
        headers: dict[str, str] = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

        if token:
            headers["Authorization"] = f"Bearer {token}"
        elif session_token:
            headers["Authorization"] = f"Bearer {session_token}"

        self._client = httpx.Client(
            base_url=self.base_url,
            headers=headers,
            timeout=timeout,
        )

    def close(self) -> None:
        """Close the HTTP client."""
        self._client.close()

    def __enter__(self) -> HTTPClient:
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()

    def _build_url(self, path: str, include_account: bool = True) -> str:
        """Build the full URL for an API endpoint."""
        if include_account and self.account_slug:
            return f"/{self.account_slug}{path}"
        return path

    def _handle_response(self, response: httpx.Response) -> Any:
        """Handle the response and raise appropriate exceptions."""
        if response.status_code == 304:
            return None  # Not modified, use cached response

        if response.status_code >= 400:
            self._raise_for_status(response)

        if response.status_code == 204:
            return None

        # Handle 201 Created with Location header but empty body
        # Follow the Location header to get the created resource
        if response.status_code == 201:
            location = response.headers.get("Location")
            if location and (not response.content or not response.content.strip()):
                # Strip base URL if present and get the resource
                if location.startswith(self.base_url):
                    location = location[len(self.base_url) :]
                # Strip .json suffix if present
                if location.endswith(".json"):
                    location = location[:-5]
                follow_response = self._client.get(location)
                if follow_response.status_code >= 400:
                    self._raise_for_status(follow_response)
                return follow_response.json()

        # Handle empty body
        if not response.content or not response.content.strip():
            return None

        return response.json()

    def _raise_for_status(self, response: httpx.Response) -> None:
        """Raise an appropriate exception based on status code."""
        try:
            body = response.json()
        except Exception:
            body = {}

        message = body.get("error", body.get("message", response.text or "Unknown error"))

        match response.status_code:
            case 400:
                raise BadRequestError(message, response_body=body)
            case 401:
                raise AuthenticationError(message, response_body=body)
            case 403:
                raise ForbiddenError(message, response_body=body)
            case 404:
                raise NotFoundError(message, response_body=body)
            case 422:
                errors = body.get("errors", {})
                raise ValidationError(message, errors=errors, response_body=body)
            case 429:
                retry_after = response.headers.get("Retry-After")
                raise RateLimitError(
                    message,
                    retry_after=int(retry_after) if retry_after else None,
                    response_body=body,
                )
            case code if code >= 500:
                raise ServerError(message, status_code=code, response_body=body)
            case _:
                raise FizzyError(message, status_code=response.status_code, response_body=body)

    def _build_params(self, params: dict[str, Any] | None) -> dict[str, Any]:
        """Build query parameters, handling arrays properly."""
        if not params:
            return {}

        result: dict[str, Any] = {}
        for key, value in params.items():
            if value is None:
                continue
            if isinstance(value, list):
                # Convert list to array params (e.g., tag_ids[] = [1, 2])
                result[f"{key}[]"] = value
            elif isinstance(value, bool):
                result[key] = str(value).lower()
            else:
                result[key] = value
        return result

    def get(
        self,
        path: str,
        params: dict[str, Any] | None = None,
        include_account: bool = True,
    ) -> tuple[Any, httpx.Response]:
        """Make a GET request."""
        url = self._build_url(path, include_account)
        headers: dict[str, str] = {}

        # Check for cached ETag
        if self._cache_enabled and self._etag_cache:
            cached_etag, cached_response = self._etag_cache.get(url)
            if cached_etag:
                headers["If-None-Match"] = cached_etag

        response = self._client.get(url, params=self._build_params(params), headers=headers)

        # Handle 304 Not Modified
        if response.status_code == 304 and self._etag_cache:
            _, cached_response = self._etag_cache.get(url)
            return cached_response, response

        data = self._handle_response(response)

        # Cache the response if ETag is present
        if self._cache_enabled and self._etag_cache:
            etag = response.headers.get("ETag")
            if etag:
                self._etag_cache.set(url, etag, data)

        return data, response

    def post(
        self,
        path: str,
        data: dict[str, Any] | None = None,
        include_account: bool = True,
    ) -> Any:
        """Make a POST request."""
        url = self._build_url(path, include_account)
        response = self._client.post(url, json=data)
        return self._handle_response(response)

    def patch(
        self,
        path: str,
        data: dict[str, Any] | None = None,
        include_account: bool = True,
    ) -> Any:
        """Make a PATCH request."""
        url = self._build_url(path, include_account)
        response = self._client.patch(url, json=data)
        return self._handle_response(response)

    def put(
        self,
        path: str,
        data: dict[str, Any] | None = None,
        include_account: bool = True,
    ) -> Any:
        """Make a PUT request."""
        url = self._build_url(path, include_account)
        response = self._client.put(url, json=data)
        return self._handle_response(response)

    def delete(
        self,
        path: str,
        include_account: bool = True,
    ) -> None:
        """Make a DELETE request."""
        url = self._build_url(path, include_account)
        response = self._client.delete(url)
        self._handle_response(response)

    def post_multipart(
        self,
        path: str,
        data: dict[str, Any] | None = None,
        files: dict[str, tuple[str, BinaryIO, str] | Path | str] | None = None,
        include_account: bool = True,
    ) -> Any:
        """Make a POST request with multipart/form-data.

        Args:
            path: API endpoint path.
            data: Form data to send.
            files: Files to upload. Dict of field_name -> (filename, file_obj, content_type)
                   or field_name -> Path/str for file path.
            include_account: Whether to include account slug in URL.

        Returns:
            Response data or None.
        """
        url = self._build_url(path, include_account)
        prepared_files = self._prepare_files(files)
        prepared_data = self._flatten_data_for_multipart(data)

        # Use a fresh client without Content-Type header for multipart
        # (the default client has Content-Type: application/json which breaks multipart)
        with httpx.Client(
            base_url=self.base_url,
            headers={
                "Accept": "application/json",
                "Authorization": self._client.headers.get("Authorization", ""),
            },
            timeout=self._client.timeout,
        ) as client:
            response = client.post(url, data=prepared_data, files=prepared_files)
            return self._handle_response(response)

    def put_multipart(
        self,
        path: str,
        data: dict[str, Any] | None = None,
        files: dict[str, tuple[str, BinaryIO, str] | Path | str] | None = None,
        include_account: bool = True,
    ) -> Any:
        """Make a PUT request with multipart/form-data.

        Args:
            path: API endpoint path.
            data: Form data to send.
            files: Files to upload. Dict of field_name -> (filename, file_obj, content_type)
                   or field_name -> Path/str for file path.
            include_account: Whether to include account slug in URL.

        Returns:
            Response data or None.
        """
        url = self._build_url(path, include_account)
        prepared_files = self._prepare_files(files)
        prepared_data = self._flatten_data_for_multipart(data)

        # Use a fresh client without Content-Type header for multipart
        with httpx.Client(
            base_url=self.base_url,
            headers={
                "Accept": "application/json",
                "Authorization": self._client.headers.get("Authorization", ""),
            },
            timeout=self._client.timeout,
        ) as client:
            response = client.put(url, data=prepared_data, files=prepared_files)
            return self._handle_response(response)

    def _prepare_files(
        self,
        files: dict[str, tuple[str, BinaryIO, str] | Path | str] | None,
    ) -> dict[str, tuple[str, BinaryIO, str]] | None:
        """Prepare files for upload."""
        if not files:
            return None

        result: dict[str, tuple[str, BinaryIO, str]] = {}
        for field_name, file_spec in files.items():
            if isinstance(file_spec, (str, Path)):
                # File path provided
                path = Path(file_spec)
                content_type = self._guess_content_type(path.name)
                # File handle is passed to httpx which manages its lifecycle
                result[field_name] = (path.name, open(path, "rb"), content_type)  # noqa: SIM115
            else:
                # Tuple (filename, file_obj, content_type) provided
                result[field_name] = file_spec
        return result

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

    def _flatten_data_for_multipart(
        self,
        data: dict[str, Any] | None,
        prefix: str = "",
    ) -> dict[str, str]:
        """Flatten nested dict for multipart form data (Rails-style bracket notation)."""
        if not data:
            return {}

        result: dict[str, str] = {}
        for key, value in data.items():
            full_key = f"{prefix}[{key}]" if prefix else key
            if isinstance(value, dict):
                result.update(self._flatten_data_for_multipart(value, full_key))
            elif isinstance(value, list):
                for item in value:
                    result[f"{full_key}[]"] = str(item)
            elif isinstance(value, bool):
                result[full_key] = str(value).lower()
            elif value is not None:
                result[full_key] = str(value)
        return result


class AsyncHTTPClient:
    """Async HTTP client wrapper with authentication and error handling."""

    DEFAULT_BASE_URL = "https://app.fizzy.do"

    def __init__(
        self,
        token: str | None = None,
        session_token: str | None = None,
        account_slug: str | None = None,
        base_url: str = DEFAULT_BASE_URL,
        cache: bool = True,
        timeout: float = 30.0,
    ) -> None:
        if not token and not session_token:
            raise ValueError("Either token or session_token must be provided")

        self.account_slug = account_slug
        self.base_url = base_url.rstrip("/")
        self._cache_enabled = cache
        self._etag_cache = ETagCache() if cache else None

        # Set up authentication headers
        headers: dict[str, str] = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

        if token:
            headers["Authorization"] = f"Bearer {token}"
        elif session_token:
            headers["Authorization"] = f"Bearer {session_token}"

        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            headers=headers,
            timeout=timeout,
        )

    async def close(self) -> None:
        """Close the HTTP client."""
        await self._client.aclose()

    async def __aenter__(self) -> AsyncHTTPClient:
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.close()

    def _build_url(self, path: str, include_account: bool = True) -> str:
        """Build the full URL for an API endpoint."""
        if include_account and self.account_slug:
            return f"/{self.account_slug}{path}"
        return path

    def _handle_response(self, response: httpx.Response) -> Any:
        """Handle the response and raise appropriate exceptions."""
        if response.status_code == 304:
            return None

        if response.status_code >= 400:
            self._raise_for_status(response)

        if response.status_code == 204:
            return None

        return response.json()

    def _raise_for_status(self, response: httpx.Response) -> None:
        """Raise an appropriate exception based on status code."""
        try:
            body = response.json()
        except Exception:
            body = {}

        message = body.get("error", body.get("message", response.text or "Unknown error"))

        match response.status_code:
            case 400:
                raise BadRequestError(message, response_body=body)
            case 401:
                raise AuthenticationError(message, response_body=body)
            case 403:
                raise ForbiddenError(message, response_body=body)
            case 404:
                raise NotFoundError(message, response_body=body)
            case 422:
                errors = body.get("errors", {})
                raise ValidationError(message, errors=errors, response_body=body)
            case 429:
                retry_after = response.headers.get("Retry-After")
                raise RateLimitError(
                    message,
                    retry_after=int(retry_after) if retry_after else None,
                    response_body=body,
                )
            case code if code >= 500:
                raise ServerError(message, status_code=code, response_body=body)
            case _:
                raise FizzyError(message, status_code=response.status_code, response_body=body)

    def _build_params(self, params: dict[str, Any] | None) -> dict[str, Any]:
        """Build query parameters, handling arrays properly."""
        if not params:
            return {}

        result: dict[str, Any] = {}
        for key, value in params.items():
            if value is None:
                continue
            if isinstance(value, list):
                result[f"{key}[]"] = value
            elif isinstance(value, bool):
                result[key] = str(value).lower()
            else:
                result[key] = value
        return result

    async def get(
        self,
        path: str,
        params: dict[str, Any] | None = None,
        include_account: bool = True,
    ) -> tuple[Any, httpx.Response]:
        """Make a GET request."""
        url = self._build_url(path, include_account)
        headers: dict[str, str] = {}

        if self._cache_enabled and self._etag_cache:
            cached_etag, cached_response = self._etag_cache.get(url)
            if cached_etag:
                headers["If-None-Match"] = cached_etag

        response = await self._client.get(url, params=self._build_params(params), headers=headers)

        if response.status_code == 304 and self._etag_cache:
            _, cached_response = self._etag_cache.get(url)
            return cached_response, response

        data = self._handle_response(response)

        if self._cache_enabled and self._etag_cache:
            etag = response.headers.get("ETag")
            if etag:
                self._etag_cache.set(url, etag, data)

        return data, response

    async def post(
        self,
        path: str,
        data: dict[str, Any] | None = None,
        include_account: bool = True,
    ) -> Any:
        """Make a POST request."""
        url = self._build_url(path, include_account)
        response = await self._client.post(url, json=data)
        return self._handle_response(response)

    async def patch(
        self,
        path: str,
        data: dict[str, Any] | None = None,
        include_account: bool = True,
    ) -> Any:
        """Make a PATCH request."""
        url = self._build_url(path, include_account)
        response = await self._client.patch(url, json=data)
        return self._handle_response(response)

    async def put(
        self,
        path: str,
        data: dict[str, Any] | None = None,
        include_account: bool = True,
    ) -> Any:
        """Make a PUT request."""
        url = self._build_url(path, include_account)
        response = await self._client.put(url, json=data)
        return self._handle_response(response)

    async def delete(
        self,
        path: str,
        include_account: bool = True,
    ) -> None:
        """Make a DELETE request."""
        url = self._build_url(path, include_account)
        response = await self._client.delete(url)
        self._handle_response(response)

    async def post_multipart(
        self,
        path: str,
        data: dict[str, Any] | None = None,
        files: dict[str, tuple[str, BinaryIO, str] | Path | str] | None = None,
        include_account: bool = True,
    ) -> Any:
        """Make a POST request with multipart/form-data.

        Args:
            path: API endpoint path.
            data: Form data to send.
            files: Files to upload. Dict of field_name -> (filename, file_obj, content_type)
                   or field_name -> Path/str for file path.
            include_account: Whether to include account slug in URL.

        Returns:
            Response data or None.
        """
        url = self._build_url(path, include_account)
        prepared_files = self._prepare_files(files)
        prepared_data = self._flatten_data_for_multipart(data)

        # Use a fresh client without Content-Type header for multipart
        async with httpx.AsyncClient(
            base_url=self.base_url,
            headers={
                "Accept": "application/json",
                "Authorization": self._client.headers.get("Authorization", ""),
            },
            timeout=self._client.timeout,
        ) as client:
            response = await client.post(url, data=prepared_data, files=prepared_files)
            return self._handle_response(response)

    async def put_multipart(
        self,
        path: str,
        data: dict[str, Any] | None = None,
        files: dict[str, tuple[str, BinaryIO, str] | Path | str] | None = None,
        include_account: bool = True,
    ) -> Any:
        """Make a PUT request with multipart/form-data.

        Args:
            path: API endpoint path.
            data: Form data to send.
            files: Files to upload. Dict of field_name -> (filename, file_obj, content_type)
                   or field_name -> Path/str for file path.
            include_account: Whether to include account slug in URL.

        Returns:
            Response data or None.
        """
        url = self._build_url(path, include_account)
        prepared_files = self._prepare_files(files)
        prepared_data = self._flatten_data_for_multipart(data)

        # Use a fresh client without Content-Type header for multipart
        async with httpx.AsyncClient(
            base_url=self.base_url,
            headers={
                "Accept": "application/json",
                "Authorization": self._client.headers.get("Authorization", ""),
            },
            timeout=self._client.timeout,
        ) as client:
            response = await client.put(url, data=prepared_data, files=prepared_files)
            return self._handle_response(response)

    def _prepare_files(
        self,
        files: dict[str, tuple[str, BinaryIO, str] | Path | str] | None,
    ) -> dict[str, tuple[str, BinaryIO, str]] | None:
        """Prepare files for upload."""
        if not files:
            return None

        result: dict[str, tuple[str, BinaryIO, str]] = {}
        for field_name, file_spec in files.items():
            if isinstance(file_spec, (str, Path)):
                path = Path(file_spec)
                content_type = self._guess_content_type(path.name)
                # File handle is passed to httpx which manages its lifecycle
                result[field_name] = (path.name, open(path, "rb"), content_type)  # noqa: SIM115
            else:
                result[field_name] = file_spec
        return result

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

    def _flatten_data_for_multipart(
        self,
        data: dict[str, Any] | None,
        prefix: str = "",
    ) -> dict[str, str]:
        """Flatten nested dict for multipart form data (Rails-style bracket notation)."""
        if not data:
            return {}

        result: dict[str, str] = {}
        for key, value in data.items():
            full_key = f"{prefix}[{key}]" if prefix else key
            if isinstance(value, dict):
                result.update(self._flatten_data_for_multipart(value, full_key))
            elif isinstance(value, list):
                for item in value:
                    result[f"{full_key}[]"] = str(item)
            elif isinstance(value, bool):
                result[full_key] = str(value).lower()
            elif value is not None:
                result[full_key] = str(value)
        return result


def parse_link_header(header: str | None) -> dict[str, str]:
    """Parse the Link header to extract pagination URLs."""
    if not header:
        return {}

    links: dict[str, str] = {}
    for part in header.split(","):
        match = re.match(r'<([^>]+)>;\s*rel="([^"]+)"', part.strip())
        if match:
            url, rel = match.groups()
            links[rel] = url

    return links
