"""TypedDict types describing raw API response shapes."""

from typing import NotRequired, TypedDict


class TeamDict(TypedDict):
    """A team within an organization."""

    id: str
    name: str


class PadDict(TypedDict):
    """A CoderPad interview pad."""

    id: str
    title: str
    state: str
    owner_email: str
    language: str | None
    private: bool
    execution_enabled: bool
    contents: str | None
    participants: list[str]
    events: str
    notes: str | None
    created_at: str
    updated_at: str
    ended_at: str | None
    url: str
    playback: str
    history: NotRequired[str]
    drawing: str | None
    type: str
    question_ids: list[int]
    pad_environment_ids: list[int]
    active_environment_id: int | None
    team: TeamDict


class PadEventDict(TypedDict):
    """An event associated with a pad."""

    message: str
    kind: str
    metadata: str | None
    user_name: str | None
    user_email: str | None
    created_at: str


class FileContentDict(TypedDict):
    """A file within a pad environment."""

    path: str
    contents: str
    history: str


class PadEnvironmentDict(TypedDict):
    """A pad environment."""

    id: int
    pad_id: int
    question_id: int | None
    example_question_id: int | None
    language: str
    file_contents: list[FileContentDict]
    created_at: str
    updated_at: str


class CandidateInstructionDict(TypedDict):
    """Instructions shown to a candidate."""

    instructions: str
    default_visible: NotRequired[bool]


class TestCaseDict(TypedDict):
    """A test case for a question."""

    id: int
    return_value: str
    visible: bool
    arguments: list[str]


class CustomFileDict(TypedDict):
    """A custom file attached to a question."""

    id: str
    title: str
    description: str
    filename: str
    filesize: str


class QuestionDict(TypedDict):
    """A CoderPad question."""

    id: int
    title: str
    owner_email: str
    language: str | None
    description: str | None
    candidate_instructions: list[CandidateInstructionDict]
    contents: str | None
    shared: bool
    used: int
    take_home: bool
    test_cases_enabled: bool
    solution: str | None
    pad_type: str
    is_draft: bool
    author_name: str
    organization_name: str
    custom_files: list[CustomFileDict]
    created_at: str
    updated_at: str
    public_take_home_setting_id: NotRequired[int]
    contents_for_test_cases: NotRequired[str]
    test_cases: NotRequired[list[TestCaseDict]]


class OrganizationUserDict(TypedDict):
    """A user within an organization."""

    email: str
    name: str
    teams: list[str]


class OrganizationStatsUserDict(TypedDict):
    """A user's pad usage statistics."""

    email: str
    name: str
    pads_created: int


class StatusResponseDict(TypedDict):
    """A response containing only a status."""

    status: str


class PadResponseDict(PadDict):
    """Response for creating or retrieving a single pad."""

    status: str


class ListPadsResponseDict(TypedDict):
    """Response for listing pads."""

    status: str
    pads: list[PadDict]
    next_page: str
    total: int


class PadEventsResponseDict(TypedDict):
    """Response for retrieving pad events."""

    status: str
    events: list[PadEventDict]
    total: int


class PadEnvironmentResponseDict(PadEnvironmentDict):
    """Response for retrieving a pad environment."""

    status: str


class QuestionResponseDict(QuestionDict):
    """Response for creating or retrieving a question."""

    status: str


class ListQuestionsResponseDict(TypedDict):
    """Response for listing questions."""

    status: str
    questions: list[QuestionDict]
    next_page: str
    total: int


class QuotaResponseDict(TypedDict):
    """Response for retrieving quota information."""

    status: str
    trial_expires_at: str
    pads_used: int
    quota_reset_at: str
    unlimited: bool
    overages_enabled: bool


class OrganizationResponseDict(TypedDict):
    """Response for retrieving organization information."""

    status: str
    organization_name: str
    user_count: int
    users: list[OrganizationUserDict]
    organization_default_language: str
    single_sign_on_supported: bool
    single_sign_in_url: str
    teams: list[TeamDict]


class OrganizationStatsResponseDict(TypedDict):
    """Response for retrieving organization statistics."""

    status: str
    start_time: str
    end_time: str
    pads_created: int
    users: list[OrganizationStatsUserDict]
