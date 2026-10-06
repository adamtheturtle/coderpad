"""Tests for `coderpad` configuration asynchronous client."""

from http import HTTPStatus

import httpx
import pytest

from coderpad.async_client import AsyncCoderPad
from coderpad.transports import (
    AsyncHTTPXTransport,
    TransportResponse,
)


def test_default_base_url() -> None:
    """The default base URL is the CoderPad app."""
    client = AsyncCoderPad(api_key="test-key")
    assert client.base_url == "https://app.coderpad.io"


def test_custom_base_url() -> None:
    """A custom base URL can be provided."""
    client = AsyncCoderPad(
        api_key="test-key",
        base_url="https://custom.example.com",
    )
    assert client.base_url == "https://custom.example.com"


@pytest.mark.asyncio
async def test_custom_transport(
    mock_coderpad_api: object,
) -> None:
    """A custom transport can be provided."""
    del mock_coderpad_api
    transport = AsyncHTTPXTransport()
    client = AsyncCoderPad(
        api_key="test-key",
        transport=transport,
    )
    result = await client.pads.list()
    assert result.total >= 0


@pytest.mark.asyncio
async def test_mock_api_available(
    async_coderpad_client: AsyncCoderPad,
) -> None:
    """The mock API fixture provides a working mock."""
    result = await async_coderpad_client.pads.list()
    assert result.total >= 0


@pytest.mark.asyncio
async def test_aclose() -> None:
    """The client can be closed."""
    client = AsyncCoderPad(api_key="test-key")
    await client.aclose()


@pytest.mark.asyncio
async def test_async_context_manager() -> None:
    """The client can be used as an async context manager."""
    async with AsyncCoderPad(
        api_key="test-key",
    ) as client:
        assert isinstance(client, AsyncCoderPad)


@pytest.mark.asyncio
async def test_close_transport_without_aclose() -> None:
    """Closing works when transport has no aclose."""

    class _NoCloseTransport:
        """A transport without an aclose method."""

        async def __call__(
            self,
            *,
            method: str,
            url: str,
            headers: dict[str, str],
            params: (dict[str, str | int] | None),
            data: dict[str, str] | None,
            files: (dict[str, tuple[str, bytes, str]] | None),
        ) -> TransportResponse:
            """Make a request."""
            assert method == "GET"
            assert url == "https://app.coderpad.io/api/pads/"
            assert headers["Authorization"] == 'Token token="test-key"'
            assert params == {}
            assert data is None
            assert files is None
            return TransportResponse(
                status_code=HTTPStatus.OK,
                headers={},
                content=b'{"pads": [], "total": 0}',
            )

    client = AsyncCoderPad(
        api_key="test-key",
        transport=_NoCloseTransport(),
    )
    assert (await client.pads.list()).total == 0
    await client.aclose()
    assert (await client.pads.list()).total == 0


@pytest.mark.asyncio
async def test_default_headers_merged_preserving_authorization() -> None:
    """Default headers merge while Authorization stays the API
    token.
    """
    client = AsyncCoderPad(
        api_key="secret",
        default_headers={
            "User-Agent": "coderpad-tests",
            "Authorization": "should-not-win",
        },
    )
    assert client.pads.headers == {
        "User-Agent": "coderpad-tests",
        "Authorization": 'Token token="secret"',
    }
    await client.aclose()


@pytest.mark.asyncio
async def test_default_headers_merged_preserving_screen_api_key() -> None:
    """Default headers merge while Screen API-Key stays the Screen key."""
    client = AsyncCoderPad(
        api_key="interview",
        screen_api_key="screen-secret",
        default_headers={
            "User-Agent": "coderpad-tests",
            "API-Key": "should-not-win",
        },
    )
    assert client.screen.headers == {
        "User-Agent": "coderpad-tests",
        "API-Key": "screen-secret",
    }
    await client.aclose()


@pytest.mark.asyncio
async def test_limits_forwarded_to_default_transport() -> None:
    """AsyncCoderPad forwards limits to the default transport."""
    limits = httpx.Limits(max_connections=10)
    client = AsyncCoderPad(api_key="test-key", limits=limits)
    transport = client.pads.transport
    assert isinstance(transport, AsyncHTTPXTransport)
    assert transport.limits is limits
    await client.aclose()


@pytest.mark.asyncio
async def test_timeout_forwarded_to_default_transport() -> None:
    """AsyncCoderPad forwards timeout to the default transport."""
    timeout = httpx.Timeout(timeout=7.5)
    client = AsyncCoderPad(api_key="test-key", timeout=timeout)
    transport = client.pads.transport
    assert isinstance(transport, AsyncHTTPXTransport)
    assert transport.timeout == timeout
    await client.aclose()


@pytest.mark.asyncio
async def test_proxy_forwarded_to_default_transport() -> None:
    """AsyncCoderPad forwards proxy to the default transport."""
    proxy = "http://proxy.example:8080"
    client = AsyncCoderPad(api_key="test-key", proxy=proxy)
    transport = client.pads.transport
    assert isinstance(transport, AsyncHTTPXTransport)
    assert transport.proxy == proxy
    await client.aclose()


@pytest.mark.asyncio
async def test_from_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """From_env loads Interview and Screen keys from the
    environment.
    """
    monkeypatch.setenv(name="CODERPAD_API_KEY", value="env-interview")
    monkeypatch.setenv(name="CODERPAD_SCREEN_API_KEY", value="env-screen")
    client = AsyncCoderPad.from_env()
    assert client.pads.headers["Authorization"] == (
        'Token token="env-interview"'
    )
    assert client.screen.headers["API-Key"] == "env-screen"
    await client.aclose()


@pytest.mark.asyncio
async def test_from_env_requires_api_key(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """From_env raises when CODERPAD_API_KEY is missing."""
    monkeypatch.delenv(name="CODERPAD_API_KEY", raising=False)
    monkeypatch.delenv(name="CODERPAD_SCREEN_API_KEY", raising=False)
    with pytest.raises(expected_exception=KeyError):
        _ = AsyncCoderPad.from_env()


@pytest.mark.asyncio
async def test_screen_lazy_requires_api_key() -> None:
    """Accessing screen without a Screen API key raises ValueError."""
    client = AsyncCoderPad(api_key="test-key")
    with pytest.raises(
        expected_exception=ValueError,
        match="screen_api_key",
    ):
        _ = client.screen
    await client.aclose()


@pytest.mark.asyncio
async def test_screen_lazy_initialized_once() -> None:
    """Screen namespace is created on first access and reused."""
    client = AsyncCoderPad(
        api_key="test-key",
        screen_api_key="screen-key",
    )
    first = client.screen
    second = client.screen
    assert first is second
    await client.aclose()


@pytest.mark.asyncio
async def test_screen_with_provided_transport() -> None:
    """Providing screen_transport closes that transport with the
    client.
    """
    transport = AsyncHTTPXTransport()
    client = AsyncCoderPad(
        api_key="test-key",
        screen_api_key="screen-key",
        screen_transport=transport,
    )
    assert client.screen.headers["API-Key"] == "screen-key"
    await client.aclose()
