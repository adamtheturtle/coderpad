"""Tests for `coderpad` pads asynchronous client."""

import json
from collections.abc import Callable
from http import HTTPStatus

import pytest
import respx

from coderpad.async_client import AsyncCoderPad
from coderpad.exceptions import NotFoundError
from coderpad.transports import (
    TransportResponse,
)
from coderpad.types import (
    Language,
    SortOrder,
)


@pytest.mark.asyncio
async def test_list_pads(
    async_coderpad_client: AsyncCoderPad,
) -> None:
    """Pads can be listed."""
    result = await async_coderpad_client.pads.list()
    assert result.total >= 0


@pytest.mark.asyncio
async def test_list_pads_with_sort(
    async_coderpad_client: AsyncCoderPad,
) -> None:
    """Pads can be listed with a sort parameter."""
    result = await async_coderpad_client.pads.list(
        sort=SortOrder.UPDATED_AT_DESC,
    )
    assert result.total >= 0


@pytest.mark.asyncio
async def test_list_pads_with_page(
    async_coderpad_client: AsyncCoderPad,
) -> None:
    """Pads can be listed with a page parameter."""
    result = await async_coderpad_client.pads.list(
        page=2,
    )
    assert result.total >= 0


@pytest.mark.asyncio
async def test_create_pad(
    async_coderpad_client: AsyncCoderPad,
) -> None:
    """A pad can be created."""
    result = await async_coderpad_client.pads.create(
        title="Test Pad",
        language="python",
    )
    assert bool(result.id)


@pytest.mark.asyncio
async def test_create_pad_all_params(
    async_coderpad_client: AsyncCoderPad,
) -> None:
    """A pad can be created with all parameters."""
    result = await async_coderpad_client.pads.create(
        title="Test Pad",
        language="python",
        contents="print('hello')",
        notes="Private notes",
    )
    assert bool(result.id)


@pytest.mark.asyncio
async def test_create_pad_minimal(
    async_coderpad_client: AsyncCoderPad,
) -> None:
    """A pad can be created with no parameters."""
    result = await async_coderpad_client.pads.create()
    assert bool(result.id)


@pytest.mark.asyncio
async def test_create_pad_with_language_enum(
    async_coderpad_client: AsyncCoderPad,
) -> None:
    """A pad can be created with a Language enum value."""
    result = await async_coderpad_client.pads.create(
        title="Test Pad",
        language=Language.PYTHON,
    )
    assert bool(result.id)


@pytest.mark.asyncio
async def test_create_pad_from_question(
    async_coderpad_client: AsyncCoderPad,
    mock_coderpad_api: respx.MockRouter,
) -> None:
    """A pad can be spawned from an existing question id."""
    result = await async_coderpad_client.pads.create(question_id=54321)
    assert bool(result.id)
    request = mock_coderpad_api.calls.last.request
    assert request.content == b"question_id=54321"


@pytest.mark.asyncio
async def test_get_pad(
    async_coderpad_client: AsyncCoderPad,
) -> None:
    """A pad can be retrieved by id."""
    result = await async_coderpad_client.pads.get(
        pad_id="ABC1234",
    )
    assert bool(result.id)


@pytest.mark.asyncio
async def test_update_pad(
    async_coderpad_client: AsyncCoderPad,
) -> None:
    """A pad can be updated."""
    await async_coderpad_client.pads.update(
        pad_id="ABC1234",
        title="Updated Title",
    )


@pytest.mark.asyncio
async def test_update_pad_no_title(
    async_coderpad_client: AsyncCoderPad,
) -> None:
    """A pad can be updated without a title."""
    await async_coderpad_client.pads.update(
        pad_id="ABC1234",
        language="python",
    )


@pytest.mark.asyncio
async def test_update_pad_all_params(
    async_coderpad_client: AsyncCoderPad,
) -> None:
    """A pad can be updated with all parameters."""
    await async_coderpad_client.pads.update(
        pad_id="ABC1234",
        title="Updated Title",
        language="python",
        contents="print('hello')",
        notes="Notes",
        ended=True,
        deleted=False,
    )


@pytest.mark.asyncio
async def test_get_pad_events(
    async_coderpad_client: AsyncCoderPad,
) -> None:
    """Pad events can be retrieved."""
    result = await async_coderpad_client.pads.get_events(
        pad_id="ABC1234",
    )
    assert result.total >= 0


@pytest.mark.asyncio
async def test_get_pad_events_with_params(
    async_coderpad_client: AsyncCoderPad,
) -> None:
    """Pad events can be retrieved with sort and page."""
    result = await async_coderpad_client.pads.get_events(
        pad_id="ABC1234",
        sort=SortOrder.CREATED_AT_ASC,
        page=1,
    )
    assert result.total >= 0


@pytest.mark.asyncio
async def test_get_pad_environment(
    async_coderpad_client: AsyncCoderPad,
) -> None:
    """A pad environment can be retrieved."""
    result = await async_coderpad_client.pads.get_environment(
        environment_id="123",
    )
    assert bool(result.id)


@pytest.mark.asyncio
async def test_live_response_variants(
    live_variant_organization_id: int,
    live_variant_response: Callable[..., TransportResponse],
) -> None:
    """Undocumented environment and organization variants are
    supported.
    """

    async def _transport(
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

    client = AsyncCoderPad(api_key="test-key", transport=_transport)
    environment = await client.pads.get_environment(
        environment_id="binary",
    )
    assert environment.file_contents[0].contents is None
    assert environment.file_contents[0].binary is True

    organization = await client.organization.get()
    assert organization.id == live_variant_organization_id
    assert organization.single_sign_in_url is None

    questions = [
        await client.questions.get(question_id="custom"),
        (await client.questions.list())[0],
        await client.questions.create(
            title="FizzBuzz",
            language="python",
        ),
    ]
    assert all(
        question.ai_assist_custom_system_prompt == "Only provide hints."
        for question in questions
    )


@pytest.mark.asyncio
async def test_get_history() -> None:
    """Editor history can be retrieved and replayed."""
    history_url = "https://coderpad-1.firebaseio.com/history.json"

    async def _history_transport(
        *,
        method: str,
        url: str,
        headers: dict[str, str],
        params: (dict[str, str | int] | None),
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

    client = AsyncCoderPad(
        api_key="test-key",
        transport=_history_transport,
    )
    history = await client.pads.get_history(history_url=history_url)
    assert history.replay() == "hi"


@pytest.mark.asyncio
async def test_get_empty_history() -> None:
    """A Firebase null response becomes an empty history."""

    async def _empty_history_transport(
        *,
        method: str,
        url: str,
        headers: dict[str, str],
        params: (dict[str, str | int] | None),
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

    client = AsyncCoderPad(
        api_key="test-key",
        transport=_empty_history_transport,
    )
    history = await client.pads.get_history(
        history_url="https://example.com/history.json",
    )
    assert not bool(history)


@pytest.mark.asyncio
async def test_get_history_error() -> None:
    """Firebase HTTP errors use the client exception hierarchy."""

    async def _error_transport(
        *,
        method: str,
        url: str,
        headers: dict[str, str],
        params: (dict[str, str | int] | None),
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

    client = AsyncCoderPad(
        api_key="test-key",
        transport=_error_transport,
    )
    with pytest.raises(expected_exception=NotFoundError):
        await client.pads.get_history(
            history_url="https://example.com/history.json",
        )


@pytest.mark.asyncio
async def test_all_yields_pads_across_pages() -> None:
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

        async def __call__(
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

    client = AsyncCoderPad(api_key="test-key", transport=_Transport())
    titles = [item.title async for item in client.pads.all()]
    assert titles == ["One", "Two"]
    await client.aclose()
