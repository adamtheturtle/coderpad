"""Fixtures for CoderPad API tests."""

import json
from collections.abc import Generator
from pathlib import Path

import pytest
import respx
from openapi_mock import add_openapi_to_respx

from coderpad_api.async_client import AsyncCoderPadClient
from coderpad_api.client import CoderPadClient

_OPENAPI_SPEC_PATH = Path(__file__).parent.parent / "openapi.json"
_BASE_URL = "https://api.interview.coderpad.io"


@pytest.fixture(name="openapi_spec")
def fixture_openapi_spec() -> dict[str, object]:
    """Load the OpenAPI spec from the repo."""
    spec_text = _OPENAPI_SPEC_PATH.read_text(encoding="utf-8")
    result: dict[str, object] = json.loads(s=spec_text)
    return result


@pytest.fixture(name="mock_coderpad_api")
def fixture_mock_coderpad_api(
    openapi_spec: dict[str, object],
) -> Generator[respx.MockRouter]:
    """Provide a respx mock router backed by the OpenAPI spec."""
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


@pytest.fixture(name="coderpad_client")
def fixture_coderpad_client(
    mock_coderpad_api: respx.MockRouter,
) -> CoderPadClient:
    """Provide a CoderPad client configured against the mock API."""
    # We reference mock_coderpad_api to ensure the mock
    # is active.
    del mock_coderpad_api
    return CoderPadClient(
        api_key="test-key",
        base_url=_BASE_URL,
    )


@pytest.fixture(name="async_coderpad_client")
def fixture_async_coderpad_client(
    mock_coderpad_api: respx.MockRouter,
) -> AsyncCoderPadClient:
    """Provide an async CoderPad client against the mock API."""
    del mock_coderpad_api
    return AsyncCoderPadClient(
        api_key="test-key",
        base_url=_BASE_URL,
    )
