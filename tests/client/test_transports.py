"""Tests for `coderpad` transports client."""

from http import HTTPStatus

import httpx
import httpx2
import pytest
import respx

from coderpad.transports import (
    HTTPStatusError,
    HTTPX2Transport,
    HTTPXTransport,
    Transport,
    TransportResponse,
)


def test_httpx_transport_is_transport() -> None:
    """HTTPXTransport satisfies the Transport protocol."""
    assert isinstance(HTTPXTransport(), Transport)


def test_close() -> None:
    """The transport can be closed."""
    transport = HTTPXTransport()
    transport.close()


def test_context_manager() -> None:
    """The transport can be used as a context manager."""
    with HTTPXTransport() as transport:
        assert isinstance(transport, HTTPXTransport)


def test_limits_passed_to_httpx_client() -> None:
    """Connection pool limits are stored on the HTTPX transport."""
    limits = httpx.Limits(max_connections=5)
    transport = HTTPXTransport(limits=limits)
    assert transport.limits is limits
    transport.close()


def test_timeout_passed_to_httpx_client() -> None:
    """A timeout is forwarded to the underlying httpx client."""
    timeout = httpx.Timeout(timeout=12.5)
    transport = HTTPXTransport(timeout=timeout)
    assert transport.timeout == timeout
    transport.close()


def test_float_timeout_passed_to_httpx_client() -> None:
    """A float timeout is accepted by the HTTPX transport."""
    float_timeout = 3.0
    transport = HTTPXTransport(timeout=float_timeout)
    assert transport.timeout == float_timeout
    transport.close()


def test_proxy_passed_to_httpx_client() -> None:
    """A proxy is stored on the HTTPX transport."""
    proxy = "http://proxy.example:8080"
    transport = HTTPXTransport(proxy=proxy)
    assert transport.proxy == proxy
    transport.close()


def test_limits_and_proxy_passed_to_httpx_client() -> None:
    """Limits and proxy can both be set on the HTTPX transport."""
    limits = httpx.Limits(max_connections=5)
    proxy = "http://proxy.example:8080"
    transport = HTTPXTransport(limits=limits, proxy=proxy)
    assert transport.limits is limits
    assert transport.proxy == proxy
    transport.close()


def test_limits_and_timeout_passed_to_httpx_client() -> None:
    """Limits and timeout can both be set on the HTTPX transport."""
    limits = httpx.Limits(max_connections=5)
    timeout = httpx.Timeout(timeout=12.5)
    transport = HTTPXTransport(limits=limits, timeout=timeout)
    assert transport.limits is limits
    assert transport.timeout == timeout
    transport.close()


def test_httpx2_transport_is_transport() -> None:
    """HTTPX2Transport satisfies the Transport protocol."""
    with HTTPX2Transport() as transport:
        assert isinstance(transport, Transport)


def test_httpx2_configuration_types() -> None:
    """HTTPX2 configuration objects are stored on the transport."""
    limits = httpx2.Limits(max_connections=5)
    proxy = httpx2.Proxy(url="http://proxy.example:8080")
    timeout = httpx2.Timeout(timeout=12.5)
    with HTTPX2Transport(
        limits=limits, proxy=proxy, timeout=timeout
    ) as transport:
        assert transport.limits is limits
        assert transport.proxy is proxy
        assert transport.timeout is timeout


def test_real_httpx2_request(httpx2_mock: respx.Router) -> None:
    """The transport makes a request through an HTTPX2 client."""
    _ = httpx2_mock.post(url="https://api.example/items").respond(
        status_code=HTTPStatus.CREATED,
        headers={"X-Family": "httpx2"},
        content=b"created",
    )

    with HTTPX2Transport() as transport:
        response = transport(
            method="POST",
            url="https://api.example/items",
            headers={"Authorization": "Token"},
            params={"page": 2},
            data=None,
            files=None,
            json={"name": "example"},
        )

    assert response == TransportResponse(
        status_code=HTTPStatus.CREATED,
        headers={
            "x-family": "httpx2",
            "content-length": "7",
        },
        content=b"created",
    )


def test_httpx2_exception_family(httpx2_mock: respx.Router) -> None:
    """HTTPX2 transport exceptions propagate without conversion."""
    error = httpx2.ConnectError(message="HTTPX2 failed")
    _ = httpx2_mock.get(url="https://api.example/failure").mock(
        side_effect=error
    )

    with (
        HTTPX2Transport() as transport,
        pytest.raises(expected_exception=httpx2.ConnectError),
    ):
        _ = transport(
            method="GET",
            url="https://api.example/failure",
            headers={},
            params=None,
            data=None,
            files=None,
        )


def test_raise_for_status_error() -> None:
    """An error status code raises HTTPStatusError."""
    error_content = b"Not Found"
    response = TransportResponse(
        status_code=HTTPStatus.NOT_FOUND,
        headers={},
        content=error_content,
    )
    with pytest.raises(expected_exception=HTTPStatusError) as exc_info:
        response.raise_for_status()
    assert exc_info.value.status_code == HTTPStatus.NOT_FOUND
    assert exc_info.value.content == error_content


def test_raise_for_status_ok() -> None:
    """A success status code does not raise."""
    response = TransportResponse(
        status_code=HTTPStatus.OK,
        headers={},
        content=b"{}",
    )
    response.raise_for_status()
