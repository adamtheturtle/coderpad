"""Validated paths for candidate Screen question resources."""

from uuid import UUID

from beartype import beartype


@beartype
def screen_question_path(*, test_id: int, question_id: str | UUID) -> str:
    """Reject invalid identities before sending credentials or
    requests.
    """
    if test_id < 1:
        message = "test_id must be a positive integer."
        raise ValueError(message)
    question_uuid = (
        question_id if isinstance(question_id, UUID) else UUID(hex=question_id)
    )
    return f"/tests/{test_id}/questions/{question_uuid}"
