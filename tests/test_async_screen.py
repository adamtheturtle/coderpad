"""Tests for asynchronous CoderPad Screen support."""

# ruff: noqa: PLR0911, PLR2004

import json as json_module
from http import HTTPStatus

import pytest

from coderpad import AsyncCoderPad
from coderpad.exceptions import AuthenticationError
from coderpad.screen_types import ScreenInvitation
from coderpad.transports import TransportResponse


class _AsyncScreenTransport:
    """Record asynchronous Screen requests."""

    def __init__(self, *, error: bool = False) -> None:
        """Create a recording transport."""
        self.calls: list[dict[str, object]] = []
        self.error = error

    async def __call__(
        self,
        *,
        method: str,
        url: str,
        headers: dict[str, str],
        params: dict[str, str | int] | None = None,
        data: dict[str, str] | None = None,
        files: dict[str, tuple[str, bytes, str]] | None = None,
        json: object | None = None,
    ) -> TransportResponse:
        """Return a response selected by the request path."""
        del data, files
        self.calls.append(
            {
                "method": method,
                "url": url,
                "headers": headers,
                "params": params or {},
                "json": json,
            },
        )
        if self.error:
            return _response(
                {"code": "Unauthorized", "message": "Invalid API key"},
                status=HTTPStatus.UNAUTHORIZED,
            )
        if url.endswith("/campaigns"):
            return _response([{"id": 7, "name": "Backend"}])
        if url.endswith("/campaigns/7/actions/send"):
            return _response({"id": 11, "test_url": "https://test.example"})
        if url.endswith("/tests"):
            return _response(
                {
                    "tests": [
                        {
                            "id": 11,
                            "status": "completed",
                            "report": dict[str, object](),
                        },
                    ],
                    "pagination": {"total": 2},
                },
            )
        if url.endswith("/tests/11/report"):
            return TransportResponse(
                status_code=HTTPStatus.OK,
                headers={"content-type": "application/pdf"},
                content=b"%PDF report",
            )
        if url.endswith("/tests/11"):
            return _response(
                {
                    "id": 11,
                    "status": "completed",
                    "report": dict[str, object](),
                },
            )
        if url.endswith("/webhook") and method == "GET":
            return _response({"url": "https://example.com/hook"})
        return TransportResponse(
            status_code=HTTPStatus.NO_CONTENT,
            headers={},
            content=b"",
        )


def _response(
    value: object,
    /,
    *,
    status: HTTPStatus = HTTPStatus.OK,
) -> TransportResponse:
    """Create a JSON transport response."""
    return TransportResponse(
        status_code=status,
        headers={"content-type": "application/json"},
        content=json_module.dumps(obj=value).encode(),
    )


def _client(transport: _AsyncScreenTransport, /) -> AsyncCoderPad:
    """Create an asynchronous client using the recording transport."""
    return AsyncCoderPad(
        api_key="interview-key",
        screen_api_key="screen-key",
        screen_transport=transport,
    )


@pytest.mark.asyncio
async def test_async_screen_matches_sync_surface() -> None:
    """The asynchronous namespaces expose equivalent operations."""
    recorder = _AsyncScreenTransport()
    client = _client(recorder)
    screen = client.screen
    campaigns = await screen.campaigns.list()
    invitation = await screen.campaigns.send_invitation(
        campaign_id=7,
        invitation=ScreenInvitation(candidate_name="Ada"),
    )
    page = await screen.tests.list(start=0, limit=1)
    test = await screen.tests.get(test_id=11, with_community_stats=True)
    await screen.tests.cancel(test_id=11)
    await screen.tests.resend(test_id=11)
    await screen.tests.delete(test_id=11)
    report = await screen.tests.report(
        test_id=11,
        report_type="full",
        anonymous=True,
        include_rank=False,
    )
    webhook = await screen.webhook.get()
    await screen.webhook.set(url="https://example.com/hook")
    await screen.webhook.delete()
    assert campaigns[0].id == 7
    assert invitation.id == 11
    assert page.pagination is not None
    assert page.pagination.total == 2
    assert test.report is not None
    assert report == b"%PDF report"
    assert recorder.calls[7]["params"] == {
        "report_type": "full",
        "anonymous": "true",
        "include_rank": "false",
    }
    assert webhook.url == "https://example.com/hook"
    await client.aclose()


@pytest.mark.asyncio
async def test_async_screen_errors_use_existing_hierarchy() -> None:
    """Async Screen failures map to the shared exception hierarchy."""
    recorder = _AsyncScreenTransport(error=True)
    screen = _client(recorder).screen
    with pytest.raises(expected_exception=AuthenticationError):
        await screen.campaigns.list()
