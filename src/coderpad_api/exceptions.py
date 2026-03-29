"""Custom exception hierarchy for the CoderPad API."""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

if TYPE_CHECKING:
    from coderpad_api.transports import TransportResponse


class CoderPadError(Exception):
    """Base exception for all CoderPad API errors.

    Attributes:
        response: The full transport response for debugging.
        status_code: The HTTP status code.
        content: The response body.
    """

    _registry: ClassVar[dict[int, type[CoderPadError]]] = {}

    def __init_subclass__(
        cls,
        *,
        status_code: int | None = None,
        **kwargs: object,
    ) -> None:
        """Register subclass for a specific HTTP status code.

        Args:
            status_code: The HTTP status code to map.
            **kwargs: Additional keyword arguments.
        """
        super().__init_subclass__(**kwargs)
        if status_code is not None:
            CoderPadError._registry[status_code] = cls

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

    @classmethod
    def from_response(
        cls,
        *,
        response: TransportResponse,
    ) -> CoderPadError:
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


class BadRequestError(CoderPadError, status_code=400):
    """Raised for 400 Bad Request responses."""


class AuthenticationError(CoderPadError, status_code=401):
    """Raised for 401 Unauthorized responses."""


class ForbiddenError(CoderPadError, status_code=403):
    """Raised for 403 Forbidden responses."""


class NotFoundError(CoderPadError, status_code=404):
    """Raised for 404 Not Found responses."""


class RateLimitError(CoderPadError, status_code=429):
    """Raised for 429 Too Many Requests responses."""


class ServerError(CoderPadError, status_code=500):
    """Raised for 500 Internal Server Error responses."""
