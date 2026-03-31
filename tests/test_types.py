"""Tests for the CoderPad types."""

from coderpad._dict_types import (
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
from coderpad.types import (
    CandidateInstruction,
    CustomFile,
    FileContent,
    Organization,
    OrganizationStats,
    OrganizationStatsUser,
    OrganizationUser,
    Pad,
    PadEnvironment,
    PadEvent,
    Question,
    Quota,
    Team,
    TestCase,
)


def _team_dict() -> TeamDict:
    """Sample TeamDict."""
    return {"id": "team-1", "name": "Backend"}


def _pad_event_dict() -> PadEventDict:
    """Sample PadEventDict."""
    return {
        "message": "Pad started",
        "kind": "start",
        "metadata": None,
        "user_name": "Alice",
        "user_email": "alice@example.com",
        "created_at": "2023-01-01T00:00:00Z",
    }


def _file_content_dict() -> FileContentDict:
    """Sample FileContentDict."""
    return {"path": "main.py", "contents": "print(1)", "history": "v1"}


def _pad_environment_dict() -> PadEnvironmentDict:
    """Sample PadEnvironmentDict."""
    return {
        "id": 1,
        "pad_id": 2,
        "question_id": 3,
        "example_question_id": 4,
        "language": "python",
        "file_contents": [_file_content_dict()],
        "created_at": "2023-01-01T00:00:00Z",
        "updated_at": "2023-01-02T00:00:00Z",
    }


def _candidate_instruction_dict() -> CandidateInstructionDict:
    """Sample CandidateInstructionDict."""
    return {"instructions": "Do the thing", "default_visible": True}


def _test_case_dict() -> TestCaseDict:
    """Sample TestCaseDict."""
    return {
        "id": 10,
        "return_value": "42",
        "visible": True,
        "arguments": ["1", "2"],
    }


def _custom_file_dict() -> CustomFileDict:
    """Sample CustomFileDict."""
    return {
        "id": "cf-1",
        "title": "Data",
        "description": "Test data",
        "filename": "data.csv",
        "filesize": "1024",
    }


def _pad_dict() -> PadDict:
    """Sample PadDict."""
    return {
        "id": "pad-1",
        "title": "Interview",
        "state": "active",
        "owner_email": "owner@example.com",
        "language": "python",
        "private": True,
        "execution_enabled": True,
        "contents": "# code",
        "participants": ["a@example.com"],
        "events": "[]",
        "notes": "Good",
        "created_at": "2023-01-01T00:00:00Z",
        "updated_at": "2023-01-02T00:00:00Z",
        "ended_at": "2023-01-03T00:00:00Z",
        "url": "https://app.coderpad.io/pad-1",
        "playback": "https://app.coderpad.io/pad-1/playback",
        "history": "v1",
        "drawing": "svg-data",
        "type": "sandbox",
        "question_ids": [1, 2],
        "pad_environment_ids": [10],
        "active_environment_id": 10,
        "team": _team_dict(),
    }


_PUBLIC_TAKE_HOME_SETTING_ID = 7


def _question_dict() -> QuestionDict:
    """Sample QuestionDict."""
    return {
        "id": 5,
        "title": "FizzBuzz",
        "owner_email": "owner@example.com",
        "language": "python",
        "description": "Write FizzBuzz",
        "candidate_instructions": [_candidate_instruction_dict()],
        "contents": "def fizzbuzz(): ...",
        "shared": False,
        "used": 3,
        "take_home": False,
        "test_cases_enabled": True,
        "solution": "def fizzbuzz(): pass",
        "pad_type": "standard",
        "is_draft": False,
        "author_name": "Author",
        "organization_name": "Org",
        "custom_files": [_custom_file_dict()],
        "created_at": "2023-01-01T00:00:00Z",
        "updated_at": "2023-01-02T00:00:00Z",
        "public_take_home_setting_id": _PUBLIC_TAKE_HOME_SETTING_ID,
        "contents_for_test_cases": "test code",
        "test_cases": [_test_case_dict()],
    }


class TestTeam:
    """Tests for ``Team``."""

    @staticmethod
    def test_from_dict() -> None:
        """A Team can be created from a dictionary."""
        data = _team_dict()
        result = Team.from_dict(data=data)
        assert result.id == data["id"]
        assert result.name == data["name"]


class TestPad:
    """Tests for ``Pad``."""

    @staticmethod
    def test_from_dict() -> None:
        """A Pad can be created from a dictionary."""
        data = _pad_dict()
        result = Pad.from_dict(data=data)
        assert result.id == data["id"]
        assert result.title == data["title"]
        assert result.state == data["state"]
        assert result.owner_email == data["owner_email"]
        assert result.language == data["language"]
        assert result.private == data["private"]
        assert result.execution_enabled == data["execution_enabled"]
        assert result.contents == data["contents"]
        assert result.participants == data["participants"]
        assert result.events == data["events"]
        assert result.notes == data["notes"]
        assert result.created_at == data["created_at"]
        assert result.updated_at == data["updated_at"]
        assert result.ended_at == data["ended_at"]
        assert result.url == data["url"]
        assert result.playback == data["playback"]
        assert result.history == "v1"
        assert result.drawing == data["drawing"]
        assert result.type == data["type"]
        assert result.question_ids == data["question_ids"]
        assert result.pad_environment_ids == data["pad_environment_ids"]
        assert result.active_environment_id == data["active_environment_id"]
        assert result.team.id == data["team"]["id"]


class TestPadEvent:
    """Tests for ``PadEvent``."""

    @staticmethod
    def test_from_dict() -> None:
        """A PadEvent can be created from a dictionary."""
        data = _pad_event_dict()
        result = PadEvent.from_dict(data=data)
        assert result.message == data["message"]
        assert result.kind == data["kind"]
        assert result.metadata == data["metadata"]
        assert result.user_name == data["user_name"]
        assert result.user_email == data["user_email"]
        assert result.created_at == data["created_at"]


class TestFileContent:
    """Tests for ``FileContent``."""

    @staticmethod
    def test_from_dict() -> None:
        """A FileContent can be created from a dictionary."""
        data = _file_content_dict()
        result = FileContent.from_dict(data=data)
        assert result.path == data["path"]
        assert result.contents == data["contents"]
        assert result.history == "v1"


class TestPadEnvironment:
    """Tests for ``PadEnvironment``."""

    @staticmethod
    def test_from_dict() -> None:
        """A PadEnvironment can be created from a dictionary."""
        data = _pad_environment_dict()
        result = PadEnvironment.from_dict(data=data)
        assert result.id == data["id"]
        assert result.pad_id == data["pad_id"]
        assert result.question_id == data["question_id"]
        assert result.example_question_id == data["example_question_id"]
        assert result.language == data["language"]
        assert len(result.file_contents) == len(data["file_contents"])
        assert result.created_at == data["created_at"]
        assert result.updated_at == data["updated_at"]


class TestCandidateInstruction:
    """Tests for ``CandidateInstruction``."""

    @staticmethod
    def test_from_dict() -> None:
        """A CandidateInstruction can be created from a dictionary."""
        data = _candidate_instruction_dict()
        result = CandidateInstruction.from_dict(data=data)
        assert result.instructions == data["instructions"]
        assert result.default_visible is True


class TestTestCase:
    """Tests for ``TestCase``."""

    @staticmethod
    def test_from_dict() -> None:
        """A TestCase can be created from a dictionary."""
        data = _test_case_dict()
        result = TestCase.from_dict(data=data)
        assert result.id == data["id"]
        assert result.return_value == data["return_value"]
        assert result.visible == data["visible"]
        assert result.arguments == data["arguments"]


class TestCustomFile:
    """Tests for ``CustomFile``."""

    @staticmethod
    def test_from_dict() -> None:
        """A CustomFile can be created from a dictionary."""
        data = _custom_file_dict()
        result = CustomFile.from_dict(data=data)
        assert result.id == data["id"]
        assert result.title == data["title"]
        assert result.description == data["description"]
        assert result.filename == data["filename"]
        assert result.filesize == data["filesize"]


class TestQuestion:
    """Tests for ``Question``."""

    @staticmethod
    def test_from_dict() -> None:
        """A Question can be created from a dictionary."""
        data = _question_dict()
        result = Question.from_dict(data=data)
        assert result.id == data["id"]
        assert result.title == data["title"]
        assert result.owner_email == data["owner_email"]
        assert result.language == data["language"]
        assert result.description == data["description"]
        assert len(result.candidate_instructions) == len(
            data["candidate_instructions"],
        )
        assert result.contents == data["contents"]
        assert result.shared == data["shared"]
        assert result.used == data["used"]
        assert result.take_home == data["take_home"]
        assert result.test_cases_enabled == data["test_cases_enabled"]
        assert result.solution == data["solution"]
        assert result.pad_type == data["pad_type"]
        assert result.is_draft == data["is_draft"]
        assert result.author_name == data["author_name"]
        assert result.organization_name == data["organization_name"]
        assert len(result.custom_files) == len(data["custom_files"])
        assert result.created_at == data["created_at"]
        assert result.updated_at == data["updated_at"]
        assert (
            result.public_take_home_setting_id == _PUBLIC_TAKE_HOME_SETTING_ID
        )
        assert result.contents_for_test_cases == "test code"
        assert result.test_cases is not None
        assert len(result.test_cases) == 1


class TestOrganizationUser:
    """Tests for ``OrganizationUser``."""

    @staticmethod
    def test_from_dict() -> None:
        """An OrganizationUser can be created from a dictionary."""
        data: OrganizationUserDict = {
            "email": "u@example.com",
            "name": "User",
            "teams": ["Backend"],
        }
        result = OrganizationUser.from_dict(data=data)
        assert result.email == data["email"]
        assert result.name == data["name"]
        assert result.teams == data["teams"]


class TestOrganizationStatsUser:
    """Tests for ``OrganizationStatsUser``."""

    @staticmethod
    def test_from_dict() -> None:
        """An OrganizationStatsUser can be created from a dictionary."""
        data: OrganizationStatsUserDict = {
            "email": "u@example.com",
            "name": "User",
            "pads_created": 5,
        }
        result = OrganizationStatsUser.from_dict(data=data)
        assert result.email == data["email"]
        assert result.name == data["name"]
        assert result.pads_created == data["pads_created"]


class TestQuota:
    """Tests for ``Quota``."""

    @staticmethod
    def test_from_dict() -> None:
        """A Quota can be created from a dictionary."""
        data: QuotaDict = {
            "trial_expires_at": "2024-01-01T00:00:00Z",
            "pads_used": 10,
            "quota_reset_at": "2024-02-01T00:00:00Z",
            "unlimited": False,
            "overages_enabled": True,
        }
        result = Quota.from_dict(data=data)
        assert result.trial_expires_at == data["trial_expires_at"]
        assert result.pads_used == data["pads_used"]
        assert result.quota_reset_at == data["quota_reset_at"]
        assert result.unlimited == data["unlimited"]
        assert result.overages_enabled == data["overages_enabled"]


class TestOrganization:
    """Tests for ``Organization``."""

    @staticmethod
    def test_from_dict() -> None:
        """An Organization can be created from a dictionary."""
        data: OrganizationDict = {
            "organization_name": "Acme",
            "user_count": 5,
            "users": [
                {"email": "u@example.com", "name": "User", "teams": ["BE"]},
            ],
            "organization_default_language": "python",
            "single_sign_on_supported": True,
            "single_sign_in_url": "https://sso.example.com",
            "teams": [_team_dict()],
        }
        result = Organization.from_dict(data=data)
        assert result.organization_name == data["organization_name"]
        assert result.user_count == data["user_count"]
        assert len(result.users) == len(data["users"])
        assert (
            result.organization_default_language
            == data["organization_default_language"]
        )
        assert (
            result.single_sign_on_supported == data["single_sign_on_supported"]
        )
        assert result.single_sign_in_url == data["single_sign_in_url"]
        assert len(result.teams) == len(data["teams"])


class TestOrganizationStats:
    """Tests for ``OrganizationStats``."""

    @staticmethod
    def test_from_dict() -> None:
        """An OrganizationStats can be created from a
        dictionary.
        """
        data: OrganizationStatsDict = {
            "start_time": "2023-01-01T00:00:00Z",
            "end_time": "2023-02-01T00:00:00Z",
            "pads_created": 42,
            "users": [
                {
                    "email": "u@example.com",
                    "name": "User",
                    "pads_created": 10,
                },
            ],
        }
        result = OrganizationStats.from_dict(data=data)
        assert result.start_time == data["start_time"]
        assert result.end_time == data["end_time"]
        assert result.pads_created == data["pads_created"]
        assert len(result.users) == len(data["users"])
