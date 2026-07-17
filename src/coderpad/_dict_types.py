"""TypedDict types describing raw API response shapes."""

from typing import NotRequired, TypedDict


class TeamDict(TypedDict):
    """A team within an organization."""

    id: str
    name: str


class PadInterviewerNotificationDict(TypedDict):
    """An interviewer notification associated with a pad."""

    id: int
    title: str
    message: str
    priority: str
    request_id: str
    auto_dismissed: bool
    dismissed_at: str | None
    useful: bool | None
    created_at: str
    updated_at: str


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
    restrict_interviewer_access: NotRequired[bool]
    pad_interviewer_notifications: NotRequired[
        list[PadInterviewerNotificationDict]
    ]


class PadEventDict(TypedDict):
    """An event associated with a pad."""

    message: str
    kind: str
    metadata: str | None
    user_name: str | None
    user_email: str | None
    created_at: str


# An editor operation stored in a pad's Firebase history. The functional
# form prevents static analysis from treating its abbreviated wire keys as
# unused Python attributes.
PadHistoryEntryDict = TypedDict(  # noqa: UP013
    "PadHistoryEntryDict",
    {
        "a": str,
        "o": list[int | str],
        "t": int,
    },
)


class FileContentDict(TypedDict):
    """A file within a pad environment."""

    path: str
    contents: str | None
    history: NotRequired[str]
    binary: NotRequired[bool]


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


class CustomDatabaseColumnDict(TypedDict):
    """A column in a question's custom database schema."""

    name: str
    type: str
    pk: bool
    nn: bool


class CustomDatabaseTableDict(TypedDict):
    """A table in a question's custom database schema."""

    name: str
    columns: list[CustomDatabaseColumnDict]


class CustomDatabaseSchemaDict(TypedDict):
    """The structured schema for a question's custom database."""

    arrangement: str
    tables: list[CustomDatabaseTableDict]


class CustomDatabaseDict(TypedDict):
    """A custom database attached to a question."""

    id: int
    title: str
    description: str
    language: str
    schema: str
    schema_json: CustomDatabaseSchemaDict


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
    custom_database: NotRequired[CustomDatabaseDict]


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


class QuotaDict(TypedDict):
    """Quota information."""

    trial_expires_at: str
    pads_used: int
    quota_reset_at: str
    unlimited: bool
    overages_enabled: bool


class OrganizationDict(TypedDict):
    """Organization information."""

    organization_name: str
    user_count: int
    users: list[OrganizationUserDict]
    organization_default_language: str
    single_sign_on_supported: bool
    single_sign_in_url: NotRequired[str]
    teams: list[TeamDict]
    id: NotRequired[int]
    child_organizations: NotRequired[list[dict[str, object]]]


class OrganizationStatsDict(TypedDict):
    """Organization usage statistics."""

    start_time: str
    end_time: str
    pads_created: int
    users: list[OrganizationStatsUserDict]
