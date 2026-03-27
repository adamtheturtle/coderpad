"""Types for the CoderPad Interview API."""

from dataclasses import dataclass
from typing import Self

from coderpad_api._dict_types import (
    CandidateInstructionDict,
    CustomFileDict,
    FileContentDict,
    OrganizationDict,
    OrganizationStatsDict,
    OrganizationStatsUserDict,
    OrganizationUserDict,
    PadDict,
    PadEnvironmentDict,
    PadEventDict,
    QuestionDict,
    QuotaDict,
    TeamDict,
    TestCaseDict,
)


@dataclass(kw_only=True)
class Team:
    """A team within an organization."""

    id: str
    name: str

    @classmethod
    def from_dict(cls, data: TeamDict) -> Self:
        """Create from an API response dictionary.

        Args:
            data: The dictionary to convert.

        Returns:
            A new instance.
        """
        return cls(
            id=data["id"],
            name=data["name"],
        )


@dataclass(kw_only=True)
class Pad:
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
    drawing: str | None
    type: str
    question_ids: list[int]
    pad_environment_ids: list[int]
    active_environment_id: int | None
    team: Team
    history: str | None = None

    @classmethod
    def from_dict(cls, data: PadDict) -> Self:
        """Create from an API response dictionary.

        Args:
            data: The dictionary to convert.

        Returns:
            A new instance.
        """
        return cls(
            id=data["id"],
            title=data["title"],
            state=data["state"],
            owner_email=data["owner_email"],
            language=data.get("language"),
            private=data["private"],
            execution_enabled=data["execution_enabled"],
            contents=data.get("contents"),
            participants=data["participants"],
            events=data["events"],
            notes=data.get("notes"),
            created_at=data["created_at"],
            updated_at=data["updated_at"],
            ended_at=data.get("ended_at"),
            url=data["url"],
            playback=data["playback"],
            drawing=data.get("drawing"),
            type=data["type"],
            question_ids=data["question_ids"],
            pad_environment_ids=data["pad_environment_ids"],
            active_environment_id=data.get(
                "active_environment_id",
            ),
            team=Team.from_dict(data=data["team"]),
            history=data.get("history"),
        )


@dataclass(kw_only=True)
class PadEvent:
    """An event associated with a pad."""

    message: str
    kind: str
    metadata: str | None
    user_name: str | None
    user_email: str | None
    created_at: str

    @classmethod
    def from_dict(
        cls,
        data: PadEventDict,
    ) -> Self:
        """Create from an API response dictionary.

        Args:
            data: The dictionary to convert.

        Returns:
            A new instance.
        """
        return cls(
            message=data["message"],
            kind=data["kind"],
            metadata=data.get("metadata"),
            user_name=data.get("user_name"),
            user_email=data.get("user_email"),
            created_at=data["created_at"],
        )


@dataclass(kw_only=True)
class FileContent:
    """A file within a pad environment."""

    path: str
    contents: str
    history: str

    @classmethod
    def from_dict(
        cls,
        data: FileContentDict,
    ) -> Self:
        """Create from an API response dictionary.

        Args:
            data: The dictionary to convert.

        Returns:
            A new instance.
        """
        return cls(
            path=data["path"],
            contents=data["contents"],
            history=data["history"],
        )


@dataclass(kw_only=True)
class PadEnvironment:
    """A pad environment."""

    id: int
    pad_id: int
    question_id: int | None
    example_question_id: int | None
    language: str
    file_contents: list[FileContent]
    created_at: str
    updated_at: str

    @classmethod
    def from_dict(
        cls,
        data: PadEnvironmentDict,
    ) -> Self:
        """Create from an API response dictionary.

        Args:
            data: The dictionary to convert.

        Returns:
            A new instance.
        """
        return cls(
            id=data["id"],
            pad_id=data["pad_id"],
            question_id=data.get("question_id"),
            example_question_id=data.get(
                "example_question_id",
            ),
            language=data["language"],
            file_contents=[
                FileContent.from_dict(data=item)
                for item in data["file_contents"]
            ],
            created_at=data["created_at"],
            updated_at=data["updated_at"],
        )


@dataclass(kw_only=True)
class CandidateInstruction:
    """Instructions shown to a candidate."""

    instructions: str
    default_visible: bool = False

    @classmethod
    def from_dict(
        cls,
        data: CandidateInstructionDict,
    ) -> Self:
        """Create from an API response dictionary.

        Args:
            data: The dictionary to convert.

        Returns:
            A new instance.
        """
        return cls(
            instructions=data["instructions"],
            default_visible=data.get(  # type: ignore[call-overload]
                "default_visible",
                False,
            ),
        )


@dataclass(kw_only=True)
class TestCase:
    """A test case for a question."""

    id: int
    return_value: str
    visible: bool
    arguments: list[str]

    @classmethod
    def from_dict(
        cls,
        data: TestCaseDict,
    ) -> Self:
        """Create from an API response dictionary.

        Args:
            data: The dictionary to convert.

        Returns:
            A new instance.
        """
        return cls(
            id=data["id"],
            return_value=data["return_value"],
            visible=data["visible"],
            arguments=data["arguments"],
        )


@dataclass(kw_only=True)
class CustomFile:
    """A custom file attached to a question."""

    id: str
    title: str
    description: str
    filename: str
    filesize: str

    @classmethod
    def from_dict(
        cls,
        data: CustomFileDict,
    ) -> Self:
        """Create from an API response dictionary.

        Args:
            data: The dictionary to convert.

        Returns:
            A new instance.
        """
        return cls(
            id=data["id"],
            title=data["title"],
            description=data["description"],
            filename=data["filename"],
            filesize=data["filesize"],
        )


@dataclass(kw_only=True)
class Question:
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
    created_at: str
    updated_at: str
    public_take_home_setting_id: int | None = None
    contents_for_test_cases: str | None = None
    test_cases: list[TestCase] | None = None

    @classmethod
    def from_dict(
        cls,
        data: QuestionDict,
    ) -> Self:
        """Create from an API response dictionary.

        Args:
            data: The dictionary to convert.

        Returns:
            A new instance.
        """
        raw_test_cases = data.get("test_cases")
        return cls(
            id=data["id"],
            title=data["title"],
            owner_email=data["owner_email"],
            language=data.get("language"),
            description=data.get("description"),
            candidate_instructions=[
                CandidateInstruction.from_dict(data=item)
                for item in data["candidate_instructions"]
            ],
            contents=data.get("contents"),
            shared=data["shared"],
            used=data["used"],
            take_home=data["take_home"],
            test_cases_enabled=data["test_cases_enabled"],
            solution=data.get("solution"),
            pad_type=data["pad_type"],
            is_draft=data["is_draft"],
            author_name=data["author_name"],
            organization_name=data["organization_name"],
            custom_files=[
                CustomFile.from_dict(data=item)
                for item in data["custom_files"]
            ],
            created_at=data["created_at"],
            updated_at=data["updated_at"],
            public_take_home_setting_id=data.get(
                "public_take_home_setting_id",
            ),
            contents_for_test_cases=data.get(
                "contents_for_test_cases",
            ),
            test_cases=[
                TestCase.from_dict(data=item) for item in raw_test_cases
            ]
            if raw_test_cases is not None
            else None,
        )


@dataclass(kw_only=True)
class OrganizationUser:
    """A user within an organization."""

    email: str
    name: str
    teams: list[str]

    @classmethod
    def from_dict(
        cls,
        data: OrganizationUserDict,
    ) -> Self:
        """Create from an API response dictionary.

        Args:
            data: The dictionary to convert.

        Returns:
            A new instance.
        """
        return cls(
            email=data["email"],
            name=data["name"],
            teams=data["teams"],
        )


@dataclass(kw_only=True)
class OrganizationStatsUser:
    """A user's pad usage statistics."""

    email: str
    name: str
    pads_created: int

    @classmethod
    def from_dict(
        cls,
        data: OrganizationStatsUserDict,
    ) -> Self:
        """Create from an API response dictionary.

        Args:
            data: The dictionary to convert.

        Returns:
            A new instance.
        """
        return cls(
            email=data["email"],
            name=data["name"],
            pads_created=data["pads_created"],
        )


@dataclass(kw_only=True)
class Quota:
    """Quota information."""

    trial_expires_at: str
    pads_used: int
    quota_reset_at: str
    unlimited: bool
    overages_enabled: bool

    @classmethod
    def from_dict(
        cls,
        data: QuotaDict,
    ) -> Self:
        """Create from an API response dictionary.

        Args:
            data: The dictionary to convert.

        Returns:
            A new instance.
        """
        return cls(
            trial_expires_at=data["trial_expires_at"],
            pads_used=data["pads_used"],
            quota_reset_at=data["quota_reset_at"],
            unlimited=data["unlimited"],
            overages_enabled=data["overages_enabled"],
        )


@dataclass(kw_only=True)
class Organization:
    """Organization information."""

    organization_name: str
    user_count: int
    users: list[OrganizationUser]
    organization_default_language: str
    single_sign_on_supported: bool
    single_sign_in_url: str
    teams: list[Team]

    @classmethod
    def from_dict(
        cls,
        data: OrganizationDict,
    ) -> Self:
        """Create from an API response dictionary.

        Args:
            data: The dictionary to convert.

        Returns:
            A new instance.
        """
        return cls(
            organization_name=data["organization_name"],
            user_count=data["user_count"],
            users=[
                OrganizationUser.from_dict(data=item) for item in data["users"]
            ],
            organization_default_language=data[
                "organization_default_language"
            ],
            single_sign_on_supported=data["single_sign_on_supported"],
            single_sign_in_url=data["single_sign_in_url"],
            teams=[Team.from_dict(data=item) for item in data["teams"]],
        )


@dataclass(kw_only=True)
class OrganizationStats:
    """Organization usage statistics."""

    start_time: str
    end_time: str
    pads_created: int
    users: list[OrganizationStatsUser]

    @classmethod
    def from_dict(
        cls,
        data: OrganizationStatsDict,
    ) -> Self:
        """Create from an API response dictionary.

        Args:
            data: The dictionary to convert.

        Returns:
            A new instance.
        """
        return cls(
            start_time=data["start_time"],
            end_time=data["end_time"],
            pads_created=data["pads_created"],
            users=[
                OrganizationStatsUser.from_dict(data=item)
                for item in data["users"]
            ],
        )
