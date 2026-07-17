"""Tests for ``coderpad``."""

import json
from http import HTTPStatus

from coderpad.transports import TransportResponse

LIVE_VARIANT_ORGANIZATION_ID = 42


def live_variant_response(*, url: str) -> TransportResponse:
    """Return synthetic examples of empirically observed API variants."""
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
            "id": LIVE_VARIANT_ORGANIZATION_ID,
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
