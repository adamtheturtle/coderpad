"""Types for the CoderPad Screen API."""

from dataclasses import dataclass, field
from typing import Self

from beartype import beartype


def _strings(value: object, /) -> list[str]:
    """Return a string list from an API value."""
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, str)]


def _optional_int(value: object, /) -> int | None:
    """Return an integer API value when present."""
    return (
        value
        if isinstance(value, int) and not isinstance(value, bool)
        else None
    )


def _optional_float(value: object, /) -> float | None:
    """Return a numeric API value when present."""
    return float(value) if isinstance(value, int | float) else None


def _optional_str(value: object, /) -> str | None:
    """Return a string API value when present."""
    return value if isinstance(value, str) else None


@beartype
@dataclass(frozen=True, kw_only=True)
class ScreenCampaign:
    """A reusable Screen assessment campaign."""

    id: int
    name: str
    languages: list[str] = field(default_factory=list)
    pinned: bool = False
    archived: bool = False

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> Self:
        """Create a campaign from an API response."""
        return cls(
            id=int(data["id"]),
            name=f"{data['name']}",
            languages=_strings(data.get("languages")),
            pinned=data.get("pinned") is True,
            archived=data.get("archived") is True,
        )


@beartype
@dataclass(frozen=True, kw_only=True)
class ScreenInvitation:
    """An invitation to a Screen campaign."""

    candidate_email: str | None = None
    candidate_name: str | None = None
    recruiter_email: str | None = None
    tags: str | None = None
    send_invitation_email: bool | None = None
    send_notification_email_on_bounce: bool | None = None

    def to_dict(self) -> dict[str, str | bool]:
        """Create the JSON request body, omitting unset fields."""
        values: dict[str, str | bool | None] = {
            "candidate_email": self.candidate_email,
            "candidate_name": self.candidate_name,
            "recruiter_email": self.recruiter_email,
            "tags": self.tags,
            "send_invitation_email": self.send_invitation_email,
            "send_notification_email_on_bounce": (
                self.send_notification_email_on_bounce
            ),
        }
        return {
            key: value for key, value in values.items() if value is not None
        }


@beartype
@dataclass(frozen=True, kw_only=True)
class ScreenInvitationResult:
    """The result of creating a Screen test invitation."""

    id: int | None
    test_url: str | None

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> Self:
        """Create an invitation result from an API response."""
        return cls(
            id=_optional_int(data.get("id")),
            test_url=_optional_str(data.get("test_url")),
        )


@beartype
@dataclass(frozen=True, kw_only=True)
class ScreenTestQuestion:
    """A question included in a Screen test."""

    id: int
    last_activity_time: int | None

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> Self:
        """Create a question from an API response."""
        return cls(
            id=int(data["id"]),
            last_activity_time=_optional_int(data.get("last_activity_time")),
        )


@beartype
@dataclass(frozen=True, kw_only=True)
class ScreenSkillResult:
    """A scored skill within a Screen report."""

    points: int | None
    score: float | None
    total_points: int | None

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> Self:
        """Create a skill result from an API response."""
        return cls(
            points=_optional_int(data.get("points")),
            score=_optional_float(data.get("score")),
            total_points=_optional_int(data.get("total_points")),
        )


@beartype
@dataclass(frozen=True, kw_only=True)
class ScreenTechnologyResult:
    """A scored technology within a Screen report."""

    points: int | None
    score: float | None
    skills: dict[str, ScreenSkillResult]
    total_points: int | None
    comparative_score: float | None

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> Self:
        """Create a technology result from an API response."""
        raw_skills = data.get("skills")
        skills = (
            {
                name: ScreenSkillResult.from_dict(data=value)
                for name, value in raw_skills.items()
                if isinstance(name, str) and isinstance(value, dict)
            }
            if isinstance(raw_skills, dict)
            else {}
        )
        return cls(
            points=_optional_int(data.get("points")),
            score=_optional_float(data.get("score")),
            skills=skills,
            total_points=_optional_int(data.get("total_points")),
            comparative_score=_optional_float(data.get("comparative_score")),
        )


@beartype
@dataclass(frozen=True, kw_only=True)
class ScreenReport:
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
    def from_dict(cls, data: dict[str, object]) -> Self:
        """Create a report from an API response."""
        raw_technologies = data.get("technologies")
        technologies = (
            {
                name: ScreenTechnologyResult.from_dict(data=value)
                for name, value in raw_technologies.items()
                if isinstance(name, str) and isinstance(value, dict)
            }
            if isinstance(raw_technologies, dict)
            else {}
        )
        raw_community_stats = data.get("community_stats")
        community_stats = (
            [
                item
                for item in raw_community_stats
                if isinstance(item, int) and not isinstance(item, bool)
            ]
            if isinstance(raw_community_stats, list)
            else None
        )
        return cls(
            duration=_optional_int(data.get("duration")),
            warnings=_strings(data.get("warnings")),
            points=_optional_int(data.get("points")),
            score=_optional_float(data.get("score")),
            technologies=technologies,
            total_duration=_optional_int(data.get("total_duration")),
            total_points=_optional_int(data.get("total_points")),
            comparative_score=_optional_float(data.get("comparative_score")),
            community_stats=community_stats,
        )


@beartype
@dataclass(frozen=True, kw_only=True)
class ScreenTest:
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
    def from_dict(cls, data: dict[str, object]) -> Self:
        """Create a test session from an API response."""
        raw_report = data.get("report")
        raw_questions = data.get("questions")
        return cls(
            id=int(data["id"]),
            status=f"{data.get('status', 'unknown')}",
            campaign_id=_optional_int(data.get("campaign_id")),
            candidate_name=_optional_str(data.get("candidate_name")),
            candidate_email=_optional_str(data.get("candidate_email")),
            tags=_strings(data.get("tags")),
            send_time=_optional_int(data.get("send_time")),
            start_time=_optional_int(data.get("start_time")),
            end_time=_optional_int(data.get("end_time")),
            last_activity_time=_optional_int(data.get("last_activity_time")),
            url=_optional_str(data.get("url")),
            test_url=_optional_str(data.get("test_url")),
            report=ScreenReport.from_dict(data=raw_report)
            if isinstance(raw_report, dict)
            else None,
            questions=[
                ScreenTestQuestion.from_dict(data=item)
                for item in raw_questions
                if isinstance(item, dict)
            ]
            if isinstance(raw_questions, list)
            else [],
        )


@beartype
@dataclass(frozen=True, kw_only=True)
class ScreenPagination:
    """Offset pagination metadata returned by Screen."""

    start: int | None
    limit: int | None
    total: int | None
    has_more_items: bool
    next_start: int | None

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> Self:
        """Create pagination metadata from an API response."""
        return cls(
            start=_optional_int(data.get("start")),
            limit=_optional_int(data.get("limit")),
            total=_optional_int(data.get("total")),
            has_more_items=data.get("has_more_items") is True,
            next_start=_optional_int(data.get("next_start")),
        )


@beartype
@dataclass(frozen=True, kw_only=True)
class ScreenTestsPage:
    """One page of Screen test sessions."""

    tests: list[ScreenTest]
    pagination: ScreenPagination | None

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> Self:
        """Create a tests page from an API response."""
        raw_tests = data.get("tests")
        raw_pagination = data.get("pagination")
        return cls(
            tests=[
                ScreenTest.from_dict(data=item)
                for item in raw_tests
                if isinstance(item, dict)
            ]
            if isinstance(raw_tests, list)
            else [],
            pagination=ScreenPagination.from_dict(data=raw_pagination)
            if isinstance(raw_pagination, dict)
            else None,
        )


@beartype
@dataclass(frozen=True, kw_only=True)
class ScreenWebhook:
    """The configured Screen webhook."""

    url: str | None

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> Self:
        """Create webhook configuration from an API response."""
        return cls(url=_optional_str(data.get("url")))
