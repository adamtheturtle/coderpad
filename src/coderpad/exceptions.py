"""Custom exception hierarchy for the CoderPad API."""

import json
from http import HTTPStatus
from typing import ClassVar, TypeGuard

from coderpad.transports import TransportResponse


def _is_object_mapping(
    value: object,
    /,
) -> TypeGuard[dict[object, object]]:
    """Return whether a value is a mapping of objects."""
    return isinstance(value, dict)


def _optional_json_string(*, payload: object, key: str) -> str | None:
    """Return a string field from a JSON object payload."""
    if not _is_object_mapping(payload):
        return None
    for entry_key, entry_value in payload.items():
        if entry_key == key and isinstance(entry_value, str):
            return entry_value
    return None


class CoderPadError(Exception):
    """Base exception for all CoderPad API errors.

    Attributes:
        response: The full transport response for debugging.
        status_code: The HTTP status code.
        content: The response body.
        code: Optional API error code from a JSON body.
        message: Optional API error message from a JSON body.
    """

    _registry: ClassVar[dict[int, type["CoderPadError"]]] = {}

    def __init_subclass__(
        cls,
        *,
        status_code: HTTPStatus | None = None,
    ) -> None:
        """Register subclass for a specific HTTP status code.

        Args:
            status_code: The HTTP status code to map.
        """
        super().__init_subclass__()
        if status_code is not None:
            CoderPadError._registry[status_code.value] = cls

    def __init__(
        self,
        *,
        response: TransportResponse,
    ) -> None:
        """Create a new CoderPad error.

        Args:
            response: The transport response that caused
                the error.
        """
        message = f"HTTP {response.status_code}"
        super().__init__(message)
        self.response: TransportResponse = response
        self.status_code: int = response.status_code
        self.content: bytes = response.content
        self.code: str | None = None
        self.message: str | None = None
        try:
            payload: object = json.loads(
                s=response.content.decode(encoding="utf-8"),
            )
        except (UnicodeDecodeError, json.JSONDecodeError):
            return
        self.code = _optional_json_string(payload=payload, key="code")
        self.message = _optional_json_string(payload=payload, key="message")

    @classmethod
    def from_response(
        cls,
        *,
        response: TransportResponse,
    ) -> "CoderPadError":
        """Create the appropriate exception for a response.

        Uses the registry to find a specific exception class
        for the response's status code, falling back to
        ``CoderPadError``.

        Args:
            response: The transport response.

        Returns:
            The appropriate exception instance.
        """
        exc_cls = cls._registry.get(
            response.status_code,
            CoderPadError,
        )
        return exc_cls(response=response)


class BadRequestError(
    CoderPadError,
    status_code=HTTPStatus.BAD_REQUEST,
):
    """Raised for 400 Bad Request responses."""


class AuthenticationError(
    CoderPadError,
    status_code=HTTPStatus.UNAUTHORIZED,
):
    """Raised for 401 Unauthorized responses."""


class ForbiddenError(
    CoderPadError,
    status_code=HTTPStatus.FORBIDDEN,
):
    """Raised for 403 Forbidden responses."""


class NotFoundError(
    CoderPadError,
    status_code=HTTPStatus.NOT_FOUND,
):
    """Raised for 404 Not Found responses."""


class RateLimitError(
    CoderPadError,
    status_code=HTTPStatus.TOO_MANY_REQUESTS,
):
    """Raised for 429 Too Many Requests responses."""


class ServerError(
    CoderPadError,
    status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
):
    """Raised for 500 Internal Server Error responses."""


class BadGatewayError(
    CoderPadError,
    status_code=HTTPStatus.BAD_GATEWAY,
):
    """Raised for 502 Bad Gateway responses."""


class ServiceUnavailableError(
    CoderPadError,
    status_code=HTTPStatus.SERVICE_UNAVAILABLE,
):
    """Raised for 503 Service Unavailable responses."""


class GatewayTimeoutError(
    CoderPadError,
    status_code=HTTPStatus.GATEWAY_TIMEOUT,
):
    """Raised for 504 Gateway Timeout responses."""
