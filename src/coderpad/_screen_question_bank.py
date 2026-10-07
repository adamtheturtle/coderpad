"""Validated UUID paths for the Screen question library."""

from uuid import UUID

from beartype import beartype
from pydantic import TypeAdapter

from coderpad._screen_response import json_object
from coderpad.screen_question_types import (
    ScreenCreatedQuestion,
    ScreenQuestionDetails,
    ScreenQuestionFilters,
    ScreenQuestionsPage,
    ScreenQuestionSummary,
)
from coderpad.screen_types import ScreenPagination
from coderpad.transports import TransportResponse


@beartype
def screen_bank_question_path(*, question_id: str | UUID) -> str:
    """Normalize a UUID without accepting arbitrary path segments."""
    identity = (
        question_id if isinstance(question_id, UUID) else UUID(hex=question_id)
    )
    return f"/questions/{identity}"


@beartype
def screen_question_params(
    *,
    filters: ScreenQuestionFilters | None,
    start: int | None,
    limit: int | None,
) -> dict[str, str | int]:
    """Serialize exact filter names while preserving false and zero values."""
    params: dict[str, str | int] = {}
    if filters is not None:
        filter_adapter: TypeAdapter[dict[str, str | int | bool]] = TypeAdapter(
            type=dict[str, str | int | bool]
        )
        values = filter_adapter.validate_python(
            filters.model_dump(exclude_none=True)
        )
        for key, value in values.items():
            if isinstance(value, bool):
                params[key] = "true" if value else "false"
            else:
                params[key] = value
    if start is not None:
        params["start"] = start
    if limit is not None:
        params["limit"] = limit
    return params


@beartype
def screen_questions_page(*, value: object) -> ScreenQuestionsPage:
    """Decode question summaries and potentially partial offset
    metadata.
    """
    data = json_object(value=value)
    raw_pagination = data.get("pagination")
    pagination = (
        ScreenPagination.from_dict(data=raw_pagination)
        if isinstance(raw_pagination, dict)
        else None
    )
    summary_adapter: TypeAdapter[list[ScreenQuestionSummary]] = TypeAdapter(
        type=list[ScreenQuestionSummary]
    )
    questions = summary_adapter.validate_python(data.get("questions", []))
    return ScreenQuestionsPage(questions=questions, pagination=pagination)


@beartype
def next_question_start(
    *, page: ScreenQuestionsPage, current: int
) -> int | None:
    """Stop at the last page and reject repeated or backward offsets."""
    pagination = page.pagination
    if (
        pagination is None
        or not pagination.has_more_items
        or pagination.next_start is None
    ):
        return None
    if pagination.next_start <= current:
        message = "Screen question pagination did not advance."
        raise ValueError(message)
    return pagination.next_start


@beartype
def screen_created_question(
    *, response: TransportResponse
) -> ScreenCreatedQuestion:
    """Return details with a case-insensitive Location header lookup."""
    location = next(
        (
            value
            for key, value in response.headers.items()
            if key.lower() == "location"
        ),
        None,
    )
    return ScreenCreatedQuestion(
        question=ScreenQuestionDetails.model_validate(obj=response.json()),
        location=location,
    )
