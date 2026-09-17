"""Tests for asynchronous CoderPad Screen support."""

import pytest

from coderpad import SCREEN_EU_BASE_URL, AsyncCoderPad
from coderpad.exceptions import AuthenticationError
from coderpad.screen_types import ScreenInvitation
from coderpad.transports import TransportResponse
from tests.conftest import ScreenTransportStub


class _AsyncScreenTransport:
    """Record asynchronous Screen requests."""

    def __init__(self, *, error: bool) -> None:
        """Create a recording transport."""
        self.transport = ScreenTransportStub(
            error=error, non_object_response=False
        )

    async def __call__(
        self,
        *,
        method: str,
        url: str,
        headers: dict[str, str],
        params: dict[str, str | int] | None,
        data: dict[str, str] | None,
        files: dict[str, tuple[str, bytes, str]] | None,
        json: object | None,
    ) -> TransportResponse:
        """Use the shared Screen response dispatcher asynchronously."""
        return self.transport(
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
        screen_transport=transport,
    )


@pytest.mark.asyncio
async def test_async_screen_matches_sync_surface() -> None:
    """The asynchronous namespaces expose equivalent operations."""
    campaign_id = 7
    expected_invitation_id = 11
    expected_test_count = 2
    test_id = 11
    recorder = _AsyncScreenTransport(error=False)
    client = _client(recorder)
    screen = client.screen
    campaigns = await screen.campaigns.list()
    invitation = await screen.campaigns.send_invitation(
        campaign_id=campaign_id,
        invitation=ScreenInvitation(
            candidate_email="ada@example.com",
            candidate_name="Ada",
        ),
    )
    page = await screen.tests.list(start=0, limit=1)
    test = await screen.tests.get(
        test_id=test_id,
        with_community_stats=True,
    )
    await screen.tests.cancel(test_id=test_id)
    await screen.tests.resend(test_id=test_id)
    await screen.tests.delete(test_id=test_id)
    report = await screen.tests.report(
        test_id=test_id,
        report_type="full",
        anonymous=True,
        include_rank=False,
    )
    typed_report = await screen.tests.report_json(
        test_id=test_id,
        with_community_stats=True,
    )
    webhook = await screen.webhook.get()
    await screen.webhook.set(url="https://example.com/hook")
    await screen.webhook.delete()
    assert campaigns[0].id == campaign_id
    assert invitation.id == expected_invitation_id
    assert page.pagination is not None
    assert page.pagination.total == expected_test_count
    assert test.report is not None
    assert report == b"%PDF report"
    assert typed_report.score == test.report.score
    assert recorder.transport.calls[7]["params"] == {
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


@pytest.mark.asyncio
async def test_async_report_json_raises_when_no_report() -> None:
    """Async report_json raises LookupError when the test has no
    report.
    """
    recorder = _AsyncScreenTransport(error=False)
    screen = _client(recorder).screen
    with pytest.raises(
        expected_exception=LookupError,
        match="Screen test 99 has no scored report",
    ):
        await screen.tests.report_json(test_id=99)


@pytest.mark.asyncio
async def test_async_tests_all_iterates_pages() -> None:
    """Async tests.all() yields tests across pagination pages."""
    recorder = _AsyncScreenTransport(error=False)
    client = _client(recorder)
    names = [
        test.candidate_name async for test in client.screen.tests.all(limit=1)
    ]
    assert names == ["Ada", "Grace"]
    await client.aclose()


@pytest.mark.asyncio
async def test_async_empty_screen_api_key_fails_fast() -> None:
    """Async Screen requests fail before transport when api_key is
    empty.
    """
    recorder = _AsyncScreenTransport(error=False)
    client = AsyncCoderPad(
        api_key="interview-key",
        screen_api_key="",
        screen_base_url=SCREEN_EU_BASE_URL,
        screen_transport=recorder,
    )
    with pytest.raises(
        expected_exception=ValueError,
        match="Screen API key is required",
    ):
        await client.screen.campaigns.list()
    assert not bool(recorder.transport.calls)
    await client.aclose()
