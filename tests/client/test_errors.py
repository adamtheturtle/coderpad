"""Tests for `coderpad` errors client."""

from http import HTTPStatus

import pytest

from coderpad.client import CoderPad
from coderpad.exceptions import (
    AuthenticationError,
    BadGatewayError,
    BadRequestError,
    CoderPadError,
    ForbiddenError,
    GatewayTimeoutError,
    NotFoundError,
    RateLimitError,
    ServerError,
    ServiceUnavailableError,
)
from coderpad.transports import (
    TransportResponse,
)


def test_bad_request() -> None:
    """A 400 response raises BadRequestError."""
    response = TransportResponse(
        status_code=HTTPStatus.BAD_REQUEST,
        headers={},
        content=b"Bad Request",
    )
    exc = CoderPadError.from_response(response=response)
    assert isinstance(exc, BadRequestError)
    assert exc.status_code == HTTPStatus.BAD_REQUEST
    assert exc.content == b"Bad Request"
    assert exc.response is response


def test_authentication_error() -> None:
    """A 401 response raises AuthenticationError."""
    response = TransportResponse(
        status_code=HTTPStatus.UNAUTHORIZED,
        headers={},
        content=b"Unauthorized",
    )
    exc = CoderPadError.from_response(response=response)
    assert isinstance(exc, AuthenticationError)


def test_forbidden_error() -> None:
    """A 403 response raises ForbiddenError."""
    response = TransportResponse(
        status_code=HTTPStatus.FORBIDDEN,
        headers={},
        content=b"Forbidden",
    )
    exc = CoderPadError.from_response(response=response)
    assert isinstance(exc, ForbiddenError)


def test_not_found_error() -> None:
    """A 404 response raises NotFoundError."""
    response = TransportResponse(
        status_code=HTTPStatus.NOT_FOUND,
        headers={},
        content=b"Not Found",
    )
    exc = CoderPadError.from_response(response=response)
    assert isinstance(exc, NotFoundError)


def test_rate_limit_error() -> None:
    """A 429 response raises RateLimitError."""
    response = TransportResponse(
        status_code=HTTPStatus.TOO_MANY_REQUESTS,
        headers={},
        content=b"Too Many Requests",
    )
    exc = CoderPadError.from_response(response=response)
    assert isinstance(exc, RateLimitError)


def test_server_error() -> None:
    """A 500 response raises ServerError."""
    response = TransportResponse(
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        headers={},
        content=b"Internal Server Error",
    )
    exc = CoderPadError.from_response(response=response)
    assert isinstance(exc, ServerError)


def test_bad_gateway_error() -> None:
    """A 502 response raises BadGatewayError."""
    response = TransportResponse(
        status_code=HTTPStatus.BAD_GATEWAY,
        headers={},
        content=b"Bad Gateway",
    )
    exc = CoderPadError.from_response(response=response)
    assert isinstance(exc, BadGatewayError)


def test_service_unavailable_error() -> None:
    """A 503 response raises ServiceUnavailableError."""
    response = TransportResponse(
        status_code=HTTPStatus.SERVICE_UNAVAILABLE,
        headers={},
        content=b"Service Unavailable",
    )
    exc = CoderPadError.from_response(response=response)
    assert isinstance(exc, ServiceUnavailableError)


def test_gateway_timeout_error() -> None:
    """A 504 response raises GatewayTimeoutError."""
    response = TransportResponse(
        status_code=HTTPStatus.GATEWAY_TIMEOUT,
        headers={},
        content=b"Gateway Timeout",
    )
    exc = CoderPadError.from_response(response=response)
    assert isinstance(exc, GatewayTimeoutError)


def test_unmapped_status_code() -> None:
    """An unmapped status code raises CoderPadError."""
    response = TransportResponse(
        status_code=HTTPStatus.IM_A_TEAPOT,
        headers={},
        content=b"I'm a teapot",
    )
    exc = CoderPadError.from_response(response=response)
    assert isinstance(exc, CoderPadError)
    assert not isinstance(
        exc,
        (
            BadRequestError,
            AuthenticationError,
            ForbiddenError,
            NotFoundError,
            RateLimitError,
            ServerError,
            BadGatewayError,
            ServiceUnavailableError,
            GatewayTimeoutError,
        ),
    )
    assert exc.status_code == HTTPStatus.IM_A_TEAPOT


def test_nonstandard_status_code() -> None:
    """A non-standard status code raises CoderPadError."""
    nonstandard_status = 999
    response = TransportResponse(
        status_code=nonstandard_status,
        headers={},
        content=b"Unknown",
    )
    exc = CoderPadError.from_response(response=response)
    assert isinstance(exc, CoderPadError)
    assert not isinstance(
        exc,
        (
            BadRequestError,
            AuthenticationError,
            ForbiddenError,
            NotFoundError,
            RateLimitError,
            ServerError,
            BadGatewayError,
            ServiceUnavailableError,
            GatewayTimeoutError,
        ),
    )
    assert exc.status_code == nonstandard_status


def test_all_subclasses_are_coderpad_errors() -> None:
    """All specific exceptions are CoderPadError subclasses."""
    response = TransportResponse(
        status_code=HTTPStatus.NOT_FOUND,
        headers={},
        content=b"Not Found",
    )
    exc = CoderPadError.from_response(response=response)
    assert isinstance(exc, CoderPadError)


def test_subclass_without_status_code() -> None:
    """A subclass without a status_code is not registered."""

    class _CustomError(CoderPadError):
        """A custom error without a mapped status code."""

    # Verify from_response never returns _CustomError for
    # any common status code.
    for code in (
        HTTPStatus.BAD_REQUEST,
        HTTPStatus.UNAUTHORIZED,
        HTTPStatus.FORBIDDEN,
        HTTPStatus.NOT_FOUND,
        HTTPStatus.IM_A_TEAPOT,
        HTTPStatus.TOO_MANY_REQUESTS,
        HTTPStatus.INTERNAL_SERVER_ERROR,
    ):
        response = TransportResponse(
            status_code=code,
            headers={},
            content=b"",
        )
        exc = CoderPadError.from_response(response=response)
        assert not isinstance(exc, _CustomError)


def test_error_message() -> None:
    """The exception message includes the status code."""
    response = TransportResponse(
        status_code=HTTPStatus.NOT_FOUND,
        headers={},
        content=b"Not Found",
    )
    exc = CoderPadError.from_response(response=response)
    assert exc.args[0] == "HTTP 404"


def test_parses_json_error_body() -> None:
    """JSON error bodies populate code and message attributes."""
    response = TransportResponse(
        status_code=HTTPStatus.UNAUTHORIZED,
        headers={},
        content=b'{"code": "Unauthorized", "message": "Invalid API key"}',
    )
    exc = CoderPadError.from_response(response=response)
    assert isinstance(exc, AuthenticationError)
    assert exc.code == "Unauthorized"
    assert exc.message == "Invalid API key"


def test_non_json_error_body_leaves_code_message_none() -> None:
    """Non-JSON bodies leave code and message as None."""
    response = TransportResponse(
        status_code=HTTPStatus.BAD_REQUEST,
        headers={},
        content=b"not-json",
    )
    exc = CoderPadError.from_response(response=response)
    assert exc.code is None
    assert exc.message is None


def test_non_object_json_error_body_leaves_code_message_none() -> None:
    """JSON arrays (non-objects) leave code and message as None."""
    response = TransportResponse(
        status_code=HTTPStatus.BAD_REQUEST,
        headers={},
        content=b'["not", "an", "object"]',
    )
    exc = CoderPadError.from_response(response=response)
    assert exc.code is None
    assert exc.message is None


def test_json_object_without_string_code_or_message() -> None:
    """JSON objects without string code/message leave them None."""
    response = TransportResponse(
        status_code=HTTPStatus.BAD_REQUEST,
        headers={},
        content=b'{"code": 123, "message": null, "other": "x"}',
    )
    exc = CoderPadError.from_response(response=response)
    assert exc.code is None
    assert exc.message is None


def test_client_raises_specific_exception() -> None:
    """The client raises specific exceptions for error responses."""

    def _error_transport(
        *,
        method: str,
        url: str,
        headers: dict[str, str],
        params: dict[str, str | int] | None,
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

    client = CoderPad(
        api_key="test-key",
        transport=_error_transport,
    )
    with pytest.raises(expected_exception=NotFoundError):
        _ = client.pads.get(pad_id="nonexistent")
