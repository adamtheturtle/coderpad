"""Setup for Sybil."""

import json
from collections.abc import Generator
from doctest import ELLIPSIS
from pathlib import Path

import pytest
import respx
from beartype import beartype
from openapi_mock import add_openapi_to_respx
from sybil import Sybil
from sybil.parsers.rest import (
    ClearNamespaceParser,
    DocTestParser,
    PythonCodeBlockParser,
)

_OPENAPI_SPEC_PATH = Path(__file__).parent / "openapi.json"
_BASE_URL = "https://api.interview.coderpad.io"


@pytest.fixture(name="mock_coderpad_api")
def fixture_mock_coderpad_api() -> Generator[respx.MockRouter]:
    """Provide a respx mock router backed by the OpenAPI spec."""
    spec_text = _OPENAPI_SPEC_PATH.read_text(encoding="utf-8")
    openapi_spec: dict[str, object] = json.loads(s=spec_text)
    with respx.mock(
        base_url=_BASE_URL,
        assert_all_called=False,
    ) as mock_router:
        add_openapi_to_respx(
            mock_obj=mock_router,
            spec=openapi_spec,
            base_url=_BASE_URL,
        )
        yield mock_router


@beartype
def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    """Apply the beartype decorator to all collected test functions."""
    for item in items:
        if isinstance(item, pytest.Function):
            item.obj = beartype(obj=item.obj)


pytest_collect_file = Sybil(
    parsers=[
        ClearNamespaceParser(),
        DocTestParser(optionflags=ELLIPSIS),
        PythonCodeBlockParser(),
    ],
    patterns=["*.rst", "*.py"],
    fixtures=["mock_coderpad_api"],
).pytest()
