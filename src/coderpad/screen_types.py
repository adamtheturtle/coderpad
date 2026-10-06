"""Types for the CoderPad Screen API."""

from typing import Annotated, ClassVar, Literal, Self, override

from beartype import beartype
from pydantic import BaseModel, ConfigDict, Field, model_validator

from coderpad.json_types import JsonValue


class _APIModel(BaseModel):
    """Base model shared by CoderPad Screen API resources."""

    model_config: ClassVar[ConfigDict] = ConfigDict(
        frozen=True,
        extra="ignore",
        strict=True,
    )


@beartype
def _json_values(value: JsonValue) -> list[JsonValue]:
    """Return a JSON list from an API value."""
    return value if isinstance(value, list) else []


@beartype
def _mapping(value: JsonValue) -> dict[str, JsonValue] | None:
    """Return a string-keyed mapping from an API value."""
    return value if isinstance(value, dict) else None


@beartype
def _strings(value: JsonValue) -> list[str]:
    """Return a string list from an API value."""
    return [
        item for item in _json_values(value=value) if isinstance(item, str)
    ]


@beartype
def _empty_strings() -> list[str]:
    """Create an empty string list."""
    return []


@beartype
def _optional_int(value: JsonValue) -> int | None:
    """Return an integer API value when present."""
    return (
        value
        if isinstance(value, int) and not isinstance(value, bool)
        else None
    )


@beartype
def _required_int(value: JsonValue) -> int:
    """Return a required integer API value."""
    if isinstance(value, int) and not isinstance(value, bool):
        return value
    msg = "Expected an integer API value"
    raise TypeError(msg)


@beartype
def _optional_float(value: JsonValue) -> float | None:
    """Return a numeric API value when present."""
    return (
        float(value)
        if isinstance(value, int | float) and not isinstance(value, bool)
        else None
    )


@beartype
def _optional_str(value: JsonValue) -> str | None:
    """Return a string API value when present."""
    return value if isinstance(value, str) else None


@beartype
class ScreenCampaign(_APIModel):
    """A reusable Screen assessment campaign."""

    id: int
    name: str
    languages: list[str] = Field(default_factory=_empty_strings)
    pinned: bool = False
    archived: bool = False

    @classmethod
    def list_from_value(cls, value: JsonValue) -> list[Self]:
        """Create campaigns from an API response value."""
        return [
            cls.from_dict(data=mapping)
            for item in _json_values(value=value)
            if (mapping := _mapping(value=item)) is not None
        ]

    @classmethod
    def from_dict(cls, data: dict[str, JsonValue]) -> Self:
        """Create a campaign from an API response."""
        return cls(
            id=_required_int(value=data["id"]),
            name=f"{data['name']}",
            languages=_strings(value=data.get("languages")),
            pinned=data.get("pinned") is True,
            archived=data.get("archived") is True,
        )


@beartype
class ScreenInvitation(_APIModel):
    """An invitation to a Screen campaign.

    Omit candidate identity to create a link the recruiter can share manually.
    Email delivery requires ``candidate_email``. Unspecified delivery uses the
    server default, which sends email only when an address is supplied.
    """

    candidate_email: str | None = None
    candidate_name: str | None = None
    recruiter_email: str | None = None
    tags: str | None = None
    send_invitation_email: bool | None = None
    send_notification_email_on_bounce: bool | None = None
    allow_duplicate_invitations: bool | None = None

    @model_validator(mode="after")
    def require_delivery_address(self) -> Self:
        """Require an address when email delivery is explicitly
        enabled.
        """
        if self.send_invitation_email is True and not bool(
            self.candidate_email
        ):
            msg = (
                "candidate_email is required when "
                "send_invitation_email is true"
            )
            raise ValueError(msg)
        return self


@beartype
class ScreenInvitationResult(_APIModel):
    """The result of creating a Screen test invitation."""

    id: int | None
    test_url: str | None

    @classmethod
    def from_dict(cls, data: dict[str, JsonValue]) -> Self:
        """Create an invitation result from an API response."""
        return cls(
            id=_optional_int(value=data.get("id")),
            test_url=_optional_str(value=data.get("test_url")),
        )


@beartype
class ScreenTestQuestion(_APIModel):
    """A question included in a Screen test."""

    id: int
    last_activity_time: int | None

    @classmethod
    def from_dict(cls, data: dict[str, JsonValue]) -> Self:
        """Create a question from an API response."""
        return cls(
            id=_required_int(value=data["id"]),
            last_activity_time=_optional_int(
                value=data.get("last_activity_time")
            ),
        )


@beartype
class ScreenSkillResult(_APIModel):
    """A scored skill within a Screen report."""

    points: int | None
    score: float | None
    total_points: int | None

    @classmethod
    def from_dict(cls, data: dict[str, JsonValue]) -> Self:
        """Create a skill result from an API response."""
        return cls(
            points=_optional_int(value=data.get("points")),
            score=_optional_float(value=data.get("score")),
            total_points=_optional_int(value=data.get("total_points")),
        )


@beartype
class ScreenTechnologyResult(_APIModel):
    """A scored technology within a Screen report."""

    points: int | None
    score: float | None
    skills: dict[str, ScreenSkillResult]
    total_points: int | None
    comparative_score: float | None

    @classmethod
    def from_dict(cls, data: dict[str, JsonValue]) -> Self:
        """Create a technology result from an API response."""
        typed_skills = _mapping(value=data.get("skills"))
        skills = (
            {
                name: ScreenSkillResult.from_dict(data=mapped)
                for name, raw_value in typed_skills.items()
                if (mapped := _mapping(value=raw_value)) is not None
            }
            if typed_skills is not None
            else {}
        )
        return cls(
            points=_optional_int(value=data.get("points")),
            score=_optional_float(value=data.get("score")),
            skills=skills,
            total_points=_optional_int(value=data.get("total_points")),
            comparative_score=_optional_float(
                value=data.get("comparative_score")
            ),
        )


@beartype
class ScreenReport(_APIModel):
    """A candidate's scored Screen report."""

    duration: int | None
    warnings: list[str]
    points: int | None
    score: float | None
    technologies: dict[str, ScreenTechnologyResult]
    total_duration: int | None
    total_points: int | None
    comparative_score: float | None
    community_stats: list[int] | None

    @classmethod
    def from_dict(cls, data: dict[str, JsonValue]) -> Self:
        """Create a report from an API response."""
        typed_technologies = _mapping(value=data.get("technologies"))
        technologies = (
            {
                name: ScreenTechnologyResult.from_dict(data=mapped)
                for name, raw_value in typed_technologies.items()
                if (mapped := _mapping(value=raw_value)) is not None
            }
            if typed_technologies is not None
            else {}
        )
        raw_community_stats: JsonValue = data.get("community_stats")
        community_items = _json_values(value=raw_community_stats)
        community_stats = (
            [
                item
                for item in community_items
                if isinstance(item, int) and not isinstance(item, bool)
            ]
            if isinstance(raw_community_stats, list)
            else None
        )
        return cls(
            duration=_optional_int(value=data.get("duration")),
            warnings=_strings(value=data.get("warnings")),
            points=_optional_int(value=data.get("points")),
            score=_optional_float(value=data.get("score")),
            technologies=technologies,
            total_duration=_optional_int(value=data.get("total_duration")),
            total_points=_optional_int(value=data.get("total_points")),
            comparative_score=_optional_float(
                value=data.get("comparative_score")
            ),
            community_stats=community_stats,
        )


@beartype
class ScreenTest(_APIModel):
    """A candidate's Screen test session."""

    id: int
    status: str
    campaign_id: int | None
    candidate_name: str | None
    candidate_email: str | None
    tags: list[str]
    send_time: int | None
    start_time: int | None
    end_time: int | None
    last_activity_time: int | None
    url: str | None
    test_url: str | None
    report: ScreenReport | None
    questions: list[ScreenTestQuestion]

    @classmethod
    def from_dict(cls, data: dict[str, JsonValue]) -> Self:
        """Create a test session from an API response."""
        raw_report = _mapping(value=data.get("report"))
        typed_questions = _json_values(value=data.get("questions"))
        status = _optional_str(value=data.get("status"))
        return cls(
            id=_required_int(value=data["id"]),
            status=status if status is not None else "unknown",
            campaign_id=_optional_int(value=data.get("campaign_id")),
            candidate_name=_optional_str(value=data.get("candidate_name")),
            candidate_email=_optional_str(value=data.get("candidate_email")),
            tags=_strings(value=data.get("tags")),
            send_time=_optional_int(value=data.get("send_time")),
            start_time=_optional_int(value=data.get("start_time")),
            end_time=_optional_int(value=data.get("end_time")),
            last_activity_time=_optional_int(
                value=data.get("last_activity_time")
            ),
            url=_optional_str(value=data.get("url")),
            test_url=_optional_str(value=data.get("test_url")),
            report=ScreenReport.from_dict(data=raw_report)
            if raw_report is not None
            else None,
            questions=[
                ScreenTestQuestion.from_dict(data=mapping)
                for item in typed_questions
                if (mapping := _mapping(value=item)) is not None
            ],
        )


@beartype
class ScreenPagination(_APIModel):
    """Offset pagination metadata returned by Screen."""

    start: int | None
    limit: int | None
    total: int | None
    has_more_items: bool
    next_start: int | None

    @classmethod
    def from_dict(cls, data: dict[str, JsonValue]) -> Self:
        """Create pagination metadata from an API response."""
        return cls(
            start=_optional_int(value=data.get("start")),
            limit=_optional_int(value=data.get("limit")),
            total=_optional_int(value=data.get("total")),
            has_more_items=data.get("has_more_items") is True,
            next_start=_optional_int(value=data.get("next_start")),
        )


@beartype
class ScreenTestsPage(_APIModel):
    """One page of Screen test sessions."""

    tests: list[ScreenTest]
    pagination: ScreenPagination | None

    @classmethod
    def from_dict(cls, data: dict[str, JsonValue]) -> Self:
        """Create a tests page from an API response."""
        typed_tests = _json_values(value=data.get("tests"))
        raw_pagination = _mapping(value=data.get("pagination"))
        return cls(
            tests=[
                ScreenTest.from_dict(data=mapping)
                for item in typed_tests
                if (mapping := _mapping(value=item)) is not None
            ],
            pagination=ScreenPagination.from_dict(data=raw_pagination)
            if raw_pagination is not None
            else None,
        )

    @override
    def __repr__(self) -> str:
        """Return a concise debug representation."""
        return (
            f"ScreenTestsPage(tests={len(self.tests)}, "
            f"pagination={self.pagination!r})"
        )


@beartype
class ScreenWebhook(_APIModel):
    """The configured Screen webhook."""

    url: str | None

    @classmethod
    def from_dict(cls, data: dict[str, JsonValue]) -> Self:
        """Create webhook configuration from an API response."""
        return cls(url=_optional_str(value=data.get("url")))


@beartype
class ScreenTeam(_APIModel):
    """A team available to the Screen API key owner."""

    id: str
    name: str
    is_default: bool


@beartype
class ScreenAccount(_APIModel):
    """Organization, recruiter, and team identity for a Screen API key."""

    organization_id: str
    recruiter_id: str
    teams: list[ScreenTeam]


class _CampaignRequestModel(_APIModel):
    """Reject unknown campaign options instead of silently dropping
    them.
    """

    model_config: ClassVar[ConfigDict] = ConfigDict(
        frozen=True,
        extra="forbid",
        strict=True,
    )


@beartype
class ScreenRandomQuestionConfiguration(_CampaignRequestModel):
    """Criteria for a randomly selected set of Screen questions."""

    domain: str | None = None
    skills: list[str] | None = None
    question_type: Literal["QUIZ", "CODE"] | None = None
    target_duration_minutes: int | None = None
    target_experience_level: Literal["JUNIOR", "SENIOR", "EXPERT"] | None = (
        None
    )
    included_question_ids: list[str] | None = None
    excluded_question_ids: list[str] | None = None

    @model_validator(mode="after")
    def validate_question_selection(self) -> Self:
        """Keep inclusion and exclusion lists mutually exclusive."""
        if (
            self.included_question_ids is not None
            and self.excluded_question_ids is not None
        ):
            message = (
                "included_question_ids and excluded_question_ids "
                "are mutually exclusive"
            )
            raise ValueError(message)
        return self


@beartype
class ScreenCampaignQuestion(_CampaignRequestModel):
    """One explicitly selected question, identified by UUID."""

    type: Literal["QUESTION"] = "QUESTION"
    question_id: str


@beartype
class ScreenRandomQuestionSet(_CampaignRequestModel):
    """A random set of questions in campaign order."""

    type: Literal["RANDOM_QUESTION_SET"] = "RANDOM_QUESTION_SET"
    configuration: ScreenRandomQuestionConfiguration


@beartype
class ScreenCampaignTimer(_CampaignRequestModel):
    """An optional campaign timer override."""

    mode: Literal["PER_QUESTION", "GLOBAL", "UNLIMITED"] | None = None
    duration_minutes: int | None = None


@beartype
class ScreenCampaignAccessPeriod(_CampaignRequestModel):
    """An optional access window using ISO 8601 instants."""

    min_start_time: str | None = None
    max_end_time: str | None = None


@beartype
class ScreenCampaignFollowUpQuestions(_CampaignRequestModel):
    """Optional follow-up questions and their answer format."""

    enabled: bool | None = None
    answer_format: Literal["TEXT", "VIDEO", "AUDIO"] | None = None


@beartype
class ScreenCampaignWebcamProctoring(_CampaignRequestModel):
    """Optional webcam recording and AI analysis settings."""

    enabled: bool | None = None
    ai_analysis_enabled: bool | None = None


@beartype
class ScreenCampaignSettings(_CampaignRequestModel):
    """Campaign overrides, with omitted values inheriting team
    defaults.
    """

    languages: list[str] | None = None
    timer: ScreenCampaignTimer | None = None
    invitation_expiration_days: int | None = None
    access_period: ScreenCampaignAccessPeriod | None = None
    send_candidate_simplified_report: bool | None = None
    copy_paste_blocked: bool | None = None
    follow_up_questions: ScreenCampaignFollowUpQuestions | None = None
    webcam_proctoring: ScreenCampaignWebcamProctoring | None = None
    full_screen_required: bool | None = None
    ai_assist_enabled: bool | None = None
    enabled_coding_agents: str | None = None


@beartype
class ScreenCampaignCreation(_CampaignRequestModel):
    """A new Screen campaign with ordered question entries."""

    name: str = Field(min_length=3, max_length=64)
    questions: list[
        Annotated[
            ScreenCampaignQuestion | ScreenRandomQuestionSet,
            Field(discriminator="type"),
        ]
    ] = Field(min_length=1)
    settings: ScreenCampaignSettings | None = None
    team_id: str | None = None


@beartype
class ScreenCreatedCampaign(_APIModel):
    """The integer ID returned after campaign creation."""

    id: int


@beartype
class ScreenAIMessage(_APIModel):
    """An ordered candidate or assistant message with original JSON output."""

    id: str
    role: Literal["USER", "ASSISTANT"]
    creation_time: str | None = None
    output_items: list[JsonValue] | None = None


@beartype
def _empty_ai_messages() -> list[ScreenAIMessage]:
    """Create an empty ordered message list."""
    return []


@beartype
class ScreenAIConversation(_APIModel):
    """A candidate PROJECT question conversation with AI Assist."""

    id: str
    subject: str | None = None
    creation_time: str | None = None
    messages: list[ScreenAIMessage] = Field(default_factory=_empty_ai_messages)
