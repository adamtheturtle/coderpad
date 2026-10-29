"""Campaign definition reads preserve settings and use Screen
credentials.
"""

from typing import TYPE_CHECKING

import pytest
import respx

from coderpad import SCREEN_EU_BASE_URL, AsyncCoderPad, CoderPad
from coderpad.exceptions import CoderPadError

if TYPE_CHECKING:
    from coderpad.json_types import JsonValue

_URL = f"{SCREEN_EU_BASE_URL}/assessment/api/v1.1/campaigns/121"
_ID = "12221d67-75bd-49ff-83ca-620267e79ed8"
_DURATION = 60
_CALL_COUNT = 2


@pytest.mark.asyncio
async def test_campaign_definition() -> None:
    """Both clients retain order, nested values, and additive response
    fields.
    """
    payload: dict[str, JsonValue] = {
        "id": 121,
        "name": "Backend",
        "team_id": _ID,
        "questions": [
            {"type": "QUESTION", "question_id": _ID, "future": True},
            {
                "type": "RANDOM_QUESTION_SET",
                "configuration": {
                    "domain": "backend",
                    "skills": [],
                    "excluded_question_ids": [],
                    "future": True,
                },
            },
        ],
        "settings": {
            "timer": {
                "mode": "GLOBAL",
                "duration_minutes": _DURATION,
                "future": 1,
            },
            "ai_assist_enabled": False,
            "enabled_coding_agents": "",
            "follow_up_questions": {"enabled": False, "future": True},
            "future": True,
        },
        "future": True,
    }
    with respx.mock() as router:
        route = router.get(url=_URL).respond(status_code=200, json=payload)
        with CoderPad(
            api_key="interview-key",
            screen_api_key="screen-key",
            screen_base_url=SCREEN_EU_BASE_URL,
        ) as client:
            result = client.screen.campaigns.get(campaign_id=121)
        async with AsyncCoderPad(
            api_key="interview-key",
            screen_api_key="screen-key",
            screen_base_url=SCREEN_EU_BASE_URL,
        ) as async_client:
            async_result = await async_client.screen.campaigns.get(
                campaign_id=121
            )
        assert result == async_result
        assert result.team_id == _ID
        assert result.questions[0].question_id == _ID
        configuration = result.questions[1].configuration
        assert configuration is not None
        assert configuration.skills == []
        assert result.settings is not None
        assert result.settings.ai_assist_enabled is False
        assert result.settings.enabled_coding_agents == ""
        assert result.settings.languages is None
        assert result.settings.timer is not None
        assert result.settings.timer.duration_minutes == _DURATION
        assert route.call_count == _CALL_COUNT
        request = route.calls.last.request
        assert request.headers["API-Key"] == "screen-key"
        assert "Authorization" not in request.headers
        assert request.content == b""


@pytest.mark.asyncio
@pytest.mark.parametrize(argnames="status", argvalues=[401, 404])
async def test_campaign_errors(status: int) -> None:
    """Missing campaigns and invalid credentials keep the public error
    contract.
    """
    with respx.mock() as router:
        _ = router.get(url=_URL).respond(
            status_code=status, json={"message": "Unavailable"}
        )
        with (
            CoderPad(
                api_key="key",
                screen_api_key="screen-key",
                screen_base_url=SCREEN_EU_BASE_URL,
            ) as client,
            pytest.raises(expected_exception=CoderPadError) as error,
        ):
            _ = client.screen.campaigns.get(campaign_id=121)
        assert error.value.status_code == status
        async with AsyncCoderPad(
            api_key="key",
            screen_api_key="screen-key",
            screen_base_url=SCREEN_EU_BASE_URL,
        ) as async_client:
            with pytest.raises(
                expected_exception=CoderPadError
            ) as async_error:
                _ = await async_client.screen.campaigns.get(campaign_id=121)
        assert async_error.value.status_code == status


@pytest.mark.asyncio
@pytest.mark.parametrize(argnames="campaign_id", argvalues=[0, -1, True])
async def test_campaign_invalid_id(campaign_id: int) -> None:
    """Reject invalid integer identities without sending requests."""
    with respx.mock() as router:
        with (
            CoderPad(api_key="key", screen_api_key="screen-key") as client,
            pytest.raises(
                expected_exception=ValueError, match="positive integer"
            ),
        ):
            _ = client.screen.campaigns.get(campaign_id=campaign_id)
        async with AsyncCoderPad(
            api_key="key", screen_api_key="screen-key"
        ) as async_client:
            with pytest.raises(
                expected_exception=ValueError, match="positive integer"
            ):
                _ = await async_client.screen.campaigns.get(
                    campaign_id=campaign_id
                )
        assert router.calls.call_count == 0
