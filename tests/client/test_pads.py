"""Tests for `coderpad` pads client."""

import json
from collections.abc import Callable
from http import HTTPStatus

import pytest
import respx
from pydantic import ValidationError

from coderpad.client import CoderPad
from coderpad.exceptions import (
    NotFoundError,
)
from coderpad.transports import (
    TransportResponse,
)
from coderpad.types import (
    Language,
    SortOrder,
)

_INVALID_PAD_RESPONSES: list[tuple[dict[str, object], type[Exception]]] = [
    ({"pads": "invalid", "total": 0}, TypeError),
    ({"pads": [], "total": "invalid"}, TypeError),
    ({"pads": [], "total": 0, "next_page": 1}, TypeError),
    ({"pads": [{}], "total": 1}, ValidationError),
]


def test_list_pads_parses_prev_page() -> None:
    """Pads.list exposes prev_page when present in the API
    response.
    """

    class _Transport:
        """Return a pads page that includes prev_page."""

        def __call__(
            self,
            *,
            method: str,
            url: str,
            headers: dict[str, str],
            params: dict[str, str | int] | None,
            data: dict[str, str] | None,
            files: (dict[str, tuple[str, bytes, str]] | None),
        ) -> TransportResponse:
            """Return synthetic paginated pads JSON."""
            del method, url, headers, params, data, files
            payload: dict[str, object] = {
                "status": "OK",
                "pads": [],
                "total": 0,
                "next_page": "https://app.coderpad.io/api/pads?page=3",
                "prev_page": "https://app.coderpad.io/api/pads?page=1",
            }
            return TransportResponse(
                status_code=HTTPStatus.OK,
                headers={},
                content=json.dumps(obj=payload).encode(),
            )

    client = CoderPad(api_key="test-key", transport=_Transport())
    result = client.pads.list()
    assert result.prev_page == "https://app.coderpad.io/api/pads?page=1"
    assert result.next_page == "https://app.coderpad.io/api/pads?page=3"
    client.close()


@pytest.mark.parametrize(
    argnames=("payload", "expected_exception"),
    argvalues=_INVALID_PAD_RESPONSES,
)
def test_list_pads_rejects_invalid_responses(
    payload: dict[str, object],
    expected_exception: type[Exception],
) -> None:
    """Pads.list rejects malformed API response values."""

    def _transport(
        *,
        method: str,
        url: str,
        headers: dict[str, str],
        params: dict[str, str | int] | None,
        data: dict[str, str] | None,
        files: (dict[str, tuple[str, bytes, str]] | None),
    ) -> TransportResponse:
        """Return a malformed pads response."""
        del method, url, headers, params, data, files
        return TransportResponse(
            status_code=HTTPStatus.OK,
            headers={},
            content=json.dumps(obj=payload).encode(),
        )

    client = CoderPad(api_key="test-key", transport=_transport)
    with pytest.raises(expected_exception=expected_exception):
        _ = client.pads.list()
    client.close()


def test_list_pads(
    coderpad_client: CoderPad,
) -> None:
    """Pads can be listed."""
    result = coderpad_client.pads.list()
    assert result.total >= 0


def test_list_pads_with_sort(
    coderpad_client: CoderPad,
) -> None:
    """Pads can be listed with a sort parameter."""
    result = coderpad_client.pads.list(
        sort=SortOrder.UPDATED_AT_DESC,
    )
    assert result.total >= 0


def test_list_pads_with_page(
    coderpad_client: CoderPad,
) -> None:
    """Pads can be listed with a page parameter."""
    result = coderpad_client.pads.list(page=2)
    assert result.total >= 0


def test_create_pad(
    coderpad_client: CoderPad,
) -> None:
    """A pad can be created."""
    result = coderpad_client.pads.create(
        title="Test Pad",
        language="python",
    )
    assert bool(result.id)


def test_create_pad_all_params(
    coderpad_client: CoderPad,
) -> None:
    """A pad can be created with all parameters."""
    result = coderpad_client.pads.create(
        title="Test Pad",
        language="python",
        contents="print('hello')",
        notes="Private notes",
    )
    assert bool(result.id)


def test_create_pad_minimal(
    coderpad_client: CoderPad,
) -> None:
    """A pad can be created with no parameters."""
    result = coderpad_client.pads.create()
    assert bool(result.id)


def test_create_pad_with_language_enum(
    coderpad_client: CoderPad,
) -> None:
    """A pad can be created with a Language enum value."""
    result = coderpad_client.pads.create(
        title="Test Pad",
        language=Language.PYTHON,
    )
    assert bool(result.id)


def test_create_pad_from_question(
    coderpad_client: CoderPad,
    mock_coderpad_api: respx.MockRouter,
) -> None:
    """A pad can be spawned from an existing question id."""
    result = coderpad_client.pads.create(question_id=54321)
    assert bool(result.id)
    request = mock_coderpad_api.calls.last.request
    assert request.content == b"question_id=54321"


def test_get_pad(
    coderpad_client: CoderPad,
) -> None:
    """A pad can be retrieved by id."""
    result = coderpad_client.pads.get(
        pad_id="ABC1234",
    )
    assert bool(result.id)


def test_update_pad(
    coderpad_client: CoderPad,
) -> None:
    """A pad can be updated."""
    coderpad_client.pads.update(
        pad_id="ABC1234",
        title="Updated Title",
    )


def test_update_pad_no_title(
    coderpad_client: CoderPad,
) -> None:
    """A pad can be updated without a title."""
    coderpad_client.pads.update(
        pad_id="ABC1234",
        language="python",
    )


def test_update_pad_all_params(
    coderpad_client: CoderPad,
) -> None:
    """A pad can be updated with all parameters."""
    coderpad_client.pads.update(
        pad_id="ABC1234",
        title="Updated Title",
        language="python",
        contents="print('hello')",
        notes="Notes",
        ended=True,
        deleted=False,
    )


def test_get_pad_events(
    coderpad_client: CoderPad,
) -> None:
    """Pad events can be retrieved."""
    result = coderpad_client.pads.get_events(
        pad_id="ABC1234",
    )
    assert result.total >= 0


def test_get_pad_events_with_params(
    coderpad_client: CoderPad,
) -> None:
    """Pad events can be retrieved with sort and page."""
    result = coderpad_client.pads.get_events(
        pad_id="ABC1234",
        sort=SortOrder.CREATED_AT_ASC,
        page=1,
    )
    assert result.total >= 0


def test_live_response_variant_rejects_unexpected_url(
    live_variant_response: Callable[..., TransportResponse],
) -> None:
    """The synthetic response fixture rejects unsupported API URLs."""
    url = "https://app.coderpad.io/api/unsupported/"
    with pytest.raises(
        expected_exception=AssertionError,
        match="Unexpected test URL",
    ):
        _ = live_variant_response(method="GET", url=url)


def test_get_pad_environment(
    coderpad_client: CoderPad,
) -> None:
    """A pad environment can be retrieved."""
    result = coderpad_client.pads.get_environment(
        environment_id="123",
    )
    assert bool(result.id)


def test_live_response_variants(
    live_variant_organization_id: int,
    live_variant_response: Callable[..., TransportResponse],
) -> None:
    """Undocumented environment and organization variants are
    supported.
    """

    def _transport(
        *,
        method: str,
        url: str,
        headers: dict[str, str],
        params: dict[str, str | int] | None,
        data: dict[str, str] | None,
        files: (dict[str, tuple[str, bytes, str]] | None),
    ) -> TransportResponse:
        """Return synthetic live-response variants."""
        del headers, params, data, files
        return live_variant_response(method=method, url=url)

    client = CoderPad(api_key="test-key", transport=_transport)
    environment = client.pads.get_environment(
        environment_id="binary",
    )
    assert environment.file_contents[0].contents is None
    assert environment.file_contents[0].binary is True

    organization = client.organization.get()
    assert organization.id == live_variant_organization_id
    assert organization.single_sign_in_url is None

    questions = [
        client.questions.get(question_id="custom"),
        client.questions.list()[0],
        client.questions.create(title="FizzBuzz", language="python"),
    ]
    assert all(
        question.ai_assist_custom_system_prompt == "Only provide hints."
        for question in questions
    )


def test_get_history() -> None:
    """Editor history can be retrieved and replayed."""
    history_url = "https://coderpad-1.firebaseio.com/history.json"

    def _history_transport(
        *,
        method: str,
        url: str,
        headers: dict[str, str],
        params: dict[str, str | int] | None,
        data: dict[str, str] | None,
        files: (dict[str, tuple[str, bytes, str]] | None),
    ) -> TransportResponse:
        """Return sample Firebase history."""
        del params, data, files
        assert method == "GET"
        assert url == history_url
        assert headers == {"Accept": "application/json"}
        return TransportResponse(
            status_code=HTTPStatus.OK,
            headers={},
            content=json.dumps(
                obj={
                    "entry-1": {
                        "a": "author-1",
                        "o": ["hi"],
                        "t": 1,
                    },
                },
            ).encode(),
        )

    client = CoderPad(
        api_key="test-key",
        transport=_history_transport,
    )
    history = client.pads.get_history(history_url=history_url)
    assert history.replay() == "hi"


def test_get_empty_history() -> None:
    """A Firebase null response becomes an empty history."""

    def _empty_history_transport(
        *,
        method: str,
        url: str,
        headers: dict[str, str],
        params: dict[str, str | int] | None,
        data: dict[str, str] | None,
        files: (dict[str, tuple[str, bytes, str]] | None),
    ) -> TransportResponse:
        """Return an empty Firebase history."""
        del method, url, headers, params, data, files
        return TransportResponse(
            status_code=HTTPStatus.OK,
            headers={},
            content=b"null",
        )

    client = CoderPad(
        api_key="test-key",
        transport=_empty_history_transport,
    )
    history = client.pads.get_history(
        history_url="https://example.com/history.json",
    )
    assert not bool(history)


def test_get_history_error() -> None:
    """Firebase HTTP errors use the client exception hierarchy."""

    def _error_transport(
        *,
        method: str,
        url: str,
        headers: dict[str, str],
        params: dict[str, str | int] | None,
        data: dict[str, str] | None,
        files: (dict[str, tuple[str, bytes, str]] | None),
    ) -> TransportResponse:
        """Return a missing history response."""
        del method, url, headers, params, data, files
        return TransportResponse(
            status_code=HTTPStatus.NOT_FOUND,
            headers={},
            content=b"Not Found",
        )

    client = CoderPad(
        api_key="test-key",
        transport=_error_transport,
    )
    with pytest.raises(expected_exception=NotFoundError):
        _ = client.pads.get_history(
            history_url="https://example.com/history.json",
        )


def test_all_yields_pads_across_pages() -> None:
    """All() follows pagination until next_page is absent."""
    pad: dict[str, object] = {
        "id": "pad-1",
        "title": "One",
        "state": "active",
        "owner_email": "owner@example.com",
        "language": "python",
        "private": True,
        "execution_enabled": True,
        "contents": "",
        "participants": [],
        "events": "[]",
        "notes": "",
        "created_at": "2023-01-01T00:00:00Z",
        "updated_at": "2023-01-02T00:00:00Z",
        "ended_at": None,
        "url": "https://app.coderpad.io/pad-1",
        "playback": "https://app.coderpad.io/pad-1/playback",
        "history": None,
        "drawing": None,
        "type": "sandbox",
        "question_ids": [],
        "pad_environment_ids": [],
        "active_environment_id": None,
        "team": {"id": "team-1", "name": "Backend"},
        "restrict_interviewer_access": False,
    }
    pages: dict[int, dict[str, object]] = {
        1: {
            "status": "OK",
            "pads": [pad],
            "total": 2,
            "next_page": "https://app.coderpad.io/api/pads/?page=2",
        },
        2: {
            "status": "OK",
            "pads": [{**pad, "id": "pad-2", "title": "Two"}],
            "total": 2,
            "next_page": None,
        },
    }

    class _Transport:
        """Serve two pad pages keyed by page query param."""

        def __call__(
            self,
            *,
            method: str,
            url: str,
            headers: dict[str, str],
            params: dict[str, str | int] | None,
            data: dict[str, str] | None,
            files: (dict[str, tuple[str, bytes, str]] | None),
        ) -> TransportResponse:
            """Return the page matching the request."""
            del method, url, headers, data, files
            page_number = 1 if params is None else int(params.get("page", 1))
            return TransportResponse(
                status_code=HTTPStatus.OK,
                headers={},
                content=json.dumps(obj=pages[page_number]).encode(),
            )

    client = CoderPad(api_key="test-key", transport=_Transport())
    titles = [item.title for item in client.pads.all()]
    assert titles == ["One", "Two"]
    client.close()
