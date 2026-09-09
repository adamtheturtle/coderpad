"""Runtime-validated CoderPad API response structures."""

from dataclasses import dataclass
from typing import TypeGuard

from beartype import beartype
from beartype.door import TypeHint

from coderpad._dict_types import PadDict


@dataclass(frozen=True, kw_only=True, slots=True)
class Page:
    """A decoded page of API objects and its pagination metadata."""

    items: list[dict[str, object]]
    total: int
    next_page: str | None
    prev_page: str | None


def _is_objects(value: object, /) -> TypeGuard[list[dict[str, object]]]:
    """Return whether a value is a list of string-keyed objects."""
    return TypeHint(hint=list[dict[str, object]]).is_bearable(obj=value)


def _is_pad(value: object, /) -> TypeGuard[PadDict]:
    """Return whether a value has the shape of a pad response."""
    return TypeHint(hint=PadDict).is_bearable(obj=value)


def _optional_string(value: object, /) -> str | None:
    """Return an optional string response value."""
    if value is None or isinstance(value, str):
        return value
    message = f"Expected an optional string, got {type(value).__name__}."
    raise TypeError(message)


@beartype
def object_response(value: dict[str, object], /) -> dict[str, object]:
    """Return a runtime-validated API response object."""
    return value


@beartype
def page_response(
    value: dict[str, object],
    /,
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
        next_page=_optional_string(value.get("next_page")),
        prev_page=_optional_string(value.get("prev_page")),
    )


def object_list(value: object, /) -> list[dict[str, object]]:
    """Return a runtime-validated list of API response objects."""
    if not _is_objects(value):
        message = "Expected a list of objects."
        raise TypeError(message)
    return value


def pad_response(value: object, /) -> PadDict:
    """Return a runtime-validated pad response."""
    if not _is_pad(value):
        message = "Expected a pad response object."
        raise TypeError(message)
    return value
