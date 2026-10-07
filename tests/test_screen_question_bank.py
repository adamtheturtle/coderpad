"""Question library reads and writes keep UUIDs and writable fields
distinct.
"""

import json
from uuid import UUID

import pytest
import respx
from pydantic import ValidationError

from coderpad import (
    SCREEN_US_BASE_URL,
    AsyncCoderPad,
    CoderPad,
    ScreenCreatedQuestion,
    ScreenEnvironmentInput,
    ScreenProjectInput,
    ScreenQuestionDetails,
    ScreenQuestionFilters,
    ScreenQuestionSave,
    ScreenQuestionSummary,
)
from coderpad.exceptions import CoderPadError
from coderpad.json_types import JsonValue

_ID = "0558b3e3-b76c-42ea-9435-8da1adb7e232"
_URL = f"{SCREEN_US_BASE_URL}/assessment/api/v1.1/questions"
_DETAIL: dict[str, JsonValue] = {
    "id": _ID,
    "version": 4,
    "type": "PROJECT",
    "title": {"en": "Pagination", "fr": "Pagination"},
    "statement": {"en": "<p>Implement pagination.</p>"},
    "locales": ["en"],
    "domain": "Algorithms",
    "difficulty": "MEDIUM",
    "points": 100,
    "duration_seconds": 1200,
    "skill": "Arrays",
    "comment": "Internal",
    "creation_time": "2026-10-01T00:00:00Z",
    "modification_time": "2026-10-02T00:00:00Z",
    "from_coderpad_question_bank": False,
    "team_id": _ID,
    "automatically_selectable": False,
    "resources": [
        {"filename": "guide.pdf", "download_url": "https://example.com/guide"}
    ],
    "project_details": {
        "environment": {"environment_id": "nodejs", "version": "22"},
        "resources": [{"resource_id": "postgresql", "version": "16"}],
        "ai_assist_allowed": False,
        "ai_assist_additional_instructions": "Guide the candidate",
        "download_url": "https://example.com/archive",
    },
    "evaluation": {
        "test_report": {
            "test_cases": [
                {
                    "key": "page-one",
                    "label": {"en": "First page"},
                    "points": 20,
                    "weight": 1,
                }
            ]
        }
    },
}
_SAVE = ScreenQuestionSave(
    type="PROJECT",
    title={"en": "Pagination"},
    statement={"en": "<p>Build it.</p>"},
    automatically_selectable=False,
    comment=None,
    project_details=ScreenProjectInput(
        environment=ScreenEnvironmentInput(
            environment_id="nodejs", version="22"
        ),
        resources=[],
        ai_assist_allowed=False,
        temporary_file_id=_ID,
    ),
)
_SAVE_JSON: dict[str, JsonValue] = {
    "type": "PROJECT",
    "title": {"en": "Pagination"},
    "statement": {"en": "<p>Build it.</p>"},
    "automatically_selectable": False,
    "project_details": {
        "environment": {"environment_id": "nodejs", "version": "22"},
        "resources": [],
        "ai_assist_allowed": False,
        "temporary_file_id": _ID,
    },
}
_FILTERS = ScreenQuestionFilters(
    type="CODE",
    duration_seconds_min=0,
    duration_seconds_max=1200,
    difficulty="MEDIUM",
    domain="Algorithms & data",
    skill="Arrays",
    programming_language="C++",
    from_coderpad_question_bank=False,
    product="SCREEN",
    sort="modification_time",
    order="desc",
)
_PARAMS = {
    "type": "CODE",
    "duration_seconds_min": "0",
    "duration_seconds_max": "1200",
    "difficulty": "MEDIUM",
    "domain": "Algorithms & data",
    "skill": "Arrays",
    "programming_language": "C++",
    "from_coderpad_question_bank": "false",
    "product": "SCREEN",
    "sort": "modification_time",
    "order": "desc",
}


def _assert_details(question: ScreenQuestionDetails) -> None:
    """Preserve multilingual text, metadata, nested resources, and false
    flags.
    """
    assert question.model_dump(exclude_unset=True) == _DETAIL
    assert question.id == _ID
    assert question.title == {"en": "Pagination", "fr": "Pagination"}
    assert question.from_coderpad_question_bank is False
    assert question.project_details is not None
    assert question.project_details.ai_assist_allowed is False
    assert question.project_details.resources is not None
    assert [
        (resource.resource_id, resource.version)
        for resource in question.project_details.resources
    ] == [("postgresql", "16")]
    assert question.evaluation is not None
    assert question.evaluation.test_report is not None
    assert question.evaluation.test_report.test_cases is not None
    assert question.evaluation.test_report.test_cases[0].key == "page-one"


@pytest.mark.parametrize(
    argnames="question_id", argvalues=[_ID, UUID(hex=_ID)]
)
def test_question_get(question_id: str | UUID) -> None:
    """Full reads use a normalized UUID path and the independent Screen
    key.
    """
    with respx.mock() as router:
        route = router.get(url=f"{_URL}/{_ID}").respond(
            status_code=200, json=_DETAIL
        )
        with CoderPad(api_key="interview", screen_api_key="screen") as client:
            question = client.screen.questions.get(question_id=question_id)
        _assert_details(question=question)
        request = route.calls.last.request
        assert request.headers["API-Key"] == "screen"
        assert request.headers.get(key="Authorization") is None
        assert dict(request.url.params) == dict[str, str]()
        assert route.call_count == 1


@pytest.mark.asyncio
async def test_async_question_get() -> None:
    """Asynchronous reads expose the same nested question details."""
    with respx.mock() as router:
        route = router.get(url=f"{_URL}/{_ID}").respond(
            status_code=200, json=_DETAIL
        )
        async with AsyncCoderPad(
            api_key="interview", screen_api_key="screen"
        ) as client:
            question = await client.screen.questions.get(question_id=_ID)
        _assert_details(question=question)
        assert route.call_count == 1


@pytest.mark.parametrize(
    argnames="location", argvalues=[None, f"{_URL}/{_ID}"]
)
def test_create_question(location: str | None) -> None:
    """Creation accepts 201, retains Location, and sends only writable
    content.
    """
    with respx.mock() as router:
        route = router.post(url=_URL).respond(
            status_code=201,
            json=_DETAIL,
            headers={} if location is None else {"Location": location},
        )
        with CoderPad(api_key="interview", screen_api_key="screen") as client:
            result = client.screen.questions.create(question=_SAVE)
        assert isinstance(result, ScreenCreatedQuestion)
        _assert_details(question=result.question)
        assert result.location == location
        assert json.loads(s=route.calls.last.request.content) == _SAVE_JSON
        assert route.call_count == 1


@pytest.mark.asyncio
async def test_async_create_question() -> None:
    """Asynchronous creation preserves raw HTML and explicit empty
    arrays.
    """
    with respx.mock() as router:
        route = router.post(url=_URL).respond(
            status_code=201,
            json=_DETAIL,
            headers={"location": f"{_URL}/{_ID}"},
        )
        async with AsyncCoderPad(
            api_key="interview", screen_api_key="screen"
        ) as client:
            result = await client.screen.questions.create(question=_SAVE)
        _assert_details(question=result.question)
        assert result.location == f"{_URL}/{_ID}"
        assert json.loads(s=route.calls.last.request.content) == _SAVE_JSON


def test_update_question() -> None:
    """Updates use PUT and never attach fetched identifiers or
    versions.
    """
    with respx.mock() as router:
        route = router.put(url=f"{_URL}/{_ID}").respond(
            status_code=200, json=_DETAIL
        )
        with CoderPad(api_key="interview", screen_api_key="screen") as client:
            question = client.screen.questions.update(
                question_id=UUID(hex=_ID), question=_SAVE
            )
        _assert_details(question=question)
        assert json.loads(s=route.calls.last.request.content) == _SAVE_JSON
        assert route.call_count == 1


@pytest.mark.asyncio
async def test_async_update_question() -> None:
    """Asynchronous updates keep omitted default and optional fields
    absent.
    """
    with respx.mock() as router:
        route = router.put(url=f"{_URL}/{_ID}").respond(
            status_code=200, json=_DETAIL
        )
        async with AsyncCoderPad(
            api_key="interview", screen_api_key="screen"
        ) as client:
            question = await client.screen.questions.update(
                question_id=_ID, question=_SAVE
            )
        _assert_details(question=question)
        assert json.loads(s=route.calls.last.request.content) == _SAVE_JSON


@pytest.mark.parametrize(
    argnames="filters",
    argvalues=[
        None,
        _FILTERS,
        ScreenQuestionFilters(from_coderpad_question_bank=True),
    ],
)
def test_list_question_filters(filters: ScreenQuestionFilters | None) -> None:
    """Every filter is preserved, including boolean strings and zero
    bounds.
    """
    with respx.mock() as router:
        route = router.get(url=_URL).respond(
            status_code=200,
            json={
                "questions": [
                    {"id": _ID, "version": 4, "title": {"en": "Pagination"}}
                ],
                "pagination": {
                    "start": 0,
                    "limit": 1,
                    "has_more_items": True,
                    "next_start": 1,
                },
            },
        )
        with CoderPad(api_key="interview", screen_api_key="screen") as client:
            page = client.screen.questions.list(
                filters=filters, start=0, limit=1
            )
        expected = (
            dict(_PARAMS)
            if filters == _FILTERS
            else {}
            if filters is None
            else {"from_coderpad_question_bank": "true"}
        )
        expected.update({"start": "0", "limit": "1"})
        assert dict(route.calls.last.request.url.params) == expected
        assert page.questions == [
            ScreenQuestionSummary(
                id=_ID, version=4, title={"en": "Pagination"}
            )
        ]
        assert page.pagination is not None
        assert page.pagination.next_start == 1


@pytest.mark.asyncio
async def test_async_empty_page() -> None:
    """Absent pagination and empty pages decode without fabricated
    summaries.
    """
    with respx.mock() as router:
        route = router.get(url=_URL).respond(
            status_code=200, json={"questions": []}
        )
        async with AsyncCoderPad(
            api_key="interview", screen_api_key="screen"
        ) as client:
            page = await client.screen.questions.list()
        assert page.questions == list[ScreenQuestionSummary]()
        assert page.pagination is None
        assert dict(route.calls.last.request.url.params) == dict[str, str]()


@pytest.mark.parametrize(
    argnames="last_page",
    argvalues=[
        {},
        {"pagination": {"has_more_items": False}},
        {"pagination": {"has_more_items": True, "next_start": None}},
    ],
)
def test_question_pagination(last_page: dict[str, JsonValue]) -> None:
    """Iteration retains filters and stops when another page is
    unavailable.
    """
    with respx.mock() as router:
        first = router.get(
            url=_URL, params={**_PARAMS, "start": "0", "limit": "1"}
        ).respond(
            status_code=200,
            json={
                "questions": [{"id": _ID}],
                "pagination": {"has_more_items": True, "next_start": 1},
            },
        )
        second = router.get(
            url=_URL, params={**_PARAMS, "start": "1", "limit": "1"}
        ).respond(status_code=200, json={"questions": [], **last_page})
        with CoderPad(api_key="interview", screen_api_key="screen") as client:
            questions = list(
                client.screen.questions.all(filters=_FILTERS, limit=1)
            )
        assert questions == [ScreenQuestionSummary(id=_ID)]
        assert (first.call_count, second.call_count) == (1, 1)


@pytest.mark.asyncio
async def test_async_question_pagination() -> None:
    """Asynchronous iteration also follows advancing offsets with all
    filters.
    """
    with respx.mock() as router:
        first = router.get(url=_URL, params={**_PARAMS, "start": "0"}).respond(
            status_code=200,
            json={
                "questions": [{"id": _ID}],
                "pagination": {"has_more_items": True, "next_start": 1},
            },
        )
        second = router.get(
            url=_URL, params={**_PARAMS, "start": "1"}
        ).respond(status_code=200, json={"questions": []})
        async with AsyncCoderPad(
            api_key="interview", screen_api_key="screen"
        ) as client:
            questions = [
                question
                async for question in client.screen.questions.all(
                    filters=_FILTERS
                )
            ]
        assert questions == [ScreenQuestionSummary(id=_ID)]
        assert (first.call_count, second.call_count) == (1, 1)


@pytest.mark.parametrize(argnames="next_start", argvalues=[0, -1])
def test_repeated_question_offsets(next_start: int) -> None:
    """Malformed pagination cannot make an iterator request pages
    forever.
    """
    with respx.mock() as router:
        route = router.get(url=_URL).respond(
            status_code=200,
            json={
                "questions": [],
                "pagination": {
                    "has_more_items": True,
                    "next_start": next_start,
                },
            },
        )
        with (
            CoderPad(api_key="interview", screen_api_key="screen") as client,
            pytest.raises(
                expected_exception=ValueError,
                match="pagination did not advance",
            ),
        ):
            _ = list(client.screen.questions.all())
        assert route.call_count == 1


def _question_operation(*, client: CoderPad, operation: str) -> None:
    """Call the selected read or write for shared error checks."""
    if operation == "get":
        _ = client.screen.questions.get(question_id=_ID)
    elif operation == "create":
        _ = client.screen.questions.create(question=_SAVE)
    else:
        _ = client.screen.questions.update(question_id=_ID, question=_SAVE)


@pytest.mark.parametrize(argnames="status", argvalues=[400, 403, 404, 409])
@pytest.mark.parametrize(
    argnames="operation", argvalues=["get", "create", "update"]
)
def test_question_errors(status: int, operation: str) -> None:
    """Permission, validation, and conflict errors retain status without
    retries.
    """
    method = {"get": "GET", "create": "POST", "update": "PUT"}[operation]
    url = _URL if operation == "create" else f"{_URL}/{_ID}"
    with respx.mock() as router:
        route = router.request(method=method, url=url).respond(
            status_code=status,
            json={"code": "InvalidQuestionPayload", "message": "Cannot save"},
        )
        with (
            CoderPad(api_key="interview", screen_api_key="screen") as client,
            pytest.raises(expected_exception=CoderPadError) as error,
        ):
            _question_operation(client=client, operation=operation)
        assert error.value.response.status_code == status
        assert route.call_count == 1


@pytest.mark.parametrize(
    argnames="payload",
    argvalues=[
        {"type": "PROJECT", "id": _ID},
        {
            "type": "CODE",
            "code_details": {
                "available_programming_language_ids": ["Python3"]
            },
        },
        {
            "type": "PROJECT",
            "project_details": {"download_url": "https://example.com/archive"},
        },
        {"type": "GAME"},
        {"type": "PROJECT", "evaluation": {"test_report": {"test_cases": []}}},
    ],
)
def test_save_rejects_read_only_fields(payload: dict[str, JsonValue]) -> None:
    """Read-only metadata is rejected at the top level and nested save
    blocks.
    """
    with pytest.raises(expected_exception=ValidationError):
        _ = ScreenQuestionSave.model_validate(obj=payload)


@pytest.mark.parametrize(
    argnames="kind",
    argvalues=[
        "CODE",
        "MCQ",
        "TEXT",
        "GAME",
        "FILE_UPLOAD",
        "PROJECT",
        "VIDEO",
        "MULTI",
        "CLASH",
        "COURSE",
    ],
)
def test_read_question_types(kind: str) -> None:
    """Read models include legacy kinds without making them writable."""
    question = ScreenQuestionDetails.model_validate(
        obj={"id": _ID, "type": kind, "unknown_new_field": True}
    )
    assert question.type == kind
    assert question.model_dump(exclude_unset=True) == {"id": _ID, "type": kind}


@pytest.mark.parametrize(
    argnames="details",
    argvalues=[
        {
            "type": "CODE",
            "code_details": {
                "mode": "SINGLE_LANGUAGE",
                "programming_language_id": "Python3",
                "starter_code": "def solve():\n    pass\n",
                "validator_code": "validate()",
                "candidate_test_code": "solve()",
                "timeout_ms": 8000,
                "available_programming_language_ids": ["Python3"],
                "function_signature": {
                    "name": "solve",
                    "parameters": [
                        {
                            "name": "items",
                            "type": {"kind": "array", "element": "int"},
                        }
                    ],
                    "return_type": {"kind": "int"},
                },
                "possible_solution": {
                    "code": "return 42",
                    "programming_language_id": "Python3",
                },
                "show_function_signature_in_statement": False,
            },
            "evaluation": {
                "validation_code": {
                    "test_cases": [
                        {
                            "label": {"en": "Boundary"},
                            "test_identifier": "testEmpty",
                            "points": 0,
                            "weight": 1,
                            "difficulty": 200,
                            "contributes_to_score": False,
                            "visible_to_candidate": False,
                        }
                    ]
                },
                "input_output": {
                    "test_cases": [
                        {
                            "label": {"en": "Output"},
                            "input": "0",
                            "output": "0",
                            "timeout_ms_by_programming_language_id": {
                                "Python3": 5000
                            },
                        }
                    ]
                },
            },
        },
        {
            "type": "CODE",
            "code_details": {
                "database_engine": {
                    "engine_id": "postgresql",
                    "version": "16",
                },
                "database_setup_script": "CREATE TABLE example (id int);",
            },
            "evaluation": {
                "sql_query_result_comparison": {
                    "reference_query": "SELECT id FROM example",
                    "comparison": {
                        "row_order_matters": False,
                        "column_order_matters": True,
                        "compare_all_tables": False,
                    },
                }
            },
        },
        {
            "type": "MCQ",
            "mcq_details": {
                "choices": [{"label": {"en": "A"}}, {"label": {"en": "B"}}],
                "selection_mode": "SINGLE",
                "randomize_choices": False,
            },
            "evaluation": {
                "choice_selection": {"correct_choice_indexes": [0]}
            },
        },
        {
            "type": "TEXT",
            "text_details": {"evaluation_mode": "AUTOMATIC"},
            "evaluation": {
                "text_answer_matching": {
                    "accepted_answers": [
                        {"value": "42", "match_type": "EXACT"}
                    ]
                }
            },
        },
        {
            "type": "GAME",
            "game_details": {
                "available_programming_language_ids": ["C++", "Python3"]
            },
        },
        {
            "type": "FILE_UPLOAD",
            "file_upload_details": {
                "download_url": "https://example.com/statement"
            },
            "evaluation": {
                "rubric": {
                    "criteria": [
                        {
                            "label": {"en": "Clarity"},
                            "skill": "Communication",
                            "points": 100,
                            "weight": 1,
                            "review_mode": "HUMAN_ONLY",
                            "description": "Explain the design",
                        }
                    ]
                }
            },
        },
        {"type": "VIDEO", "video_details": {"recording_media": "AUDIO"}},
    ],
)
def test_type_specific_question_content(details: dict[str, JsonValue]) -> None:
    """Read content retains localized choices, authoring data, and grading
    settings.
    """
    payload: dict[str, JsonValue] = {"id": _ID, **details}
    question = ScreenQuestionDetails.model_validate(obj=payload)
    assert question.model_dump(exclude_unset=True) == payload


@pytest.mark.asyncio
@pytest.mark.parametrize(argnames="operation", argvalues=["create", "update"])
async def test_async_write_conflicts(operation: str) -> None:
    """Asynchronous writes surface business-rule conflicts after one
    request.
    """
    with respx.mock() as router:
        route = router.request(
            method="POST" if operation == "create" else "PUT",
            url=_URL if operation == "create" else f"{_URL}/{_ID}",
        ).respond(status_code=409, json={"code": "ConflictQuestionPayload"})
        async with AsyncCoderPad(
            api_key="interview", screen_api_key="screen"
        ) as client:
            if operation == "create":
                with pytest.raises(expected_exception=CoderPadError):
                    _ = await client.screen.questions.create(question=_SAVE)
            else:
                with pytest.raises(expected_exception=CoderPadError):
                    _ = await client.screen.questions.update(
                        question_id=_ID, question=_SAVE
                    )
        assert route.call_count == 1
