"""Tests for `coderpad` transports asynchronous client."""

from http import HTTPStatus

import httpx
import httpx2
import pytest
import respx

from coderpad.transports import (
    AsyncHTTPX2Transport,
    AsyncHTTPXTransport,
    AsyncTransport,
    TransportResponse,
)


def test_async_httpx_transport_is_async_transport() -> None:
    """AsyncHTTPXTransport satisfies AsyncTransport."""
    assert isinstance(
        AsyncHTTPXTransport(),
        AsyncTransport,
    )


@pytest.mark.asyncio
async def test_aclose() -> None:
    """The transport can be closed."""
    transport = AsyncHTTPXTransport()
    await transport.aclose()


@pytest.mark.asyncio
async def test_async_context_manager() -> None:
    """The transport can be used as an async context manager."""
    async with AsyncHTTPXTransport() as transport:
        assert isinstance(
            transport,
            AsyncHTTPXTransport,
        )


@pytest.mark.asyncio
async def test_limits_passed_to_httpx_client() -> None:
    """Connection pool limits are stored on the async HTTPX
    transport.
    """
    limits = httpx.Limits(max_connections=5)
    transport = AsyncHTTPXTransport(limits=limits)
    assert transport.limits is limits
    await transport.aclose()


@pytest.mark.asyncio
async def test_timeout_passed_to_httpx_client() -> None:
    """A timeout is forwarded to the underlying async httpx client."""
    timeout = httpx.Timeout(timeout=12.5)
    transport = AsyncHTTPXTransport(timeout=timeout)
    assert transport.timeout == timeout
    await transport.aclose()


@pytest.mark.asyncio
async def test_proxy_passed_to_httpx_client() -> None:
    """A proxy is stored on the async HTTPX transport."""
    proxy = "http://proxy.example:8080"
    transport = AsyncHTTPXTransport(proxy=proxy)
    assert transport.proxy == proxy
    await transport.aclose()


@pytest.mark.asyncio
async def test_limits_and_proxy_passed_to_httpx_client() -> None:
    """Limits and proxy can both be set on the async HTTPX
    transport.
    """
    limits = httpx.Limits(max_connections=5)
    proxy = "http://proxy.example:8080"
    transport = AsyncHTTPXTransport(limits=limits, proxy=proxy)
    assert transport.limits is limits
    assert transport.proxy == proxy
    await transport.aclose()


@pytest.mark.asyncio
async def test_limits_and_timeout_passed_to_httpx_client() -> None:
    """Limits and timeout can both be set on the async HTTPX
    transport.
    """
    limits = httpx.Limits(max_connections=5)
    timeout = httpx.Timeout(timeout=12.5)
    transport = AsyncHTTPXTransport(limits=limits, timeout=timeout)
    assert transport.limits is limits
    assert transport.timeout == timeout
    await transport.aclose()


@pytest.mark.asyncio
async def test_async_httpx2_transport_is_async_transport() -> None:
    """AsyncHTTPX2Transport satisfies AsyncTransport."""
    async with AsyncHTTPX2Transport() as transport:
        assert isinstance(transport, AsyncTransport)


@pytest.mark.asyncio
async def test_httpx2_configuration_types() -> None:
    """HTTPX2 configuration objects are stored on the transport."""
    limits = httpx2.Limits(max_connections=5)
    proxy = httpx2.Proxy(url="http://proxy.example:8080")
    timeout = httpx2.Timeout(timeout=12.5)
    async with AsyncHTTPX2Transport(
        limits=limits, proxy=proxy, timeout=timeout
    ) as transport:
        assert transport.limits is limits
        assert transport.proxy is proxy
        assert transport.timeout is timeout


@pytest.mark.asyncio
async def test_real_httpx2_request(httpx2_mock: respx.Router) -> None:
    """The transport makes a request through an HTTPX2 async
    client.
    """
    _ = httpx2_mock.get(url="https://api.example/items").respond(
        status_code=HTTPStatus.OK,
        headers={"X-Family": "httpx2"},
        content=b"listed",
    )

    async with AsyncHTTPX2Transport() as transport:
        response = await transport(
            method="GET",
            url="https://api.example/items",
            headers={"Authorization": "Token"},
            params={"page": 2},
            data=None,
            files=None,
        )

    assert response == TransportResponse(
        status_code=HTTPStatus.OK,
        headers={
            "x-family": "httpx2",
            "content-length": "6",
        },
        content=b"listed",
    )


@pytest.mark.asyncio
async def test_httpx2_exception_family(
    httpx2_mock: respx.Router,
) -> None:
    """HTTPX2 transport exceptions propagate without conversion."""
    error = httpx2.ConnectError(message="HTTPX2 failed")
    _ = httpx2_mock.get(url="https://api.example/failure").mock(
        side_effect=error
    )

    with pytest.raises(expected_exception=httpx2.ConnectError):
        async with AsyncHTTPX2Transport() as transport:
            await transport(
                method="GET",
                url="https://api.example/failure",
                headers={},
                params=None,
                data=None,
                files=None,
            )
