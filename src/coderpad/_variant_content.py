"""JSON request attributes for question variants."""

from collections.abc import Sequence
from enum import Enum
from inspect import Parameter, signature

from beartype import beartype

from coderpad.json_types import JsonValue
from coderpad.transports import AsyncJSONTransport, JSONTransport
from coderpad.types import Language, QuestionVariantFileContent


class Unset(Enum):
    """An omitted attribute, distinct from an explicit JSON null."""

    OMITTED = "unset"


UNSET = Unset.OMITTED


@beartype
def variant_attributes(
    *,
    language: Language | str | None,
    contents: str | Unset | None,
    file_contents: Sequence[QuestionVariantFileContent] | str | None,
    solution: str | None,
) -> dict[str, JsonValue]:
    """Encode only supplied attributes, preserving blank code and null
    code.

    Project files layer over the template on create and replace files on
    update. An empty file list restores the template on update.
    """
    if contents is not UNSET and file_contents is not None:
        message = "contents and file_contents cannot be combined."
        raise ValueError(message)
    data: dict[str, JsonValue] = {}
    if language is not None:
        data["language"] = (
            language.value if isinstance(language, Language) else language
        )
    if not isinstance(contents, Unset):
        data["contents"] = contents
    if file_contents is not None:
        data["file_contents"] = (
            file_contents
            if isinstance(file_contents, str)
            else [file.model_dump(exclude_none=True) for file in file_contents]
        )
    if solution is not None:
        data["solution"] = solution
    return data


@beartype
def require_json_transport(transport: object) -> JSONTransport:
    """Validate JSON keyword support without confusing callable
    protocols.
    """
    if isinstance(transport, JSONTransport) and _accepts_json(
        transport=transport
    ):
        return transport
    message = "Question variants require a JSON-capable transport."
    raise TypeError(message)


@beartype
def require_async_json_transport(transport: object) -> AsyncJSONTransport:
    """Validate JSON support on an asynchronous Interview transport."""
    if isinstance(transport, AsyncJSONTransport) and _accepts_json(
        transport=transport
    ):
        return transport
    message = "Question variants require a JSON-capable transport."
    raise TypeError(message)


@beartype
def _accepts_json(transport: object) -> bool:
    """Return whether the callable accepts the JSON keyword."""
    if not callable(transport):
        return False
    parameters = signature(obj=transport).parameters
    return "json" in parameters or any(
        parameter.kind == Parameter.VAR_KEYWORD
        for parameter in parameters.values()
    )
