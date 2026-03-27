"""Types for the CoderPad Interview API."""

from typing import NotRequired, TypedDict


class Team(TypedDict):
    """A team within an organization."""

    id: str
    name: str


class Pad(TypedDict):
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
    history: str
    drawing: str | None
    type: str
    question_ids: list[int]
    pad_environment_ids: list[int]
    active_environment_id: int | None
    team: Team


class PadEvent(TypedDict):
    """An event associated with a pad."""

    message: str
    kind: str
    metadata: str | None
    user_name: str | None
    user_email: str | None
    created_at: str


class FileContent(TypedDict):
    """A file within a pad environment."""

    path: str
    contents: str
    history: str


class PadEnvironment(TypedDict):
    """A pad environment."""

    id: int
    pad_id: int
    question_id: int | None
    example_question_id: int | None
    language: str
    file_contents: list[FileContent]
    created_at: str
    updated_at: str


class CandidateInstruction(TypedDict):
    """Instructions shown to a candidate."""

    instructions: str
    default_visible: bool


class TestCase(TypedDict):
    """A test case for a question."""

    id: int
    return_value: str
    visible: bool
    arguments: list[str]


class CustomFile(TypedDict):
    """A custom file attached to a question."""

    id: str
    title: str
    description: str
    filename: str
    filesize: str


class Question(TypedDict):
    """A CoderPad question."""

    id: int
    title: str
    owner_email: str
    language: str | None
    description: str | None
    candidate_instructions: list[CandidateInstruction]
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
    custom_files: list[CustomFile]
    public_take_home_setting_id: NotRequired[int]
    contents_for_test_cases: NotRequired[str]
    test_cases: NotRequired[list[TestCase]]
    created_at: str
    updated_at: str


class OrganizationUser(TypedDict):
    """A user within an organization."""

    email: str
    name: str
    teams: list[str]


class OrganizationStatsUser(TypedDict):
    """A user's pad usage statistics."""

    email: str
    name: str
    pads_created: int


class StatusResponse(TypedDict):
    """A response containing only a status."""

    status: str


class PadResponse(Pad):
    """Response for creating or retrieving a single pad."""

    status: str


class ListPadsResponse(TypedDict):
    """Response for listing pads."""

    status: str
    pads: list[Pad]
    next_page: str
    total: int


class PadEventsResponse(TypedDict):
    """Response for retrieving pad events."""

    status: str
    events: list[PadEvent]
    total: int


class PadEnvironmentResponse(PadEnvironment):
    """Response for retrieving a pad environment."""

    status: str


class QuestionResponse(Question):
    """Response for creating or retrieving a single question."""

    status: str


class ListQuestionsResponse(TypedDict):
    """Response for listing questions."""

    status: str
    questions: list[Question]
    next_page: str
    total: int


class QuotaResponse(TypedDict):
    """Response for retrieving quota information."""

    status: str
    trial_expires_at: str
    pads_used: int
    quota_reset_at: str
    unlimited: bool
    overages_enabled: bool


class OrganizationResponse(TypedDict):
    """Response for retrieving organization information."""

    status: str
    organization_name: str
    user_count: int
    users: list[OrganizationUser]
    organization_default_language: str
    single_sign_on_supported: bool
    single_sign_in_url: str
    teams: list[Team]


class OrganizationStatsResponse(TypedDict):
    """Response for retrieving organization statistics."""

    status: str
    start_time: str
    end_time: str
    pads_created: int
    users: list[OrganizationStatsUser]
