"""Shared synthetic Interview pad responses."""

from coderpad.json_types import JsonValue


def pad_payload() -> dict[str, JsonValue]:
    """Provide a complete pad with optional access metadata."""
    return {
        "id": "abcdefgh",
        "title": "Interview",
        "state": "active",
        "owner_email": "owner@example.com",
        "language": "python3",
        "private": False,
        "execution_enabled": False,
        "contents": "",
        "participants": [],
        "events": "",
        "notes": "",
        "created_at": "2026-10-06T12:00:00Z",
        "updated_at": "2026-10-06T12:00:00Z",
        "ended_at": None,
        "url": "https://app.coderpad.io/abcdefgh",
        "playback": "https://app.coderpad.io/abcdefgh/playback",
        "drawing": None,
        "type": "interview",
        "question_ids": [123],
        "pad_environment_ids": [],
        "active_environment_id": None,
        "team": {"id": "team-1", "name": "Backend"},
        "allowed_interviewer_emails": [],
        "restrict_interviewer_access": False,
    }
