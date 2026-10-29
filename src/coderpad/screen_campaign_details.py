"""Read models for complete Screen assessment campaign definitions."""

from typing import ClassVar

from pydantic import BaseModel, ConfigDict


class _CampaignReadModel(BaseModel):
    """Accept additive response fields without changing write
    validation.
    """

    model_config: ClassVar[ConfigDict] = ConfigDict(
        frozen=True, extra="ignore", strict=True
    )


class ScreenRandomQuestionConfigurationDetails(_CampaignReadModel):
    """Criteria of a randomly selected question set."""

    domain: str | None = None
    skills: list[str] | None = None
    question_type: str | None = None
    target_duration_minutes: int | None = None
    target_experience_level: str | None = None
    included_question_ids: list[str] | None = None
    excluded_question_ids: list[str] | None = None


class ScreenCampaignQuestionDetails(_CampaignReadModel):
    """An ordered explicit question or random set in a campaign."""

    type: str
    question_id: str | None = None
    configuration: ScreenRandomQuestionConfigurationDetails | None = None


class ScreenCampaignTimerDetails(_CampaignReadModel):
    """The campaign's timer mode and optional duration."""

    mode: str | None = None
    duration_minutes: int | None = None


class ScreenCampaignAccessPeriodDetails(_CampaignReadModel):
    """Access-window instants, preserved as ISO 8601 strings."""

    min_start_time: str | None = None
    max_end_time: str | None = None


class ScreenCampaignFollowUpQuestionsDetails(_CampaignReadModel):
    """Follow-up question availability and answer format."""

    enabled: bool | None = None
    answer_format: str | None = None


class ScreenCampaignWebcamProctoringDetails(_CampaignReadModel):
    """Webcam recording and analysis settings."""

    enabled: bool | None = None
    ai_analysis_enabled: bool | None = None


class ScreenCampaignSettingsDetails(_CampaignReadModel):
    """Returned campaign settings, retaining omission, false, and empty
    values.
    """

    languages: list[str] | None = None
    timer: ScreenCampaignTimerDetails | None = None
    invitation_expiration_days: int | None = None
    access_period: ScreenCampaignAccessPeriodDetails | None = None
    send_candidate_simplified_report: bool | None = None
    copy_paste_blocked: bool | None = None
    follow_up_questions: ScreenCampaignFollowUpQuestionsDetails | None = None
    webcam_proctoring: ScreenCampaignWebcamProctoringDetails | None = None
    full_screen_required: bool | None = None
    ai_assist_enabled: bool | None = None
    enabled_coding_agents: str | None = None


class ScreenCampaignDetails(_CampaignReadModel):
    """A complete reusable assessment definition, separate from test
    sessions.
    """

    id: int
    name: str
    questions: list[ScreenCampaignQuestionDetails]
    settings: ScreenCampaignSettingsDetails | None = None
    team_id: str | None = None
