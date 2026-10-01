"""Validation and ZIP packaging for question content sources."""

from collections.abc import Iterator, Sequence
from io import BytesIO
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from beartype import beartype

from coderpad.types import QuestionFileContent


@beartype
def validate_mutually_exclusive_question_content(
    *,
    contents: str | None,
    file_contents: Sequence[QuestionFileContent] | None,
    zip_file: Path | None,
    directory: Path | None,
    exclude: Sequence[str],
) -> None:
    """Raise if more than one question content source is set.

    Args:
        contents: Legacy single-file contents.
        file_contents: Multi-file contents.
        zip_file: Zip archive of multi-file contents.
        directory: Directory to upload as a ZIP archive.
        exclude: Relative path patterns excluded from directory uploads.

    Raises:
        ValueError: If more than one content source is provided.
    """
    provided = [
        name
        for name, value in (
            ("contents", contents),
            ("file_contents", file_contents),
            ("zip_file", zip_file),
            ("directory", directory),
        )
        if value is not None
    ]
    if len(provided) > 1:
        msg = (
            "Provide at most one of contents, file_contents, "
            f"zip_file, or directory; got {', '.join(provided)}."
        )
        raise ValueError(msg)
    if len(exclude) > 0 and directory is None:
        msg = "exclude requires directory."
        raise ValueError(msg)


@beartype
def _directory_files(
    *, directory: Path, prefix: Path, exclude: Sequence[str]
) -> Iterator[tuple[Path, Path]]:
    """Yield sorted paths, pruning exclusions and rejecting symbolic links."""
    for path in sorted(directory.iterdir()):
        relative = prefix / path.name
        if any(relative.match(path_pattern=pattern) for pattern in exclude):
            continue
        if path.is_symlink():
            msg = f"Directory uploads do not support symbolic links: {path}"
            raise ValueError(msg)
        if path.is_dir():
            yield from _directory_files(
                directory=path, prefix=relative, exclude=exclude
            )
        else:
            yield path, relative


@beartype
def question_upload_files(
    *, zip_file: Path | None, directory: Path | None, exclude: Sequence[str]
) -> dict[str, tuple[str, bytes, str]] | None:
    """Build the multipart ZIP field without creating temporary files."""
    if directory is not None:
        if not directory.is_dir():
            msg = f"Not a directory: {directory}"
            raise NotADirectoryError(msg)
        with BytesIO() as buffer:
            with ZipFile(
                file=buffer, mode="w", compression=ZIP_DEFLATED
            ) as archive:
                for path, relative in _directory_files(
                    directory=directory, prefix=Path(), exclude=exclude
                ):
                    archive.write(
                        filename=path,
                        arcname=relative.as_posix(),
                    )
            contents = buffer.getvalue()
        filename = "project.zip"
    elif zip_file is not None:
        filename = zip_file.name
        contents = zip_file.read_bytes()
    else:
        return None
    return {"question[zip_file]": (filename, contents, "application/zip")}
