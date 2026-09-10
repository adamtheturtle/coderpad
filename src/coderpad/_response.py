"""Runtime-validated CoderPad API response structures."""

from dataclasses import dataclass
from typing import TypeGuard

from beartype import beartype
from beartype.door import TypeHint

from coderpad.json_types import JsonValue


@dataclass(frozen=True, kw_only=True, slots=True)
class Page:
    """A decoded page of API objects and its pagination metadata."""

    items: list[dict[str, JsonValue]]
    total: int
    next_page: str | None
    prev_page: str | None


def _is_objects(
    value: object,
    /,
) -> TypeGuard[list[dict[str, JsonValue]]]:
    """Return whether a value is a list of string-keyed objects."""
    return TypeHint(hint=list[dict[str, JsonValue]]).is_bearable(obj=value)


def _optional_string(value: object) -> str | None:
    """Return an optional string response value."""
    if value is None or isinstance(value, str):
        return value
    message = f"Expected an optional string, got {type(value).__name__}."
    raise TypeError(message)


@beartype
def object_response(
    value: dict[str, JsonValue],
) -> dict[str, JsonValue]:
    """Return a runtime-validated API response object."""
    return value


@beartype
def page_response(
    value: dict[str, JsonValue],
    *,
    item_key: str,
) -> Page:
    """Decode and validate a paginated API response."""
    items = value[item_key]
    if not _is_objects(items):
        message = f"Expected '{item_key}' to be a list of objects."
        raise TypeError(message)
    total = value["total"]
    if not isinstance(total, int):
        message = "Expected 'total' to be an integer."
        raise TypeError(message)
    return Page(
        items=items,
        total=total,
        next_page=_optional_string(value=value.get("next_page")),
        prev_page=_optional_string(value=value.get("prev_page")),
    )


def object_list(value: object) -> list[dict[str, JsonValue]]:
    """Return a runtime-validated list of API response objects."""
    if not _is_objects(value):
        message = "Expected a list of objects."
        raise TypeError(message)
    return value
