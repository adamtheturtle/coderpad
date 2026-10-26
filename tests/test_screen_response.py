"""Screen response validation rejects non-JSON transport values."""

import pytest
from pydantic import ValidationError

from coderpad._screen_response import json_value


@pytest.mark.parametrize(
    argnames="value",
    argvalues=[b"text", (1,), {"items": (1,)}, {"bytes": b"text"}],
)
def test_non_json_transport_values_are_rejected(value: object) -> None:
    """Non-JSON values cannot become valid payloads through coercion."""
    with pytest.raises(
        expected_exception=ValidationError, match="invalid-json-value"
    ):
        _ = json_value(value=value)
