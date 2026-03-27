"""Fixtures for CoderPad API tests."""

import json
from collections.abc import Generator
from pathlib import Path
from typing import Any

import pytest
import respx
from openapi_mock import add_openapi_to_respx

_OPENAPI_SPEC_PATH = Path(__file__).parent.parent / "openapi.json"
_BASE_URL = "https://api.interview.coderpad.io"


@pytest.fixture
def fixture_openapi_spec() -> dict[str, Any]:
    """Load the OpenAPI spec from the repo."""
    spec_text = _OPENAPI_SPEC_PATH.read_text(encoding="utf-8")
    result: dict[str, Any] = json.loads(spec_text)
    return result


@pytest.fixture
def fixture_mock_coderpad_api(
    fixture_openapi_spec: dict[str, Any],
) -> Generator[respx.MockRouter]:
    """Provide a respx mock router backed by the OpenAPI spec."""
    with respx.mock(
        base_url=_BASE_URL,
        assert_all_called=False,
    ) as mock_router:
        add_openapi_to_respx(
            mock_obj=mock_router,
            spec=fixture_openapi_spec,
            base_url=_BASE_URL,
        )
        yield mock_router
