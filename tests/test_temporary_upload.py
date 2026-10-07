"""Screen archive uploads use raw bytes and exact body lengths."""

import httpx
import pytest
import respx
from pydantic import ValidationError

from coderpad import (
    SCREEN_US_BASE_URL,
    AsyncCoderPad,
    CoderPad,
    ScreenTemporaryFile,
)
from coderpad._binary_content import (
    require_async_binary_transport,
    require_binary_transport,
)
from coderpad.exceptions import CoderPadError
from coderpad.transports import (
    AsyncHTTPX2Transport,
    HTTPX2Transport,
    TransportResponse,
)
from tests.conftest import ScreenTransportStub

_URL = f"{SCREEN_US_BASE_URL}/assessment/api/v1.1/temporary-file"
_ID = "12345678-1234-1234-1234-123456789012"
_LIMIT = 52_428_800
_ARCHIVE = b"\x1f\x8b\x00\xff\x80archive\x00"
_HEADERS = {
    "content-length": "1",
    "Content-Length": "2",
    "content-type": "application/json",
    "Content-Type": "multipart/form-data",
    "X-Request-ID": "upload-1",
}


def _assert_upload(*, request: httpx.Request, content: bytes) -> None:
    """Assert byte identity and replacement of all stale body headers."""
    assert str(object=request.url) == _URL
    assert request.method == "POST"
    assert request.content == content
    assert request.headers.get_list(key="Content-Length") == [
        str(object=len(content))
    ]
    assert request.headers.get_list(key="Content-Type") == ["application/gzip"]
    assert request.headers["API-Key"] == "screen-key"
    assert request.headers["X-Request-ID"] == "upload-1"
    assert request.headers.get(key="Authorization") is None


@pytest.mark.parametrize(
    argnames="content",
    argvalues=[b"", _ARCHIVE, b"x" * _LIMIT],
    ids=["empty", "binary", "maximum-size"],
)
def test_upload(content: bytes) -> None:
    """Uploads include the exact limit and never JSON-encode archive bytes."""
    with respx.mock() as router:
        route = router.post(url=_URL).respond(
            status_code=200, json={"id": _ID}
        )
        with CoderPad(
            api_key="interview-key",
            screen_api_key="screen-key",
            default_headers=_HEADERS,
        ) as client:
            result = client.screen.temporary_files.upload(content=content)
        assert result == ScreenTemporaryFile(id=_ID)
        assert result.id == _ID
        assert route.call_count == 1
        _assert_upload(request=route.calls.last.request, content=content)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    argnames="content",
    argvalues=[b"", _ARCHIVE, b"x" * _LIMIT],
    ids=["empty", "binary", "maximum-size"],
)
async def test_async_upload(content: bytes) -> None:
    """Async uploads preserve the same size boundary and exact body
    bytes.
    """
    with respx.mock() as router:
        route = router.post(url=_URL).respond(
            status_code=200, json={"id": _ID}
        )
        async with AsyncCoderPad(
            api_key="interview-key",
            screen_api_key="screen-key",
            default_headers=_HEADERS,
        ) as client:
            result = await client.screen.temporary_files.upload(
                content=content
            )
        assert result == ScreenTemporaryFile(id=_ID)
        assert route.call_count == 1
        _assert_upload(request=route.calls.last.request, content=content)


def test_httpx2_upload(httpx2_mock: respx.Router) -> None:
    """HTTPX2 transports also support raw binary content."""
    route = httpx2_mock.post(url=_URL).respond(
        status_code=200, json={"id": _ID}
    )
    with CoderPad(
        api_key="interview-key",
        screen_api_key="screen-key",
        screen_transport=HTTPX2Transport(),
        default_headers=_HEADERS,
    ) as client:
        assert client.screen.temporary_files.upload(content=_ARCHIVE).id == _ID
    _assert_upload(request=route.calls.last.request, content=_ARCHIVE)
    assert route.call_count == 1


@pytest.mark.asyncio
async def test_async_httpx2_upload(httpx2_mock: respx.Router) -> None:
    """Asynchronous HTTPX2 requests use raw bytes without re-encoding."""
    route = httpx2_mock.post(url=_URL).respond(
        status_code=200, json={"id": _ID}
    )
    async with AsyncCoderPad(
        api_key="interview-key",
        screen_api_key="screen-key",
        screen_transport=AsyncHTTPX2Transport(),
        default_headers=_HEADERS,
    ) as client:
        assert (
            await client.screen.temporary_files.upload(content=_ARCHIVE)
        ).id == _ID
    _assert_upload(request=route.calls.last.request, content=_ARCHIVE)
    assert route.call_count == 1


def test_oversize_upload() -> None:
    """Oversize inputs fail before networking starts."""
    with (
        respx.mock() as router,
        CoderPad(
            api_key="interview-key", screen_api_key="screen-key"
        ) as client,
    ):
        with pytest.raises(expected_exception=ValueError, match="52428800"):
            _ = client.screen.temporary_files.upload(
                content=b"x" * (_LIMIT + 1)
            )
        assert router.calls.call_count == 0


@pytest.mark.asyncio
async def test_async_oversize_upload() -> None:
    """Async oversize bodies also fail locally before networking
    starts.
    """
    with respx.mock() as router:
        async with AsyncCoderPad(
            api_key="interview-key", screen_api_key="screen-key"
        ) as client:
            with pytest.raises(
                expected_exception=ValueError, match="52428800"
            ):
                _ = await client.screen.temporary_files.upload(
                    content=b"x" * (_LIMIT + 1)
                )
        assert router.calls.call_count == 0


@pytest.mark.parametrize(argnames="status", argvalues=[400, 403])
def test_upload_api_errors(status: int) -> None:
    """Bad archives and permission failures are never automatically
    retried.
    """
    with respx.mock() as router:
        route = router.post(url=_URL).respond(
            status_code=status, json={"message": "Forbidden"}
        )
        with (
            CoderPad(
                api_key="interview-key", screen_api_key="screen-key"
            ) as client,
            pytest.raises(expected_exception=CoderPadError) as error,
        ):
            _ = client.screen.temporary_files.upload(content=_ARCHIVE)
        assert error.value.status_code == status
        assert route.call_count == 1


@pytest.mark.asyncio
@pytest.mark.parametrize(argnames="status", argvalues=[400, 403])
async def test_async_upload_api_errors(status: int) -> None:
    """Async uploads preserve permission and bad-request errors without
    retries.
    """
    with respx.mock() as router:
        route = router.post(url=_URL).respond(
            status_code=status, json={"message": "Forbidden"}
        )
        async with AsyncCoderPad(
            api_key="interview-key", screen_api_key="screen-key"
        ) as client:
            with pytest.raises(expected_exception=CoderPadError) as error:
                _ = await client.screen.temporary_files.upload(
                    content=_ARCHIVE
                )
        assert error.value.status_code == status
        assert route.call_count == 1


def test_upload_invalid_response() -> None:
    """Malformed success payloads are rejected rather than returning bad
    IDs.
    """
    with respx.mock() as router:
        route = router.post(url=_URL).respond(status_code=200, json={"id": 1})
        with (
            CoderPad(
                api_key="interview-key", screen_api_key="screen-key"
            ) as client,
            pytest.raises(expected_exception=ValidationError),
        ):
            _ = client.screen.temporary_files.upload(content=_ARCHIVE)
        assert route.call_count == 1


def test_json_only_transport(
    screen_transport_stub: ScreenTransportStub,
) -> None:
    """A JSON-only custom transport remains usable until a raw upload is
    asked.
    """
    with CoderPad(
        api_key="interview-key",
        screen_api_key="screen-key",
        screen_transport=screen_transport_stub,
    ) as client:
        expected_id = 7
        assert client.screen.campaigns.list()[0].id == expected_id
        with pytest.raises(
            expected_exception=TypeError, match="binary-capable"
        ):
            _ = client.screen.temporary_files.upload(content=_ARCHIVE)
    assert len(screen_transport_stub.calls) == 1


def test_non_callable_binary_transports() -> None:
    """Missing callable capability is rejected for both transport
    protocols.
    """
    with pytest.raises(expected_exception=TypeError, match="binary-capable"):
        _ = require_binary_transport(transport=object())
    with pytest.raises(expected_exception=TypeError, match="binary-capable"):
        _ = require_async_binary_transport(transport=object())


@pytest.mark.asyncio
async def test_async_json_only_transport() -> None:
    """A JSON-only async transport remains usable for existing
    operations.
    """
    calls: list[tuple[str, str]] = []

    async def json_only(
        *,
        method: str,
        url: str,
        headers: dict[str, str],
        params: dict[str, str | int] | None,
        data: dict[str, str] | None,
        files: dict[str, tuple[str, bytes, str]] | None,
        json: object | None,
    ) -> TransportResponse:
        """Record existing JSON calls without providing binary upload
        support.
        """
        del headers, params, data, files, json
        calls.append((method, url))
        return TransportResponse(
            status_code=200, headers={}, content=b'[{"id":7,"name":"Empty"}]'
        )

    async with AsyncCoderPad(
        api_key="interview-key",
        screen_api_key="screen-key",
        screen_transport=json_only,
    ) as client:
        expected_id = 7
        assert (await client.screen.campaigns.list())[0].id == expected_id
        with pytest.raises(
            expected_exception=TypeError, match="binary-capable"
        ):
            _ = await client.screen.temporary_files.upload(content=_ARCHIVE)
    assert calls == [
        ("GET", f"{SCREEN_US_BASE_URL}/assessment/api/v1.1/campaigns")
    ]
