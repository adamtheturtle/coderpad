"""Typed campaign creation through synchronous and async transports."""

import json
from http import HTTPStatus

import pytest
import respx
from httpx import Response
from pydantic import ValidationError

from coderpad import (
    AsyncCoderPad,
    CoderPad,
    ForbiddenError,
    ScreenCampaignAccessPeriod,
    ScreenCampaignCreation,
    ScreenCampaignFollowUpQuestions,
    ScreenCampaignQuestion,
    ScreenCampaignSettings,
    ScreenCampaignTimer,
    ScreenCampaignWebcamProctoring,
    ScreenRandomQuestionConfiguration,
    ScreenRandomQuestionSet,
)

_URL = "https://screen.coderpad.io/assessment/api/v1.1/campaigns"
_QUESTION_ID = "12221d67-75bd-49ff-83ca-620267e79ed8"
_TEAM_ID = "0558b3e3-b76c-42ea-9435-8da1adb7e232"


def _settings() -> ScreenCampaignSettings:
    """Settings exercise false values, empty agents, and nested
    overrides.
    """
    return ScreenCampaignSettings(
        languages=["en", "fr"],
        timer=ScreenCampaignTimer(mode="PER_QUESTION"),
        invitation_expiration_days=14,
        access_period=ScreenCampaignAccessPeriod(
            min_start_time="2026-10-06T08:00:00Z"
        ),
        send_candidate_simplified_report=False,
        copy_paste_blocked=True,
        follow_up_questions=ScreenCampaignFollowUpQuestions(
            enabled=True, answer_format="TEXT"
        ),
        webcam_proctoring=ScreenCampaignWebcamProctoring(
            enabled=True, ai_analysis_enabled=False
        ),
        full_screen_required=True,
        ai_assist_enabled=False,
        enabled_coding_agents="",
    )


def _questions() -> list[ScreenCampaignQuestion | ScreenRandomQuestionSet]:
    """Explicit and random questions retain their order."""
    return [
        ScreenCampaignQuestion(question_id=_QUESTION_ID),
        ScreenRandomQuestionSet(
            configuration=ScreenRandomQuestionConfiguration(
                domain="backend",
                skills=["Algorithms"],
                question_type="CODE",
                target_duration_minutes=30,
                target_experience_level="SENIOR",
                excluded_question_ids=[_QUESTION_ID],
            )
        ),
    ]


@pytest.mark.asyncio
async def test_create_campaign() -> None:
    """Both clients send identical JSON and decode HTTP 201 IDs."""
    expected_call_count = 2
    expected = {
        "name": "Backend Engineer",
        "team_id": _TEAM_ID,
        "questions": [
            {"type": "QUESTION", "question_id": _QUESTION_ID},
            {
                "type": "RANDOM_QUESTION_SET",
                "configuration": {
                    "domain": "backend",
                    "skills": ["Algorithms"],
                    "question_type": "CODE",
                    "target_duration_minutes": 30,
                    "target_experience_level": "SENIOR",
                    "excluded_question_ids": [_QUESTION_ID],
                },
            },
        ],
        "settings": {
            "languages": ["en", "fr"],
            "timer": {"mode": "PER_QUESTION"},
            "invitation_expiration_days": 14,
            "access_period": {"min_start_time": "2026-10-06T08:00:00Z"},
            "send_candidate_simplified_report": False,
            "copy_paste_blocked": True,
            "follow_up_questions": {"enabled": True, "answer_format": "TEXT"},
            "webcam_proctoring": {
                "enabled": True,
                "ai_analysis_enabled": False,
            },
            "full_screen_required": True,
            "ai_assist_enabled": False,
            "enabled_coding_agents": "",
        },
    }
    with respx.mock() as router:
        route = router.post(url=_URL).mock(
            return_value=Response(status_code=201, json={"id": 121})
        )
        with CoderPad(
            api_key="interview-key", screen_api_key="screen-key"
        ) as client:
            result = client.screen.campaigns.create(
                name="Backend Engineer",
                questions=_questions(),
                settings=_settings(),
                team_id=_TEAM_ID,
            )
        assert result.model_dump() == {"id": 121}
        assert json.loads(s=route.calls.last.request.content) == expected
        assert route.calls.last.request.headers["API-Key"] == "screen-key"
        assert (
            route.calls.last.request.headers.get(key="Authorization") is None
        )
        async with AsyncCoderPad(
            api_key="interview-key", screen_api_key="screen-key"
        ) as client:
            result = await client.screen.campaigns.create(
                name="Backend Engineer",
                questions=_questions(),
                settings=_settings(),
                team_id=_TEAM_ID,
            )
        assert result.model_dump() == {"id": 121}
        assert json.loads(s=route.calls.last.request.content) == expected
        assert route.call_count == expected_call_count


@pytest.mark.asyncio
async def test_create_campaign_defaults_and_feature_error() -> None:
    """Defaults stay omitted and forbidden creation is never retried."""
    expected_call_count = 2
    expected = {
        "name": "Default team",
        "questions": [{"type": "QUESTION", "question_id": _QUESTION_ID}],
    }
    with respx.mock() as router:
        route = router.post(url=_URL).mock(
            return_value=Response(
                status_code=403,
                json={"code": "feature_unavailable", "message": "Unavailable"},
            )
        )
        with CoderPad(api_key="key", screen_api_key="screen-key") as client:
            with pytest.raises(expected_exception=ForbiddenError) as error:
                _ = client.screen.campaigns.create(
                    name="Default team",
                    questions=[
                        ScreenCampaignQuestion(question_id=_QUESTION_ID)
                    ],
                )
            assert error.value.status_code == HTTPStatus.FORBIDDEN
        assert json.loads(s=route.calls.last.request.content) == expected
        async with AsyncCoderPad(
            api_key="key", screen_api_key="screen-key"
        ) as client:
            with pytest.raises(expected_exception=ForbiddenError) as error:
                _ = await client.screen.campaigns.create(
                    name="Default team",
                    questions=[
                        ScreenCampaignQuestion(question_id=_QUESTION_ID)
                    ],
                )
            assert error.value.status_code == HTTPStatus.FORBIDDEN
        assert json.loads(s=route.calls.last.request.content) == expected
        assert route.call_count == expected_call_count


def test_campaign_selection_validation() -> None:
    """Question selections reject conflicting lists and malformed
    entries.
    """
    with pytest.raises(
        expected_exception=ValidationError, match="mutually exclusive"
    ) as error:
        _ = ScreenRandomQuestionConfiguration(
            included_question_ids=[], excluded_question_ids=[]
        )
    assert error.value.error_count() == 1
    expected_error_count = 2
    with pytest.raises(expected_exception=ValidationError) as error:
        _invalid_campaign = ScreenCampaignCreation(name="AB", questions=[])
    assert error.value.error_count() == expected_error_count
    with pytest.raises(expected_exception=ValidationError) as error:
        _invalid_settings = ScreenCampaignSettings.model_validate(
            obj={"unsupported_feature": True}
        )
    assert error.value.error_count() == 1
    assert ScreenRandomQuestionConfiguration(
        included_question_ids=[_QUESTION_ID]
    ).model_dump(exclude_none=True) == {
        "included_question_ids": [_QUESTION_ID]
    }
