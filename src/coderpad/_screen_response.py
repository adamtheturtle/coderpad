"""Runtime validation for CoderPad Screen response bodies."""

from pydantic import TypeAdapter

from coderpad.json_types import JsonValue


def json_value(*, value: object) -> JsonValue:
    """Return a runtime-validated JSON value from a transport."""
    adapter: TypeAdapter[JsonValue] = TypeAdapter(type=JsonValue)
    return adapter.validate_python(value)


def json_object(*, value: object) -> dict[str, JsonValue]:
    """Return a runtime-validated JSON object from a transport."""
    parsed = json_value(value=value)
    if not isinstance(parsed, dict):
        message = "Expected an object response."
        raise TypeError(message)
    return parsed
