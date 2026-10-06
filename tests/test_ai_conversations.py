"""Ordered Screen AI conversations retain evolving structured output."""

from uuid import UUID

import pytest
import respx
from pydantic import ValidationError

from coderpad import (
    SCREEN_US_BASE_URL,
    AsyncCoderPad,
    CoderPad,
    ScreenAIConversation,
    ScreenAIMessage,
)
from coderpad.exceptions import CoderPadError
from coderpad.json_types import JsonValue

_QUESTION_ID = "12345678-1234-1234-1234-123456789012"
_URL = (
    f"{SCREEN_US_BASE_URL}/assessment/api/v1.1/tests/11/"
    f"questions/{_QUESTION_ID}/ai-assist-conversations"
)
_TIME = "2026-09-29T14:03:12.345Z"
_OUTPUT: list[JsonValue] = [
    {
        "id": "output-1",
        "type": "message",
        "content": [{"type": "text", "text": "Explain the error"}],
        "unknown": {"future": [True, None, 3]},
    },
    {
        "id": "output-2",
        "type": "function_call",
        "name": "inspect",
        "arguments": {"path": "main.py"},
    },
]
_RESPONSE: dict[str, JsonValue] = {
    "conversations": [
        {
            "id": "conversation-1",
            "subject": "Debugging",
            "creation_time": _TIME,
            "messages": [
                {
                    "id": "message-1",
                    "role": "USER",
                    "creation_time": _TIME,
                    "output_items": _OUTPUT,
                },
                {
                    "id": "message-2",
                    "role": "ASSISTANT",
                    "creation_time": _TIME,
                    "output_items": [],
                },
            ],
        },
        {
            "id": "conversation-2",
            "messages": [{"id": "message-3", "role": "ASSISTANT"}],
        },
    ],
}


def _assert_conversations(*, result: list[ScreenAIConversation]) -> None:
    """Assert order, timestamps, exported types, and unknown output fields."""
    assert [conversation.id for conversation in result] == [
        "conversation-1",
        "conversation-2",
    ]
    assert result[0].subject == "Debugging"
    assert result[0].creation_time == _TIME
    assert result[1].subject is None
    assert result[1].creation_time is None
    assert [message.id for message in result[0].messages] == [
        "message-1",
        "message-2",
    ]
    assert [message.role for message in result[0].messages] == [
        "USER",
        "ASSISTANT",
    ]
    assert [message.creation_time for message in result[0].messages] == [
        _TIME,
        _TIME,
    ]
    assert result[0].messages[0].output_items == _OUTPUT
    assert result[0].messages[1].output_items == list[JsonValue]()
    assert result[1].messages[0].output_items is None
    assert result[1].messages[0].creation_time is None
    assert isinstance(result[0].messages[0], ScreenAIMessage)


@pytest.mark.parametrize(
    argnames="question_id", argvalues=[_QUESTION_ID, UUID(hex=_QUESTION_ID)]
)
def test_conversations(question_id: str | UUID) -> None:
    """Synchronous requests use only the independent Screen key."""
    with respx.mock() as router:
        route = router.get(url=_URL).respond(status_code=200, json=_RESPONSE)
        with CoderPad(
            api_key="interview-key", screen_api_key="screen-key"
        ) as client:
            result = client.screen.tests.ai_assist_conversations(
                test_id=11, question_id=question_id
            )
        _assert_conversations(result=result)
        assert route.call_count == 1
        request = route.calls.last.request
        assert str(object=request.url) == _URL
        assert request.content == b""
        assert request.headers.get(key="Authorization") is None
        assert request.headers["API-Key"] == "screen-key"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    argnames="question_id", argvalues=[_QUESTION_ID, UUID(hex=_QUESTION_ID)]
)
async def test_async_conversations(question_id: str | UUID) -> None:
    """Asynchronous requests retain the same fields and credentials."""
    with respx.mock() as router:
        route = router.get(url=_URL).respond(status_code=200, json=_RESPONSE)
        async with AsyncCoderPad(
            api_key="interview-key", screen_api_key="screen-key"
        ) as client:
            result = await client.screen.tests.ai_assist_conversations(
                test_id=11, question_id=question_id
            )
        _assert_conversations(result=result)
        assert route.call_count == 1
        request = route.calls.last.request
        assert str(object=request.url) == _URL
        assert request.content == b""
        assert request.headers.get(key="Authorization") is None
        assert request.headers["API-Key"] == "screen-key"


@pytest.mark.parametrize(
    argnames="payload", argvalues=[{}, {"conversations": []}]
)
def test_empty_conversations(payload: dict[str, JsonValue]) -> None:
    """Missing and empty collections produce empty ordered lists."""
    with respx.mock() as router:
        _ = router.get(url=_URL).respond(status_code=200, json=payload)
        with CoderPad(
            api_key="interview-key", screen_api_key="screen-key"
        ) as client:
            assert (
                client.screen.tests.ai_assist_conversations(
                    test_id=11, question_id=_QUESTION_ID
                )
                == list[ScreenAIConversation]()
            )
    assert (
        ScreenAIConversation(id="conversation-1").messages
        == list[ScreenAIMessage]()
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    argnames="payload", argvalues=[{}, {"conversations": []}]
)
async def test_async_empty_conversations(
    payload: dict[str, JsonValue],
) -> None:
    """Asynchronous empty collections have the same behavior."""
    with respx.mock() as router:
        _ = router.get(url=_URL).respond(status_code=200, json=payload)
        async with AsyncCoderPad(
            api_key="interview-key", screen_api_key="screen-key"
        ) as client:
            assert (
                await client.screen.tests.ai_assist_conversations(
                    test_id=11, question_id=_QUESTION_ID
                )
                == list[ScreenAIConversation]()
            )


@pytest.mark.parametrize(argnames="status", argvalues=[404, 409])
def test_conversation_errors(status: int) -> None:
    """Missing projects and unfinished tests use the public API errors."""
    with respx.mock() as router:
        route = router.get(url=_URL).respond(
            status_code=status, json={"message": "Unavailable"}
        )
        with (
            CoderPad(
                api_key="interview-key", screen_api_key="screen-key"
            ) as client,
            pytest.raises(expected_exception=CoderPadError) as error,
        ):
            _ = client.screen.tests.ai_assist_conversations(
                test_id=11, question_id=_QUESTION_ID
            )
        assert error.value.status_code == status
        assert route.call_count == 1


@pytest.mark.asyncio
@pytest.mark.parametrize(argnames="status", argvalues=[404, 409])
async def test_async_conversation_errors(status: int) -> None:
    """Asynchronous API errors have the same status and no retry."""
    with respx.mock() as router:
        route = router.get(url=_URL).respond(
            status_code=status, json={"message": "Unavailable"}
        )
        async with AsyncCoderPad(
            api_key="interview-key", screen_api_key="screen-key"
        ) as client:
            with pytest.raises(expected_exception=CoderPadError) as error:
                _ = await client.screen.tests.ai_assist_conversations(
                    test_id=11, question_id=_QUESTION_ID
                )
        assert error.value.status_code == status
        assert route.call_count == 1


def test_invalid_conversation_role() -> None:
    """Malformed response roles are rejected rather than invented."""
    with respx.mock() as router:
        _ = router.get(url=_URL).respond(
            status_code=200,
            json={
                "conversations": [
                    {
                        "id": "conversation",
                        "messages": [{"id": "message", "role": "UNKNOWN"}],
                    }
                ]
            },
        )
        with (
            CoderPad(
                api_key="interview-key", screen_api_key="screen-key"
            ) as client,
            pytest.raises(expected_exception=ValidationError),
        ):
            _ = client.screen.tests.ai_assist_conversations(
                test_id=11, question_id=_QUESTION_ID
            )


@pytest.mark.parametrize(
    argnames=("test_id", "question_id"),
    argvalues=[(0, _QUESTION_ID), (11, "invalid/path")],
)
def test_invalid_conversation_identity(test_id: int, question_id: str) -> None:
    """Malformed resource identities fail before sending credentials."""
    with (
        respx.mock() as router,
        CoderPad(
            api_key="interview-key", screen_api_key="screen-key"
        ) as client,
    ):
        with pytest.raises(
            expected_exception=ValueError, match=r"positive integer|UUID"
        ):
            _ = client.screen.tests.ai_assist_conversations(
                test_id=test_id, question_id=question_id
            )
        assert router.calls.call_count == 0
