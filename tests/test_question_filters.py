"""Question filters, repeated query keys, and incremental enumeration."""

from collections.abc import Callable
from urllib.parse import parse_qs

import pytest
import respx
from httpx import Request, Response

from coderpad import AsyncCoderPad, CoderPad, QuestionSortOrder
from coderpad._pagination import next_page_number
from coderpad.transports import TransportResponse

_ORIGIN = "https://interview.example.com"


@pytest.mark.parametrize(argnames="organization", argvalues=[False, True])
@pytest.mark.asyncio
async def test_filtered_question_enumeration(
    live_variant_response: Callable[..., TransportResponse],
    *,
    organization: bool,
) -> None:
    """Both enumerators preserve filters and follow the exact next
    page.
    """
    path = "/api/organization/questions" if organization else "/api/questions/"
    payload = live_variant_response(
        method="GET", url="https://app.coderpad.io/api/questions/"
    ).json()
    assert isinstance(payload, dict)
    questions = payload["questions"]
    assert isinstance(questions, list)
    expected_ids = [42, 42]
    requests: list[Request] = []

    def respond(request: Request) -> Response:
        """Return a nonconsecutive second page."""
        requests.append(request)
        return Response(
            status_code=200,
            json={
                "questions": questions,
                "total": 2,
                "next_page": _ORIGIN + path + "?page=4"
                if request.url.params.get(key="page") == "1"
                else None,
            },
        )

    with respx.mock() as router:
        _ = router.get(url=_ORIGIN + path).mock(side_effect=respond)
        with CoderPad(api_key="key", base_url=_ORIGIN) as client:
            pages = (
                client.organization.questions.all(
                    sort=QuestionSortOrder.USED_DESC,
                    pad_type="live",
                    language="python",
                )
                if organization
                else client.questions.all(
                    sort=QuestionSortOrder.TITLE_ASC,
                    text="arrays & strings",
                    pad_types=["live", "take_home"],
                )
            )
            assert [question.id for question in pages] == expected_ids
        async with AsyncCoderPad(
            api_key="key", base_url=_ORIGIN
        ) as async_client:
            async_pages = (
                async_client.organization.questions.all(
                    sort=QuestionSortOrder.USED_DESC,
                    pad_type="live",
                    language="python",
                )
                if organization
                else async_client.questions.all(
                    sort=QuestionSortOrder.TITLE_ASC,
                    text="arrays & strings",
                    pad_types=["live", "take_home"],
                )
            )
            assert [
                question.id async for question in async_pages
            ] == expected_ids
    filters = (
        {"pad_type": ["live"], "language": ["python"], "sort": ["used,desc"]}
        if organization
        else {
            "text": ["arrays & strings"],
            "pad_types[]": ["live", "take_home"],
            "sort": ["title,asc"],
        }
    )
    assert [
        parse_qs(qs=request.url.query.decode()) for request in requests
    ] == [
        {**filters, "page": ["1"]},
        {**filters, "page": ["4"]},
        {**filters, "page": ["1"]},
        {**filters, "page": ["4"]},
    ]


def test_explicit_empty_question_filter() -> None:
    """Empty repeatable filters do not invent an empty-valued filter."""
    with respx.mock() as router:
        route = router.get(url=_ORIGIN + "/api/questions/").mock(
            return_value=Response(
                status_code=200,
                json={"questions": [], "total": 0, "next_page": None},
            )
        )
        with CoderPad(api_key="key", base_url=_ORIGIN) as client:
            _ = client.questions.list(pad_types=[])
        assert route.calls.last.request.url.query == b""


@pytest.mark.parametrize(
    argnames="next_page", argvalues=["?cursor=opaque", "?page=1"]
)
def test_question_pagination_requires_progress(next_page: str) -> None:
    """Question enumeration requires a supported numeric page link."""
    with pytest.raises(
        expected_exception=ValueError, match="numeric"
    ) as error:
        _ = next_page_number(
            next_page=next_page,
            base_url=_ORIGIN,
            path="/api/questions/",
            after_page=1,
        )
    assert (
        str(object=error.value)
        == "This endpoint requires an advancing numeric pagination link."
    )


@pytest.mark.parametrize(
    argnames="sort",
    argvalues=[
        QuestionSortOrder.CREATED_AT_ASC,
        QuestionSortOrder.CREATED_AT_DESC,
        QuestionSortOrder.UPDATED_AT_ASC,
        QuestionSortOrder.UPDATED_AT_DESC,
        QuestionSortOrder.TITLE_ASC,
        QuestionSortOrder.TITLE_DESC,
        QuestionSortOrder.USED_ASC,
        QuestionSortOrder.USED_DESC,
    ],
)
def test_question_sort_values(sort: QuestionSortOrder) -> None:
    """Every question-specific sort value reaches the API unchanged."""
    with respx.mock() as router:
        route = router.get(url=_ORIGIN + "/api/questions/").mock(
            return_value=Response(
                status_code=200,
                json={"questions": [], "total": 0, "next_page": None},
            )
        )
        with CoderPad(api_key="key", base_url=_ORIGIN) as client:
            _ = client.questions.list(sort=sort)
        assert parse_qs(qs=route.calls.last.request.url.query.decode()) == {
            "sort": [str(object=sort)]
        }
