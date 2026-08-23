"""Validation helpers for question content sources."""

from collections.abc import Sequence
from pathlib import Path

from coderpad.types import QuestionFileContent


def validate_mutually_exclusive_question_content(
    *,
    contents: str | None,
    file_contents: Sequence[QuestionFileContent] | None,
    zip_file: Path | None,
) -> None:
    """Raise if more than one question content source is set.

    Args:
        contents: Legacy single-file contents.
        file_contents: Multi-file contents.
        zip_file: Zip archive of multi-file contents.

    Raises:
        ValueError: If more than one content source is provided.
    """
    provided = [
        name
        for name, value in (
            ("contents", contents),
            ("file_contents", file_contents),
            ("zip_file", zip_file),
        )
        if value is not None
    ]
    if len(provided) > 1:
        msg = (
            "Provide at most one of contents, file_contents, or "
            f"zip_file; got {', '.join(provided)}."
        )
        raise ValueError(msg)
