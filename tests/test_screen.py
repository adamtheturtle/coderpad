"""Tests for synchronous CoderPad Screen support."""

# ruff: noqa: PLR0911, PLR2004

import json
from http import HTTPStatus

import pytest

from coderpad import SCREEN_EU_BASE_URL, CoderPad
from coderpad.exceptions import AuthenticationError
from coderpad.screen_types import ScreenInvitation
from coderpad.transports import TransportResponse

_TEST = {
    "id": 11,
    "status": "completed",
    "campaign_id": 7,
    "candidate_name": "Ada",
    "candidate_email": "ada@example.com",
    "tags": ["python"],
    "send_time": 1000,
    "questions": [{"id": 3, "last_activity_time": 1100}],
    "report": {
        "score": 90,
        "technologies": {
            "Python": {
                "score": 95,
                "skills": {
                    "Language": {
                        "points": 9,
                        "score": 90,
                        "total_points": 10,
                    },
                },
            },
        },
        "community_stats": [1, 2, 3],
    },
}


class _ScreenTransport:
    """Record requests and return representative Screen responses."""

    def __init__(self, *, error: bool = False) -> None:
        """Create a recording transport."""
        self.calls: list[dict[str, object]] = []
        self.error = error

    def __call__(
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
            return _response(
                [
                    {
                        "id": 7,
                        "name": "Backend",
                        "languages": ["python"],
                    },
                ],
            )
        if url.endswith("/campaigns/7/actions/send"):
            return _response({"id": 11, "test_url": "https://test.example"})
        if url.endswith("/tests"):
            return _response(
                {
                    "tests": [_TEST],
                    "pagination": {
                        "start": 0,
                        "limit": 1,
                        "total": 2,
                        "has_more_items": True,
                        "next_start": 1,
                    },
                },
            )
        if url.endswith("/tests/11/report"):
            return TransportResponse(
                status_code=HTTPStatus.OK,
                headers={"content-type": "application/pdf"},
                content=b"%PDF report",
            )
        if url.endswith("/tests/11"):
            return _response(_TEST)
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
        content=json.dumps(obj=value).encode(),
    )


def _client(
    transport: _ScreenTransport,
    /,
    *,
    base_url: str = SCREEN_EU_BASE_URL,
) -> CoderPad:
    """Create a client using the recording transport."""
    return CoderPad(
        api_key="interview-key",
        screen_api_key="screen-key",
        screen_base_url=base_url,
        transport=transport,
    )


def test_campaigns_and_invitation() -> None:
    """Campaigns and invitations use Screen authentication and JSON."""
    transport = _ScreenTransport()
    client = _client(transport)
    campaigns = client.screen.campaigns.list()
    invitation = ScreenInvitation(candidate_email="ada@example.com")
    result = client.screen.campaigns.send_invitation(
        campaign_id=campaigns[0].id,
        invitation=invitation,
    )
    assert campaigns[0].languages == ["python"]
    assert not campaigns[0].pinned
    assert not campaigns[0].archived
    assert result.id == 11
    assert result.test_url == "https://test.example"
    assert transport.calls[0]["headers"] == {"API-Key": "screen-key"}
    assert transport.calls[1]["json"] == {"candidate_email": "ada@example.com"}
    assert f"{transport.calls[0]['url']}".startswith(SCREEN_EU_BASE_URL)


def test_tests_filters_pagination_and_decoding() -> None:
    """Test list filters, pagination, and nested models are preserved."""
    transport = _ScreenTransport()
    page = _client(transport).screen.tests.list(
        campaign_id=7,
        status="completed",
        tag="python",
        search="Ada",
        product="screen",
        candidate_email="ada@example.com",
        from_time=100,
        to_time=200,
        start=0,
        limit=1,
    )
    assert page.pagination is not None
    assert page.pagination.next_start == 1
    assert page.pagination.has_more_items
    assert page.tests[0].send_time == 1000
    assert page.tests[0].last_activity_time is None
    assert page.tests[0].test_url is None
    assert page.tests[0].questions[0].last_activity_time == 1100
    assert page.tests[0].report is not None
    screen_report = page.tests[0].report
    assert screen_report.duration is None
    assert not screen_report.warnings
    assert screen_report.points is None
    assert screen_report.score == 90
    assert screen_report.total_duration is None
    assert screen_report.total_points is None
    assert screen_report.comparative_score is None
    assert screen_report.community_stats == [1, 2, 3]
    technology = screen_report.technologies["Python"]
    assert technology.points is None
    assert technology.score == 95
    assert technology.total_points is None
    assert technology.comparative_score is None
    skill = technology.skills["Language"]
    assert skill.points == 9
    assert skill.score == 90
    assert skill.total_points == 10
    assert transport.calls[-1]["params"] == {
        "campaignId": 7,
        "status": "completed",
        "tag": "python",
        "search": "Ada",
        "product": "screen",
        "candidateEmail": "ada@example.com",
        "from": 100,
        "to": 200,
        "start": 0,
        "limit": 1,
    }


def test_get_actions_report_and_webhook() -> None:
    """Test retrieval, mutations, PDF bytes, and webhook operations."""
    transport = _ScreenTransport()
    screen = _client(transport).screen
    test = screen.tests.get(test_id=11, with_community_stats=True)
    screen.tests.cancel(test_id=11)
    screen.tests.resend(test_id=11)
    screen.tests.delete(test_id=11)
    report = screen.tests.report(
        test_id=11,
        report_type="simplified",
        anonymous=True,
    )
    webhook = screen.webhook.get()
    screen.webhook.set(url="https://example.com/new-hook")
    screen.webhook.delete()
    assert test.candidate_name == "Ada"
    assert transport.calls[0]["params"] == {"withCommunityStats": "true"}
    assert report == b"%PDF report"
    assert webhook.url == "https://example.com/hook"
    assert transport.calls[-2]["json"] == "https://example.com/new-hook"


def test_screen_errors_use_existing_hierarchy() -> None:
    """Screen HTTP failures map to the shared exception hierarchy."""
    with pytest.raises(expected_exception=AuthenticationError):
        _client(_ScreenTransport(error=True)).screen.campaigns.list()
