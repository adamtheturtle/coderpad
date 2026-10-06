"""Exact pad mutation requests and replacement access lists."""

import json
from urllib.parse import parse_qs

import httpx
import pytest
import respx
from pydantic import TypeAdapter

from coderpad._dict_types import PadDict
from coderpad.async_client import AsyncCoderPad
from coderpad.client import CoderPad
from coderpad.exceptions import CoderPadError
from coderpad.json_types import JsonValue
from coderpad.types import Pad

_EMAIL_CASES: list[list[str] | None] = [
    None,
    [],
    ["first@example.com", "second@example.com"],
]
_URL = "https://app.coderpad.io/api/pads/"


def _pad_payload() -> dict[str, JsonValue]:
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


def _assert_request(
    *,
    request: httpx.Request,
    operation: str,
    emails: list[str] | None,
    enabled: bool,
) -> None:
    """Assert the entire payload, including JSON/form type
    distinctions.
    """
    settings: dict[str, JsonValue] = {
        "title": "Interview",
        "language": "python3",
        "notes": "",
        "private": enabled,
        "execution_enabled": "true" if enabled else "false",
        "user_email": "owner@example.com",
        "restrict_interviewer_access": enabled,
        "disable_coaching_tips": enabled,
    }
    if operation == "create":
        settings.update(
            {
                "question_id": 123,
                "team_id": "team-1",
                "take_home": enabled,
                "take_home_time_limit": 30,
                "ai_assist_enabled": enabled,
            }
        )
    else:
        settings.update({"ended": False, "deleted": False, "contents": ""})
    if emails is not None:
        settings["allowed_interviewer_emails"] = list[JsonValue](emails)
        assert json.loads(s=request.content) == {"pad": settings}
        assert request.headers["Content-Type"] == "application/json"
    else:
        expected = {
            name: [
                ("true" if value else "false")
                if isinstance(value, bool)
                else str(object=value)
            ]
            for name, value in settings.items()
        }
        assert (
            parse_qs(qs=request.content.decode(), keep_blank_values=True)
            == expected
        )
        assert (
            request.headers["Content-Type"]
            == "application/x-www-form-urlencoded"
        )
    assert request.headers["Authorization"] == 'Token token="synthetic-key"'


@pytest.mark.parametrize(argnames="operation", argvalues=["create", "update"])
@pytest.mark.parametrize(argnames="emails", argvalues=_EMAIL_CASES)
@pytest.mark.parametrize(argnames="enabled", argvalues=[False, True])
def test_pad_controls(
    operation: str, emails: list[str] | None, *, enabled: bool
) -> None:
    """Synchronous mutations preserve omitted, empty, and populated
    lists.
    """
    with respx.mock() as router:
        route = router.request(
            method="POST" if operation == "create" else "PUT",
            url=_URL if operation == "create" else _URL + "abcdefgh",
        ).respond(status_code=200, json=_pad_payload())
        with CoderPad(api_key="synthetic-key") as client:
            if operation == "create":
                pad = client.pads.create(
                    title="Interview",
                    language="python3",
                    notes="",
                    question_id=123,
                    private=enabled,
                    execution_enabled=enabled,
                    user_email="owner@example.com",
                    restrict_interviewer_access=enabled,
                    allowed_interviewer_emails=emails,
                    disable_coaching_tips=enabled,
                    team_id="team-1",
                    take_home=enabled,
                    take_home_time_limit=30,
                    ai_assist_enabled=enabled,
                )
                # The empty response list differs from absent metadata.
                # pylint: disable-next=use-implicit-booleaness-not-comparison
                assert pad.allowed_interviewer_emails == []
            else:
                client.pads.update(
                    pad_id="abcdefgh",
                    title="Interview",
                    language="python3",
                    notes="",
                    contents="",
                    ended=False,
                    deleted=False,
                    private=enabled,
                    execution_enabled=enabled,
                    user_email="owner@example.com",
                    restrict_interviewer_access=enabled,
                    allowed_interviewer_emails=emails,
                    disable_coaching_tips=enabled,
                )
        assert route.call_count == 1
        _assert_request(
            request=route.calls.last.request,
            operation=operation,
            emails=emails,
            enabled=enabled,
        )


@pytest.mark.asyncio
@pytest.mark.parametrize(argnames="operation", argvalues=["create", "update"])
@pytest.mark.parametrize(argnames="emails", argvalues=_EMAIL_CASES)
@pytest.mark.parametrize(argnames="enabled", argvalues=[False, True])
async def test_async_pad_controls(
    operation: str, emails: list[str] | None, *, enabled: bool
) -> None:
    """Asynchronous mutations use the same exact fields and encoding."""
    with respx.mock() as router:
        route = router.request(
            method="POST" if operation == "create" else "PUT",
            url=_URL if operation == "create" else _URL + "abcdefgh",
        ).respond(status_code=200, json=_pad_payload())
        async with AsyncCoderPad(api_key="synthetic-key") as client:
            if operation == "create":
                pad = await client.pads.create(
                    title="Interview",
                    language="python3",
                    notes="",
                    question_id=123,
                    private=enabled,
                    execution_enabled=enabled,
                    user_email="owner@example.com",
                    restrict_interviewer_access=enabled,
                    allowed_interviewer_emails=emails,
                    disable_coaching_tips=enabled,
                    team_id="team-1",
                    take_home=enabled,
                    take_home_time_limit=30,
                    ai_assist_enabled=enabled,
                )
                # The empty response list differs from absent metadata.
                assert pad.allowed_interviewer_emails == []
            else:
                await client.pads.update(
                    pad_id="abcdefgh",
                    title="Interview",
                    language="python3",
                    notes="",
                    contents="",
                    ended=False,
                    deleted=False,
                    private=enabled,
                    execution_enabled=enabled,
                    user_email="owner@example.com",
                    restrict_interviewer_access=enabled,
                    allowed_interviewer_emails=emails,
                    disable_coaching_tips=enabled,
                )
        assert route.call_count == 1
        _assert_request(
            request=route.calls.last.request,
            operation=operation,
            emails=emails,
            enabled=enabled,
        )


@pytest.mark.parametrize(argnames="operation", argvalues=["create", "update"])
def test_pad_control_errors(operation: str) -> None:
    """JSON access-list mutations surface API errors without retries."""
    with respx.mock() as router:
        route = router.request(
            method="POST" if operation == "create" else "PUT",
            url=_URL if operation == "create" else _URL + "abcdefgh",
        ).respond(status_code=403, json={"message": "Forbidden"})
        with CoderPad(api_key="synthetic-key") as client:
            if operation == "create":
                with pytest.raises(expected_exception=CoderPadError):
                    _ = client.pads.create(allowed_interviewer_emails=[])
            else:
                with pytest.raises(expected_exception=CoderPadError):
                    client.pads.update(
                        pad_id="abcdefgh", allowed_interviewer_emails=[]
                    )
        assert route.call_count == 1


@pytest.mark.asyncio
@pytest.mark.parametrize(argnames="operation", argvalues=["create", "update"])
async def test_async_pad_control_errors(operation: str) -> None:
    """Async JSON mutations surface the same API errors without
    retries.
    """
    with respx.mock() as router:
        route = router.request(
            method="POST" if operation == "create" else "PUT",
            url=_URL if operation == "create" else _URL + "abcdefgh",
        ).respond(status_code=403, json={"message": "Forbidden"})
        async with AsyncCoderPad(api_key="synthetic-key") as client:
            if operation == "create":
                with pytest.raises(expected_exception=CoderPadError):
                    _ = await client.pads.create(allowed_interviewer_emails=[])
            else:
                with pytest.raises(expected_exception=CoderPadError):
                    await client.pads.update(
                        pad_id="abcdefgh", allowed_interviewer_emails=[]
                    )
        assert route.call_count == 1


@pytest.mark.parametrize(argnames="emails", argvalues=_EMAIL_CASES)
def test_pad_access_metadata(emails: list[str] | None) -> None:
    """Both pad decoders preserve optional response lists exactly."""
    payload = _pad_payload()
    payload["allowed_interviewer_emails"] = (
        None if emails is None else list[JsonValue](emails)
    )
    for model in [
        Pad.model_validate(obj=payload),
        Pad.from_dict(data=TypeAdapter(type=PadDict).validate_python(payload)),
    ]:
        assert model.allowed_interviewer_emails == emails
    _ = payload.pop("allowed_interviewer_emails")
    assert Pad.model_validate(obj=payload).allowed_interviewer_emails is None
    assert (
        Pad.from_dict(
            data=TypeAdapter(type=PadDict).validate_python(payload)
        ).allowed_interviewer_emails
        is None
    )
