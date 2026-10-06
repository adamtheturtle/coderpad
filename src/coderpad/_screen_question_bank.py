"""Validated UUID paths for the Screen question library."""

from uuid import UUID

from beartype import beartype


@beartype
def screen_bank_question_path(*, question_id: str | UUID) -> str:
    """Normalize a UUID without accepting arbitrary path segments."""
    identity = (
        question_id if isinstance(question_id, UUID) else UUID(hex=question_id)
    )
    return f"/questions/{identity}"
