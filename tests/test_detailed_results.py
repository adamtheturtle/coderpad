"""UUID detail reports preserve candidate submissions and partial
grading.
"""

import pytest
import respx
from pydantic import ValidationError

from coderpad import (
    SCREEN_US_BASE_URL,
    AsyncCoderPad,
    CoderPad,
    ScreenDetailedQuestion,
    ScreenTest,
    ScreenTestQuestion,
)
from coderpad.exceptions import CoderPadError
from coderpad.json_types import JsonValue

_TEST_ID = 42
_FORBIDDEN = 403
_ID = "0558b3e3-b76c-42ea-9435-8da1adb7e232"
_URL = f"{SCREEN_US_BASE_URL}/assessment/api/v1.1/tests/42"
_QUESTION: dict[str, JsonValue] = {
    "id": _ID,
    "version": 4,
    "type": "PROJECT",
    "title": "Pagination",
    "domain": "API design",
    "warnings": [
        {
            "type": "CUSTOM_COMPANY_WARNING",
            "level": "UNUSUAL_ACTIVITY",
            "message": "Review activity",
        }
    ],
    "answer": {
        "project_answer": {
            "download_url": "/assessment/api/v1.1/tests/42/questions/"
            + _ID
            + "/project",
            "ai_assist_conversation_count": 0,
        }
    },
    "evaluation": {
        "rubric": {
            "criteria": [
                {
                    "label": "Clarity",
                    "description": "Explain the API",
                    "skill": "Communication",
                    "outcome": "PENDING_MANUAL_REVIEW",
                    "max_points": 10,
                    "awarded_points": None,
                    "result_message": "Review required",
                    "result_overridden_by_recruiter": False,
                    "review_mode": "AI_SUGGESTIONS",
                    "ai_review": {
                        "rationale": "Insufficient context",
                        "no_recommendation_reason": "CONFIDENCE_SCORE_TOO_LOW",
                    },
                },
                {
                    "label": "Correctness",
                    "outcome": "PASSED",
                    "awarded_points": 5,
                    "review_mode": "AI_GRADING",
                    "ai_review": {
                        "recommended_outcome": "PASSED",
                        "rationale": "Correct",
                    },
                },
            ]
        },
        "test_report": {
            "test_cases": [
                {
                    "key": "page-one",
                    "label": "First page",
                    "skill": "API design",
                    "outcome": "PASSED",
                    "output": "ok\n",
                    "test_identifier": "pagination.test#first",
                    "max_points": 20,
                    "awarded_points": 20,
                    "result_overridden_by_recruiter": False,
                },
                {
                    "key": "boundary",
                    "outcome": "NOT_RUN",
                    "awarded_points": None,
                },
            ]
        },
    },
    "max_points": 30,
    "awarded_points": 0,
    "time_limit_seconds": 1200,
    "time_spent_seconds": 1043,
    "first_access_time": 1685545371216,
    "submission_time": 1685545372216,
    "last_activity_time": 1685545373216,
    "answer_status": "ANSWERED",
    "grading_status": "PENDING_MANUAL_REVIEW",
    "timed_out": False,
    "result_overridden_by_recruiter": False,
    "marked_as_cheated_by_recruiter": False,
    "time_spent_outside_environment_seconds": 0,
    "environment_exit_count": 0,
}
_PAYLOAD: dict[str, JsonValue] = {
    "id": 42,
    "status": "need review",
    "timer_type": "PER_QUESTION",
    "organization_id": "organization-id",
    "candidate_language": "en",
    "approval_status": "TO_REVIEW",
    "questions": [_QUESTION],
    "report": {
        "warnings": ["Session warning"],
        "marked_as_cheated_by_recruiter": False,
        "time_spent_outside_environment_seconds": 0,
        "environment_exit_count": 0,
    },
}


def _assert_detail(result: ScreenTest) -> None:
    """Keep identities, order, explicit values, and pending reviews intact."""
    assert result.id == _TEST_ID
    assert result.status == "need review"
    assert (
        result.timer_type,
        result.organization_id,
        result.candidate_language,
        result.approval_status,
    ) == ("PER_QUESTION", "organization-id", "en", "TO_REVIEW")
    assert len(result.questions) == 1
    question = result.questions[0]
    assert isinstance(question, ScreenDetailedQuestion)
    assert question.model_dump(exclude_unset=True) == _QUESTION
    assert (
        question.id,
        question.version,
        question.type,
        question.title,
        question.domain,
    ) == (_ID, 4, "PROJECT", "Pagination", "API design")
    assert (
        question.answer_status,
        question.grading_status,
        question.awarded_points,
        question.max_points,
    ) == ("ANSWERED", "PENDING_MANUAL_REVIEW", 0, 30)
    assert (
        question.first_access_time,
        question.submission_time,
        question.last_activity_time,
    ) == (1685545371216, 1685545372216, 1685545373216)
    assert (
        question.time_limit_seconds,
        question.time_spent_seconds,
        question.timed_out,
    ) == (1200, 1043, False)
    assert (
        question.result_overridden_by_recruiter,
        question.marked_as_cheated_by_recruiter,
        question.time_spent_outside_environment_seconds,
        question.environment_exit_count,
    ) == (False, False, 0, 0)
    assert question.warnings is not None
    assert [
        (warning.type, warning.level, warning.message)
        for warning in question.warnings
    ] == [("CUSTOM_COMPANY_WARNING", "UNUSUAL_ACTIVITY", "Review activity")]
    assert question.answer is not None
    assert question.answer.project_answer is not None
    assert question.answer.project_answer.ai_assist_conversation_count == 0
    assert (
        question.answer.project_answer.download_url
        == "/assessment/api/v1.1/tests/42/questions/" + _ID + "/project"
    )
    assert question.evaluation is not None
    assert question.evaluation.rubric is not None
    criteria = question.evaluation.rubric.criteria
    assert criteria is not None
    assert [
        (criterion.label, criterion.outcome, criterion.awarded_points)
        for criterion in criteria
    ] == [
        ("Clarity", "PENDING_MANUAL_REVIEW", None),
        ("Correctness", "PASSED", 5),
    ]
    assert criteria[0].ai_review is not None
    assert criteria[0].ai_review.recommended_outcome is None
    assert (
        criteria[0].ai_review.no_recommendation_reason
        == "CONFIDENCE_SCORE_TOO_LOW"
    )
    assert criteria[1].ai_review is not None
    assert criteria[1].ai_review.recommended_outcome == "PASSED"
    assert question.evaluation.test_report is not None
    cases = question.evaluation.test_report.test_cases
    assert cases is not None
    assert [
        (case.key, case.outcome, case.awarded_points) for case in cases
    ] == [("page-one", "PASSED", 20), ("boundary", "NOT_RUN", None)]
    assert cases[0].output == "ok\n"
    assert result.report is not None
    assert result.report.warnings == ["Session warning"]
    assert (
        result.report.marked_as_cheated_by_recruiter,
        result.report.time_spent_outside_environment_seconds,
        result.report.environment_exit_count,
    ) == (False, 0, 0)


def test_detailed_get() -> None:
    """Detail UUIDs decode without changing the request or fetching
    media.
    """
    with respx.mock() as router:
        route = router.get(url=_URL).respond(status_code=200, json=_PAYLOAD)
        with CoderPad(
            api_key="interview-key", screen_api_key="screen-key"
        ) as client:
            result = client.screen.tests.get(
                test_id=42, with_community_stats=True
            )
        _assert_detail(result=result)
        assert route.call_count == 1
        request = route.calls.last.request
        assert dict(request.url.params) == {"withCommunityStats": "true"}
        assert request.headers["API-Key"] == "screen-key"
        assert request.headers.get(key="Authorization") is None


@pytest.mark.asyncio
async def test_async_detailed_get() -> None:
    """The asynchronous client exposes the same detailed report models."""
    with respx.mock() as router:
        route = router.get(url=_URL).respond(status_code=200, json=_PAYLOAD)
        async with AsyncCoderPad(
            api_key="interview-key", screen_api_key="screen-key"
        ) as client:
            result = await client.screen.tests.get(test_id=42)
        _assert_detail(result=result)
        assert dict(route.calls.last.request.url.params) == dict[str, str]()
        assert route.calls.last.request.headers["API-Key"] == "screen-key"


@pytest.mark.parametrize(
    argnames="timer", argvalues=[None, "GLOBAL", "UNLIMITED", "PER_QUESTION"]
)
@pytest.mark.parametrize(
    argnames="questions", argvalues=[None, [], [{"id": _ID}]]
)
def test_partial_detail(
    timer: str | None, questions: list[JsonValue] | None
) -> None:
    """Restricted and unfinished reports preserve absent timers and
    answers.
    """
    payload: dict[str, JsonValue] = {"id": 42, "timer_type": timer}
    if questions is not None:
        payload["questions"] = questions
    result = ScreenTest.from_dict(data=payload)
    assert result.timer_type == timer
    assert result.report is None
    if questions is not None and bool(questions):
        question = result.questions[0]
        assert isinstance(question, ScreenDetailedQuestion)
        assert question.id == _ID
        assert (
            question.answer,
            question.evaluation,
            question.warnings,
            question.time_limit_seconds,
            question.awarded_points,
            question.marked_as_cheated_by_recruiter,
        ) == (None, None, None, None, None, None)
    else:
        assert result.questions == list[ScreenDetailedQuestion]()


def test_list_summary_compatibility() -> None:
    """List summaries retain integer question IDs and pagination
    behavior.
    """
    with respx.mock() as router:
        route = router.get(url=_URL.rsplit(sep="/", maxsplit=1)[0]).respond(
            status_code=200,
            json={
                "tests": [
                    {
                        "id": 42,
                        "questions": [{"id": 123, "last_activity_time": 0}],
                    }
                ]
            },
        )
        with CoderPad(
            api_key="interview-key", screen_api_key="screen-key"
        ) as client:
            page = client.screen.tests.list()
        assert page.tests[0].questions == [
            ScreenTestQuestion(id=123, last_activity_time=0)
        ]
        assert route.call_count == 1


@pytest.mark.parametrize(argnames="status", argvalues=[400, 403, 404])
def test_detail_errors(status: int) -> None:
    """Detail failures keep their status and are never retried."""
    with respx.mock() as router:
        route = router.get(url=_URL).respond(
            status_code=status, json={"code": "NotFoundTestId"}
        )
        with (
            CoderPad(
                api_key="interview-key", screen_api_key="screen-key"
            ) as client,
            pytest.raises(expected_exception=CoderPadError) as error,
        ):
            _ = client.screen.tests.get(test_id=42)
        assert error.value.response.status_code == status
        assert route.call_count == 1


@pytest.mark.asyncio
async def test_async_detail_error() -> None:
    """Asynchronous permission failures use the same exception
    contract.
    """
    with respx.mock() as router:
        route = router.get(url=_URL).respond(
            status_code=403, json={"code": "FeatureNotAvailable"}
        )
        async with AsyncCoderPad(
            api_key="interview-key", screen_api_key="screen-key"
        ) as client:
            with pytest.raises(expected_exception=CoderPadError) as error:
                _ = await client.screen.tests.get(test_id=42)
        assert error.value.response.status_code == _FORBIDDEN
        assert route.call_count == 1


@pytest.mark.parametrize(
    argnames="payload",
    argvalues=[
        {"id": _ID, "awarded_points": "0"},
        {
            "id": _ID,
            "answer": {"mcq_answer": {"selected_choice_indexes": [True]}},
        },
        {"id": _ID, "warnings": [{"type": "custom", "level": "INVALID"}]},
    ],
)
def test_invalid_detail_types(payload: dict[str, JsonValue]) -> None:
    """Malformed known fields fail instead of coercing scores or
    indexes.
    """
    with pytest.raises(expected_exception=ValidationError):
        _ = ScreenTest.from_dict(data={"id": 42, "questions": [payload]})


@pytest.mark.parametrize(
    argnames="question",
    argvalues=[
        {
            "id": _ID,
            "type": "CODE",
            "answer": {
                "code_answer": {
                    "code": "print(0)\r\n",
                    "programming_language_id": "Python3",
                }
            },
            "evaluation": {
                "validation_code": {
                    "test_cases": [
                        {
                            "label": "Boundary",
                            "skill": "Collections",
                            "outcome": "FAILED",
                            "test_identifier": "testEmpty",
                            "max_points": 20,
                            "awarded_points": 0,
                            "result_message": "Timeout",
                            "result_overridden_by_recruiter": False,
                            "timed_out": True,
                        }
                    ]
                },
                "input_output": {
                    "test_cases": [
                        {
                            "label": "Output",
                            "skill": "Complexity",
                            "outcome": "NOT_RUN",
                            "max_points": 10,
                            "awarded_points": None,
                            "result_message": "Not run",
                            "result_overridden_by_recruiter": False,
                            "timed_out": False,
                        }
                    ]
                },
                "sql_query_result_comparison": {
                    "outcome": "PASSED",
                    "max_points": 5,
                    "awarded_points": 5,
                    "result_message": "Rows match",
                    "result_overridden_by_recruiter": True,
                    "timed_out": False,
                },
            },
        },
        {
            "id": _ID,
            "type": "GAME",
            "answer": {"game_answer": {"code": "move();\n"}},
        },
        {
            "id": _ID,
            "type": "TEXT",
            "answer": {"text_answer": {"text": "42"}},
            "evaluation": {
                "text_answer_matching": {
                    "accepted_answers": [
                        {"value": "42", "match_type": "EXACT"},
                        {"value": "[0-9]+", "match_type": "REGEX"},
                    ]
                }
            },
        },
        {
            "id": _ID,
            "type": "MCQ",
            "answer": {"mcq_answer": {"selected_choice_indexes": [2, 0]}},
            "evaluation": {
                "choice_selection": {"correct_choice_indexes": [0, 2]}
            },
            "mcq_details": {
                "choices": [
                    {"label": "Linear"},
                    {"label": "Quadratic"},
                    {"label": "Constant"},
                ],
                "selection_mode": "MULTIPLE",
                "randomize_choices": False,
            },
        },
        {
            "id": _ID,
            "type": "FILE_UPLOAD",
            "answer": {
                "file_upload_answer": {
                    "filename": "architecture.pdf",
                    "download_url": "https://example.com/file?signed=temporary",
                    "candidate_comment": "Design",
                }
            },
        },
        {
            "id": _ID,
            "type": "VIDEO",
            "answer": {
                "video_answer": {
                    "recordings": [
                        {
                            "id": _ID,
                            "url": "https://example.com/video",
                            "transcript_url": "https://example.com/transcript",
                            "duration_seconds": 187,
                        },
                        {
                            "id": "0558b3e3-b76c-42ea-9435-8da1adb7e233",
                            "duration_seconds": 0,
                        },
                    ],
                    "recording_availability": "AVAILABLE",
                    "candidate_comment": "Explanation",
                }
            },
        },
        {
            "id": _ID,
            "type": "VIDEO",
            "answer": {
                "video_answer": {
                    "recording_availability": "UNAVAILABLE",
                    "candidate_comment": "Deleted",
                }
            },
        },
        {
            "id": _ID,
            "type": "MULTI",
            "evaluation": {"rubric": {"criteria": []}},
            "warnings": [],
        },
    ],
)
def test_answer_and_evaluation_formats(question: dict[str, JsonValue]) -> None:
    """All submission and grading blocks survive detail response
    decoding.
    """
    result = ScreenTest.from_dict(data={"id": 42, "questions": [question]})
    assert isinstance(result.questions[0], ScreenDetailedQuestion)
    assert result.questions[0].model_dump(exclude_unset=True) == question


def test_unknown_fields_do_not_break_detail() -> None:
    """Additive service metadata is ignored without dropping known
    data.
    """
    result = ScreenTest.from_dict(
        data={
            "id": 42,
            "new_session_field": True,
            "questions": [
                {
                    "id": _ID,
                    "new_question_field": {},
                    "answer": {
                        "text_answer": {
                            "text": "Answer",
                            "new_answer_field": 1,
                        }
                    },
                }
            ],
        }
    )
    question = result.questions[0]
    assert isinstance(question, ScreenDetailedQuestion)
    assert question.answer is not None
    assert question.answer.text_answer is not None
    assert question.answer.text_answer.text == "Answer"


@pytest.mark.parametrize(
    argnames="flag", argvalues=[True, False, None, "false"]
)
def test_report_activity_flags(flag: JsonValue) -> None:
    """Only Boolean values become recruiter flags, preserving false and
    zero.
    """
    result = ScreenTest.from_dict(
        data={
            "id": 42,
            "report": {
                "marked_as_cheated_by_recruiter": flag,
                "time_spent_outside_environment_seconds": 0,
                "environment_exit_count": 0,
            },
        }
    )
    assert result.report is not None
    assert result.report.marked_as_cheated_by_recruiter is (
        flag if isinstance(flag, bool) else None
    )
