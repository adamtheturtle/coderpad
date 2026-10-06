"""Tests for `coderpad` errors asynchronous client."""

from http import HTTPStatus

import pytest

from coderpad.async_client import AsyncCoderPad
from coderpad.exceptions import NotFoundError
from coderpad.transports import (
    TransportResponse,
)


@pytest.mark.asyncio
async def test_client_raises_specific_exception() -> None:
    """The async client raises specific exceptions."""

    async def _error_transport(
        *,
        method: str,
        url: str,
        headers: dict[str, str],
        params: (dict[str, str | int] | None),
        data: dict[str, str] | None,
        files: (dict[str, tuple[str, bytes, str]] | None),
    ) -> TransportResponse:
        """Return a 404 response."""
        del method, url, headers, params, data, files
        return TransportResponse(
            status_code=HTTPStatus.NOT_FOUND,
            headers={},
            content=b"Not Found",
        )

    client = AsyncCoderPad(
        api_key="test-key",
        transport=_error_transport,
    )
    with pytest.raises(
        expected_exception=NotFoundError,
    ):
        await client.pads.get(pad_id="nonexistent")
