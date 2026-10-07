"""Raw request capability and Screen upload size validation."""

from collections.abc import Mapping
from inspect import Parameter, signature

from beartype import beartype

from coderpad.transports import AsyncBinaryTransport, BinaryTransport

_LIMIT = 52_428_800


@beartype
def validate_screen_archive(*, content: bytes) -> None:
    """Reject oversize archives before any upload can start."""
    if len(content) > _LIMIT:
        message = "Screen archives must not exceed 52428800 bytes."
        raise ValueError(message)


@beartype
def _accepts_content(
    *, transport: BinaryTransport | AsyncBinaryTransport
) -> bool:
    """Check raw-body keyword support on callable transport
    implementations.
    """
    parameters = signature(obj=transport).parameters
    return "content" in parameters or any(
        parameter.kind == Parameter.VAR_KEYWORD
        for parameter in parameters.values()
    )


@beartype
def require_binary_transport(*, transport: object) -> BinaryTransport:
    """Require binary support only when a raw upload is requested."""
    if isinstance(transport, BinaryTransport) and _accepts_content(
        transport=transport
    ):
        return transport
    message = "Screen uploads require a binary-capable transport."
    raise TypeError(message)


@beartype
def require_async_binary_transport(
    *, transport: object
) -> AsyncBinaryTransport:
    """Require asynchronous binary support only for raw uploads."""
    if isinstance(transport, AsyncBinaryTransport) and _accepts_content(
        transport=transport
    ):
        return transport
    message = "Screen uploads require a binary-capable transport."
    raise TypeError(message)


@beartype
def screen_archive_headers(
    *, headers: Mapping[str, str], content: bytes
) -> dict[str, str]:
    """Replace body headers regardless of caller-provided
    capitalization.
    """
    result = {
        name: value
        for name, value in headers.items()
        if name.lower() not in {"content-length", "content-type"}
    }
    result.update(
        {
            "Content-Type": "application/gzip",
            "Content-Length": str(object=len(content)),
        }
    )
    return result
