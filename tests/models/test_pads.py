"""Tests for `coderpad` pads models."""

# pytest-beartype resolves fixture parameter annotations at runtime.
from coderpad._dict_types import (
    FileContentDict,
    PadDict,
    PadEnvironmentDict,
    PadEventDict,
    PadHistoryEntryDict,
    PadInterviewerNotificationDict,
    TeamDict,
)
from coderpad.types import (
    FileContent,
    Pad,
    PadEnvironment,
    PadEvent,
    PadHistory,
    PadHistoryEntry,
    PadInterviewerNotification,
    PaginatedList,
)


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


def _pad_interviewer_notification_dict() -> PadInterviewerNotificationDict:
    """Sample PadInterviewerNotificationDict."""
    return {
        "id": 11,
        "title": "Interview signal",
        "message": "Consider asking a follow-up question.",
        "priority": "normal",
        "request_id": "request-1",
        "auto_dismissed": False,
        "dismissed_at": None,
        "useful": None,
        "created_at": "2023-01-01T00:00:00Z",
        "updated_at": "2023-01-01T00:00:00Z",
    }


def _file_content_dict() -> FileContentDict:
    """Sample FileContentDict."""
    return {
        "path": "main.py",
        "contents": "print(1)",
        "history": "v1",
        "binary": False,
    }


def _pad_history_entry_dict() -> PadHistoryEntryDict:
    """Sample PadHistoryEntryDict."""
    return {
        "a": "author-1",
        "o": [1, "X", -2],
        "t": 1_700_000_000_000,
    }


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


def _pad_dict(*, team_dict: TeamDict) -> PadDict:
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
        "team": team_dict,
        "restrict_interviewer_access": True,
        "pad_interviewer_notifications": [
            _pad_interviewer_notification_dict(),
        ],
    }


def test_pad_from_dict(team_dict: TeamDict) -> None:
    """A Pad can be created from a dictionary."""
    data = _pad_dict(team_dict=team_dict)
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
    assert result.restrict_interviewer_access is True
    assert len(result.pad_interviewer_notifications) == 1


def test_from_dict_without_empirically_observed_fields(
    team_dict: TeamDict,
) -> None:
    """A Pad remains compatible with published response fields."""
    data = _pad_dict(team_dict=team_dict)
    del data["restrict_interviewer_access"]
    del data["pad_interviewer_notifications"]
    result = Pad.from_dict(data=data)
    assert result.restrict_interviewer_access is None
    assert not bool(result.pad_interviewer_notifications)


def test_pad_interviewer_notification_from_dict() -> None:
    """An interviewer notification can be created from a
    dictionary.
    """
    data = _pad_interviewer_notification_dict()
    result = PadInterviewerNotification.from_dict(data=data)
    assert result.id == data["id"]
    assert result.title == data["title"]
    assert result.priority == data["priority"]
    assert result.request_id == data["request_id"]
    assert result.auto_dismissed == data["auto_dismissed"]
    assert result.dismissed_at is None
    assert result.useful is None


def test_pad_event_from_dict() -> None:
    """A PadEvent can be created from a dictionary."""
    data = _pad_event_dict()
    result = PadEvent.from_dict(data=data)
    assert result.message == data["message"]
    assert result.kind == data["kind"]
    assert result.metadata == data["metadata"]
    assert result.user_name == data["user_name"]
    assert result.user_email == data["user_email"]
    assert result.created_at == data["created_at"]


def test_model_validate_without_optional_fields() -> None:
    """Pydantic parsing accepts omitted optional response fields."""
    result = PadEvent.model_validate(
        obj={
            "message": "Pad started",
            "kind": "start",
            "created_at": "2023-01-01T00:00:00Z",
        },
    )
    assert result.metadata is None
    assert result.user_name is None
    assert result.user_email is None


def test_file_content_from_dict() -> None:
    """A FileContent can be created from a dictionary."""
    data = _file_content_dict()
    result = FileContent.from_dict(data=data)
    assert result.path == data["path"]
    assert result.contents == data["contents"]
    assert result.history == "v1"
    assert result.binary is False


def test_from_dict_without_history() -> None:
    """A FileContent can omit its optional history URL."""
    data: FileContentDict = {
        "path": "main.py",
        "contents": "print(1)",
    }
    result = FileContent.from_dict(data=data)
    assert result.history is None
    assert result.binary is False


def test_from_dict_for_binary_file() -> None:
    """A binary FileContent can have no text contents."""
    data: FileContentDict = {
        "path": "image.png",
        "contents": None,
        "binary": True,
    }
    result = FileContent.from_dict(data=data)
    assert result.contents is None
    assert result.binary is True


def test_pad_history_entry_from_dict() -> None:
    """A history entry can be created from a dictionary."""
    data = _pad_history_entry_dict()
    result = PadHistoryEntry.from_dict(
        entry_id="entry-1",
        data=data,
    )
    assert result.id == "entry-1"
    assert result.author == data["a"]
    assert result.operations == data["o"]
    assert result.timestamp == data["t"]


def test_apply() -> None:
    """Text operations can be applied to existing contents."""
    entry = PadHistoryEntry.from_dict(
        entry_id="entry-1",
        data=_pad_history_entry_dict(),
    )
    assert entry.apply(contents="abcd") == "aXd"


def test_from_dict_orders_and_replays_entries() -> None:
    """History entries are ordered and can be replayed."""
    history = PadHistory.from_dict(
        data={
            "later": {
                "a": "author-1",
                "o": [2, "!"],
                "t": 2,
            },
            "earlier": {
                "a": "author-1",
                "o": [1, "i"],
                "t": 1,
            },
        },
    )
    assert [entry.id for entry in history] == ["earlier", "later"]
    assert history.replay(initial_contents="h") == "hi!"


def test_pad_environment_from_dict() -> None:
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


def test_paginated_list_prev_page() -> None:
    """PaginatedList stores prev_page from construction."""
    page = PaginatedList(
        ["a"],
        total=2,
        next_page="https://example.com?page=2",
        prev_page="https://example.com?page=0",
    )
    assert page.prev_page == "https://example.com?page=0"
    assert page.next_page == "https://example.com?page=2"


def test_paginated_list_prev_page_defaults_none() -> None:
    """PaginatedList defaults prev_page to None."""
    page = PaginatedList(["a"], total=1)
    assert page.prev_page is None


def test_pad_analytics(team_dict: TeamDict) -> None:
    """Optional analytics preserve structured content and optional review
    fields.
    """
    data = _pad_dict(team_dict=team_dict)
    data["interview_highlights"] = "Explained the tradeoffs."
    data["interview_outline"] = {"sections": [{"title": "Implementation"}]}
    data["transcript"] = [
        {
            "id": "entry-1",
            "kind": "system_message",
            "text": "Recording started",
            "timestamp": 1790000000123,
            "speaker_name": None,
            "speaker_role": None,
        }
    ]
    data["transcript_source_unavailable"] = False
    data["review_reports"] = [
        {
            "id": "review-1",
            "status": "failed",
            "report": None,
            "error": "Unavailable",
            "prompt": "Review solution",
            "summary": None,
            "icon": None,
            "user_id": None,
            "file_paths": ["main.py"],
            "created_at": "2026-10-06T12:00:00Z",
            "updated_at": "2026-10-06T12:00:01Z",
        }
    ]
    for pad in [Pad.from_dict(data=data), Pad.model_validate(obj=data)]:
        assert pad.interview_highlights == data["interview_highlights"]
        assert pad.interview_outline == data["interview_outline"]
        assert pad.transcript is not None
        assert [entry.model_dump() for entry in pad.transcript] == data[
            "transcript"
        ]
        assert pad.transcript[0].speaker_name is None
        assert pad.transcript[0].speaker_role is None
        assert pad.transcript_source_unavailable is False
        assert pad.review_reports is not None
        assert pad.review_reports[0].error == "Unavailable"
        assert pad.review_reports[0].file_paths == ["main.py"]
        assert pad.review_reports[0].report is None
        assert pad.review_reports[0].prompt == "Review solution"
        assert pad.review_reports[0].summary is None
        assert pad.review_reports[0].icon is None
        assert pad.review_reports[0].user_id is None


def test_pad_analytics_availability(team_dict: TeamDict) -> None:
    """Absent and empty analytics preserve source availability."""
    absent = Pad.from_dict(data=_pad_dict(team_dict=team_dict))
    assert absent.interview_highlights is None
    assert absent.interview_outline is None
    assert absent.transcript is None
    assert absent.review_reports is None
    assert absent.transcript_source_unavailable is None
    data = _pad_dict(team_dict=team_dict)
    data["transcript"] = []
    data["review_reports"] = []
    data["transcript_source_unavailable"] = True
    unavailable = Pad.from_dict(data=data)
    # Empty lists differ from absent analytics.
    # pylint: disable-next=use-implicit-booleaness-not-comparison
    assert unavailable.transcript == []
    # pylint: disable-next=use-implicit-booleaness-not-comparison
    assert unavailable.review_reports == []
    assert unavailable.transcript_source_unavailable is True
