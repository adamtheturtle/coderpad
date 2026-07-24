"""Tests for asynchronous CoderPad Screen support."""

# ruff: noqa: PLR2004

import pytest

from coderpad import AsyncCoderPad
from coderpad.screen_types import ScreenInvitation
from coderpad.transports import TransportResponse

from .test_screen import _ScreenTransport


class _AsyncScreenTransport:
    """Asynchronously adapt the shared recording transport."""

    def __init__(self, sync: _ScreenTransport) -> None:
        """Create an asynchronous transport adapter."""
        self.sync = sync

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
        """Forward to the synchronous recording transport."""
        return self.sync(
            method=method,
            url=url,
            headers=headers,
            params=params,
            data=data,
            files=files,
            json=json,
        )


def _client(transport: _AsyncScreenTransport, /) -> AsyncCoderPad:
    """Create an asynchronous client using the recording transport."""
    return AsyncCoderPad(
        api_key="interview-key",
        screen_api_key="screen-key",
        transport=transport,
    )


@pytest.mark.asyncio
async def test_async_screen_matches_sync_surface() -> None:
    """The asynchronous namespaces expose equivalent operations."""
    recorder = _ScreenTransport()
    screen = _client(_AsyncScreenTransport(sync=recorder)).screen
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
    report = await screen.tests.report(test_id=11)
    webhook = await screen.webhook.get()
    await screen.webhook.set(url="https://example.com/hook")
    await screen.webhook.delete()
    assert campaigns[0].id == 7
    assert invitation.id == 11
    assert page.pagination is not None
    assert page.pagination.total == 2
    assert test.report is not None
    assert report == b"%PDF report"
    assert webhook.url == "https://example.com/hook"
