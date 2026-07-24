"""Synchronous CoderPad Screen API namespaces."""

import builtins
from http import HTTPStatus

from beartype import beartype

from coderpad.exceptions import CoderPadError
from coderpad.screen_types import (
    ScreenCampaign,
    ScreenInvitation,
    ScreenInvitationResult,
    ScreenTest,
    ScreenTestsPage,
    ScreenWebhook,
)
from coderpad.transports import JSONTransport, TransportResponse

SCREEN_US_BASE_URL = "https://www.codingame.com"
SCREEN_EU_BASE_URL = "https://www.codingame.eu"
_SCREEN_PREFIX = "/assessment/api/v1.1"


@beartype
class _ScreenNamespace:
    """Shared synchronous Screen request handling."""

    def __init__(
        self,
        *,
        transport: JSONTransport,
        api_key: str,
        base_url: str,
    ) -> None:
        """Create shared Screen request state."""
        self.transport: JSONTransport = transport
        self.base_url: str = base_url.rstrip("/")
        self.headers: dict[str, str] = {"API-Key": api_key}

    def _request(
        self,
        *,
        method: str,
        path: str,
        params: dict[str, str | int] | None = None,
        json: object | None = None,
    ) -> TransportResponse:
        """Make a Screen request and map HTTP failures."""
        response = self.transport(
            method=method,
            url=self.base_url + _SCREEN_PREFIX + path,
            headers=self.headers,
            params=params,
            json=json,
        )
        if response.status_code >= HTTPStatus.BAD_REQUEST:
            raise CoderPadError.from_response(response=response)
        return response


@beartype
class ScreenCampaignsNamespace(_ScreenNamespace):
    """Screen campaign operations."""

    def list(self) -> builtins.list[ScreenCampaign]:
        """List assessment campaigns."""
        response = self._request(method="GET", path="/campaigns")
        raw_campaigns: object = response.json()
        return ScreenCampaign.list_from_value(value=raw_campaigns)

    def send_invitation(
        self,
        *,
        campaign_id: int,
        invitation: ScreenInvitation,
    ) -> ScreenInvitationResult:
        """Create a test session and optionally email the candidate."""
        response = self._request(
            method="POST",
            path=f"/campaigns/{campaign_id}/actions/send",
            json=invitation.to_dict(),
        )
        return ScreenInvitationResult.from_dict(data=response.json())


@beartype
class ScreenTestsNamespace(_ScreenNamespace):
    """Screen test-session operations."""

    def list(
        self,
        *,
        campaign_id: int | None = None,
        status: str | None = None,
        tag: str | None = None,
        search: str | None = None,
        product: str | None = None,
        candidate_email: str | None = None,
        from_time: int | None = None,
        to_time: int | None = None,
        start: int | None = None,
        limit: int | None = None,
    ) -> ScreenTestsPage:
        """List one offset-paginated page of tests.

        Pass ``page.pagination.next_start`` to ``start`` while
        ``has_more_items`` is true to traverse subsequent pages.
        """
        params: dict[str, str | int] = {}
        values: tuple[tuple[str, str | int | None], ...] = (
            ("campaignId", campaign_id),
            ("status", status),
            ("tag", tag),
            ("search", search),
            ("product", product),
            ("candidateEmail", candidate_email),
            ("from", from_time),
            ("to", to_time),
            ("start", start),
            ("limit", limit),
        )
        params.update(
            (key, value) for key, value in values if value is not None
        )
        response = self._request(method="GET", path="/tests", params=params)
        return ScreenTestsPage.from_dict(data=response.json())

    def get(
        self,
        *,
        test_id: int,
        with_community_stats: bool = False,
    ) -> ScreenTest:
        """Retrieve one test session."""
        params: dict[str, str | int] = (
            {"withCommunityStats": "true"} if with_community_stats else {}
        )
        response = self._request(
            method="GET",
            path=f"/tests/{test_id}",
            params=params,
        )
        return ScreenTest.from_dict(data=response.json())

    def cancel(self, *, test_id: int) -> None:
        """Cancel a test invitation."""
        self._request(method="POST", path=f"/tests/{test_id}/actions/cancel")

    def resend(self, *, test_id: int) -> None:
        """Resend a test invitation."""
        self._request(method="POST", path=f"/tests/{test_id}/actions/resend")

    def delete(self, *, test_id: int) -> None:
        """Delete a test session."""
        self._request(method="DELETE", path=f"/tests/{test_id}")

    def report(
        self,
        *,
        test_id: int,
        report_type: str | None = None,
        anonymous: bool | None = None,
        include_rank: bool | None = None,
        include_comparative_score: bool | None = None,
    ) -> bytes:
        """Download a test report without writing it to disk."""
        params: dict[str, str | int] = {}
        values: tuple[tuple[str, str | bool | None], ...] = (
            ("report_type", report_type),
            ("anonymous", anonymous),
            ("include_rank", include_rank),
            ("include_comparative_score", include_comparative_score),
        )
        for key, value in values:
            if isinstance(value, bool):
                params[key] = "true" if value else "false"
            elif value is not None:
                params[key] = value
        return self._request(
            method="GET",
            path=f"/tests/{test_id}/report",
            params=params,
        ).content


@beartype
class ScreenWebhookNamespace(_ScreenNamespace):
    """Screen webhook operations."""

    def get(self) -> ScreenWebhook:
        """Retrieve webhook configuration."""
        response = self._request(method="GET", path="/webhook")
        return ScreenWebhook.from_dict(data=response.json())

    def set(self, *, url: str) -> None:
        """Set or replace the webhook URL."""
        self._request(method="POST", path="/webhook", json=url)

    def delete(self) -> None:
        """Delete the webhook configuration."""
        self._request(method="DELETE", path="/webhook")


@beartype
class ScreenNamespace(_ScreenNamespace):
    """Root namespace for the synchronous Screen API."""

    def __init__(
        self,
        *,
        transport: JSONTransport,
        api_key: str,
        base_url: str,
    ) -> None:
        """Create the root Screen namespace."""
        super().__init__(
            transport=transport,
            api_key=api_key,
            base_url=base_url,
        )
        self.campaigns: ScreenCampaignsNamespace = ScreenCampaignsNamespace(
            transport=transport,
            api_key=api_key,
            base_url=base_url,
        )
        self.tests: ScreenTestsNamespace = ScreenTestsNamespace(
            transport=transport,
            api_key=api_key,
            base_url=base_url,
        )
        self.webhook: ScreenWebhookNamespace = ScreenWebhookNamespace(
            transport=transport,
            api_key=api_key,
            base_url=base_url,
        )
