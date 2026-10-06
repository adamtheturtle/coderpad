"""Pad form settings and lossless JSON access-list requests."""

from collections.abc import Mapping, Sequence

from beartype import beartype

from coderpad.json_types import JsonValue

_BOOLEAN_FIELDS = frozenset(
    {
        "private",
        "restrict_interviewer_access",
        "disable_coaching_tips",
        "take_home",
        "ai_assist_enabled",
        "ended",
        "deleted",
    }
)
_INTEGER_FIELDS = frozenset({"question_id", "take_home_time_limit"})


@beartype
def pad_settings_fields(
    *, settings: Mapping[str, str | int | bool | None]
) -> dict[str, str]:
    """Omit defaults and retain explicit false values in form requests."""
    return {
        name: ("true" if value else "false")
        if isinstance(value, bool)
        else str(object=value)
        for name, value in settings.items()
        if value is not None
    }


@beartype
def pad_json_attributes(
    *, data: Mapping[str, str], emails: Sequence[str]
) -> dict[str, JsonValue]:
    """Preserve an empty access list and the required execution string."""
    attributes: dict[str, JsonValue] = {}
    for name, value in data.items():
        if name in _BOOLEAN_FIELDS:
            attributes[name] = value == "true"
        elif name in _INTEGER_FIELDS:
            attributes[name] = int(value)
        else:
            attributes[name] = value
    attributes["allowed_interviewer_emails"] = list(emails)
    return {"pad": attributes}
