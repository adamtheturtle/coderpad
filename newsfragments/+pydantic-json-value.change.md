Use Pydantic's `JsonValue` for JSON payloads while preserving the `coderpad.json_types.JsonValue` import.
Reject non-JSON Python values, such as bytes and tuples, instead of coercing them during response validation.
