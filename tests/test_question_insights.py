"""Screen question insight responses retain partial metrics and score
buckets.
"""

from uuid import UUID

import pytest
import respx

from coderpad import (
    SCREEN_US_BASE_URL,
    AsyncCoderPad,
    CoderPad,
    ScreenQuestionInsights,
    ScreenQuestionRepartitionInsights,
    ScreenQuestionScoreRangeInsights,
    ScreenQuestionScoresDistributionInsights,
    ScreenQuestionUsageInsights,
)
from coderpad.exceptions import CoderPadError
from coderpad.json_types import JsonValue

_ID = "12345678-1234-1234-1234-123456789012"
_URL = f"{SCREEN_US_BASE_URL}/assessment/api/v1.1/questions/{_ID}/insights"
_USAGE = ScreenQuestionUsageInsights(
    view_count=42,
    last_view_time="2026-09-29T14:03:12.345Z",
    average_answer_duration_seconds=120,
    timeout_rate=0.05,
    average_score=0.75,
)
_ANSWER = ScreenQuestionRepartitionInsights(
    label="Option A", count=10, percentage=0.5, correct=False
)
_TESTCASE = ScreenQuestionRepartitionInsights(
    label="Boundary", count=5, percentage=0.25
)
_SCORES = ScreenQuestionScoresDistributionInsights(
    distribution=[
        ScreenQuestionScoreRangeInsights(
            score_range="ZERO_SCORE", candidate_count=5
        ),
        ScreenQuestionScoreRangeInsights(
            score_range="PARTIAL_SCORE", candidate_count=10
        ),
        ScreenQuestionScoreRangeInsights(
            score_range="FULL_SCORE", candidate_count=15
        ),
    ],
    total_candidates=30,
)
_PAYLOAD: dict[str, JsonValue] = {
    "id": _ID,
    "usage": {
        "view_count": 42,
        "last_view_time": "2026-09-29T14:03:12.345Z",
        "average_answer_duration_seconds": 120,
        "timeout_rate": 0.05,
        "average_score": 0.75,
    },
    "frequent_answers": [
        {"label": "Option A", "count": 10, "percentage": 0.5, "correct": False}
    ],
    "testcases_success": [
        {"label": "Boundary", "count": 5, "percentage": 0.25}
    ],
    "scores_distribution": {
        "distribution": [
            {"score_range": "ZERO_SCORE", "candidate_count": 5},
            {"score_range": "PARTIAL_SCORE", "candidate_count": 10},
            {"score_range": "FULL_SCORE", "candidate_count": 15},
        ],
        "total_candidates": 30,
    },
}


def _assert_insights(*, result: ScreenQuestionInsights) -> None:
    """Assert the public typed metrics without losing explicit false
    values.
    """
    assert result.id == _ID
    assert result.usage == _USAGE
    assert result.frequent_answers == [_ANSWER]
    assert result.testcases_success == [_TESTCASE]
    assert result.scores_distribution == _SCORES
    assert result.usage is not None
    assert {
        "views": result.usage.view_count,
        "last": result.usage.last_view_time,
        "duration": result.usage.average_answer_duration_seconds,
        "timeout": result.usage.timeout_rate,
        "score": result.usage.average_score,
    } == {
        "views": 42,
        "last": "2026-09-29T14:03:12.345Z",
        "duration": 120,
        "timeout": 0.05,
        "score": 0.75,
    }
    assert result.frequent_answers is not None
    answer = result.frequent_answers[0]
    assert {
        "label": answer.label,
        "count": answer.count,
        "percentage": answer.percentage,
        "correct": answer.correct,
    } == {
        "label": "Option A",
        "count": 10,
        "percentage": 0.5,
        "correct": False,
    }
    assert result.scores_distribution is not None
    assert (
        result.scores_distribution.total_candidates == _SCORES.total_candidates
    )
    assert result.scores_distribution.distribution is not None
    assert [
        (bucket.score_range, bucket.candidate_count)
        for bucket in result.scores_distribution.distribution
    ] == [("ZERO_SCORE", 5), ("PARTIAL_SCORE", 10), ("FULL_SCORE", 15)]


@pytest.mark.parametrize(
    argnames="question_id", argvalues=[_ID, UUID(hex=_ID)]
)
@pytest.mark.parametrize(argnames="language", argvalues=[None, "C++ & Python"])
def test_insights(question_id: str | UUID, language: str | None) -> None:
    """Exact language filters and Screen credentials reach the insights
    route.
    """
    with respx.mock() as router:
        route = router.get(url=_URL).respond(status_code=200, json=_PAYLOAD)
        with CoderPad(
            api_key="interview-key", screen_api_key="screen-key"
        ) as client:
            result = client.screen.questions.insights(
                question_id=question_id, programming_language=language
            )
        _assert_insights(result=result)
        assert route.call_count == 1
        request = route.calls.last.request
        assert dict(request.url.params) == (
            {} if language is None else {"programming_language": language}
        )
        assert request.headers["API-Key"] == "screen-key"
        assert request.headers.get(key="Authorization") is None
        assert request.content == b""


@pytest.mark.asyncio
@pytest.mark.parametrize(
    argnames="question_id", argvalues=[_ID, UUID(hex=_ID)]
)
@pytest.mark.parametrize(argnames="language", argvalues=[None, "C++ & Python"])
async def test_async_insights(
    question_id: str | UUID, language: str | None
) -> None:
    """Asynchronous insight requests preserve the same typed data and
    query.
    """
    with respx.mock() as router:
        route = router.get(url=_URL).respond(status_code=200, json=_PAYLOAD)
        async with AsyncCoderPad(
            api_key="interview-key", screen_api_key="screen-key"
        ) as client:
            result = await client.screen.questions.insights(
                question_id=question_id, programming_language=language
            )
        _assert_insights(result=result)
        assert route.call_count == 1
        request = route.calls.last.request
        assert dict(request.url.params) == (
            {} if language is None else {"programming_language": language}
        )
        assert request.headers["API-Key"] == "screen-key"
        assert request.headers.get(key="Authorization") is None
        assert request.content == b""


@pytest.mark.parametrize(
    argnames="payload",
    argvalues=[
        {},
        {
            "frequent_answers": [],
            "testcases_success": [],
            "scores_distribution": {"distribution": [], "total_candidates": 0},
        },
        {"usage": {"view_count": 0}},
    ],
)
def test_partial_insights(payload: dict[str, JsonValue]) -> None:
    """Omitted metrics, zero counts, and explicit empty lists survive
    decoding.
    """
    with respx.mock() as router:
        _ = router.get(url=_URL).respond(status_code=200, json=payload)
        with CoderPad(
            api_key="interview-key", screen_api_key="screen-key"
        ) as client:
            result = client.screen.questions.insights(question_id=_ID)
        assert result.model_dump(exclude_unset=True) == payload


@pytest.mark.asyncio
@pytest.mark.parametrize(
    argnames="payload",
    argvalues=[
        {},
        {
            "frequent_answers": [],
            "testcases_success": [],
            "scores_distribution": {"distribution": [], "total_candidates": 0},
        },
        {"usage": {"view_count": 0}},
    ],
)
async def test_async_partial_insights(payload: dict[str, JsonValue]) -> None:
    """Async partial insight responses preserve absence and explicit
    emptiness.
    """
    with respx.mock() as router:
        _ = router.get(url=_URL).respond(status_code=200, json=payload)
        async with AsyncCoderPad(
            api_key="interview-key", screen_api_key="screen-key"
        ) as client:
            result = await client.screen.questions.insights(question_id=_ID)
        assert result.model_dump(exclude_unset=True) == payload


@pytest.mark.parametrize(argnames="status", argvalues=[400, 404])
def test_insight_errors(status: int) -> None:
    """Invalid languages and unavailable questions retain API error
    statuses.
    """
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
            _ = client.screen.questions.insights(question_id=_ID)
        assert error.value.status_code == status
        assert route.call_count == 1


@pytest.mark.asyncio
@pytest.mark.parametrize(argnames="status", argvalues=[400, 404])
async def test_async_insight_errors(status: int) -> None:
    """Async HTTP errors use the same exception contract without
    retries.
    """
    with respx.mock() as router:
        route = router.get(url=_URL).respond(
            status_code=status, json={"message": "Unavailable"}
        )
        async with AsyncCoderPad(
            api_key="interview-key", screen_api_key="screen-key"
        ) as client:
            with pytest.raises(expected_exception=CoderPadError) as error:
                _ = await client.screen.questions.insights(question_id=_ID)
        assert error.value.status_code == status
        assert route.call_count == 1


def test_invalid_insight_identity() -> None:
    """Arbitrary path segments fail before credentials are sent."""
    with (
        respx.mock() as router,
        CoderPad(
            api_key="interview-key", screen_api_key="screen-key"
        ) as client,
    ):
        with pytest.raises(expected_exception=ValueError, match="UUID"):
            _ = client.screen.questions.insights(question_id="invalid/path")
        assert router.calls.call_count == 0
