"""Synchronous CoderPad Screen API namespaces."""

import builtins
from collections.abc import Iterator, Sequence
from http import HTTPStatus
from uuid import UUID

from beartype import beartype
from pydantic import TypeAdapter

from coderpad._binary_content import (
    require_binary_transport,
    screen_archive_headers,
    validate_screen_archive,
)
from coderpad._screen_question import screen_question_path
from coderpad._screen_question_bank import (
    next_question_start,
    screen_bank_question_path,
    screen_created_question,
    screen_question_params,
    screen_questions_page,
)
from coderpad._screen_response import (
    json_object,
    json_value,
    require_screen_api_key,
)
from coderpad.exceptions import CoderPadError
from coderpad.screen_question_inputs import ScreenQuestionSave
from coderpad.screen_question_types import (
    ScreenCreatedQuestion,
    ScreenQuestionDetails,
    ScreenQuestionFilters,
    ScreenQuestionsPage,
    ScreenQuestionSummary,
)
from coderpad.screen_types import (
    ScreenAccount,
    ScreenAIConversation,
    ScreenCampaign,
    ScreenCampaignCreation,
    ScreenCampaignQuestion,
    ScreenCampaignSettings,
    ScreenCreatedCampaign,
    ScreenInvitation,
    ScreenInvitationResult,
    ScreenQuestionInsights,
    ScreenRandomQuestionSet,
    ScreenReport,
    ScreenTemporaryFile,
    ScreenTest,
    ScreenTestsPage,
    ScreenWebhook,
)
from coderpad.transports import JSONTransport, TransportResponse

SCREEN_US_BASE_URL = "https://screen.coderpad.io"
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
        default_headers: dict[str, str] | None,
    ) -> None:
        """Create shared Screen request state."""
        self.transport: JSONTransport = transport
        self.base_url: str = base_url.rstrip("/")
        self.api_key: str = api_key
        self.headers: dict[str, str] = {
            **(default_headers if default_headers is not None else {}),
            "API-Key": api_key,
        }

    def _request(
        self,
        *,
        method: str,
        path: str,
        params: dict[str, str | int] | None,
        json: object | None,
    ) -> TransportResponse:
        """Make a Screen request and map HTTP failures."""
        require_screen_api_key(api_key=self.api_key)
        response = self.transport(
            method=method,
            url=self.base_url + _SCREEN_PREFIX + path,
            headers=self.headers,
            params=params,
            data=None,
            files=None,
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
        response = self._request(
            method="GET", path="/campaigns", params=None, json=None
        )
        return ScreenCampaign.list_from_value(
            value=json_value(value=response.json())
        )

    def create(
        self,
        *,
        name: str,
        questions: Sequence[ScreenCampaignQuestion | ScreenRandomQuestionSet],
        settings: ScreenCampaignSettings | None = None,
        team_id: str | None = None,
    ) -> ScreenCreatedCampaign:
        """Create a campaign once, preserving omitted team defaults.

        Account feature restrictions and incompatible settings are reported
        by the service. Creation is never automatically retried.
        """
        campaign = ScreenCampaignCreation(
            name=name,
            questions=list(questions),
            settings=settings,
            team_id=team_id,
        )
        response = self._request(
            method="POST",
            path="/campaigns",
            params=None,
            json=campaign.model_dump(exclude_none=True),
        )
        return ScreenCreatedCampaign.model_validate(obj=response.json())

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
            json=invitation.model_dump(exclude_none=True),
            params=None,
        )
        return ScreenInvitationResult.from_dict(
            data=json_object(value=response.json())
        )


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
        response = self._request(
            method="GET", path="/tests", params=params, json=None
        )
        return ScreenTestsPage.from_dict(
            data=json_object(value=response.json())
        )

    def all(
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
        limit: int | None = None,
    ) -> Iterator[ScreenTest]:
        """Yield all tests across offset-paginated responses.

        Args:
            campaign_id: Filter by campaign id.
            status: Filter by status.
            tag: Filter by tag.
            search: Free-text search.
            product: Filter by product.
            candidate_email: Filter by candidate email.
            from_time: Lower bound timestamp.
            to_time: Upper bound timestamp.
            limit: Page size.

        Yields:
            Each test until ``pagination.has_more_items`` is false.
        """
        start: int | None = None
        while True:
            page = self.list(
                campaign_id=campaign_id,
                status=status,
                tag=tag,
                search=search,
                product=product,
                candidate_email=candidate_email,
                from_time=from_time,
                to_time=to_time,
                start=start,
                limit=limit,
            )
            yield from page.tests
            pagination = page.pagination
            if (
                pagination is None
                or not pagination.has_more_items
                or pagination.next_start is None
            ):
                break
            start = pagination.next_start

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
            json=None,
        )
        return ScreenTest.from_dict(data=json_object(value=response.json()))

    def cancel(self, *, test_id: int) -> None:
        """Cancel a test invitation."""
        _ = self._request(
            method="POST",
            path=f"/tests/{test_id}/actions/cancel",
            params=None,
            json=None,
        )

    def resend(self, *, test_id: int) -> None:
        """Resend a test invitation."""
        _ = self._request(
            method="POST",
            path=f"/tests/{test_id}/actions/resend",
            params=None,
            json=None,
        )

    def delete(self, *, test_id: int) -> None:
        """Delete a test session."""
        _ = self._request(
            method="DELETE", path=f"/tests/{test_id}", params=None, json=None
        )

    def ai_assist_conversations(
        self, *, test_id: int, question_id: str | UUID
    ) -> builtins.list[ScreenAIConversation]:
        """Retrieve PROJECT question conversations after completion or
        review.

        Conversation and message order and structured output are preserved.
        A missing project question raises the normal 404 error, and a test
        that is still running raises the normal 409 error.
        """
        path = screen_question_path(test_id=test_id, question_id=question_id)
        response = self._request(
            method="GET",
            path=path + "/ai-assist-conversations",
            params=None,
            json=None,
        )
        data = json_object(value=response.json())
        return TypeAdapter(
            type=builtins.list[ScreenAIConversation]
        ).validate_python(data.get("conversations", []))

    def project_archive(
        self, *, test_id: int, question_id: str | UUID
    ) -> bytes:
        """Download a compressed project archive with the candidate's
        changes applied.

        Returns the original binary archive without extracting it or writing
        files. Configure the client transport timeout for slow generation.
        HTTP and transport errors use the same contract as report downloads.
        """
        path = screen_question_path(test_id=test_id, question_id=question_id)
        response = self._request(
            method="GET", path=path + "/project", params=None, json=None
        )
        return response.content

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
            json=None,
        ).content

    def report_json(
        self,
        *,
        test_id: int,
        with_community_stats: bool = False,
    ) -> ScreenReport:
        """Return the typed JSON report embedded in a test session.

        The Screen ``/tests/{id}/report`` endpoint serves PDF bytes.
        Scored report fields are returned on ``GET /tests/{id}`` as
        ``ScreenTest.report``; this helper fetches that payload and
        returns the typed report.

        Args:
            test_id: The Screen test session id.
            with_community_stats: Whether to include community
                statistics on the report.

        Returns:
            The typed scored report.

        Raises:
            LookupError: If the test exists but has no report yet.
        """
        test = self.get(
            test_id=test_id,
            with_community_stats=with_community_stats,
        )
        if test.report is None:
            message = f"Screen test {test_id} has no scored report"
            raise LookupError(message)
        return test.report


@beartype
class ScreenQuestionsNamespace(_ScreenNamespace):
    """Screen question library reads and statistics."""

    def list(
        self,
        *,
        filters: ScreenQuestionFilters | None = None,
        start: int | None = None,
        limit: int | None = None,
    ) -> ScreenQuestionsPage:
        """List summaries with offset pagination and explicit filters."""
        response = self._request(
            method="GET",
            path="/questions",
            json=None,
            params=screen_question_params(
                filters=filters, start=start, limit=limit
            ),
        )
        return screen_questions_page(value=response.json())

    def all(
        self,
        *,
        filters: ScreenQuestionFilters | None = None,
        start: int = 0,
        limit: int | None = None,
    ) -> Iterator[ScreenQuestionSummary]:
        """Iterate summaries while retaining filters and rejecting repeated
        offsets.
        """
        while True:
            page = self.list(filters=filters, start=start, limit=limit)
            yield from page.questions
            next_start = next_question_start(page=page, current=start)
            if next_start is None:
                break
            start = next_start

    def get(self, *, question_id: str | UUID) -> ScreenQuestionDetails:
        """Retrieve a complete question by UUID."""
        response = self._request(
            method="GET",
            path=screen_bank_question_path(question_id=question_id),
            params=None,
            json=None,
        )
        return ScreenQuestionDetails.model_validate(obj=response.json())

    def create(self, *, question: ScreenQuestionSave) -> ScreenCreatedQuestion:
        """Create a question once, returning details and the Location
        header.
        """
        response = self._request(
            method="POST",
            path="/questions",
            params=None,
            json=question.model_dump(exclude_none=True, exclude_unset=True),
        )
        return screen_created_question(response=response)

    def update(
        self, *, question_id: str | UUID, question: ScreenQuestionSave
    ) -> ScreenQuestionDetails:
        """Save new content using only explicit writable fields, without
        retries.
        """
        response = self._request(
            method="PUT",
            path=screen_bank_question_path(question_id=question_id),
            params=None,
            json=question.model_dump(exclude_none=True, exclude_unset=True),
        )
        return ScreenQuestionDetails.model_validate(obj=response.json())

    def insights(
        self,
        *,
        question_id: str | UUID,
        programming_language: str | None = None,
    ) -> ScreenQuestionInsights:
        """Retrieve usage, answer, test-case, and score statistics."""
        path = screen_bank_question_path(question_id=question_id)
        params: dict[str, str | int] = {}
        if programming_language is not None:
            params["programming_language"] = programming_language
        response = self._request(
            method="GET", path=path + "/insights", params=params, json=None
        )
        return ScreenQuestionInsights.model_validate(obj=response.json())


@beartype
class ScreenTemporaryFilesNamespace(_ScreenNamespace):
    """Raw temporary uploads for Screen project questions."""

    def upload(self, *, content: bytes) -> ScreenTemporaryFile:
        """Upload raw bytes once and return their temporary identifier."""
        validate_screen_archive(content=content)
        require_screen_api_key(api_key=self.api_key)
        transport = require_binary_transport(transport=self.transport)
        response = transport(
            method="POST",
            url=self.base_url + _SCREEN_PREFIX + "/temporary-file",
            headers=screen_archive_headers(
                headers=self.headers, content=content
            ),
            params=None,
            data=None,
            files=None,
            json=None,
            content=content,
        )
        if response.status_code >= HTTPStatus.BAD_REQUEST:
            raise CoderPadError.from_response(response=response)
        return ScreenTemporaryFile.model_validate(obj=response.json())


@beartype
class ScreenWebhookNamespace(_ScreenNamespace):
    """Screen webhook operations."""

    def get(self) -> ScreenWebhook:
        """Retrieve webhook configuration."""
        response = self._request(
            method="GET", path="/webhook", params=None, json=None
        )
        return ScreenWebhook.from_dict(data=json_object(value=response.json()))

    def set(self, *, url: str) -> None:
        """Set or replace the webhook URL."""
        _ = self._request(
            method="POST", path="/webhook", json=url, params=None
        )

    def delete(self) -> None:
        """Delete the webhook configuration."""
        _ = self._request(
            method="DELETE", path="/webhook", params=None, json=None
        )


@beartype
class ScreenNamespace(_ScreenNamespace):
    """Root namespace for the synchronous Screen API."""

    def me(self) -> ScreenAccount:
        """Retrieve the Screen key owner and available teams."""
        response = self._request(
            method="GET", path="/me", params=None, json=None
        )
        return ScreenAccount.model_validate(obj=response.json())

    def __init__(
        self,
        *,
        transport: JSONTransport,
        api_key: str,
        base_url: str,
        default_headers: dict[str, str] | None = None,
    ) -> None:
        """Create the root Screen namespace."""
        super().__init__(
            transport=transport,
            api_key=api_key,
            base_url=base_url,
            default_headers=default_headers,
        )
        self.campaigns: ScreenCampaignsNamespace = ScreenCampaignsNamespace(
            transport=transport,
            api_key=api_key,
            base_url=base_url,
            default_headers=default_headers,
        )
        self.tests: ScreenTestsNamespace = ScreenTestsNamespace(
            transport=transport,
            api_key=api_key,
            base_url=base_url,
            default_headers=default_headers,
        )
        self.questions: ScreenQuestionsNamespace = ScreenQuestionsNamespace(
            transport=transport,
            api_key=api_key,
            base_url=base_url,
            default_headers=default_headers,
        )
        self.temporary_files: ScreenTemporaryFilesNamespace = (
            ScreenTemporaryFilesNamespace(
                transport=transport,
                api_key=api_key,
                base_url=base_url,
                default_headers=default_headers,
            )
        )
        self.webhook: ScreenWebhookNamespace = ScreenWebhookNamespace(
            transport=transport,
            api_key=api_key,
            base_url=base_url,
            default_headers=default_headers,
        )
