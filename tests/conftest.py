"""Fixtures for CoderPad API tests."""

import json
from collections.abc import Callable, Generator
from http import HTTPStatus

import pytest
import respx
from openapi_mock import add_openapi_to_respx

from coderpad.async_client import AsyncCoderPad
from coderpad.client import CoderPad
from coderpad.transports import TransportResponse

_BASE_URL = "https://app.coderpad.io"
_LIVE_VARIANT_ORGANIZATION_ID = 42


@pytest.fixture(name="live_variant_organization_id")
def fixture_live_variant_organization_id() -> int:
    """Organization id used by synthetic live-variant fixtures."""
    return _LIVE_VARIANT_ORGANIZATION_ID


@pytest.fixture(name="live_variant_response")
def fixture_live_variant_response() -> Callable[
    ...,
    TransportResponse,
]:
    """Return synthetic examples of empirically observed API variants."""

    def live_variant_response(*, url: str) -> TransportResponse:
        """Build a synthetic live-variant response for ``url``."""
        if url.endswith("/api/pad_environments/binary"):
            payload: dict[str, object] = {
                "status": "OK",
                "id": 1,
                "pad_id": 2,
                "question_id": None,
                "example_question_id": None,
                "language": "python",
                "file_contents": [
                    {
                        "path": "image.png",
                        "contents": None,
                        "history": "https://example.com/history.json",
                        "binary": True,
                    },
                ],
                "created_at": "2026-07-16T00:00:00Z",
                "updated_at": "2026-07-16T00:00:00Z",
            }
        elif url.endswith("/api/organization"):
            payload = {
                "status": "OK",
                "id": _LIVE_VARIANT_ORGANIZATION_ID,
                "organization_name": "Example Organization",
                "user_count": 0,
                "users": [],
                "organization_default_language": "python",
                "single_sign_on_supported": False,
                "teams": [],
                "child_organizations": [],
            }
        else:  # pragma: no cover
            msg = f"Unexpected test URL: {url}"
            raise AssertionError(msg)
        return TransportResponse(
            status_code=HTTPStatus.OK,
            headers={},
            content=json.dumps(obj=payload).encode(),
        )

    return live_variant_response


@pytest.fixture(name="openapi_spec")
def fixture_openapi_spec(request: pytest.FixtureRequest) -> dict[str, object]:
    """Load the OpenAPI spec from the repo."""
    openapi_spec_path = request.config.rootpath / "openapi.json"
    spec_text = openapi_spec_path.read_text(encoding="utf-8")
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
) -> CoderPad:
    """Provide a CoderPad client configured against the mock API."""
    # We reference mock_coderpad_api to ensure the mock
    # is active.
    del mock_coderpad_api
    return CoderPad(
        api_key="test-key",
        base_url=_BASE_URL,
    )


@pytest.fixture(name="async_coderpad_client")
def fixture_async_coderpad_client(
    mock_coderpad_api: respx.MockRouter,
) -> AsyncCoderPad:
    """Provide an async CoderPad client against the mock API."""
    del mock_coderpad_api
    return AsyncCoderPad(
        api_key="test-key",
        base_url=_BASE_URL,
    )
