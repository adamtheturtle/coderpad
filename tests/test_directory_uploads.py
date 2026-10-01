"""Directory uploads use the ZIP importer through each question API."""

from collections.abc import Awaitable, Sequence
from email import policy
from email.parser import BytesParser
from io import BytesIO
from pathlib import Path
from zipfile import ZipFile

import pytest
import respx

from coderpad.async_client import AsyncCoderPad
from coderpad.client import CoderPad
from coderpad.types import Question, QuestionFileContent


@pytest.fixture(name="upload_client", params=["sync", "async"])
def fixture_upload_client(
    request: pytest.FixtureRequest,
    coderpad_client: CoderPad,
    async_coderpad_client: AsyncCoderPad,
) -> CoderPad | AsyncCoderPad:
    """Exercise both client implementations through their public APIs."""
    if request.param == "sync":
        return coderpad_client
    return async_coderpad_client


async def _upload(
    *,
    client: CoderPad | AsyncCoderPad,
    create: bool,
    directory: Path | None,
    exclude: Sequence[str],
    contents: str | None,
    file_contents: Sequence[QuestionFileContent] | None,
    zip_file: Path | None,
) -> None:
    """Upload using one of the four public create/update methods."""
    result: Question | Awaitable[Question] | Awaitable[None] | None
    if create:
        result = client.questions.create(
            title="Directory upload",
            language="multifile_python",
            directory=directory,
            exclude=exclude,
            contents=contents,
            file_contents=file_contents,
            zip_file=zip_file,
        )
    else:
        result = client.questions.update(
            question_id="123",
            directory=directory,
            exclude=exclude,
            contents=contents,
            file_contents=file_contents,
            zip_file=zip_file,
        )
    if isinstance(result, Awaitable):
        await result


def _archive_contents(*, router: respx.MockRouter) -> dict[str, bytes]:
    """Read the ZIP from the actual outgoing multipart request."""
    request = router.calls.last.request
    message = BytesParser(policy=policy.default).parsebytes(
        text=(
            f"Content-Type: {request.headers['Content-Type']}\r\n\r\n"
        ).encode()
        + request.content,
    )
    parts = [
        part
        for part in message.iter_parts()
        if part.get_filename() is not None
    ]
    assert len(parts) == 1
    part = parts[0]
    assert (
        part.get_param(param="name", header="content-disposition")
        == "question[zip_file]"
    )
    assert part.get_content_type() == "application/zip"
    payload = part.get_payload(decode=True)
    assert isinstance(payload, bytes)
    with ZipFile(file=BytesIO(initial_bytes=payload)) as archive:
        return {name: archive.read(name=name) for name in archive.namelist()}


@pytest.mark.asyncio
@pytest.mark.parametrize(argnames="create", argvalues=[True, False])
async def test_directory_preserves_files(
    upload_client: CoderPad | AsyncCoderPad,
    mock_coderpad_api: respx.MockRouter,
    tmp_path: Path,
    *,
    create: bool,
) -> None:
    """Preserve nested paths, hidden files, binary bytes and empty
    files.
    """
    expected = {
        ".cpad": b'{"targets": {}}\n',
        "nested/main.py": "print('caf\u00e9')\r\n".encode(),
        "nested/image.bin": bytes(range(256)),
        "empty.txt": b"",
        "uv.lock": b"keep unless explicitly excluded",
    }
    for name, data in expected.items():
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        _ = path.write_bytes(data=data)
    await _upload(
        client=upload_client,
        create=create,
        directory=tmp_path,
        exclude=(),
        contents=None,
        file_contents=None,
        zip_file=None,
    )
    assert _archive_contents(router=mock_coderpad_api) == expected


@pytest.mark.asyncio
@pytest.mark.parametrize(argnames="create", argvalues=[True, False])
async def test_directory_exclusions(
    upload_client: CoderPad | AsyncCoderPad,
    mock_coderpad_api: respx.MockRouter,
    tmp_path: Path,
    *,
    create: bool,
) -> None:
    """Prune directories and match file patterns at any depth."""
    paths = [
        "main.py",
        "nested/keep.py",
        "uv.lock",
        "nested/generated.pyc",
        "node_modules/dependency.js",
        "nested/node_modules/dependency.js",
        "package.egg-info/metadata",
        "nested/private/secret.txt",
    ]
    for name in paths:
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        _ = path.write_bytes(data=b"data")
    await _upload(
        client=upload_client,
        create=create,
        directory=tmp_path,
        exclude=(
            "node_modules",
            "*.egg-info",
            "*.pyc",
            "uv.lock",
            "nested/private",
        ),
        contents=None,
        file_contents=None,
        zip_file=None,
    )
    assert _archive_contents(router=mock_coderpad_api) == {
        "main.py": b"data",
        "nested/keep.py": b"data",
    }


@pytest.mark.asyncio
@pytest.mark.parametrize(argnames="create", argvalues=[True, False])
async def test_empty_directory(
    upload_client: CoderPad | AsyncCoderPad,
    mock_coderpad_api: respx.MockRouter,
    tmp_path: Path,
    *,
    create: bool,
) -> None:
    """An empty directory still produces a valid ZIP upload."""
    await _upload(
        client=upload_client,
        create=create,
        directory=tmp_path,
        exclude=(),
        contents=None,
        file_contents=None,
        zip_file=None,
    )
    assert _archive_contents(router=mock_coderpad_api) == {}


@pytest.mark.asyncio
@pytest.mark.parametrize(argnames="create", argvalues=[True, False])
@pytest.mark.parametrize(argnames="existing_file", argvalues=[True, False])
async def test_invalid_directory(
    upload_client: CoderPad | AsyncCoderPad,
    mock_coderpad_api: respx.MockRouter,
    tmp_path: Path,
    *,
    create: bool,
    existing_file: bool,
) -> None:
    """Reject missing directories and regular files before HTTP
    requests.
    """
    path = tmp_path / "invalid"
    if existing_file:
        _ = path.write_bytes(data=b"data")
    with pytest.raises(
        expected_exception=NotADirectoryError, match="Not a directory"
    ):
        await _upload(
            client=upload_client,
            create=create,
            directory=path,
            exclude=(),
            contents=None,
            file_contents=None,
            zip_file=None,
        )
    assert len(mock_coderpad_api.calls) == 0


@pytest.mark.asyncio
@pytest.mark.parametrize(argnames="create", argvalues=[True, False])
@pytest.mark.parametrize(
    argnames="source", argvalues=["contents", "file_contents", "zip_file"]
)
async def test_conflicting_directory_content(
    upload_client: CoderPad | AsyncCoderPad,
    mock_coderpad_api: respx.MockRouter,
    tmp_path: Path,
    source: str,
    *,
    create: bool,
) -> None:
    """Even empty content sources conflict with a directory upload."""
    with pytest.raises(expected_exception=ValueError, match="directory"):
        await _upload(
            client=upload_client,
            create=create,
            directory=tmp_path,
            exclude=(),
            contents="" if source == "contents" else None,
            file_contents=[] if source == "file_contents" else None,
            zip_file=tmp_path / "unused.zip" if source == "zip_file" else None,
        )
    assert len(mock_coderpad_api.calls) == 0


@pytest.mark.asyncio
@pytest.mark.parametrize(argnames="create", argvalues=[True, False])
async def test_exclusions_require_directory(
    upload_client: CoderPad | AsyncCoderPad,
    mock_coderpad_api: respx.MockRouter,
    *,
    create: bool,
) -> None:
    """Reject exclusions that would otherwise be silently ignored."""
    with pytest.raises(
        expected_exception=ValueError, match="exclude requires directory"
    ):
        await _upload(
            client=upload_client,
            create=create,
            directory=None,
            exclude=("node_modules",),
            contents=None,
            file_contents=None,
            zip_file=None,
        )
    assert len(mock_coderpad_api.calls) == 0


@pytest.mark.asyncio
@pytest.mark.parametrize(argnames="create", argvalues=[True, False])
@pytest.mark.parametrize(argnames="target_directory", argvalues=[True, False])
async def test_directory_symlinks(
    upload_client: CoderPad | AsyncCoderPad,
    mock_coderpad_api: respx.MockRouter,
    tmp_path: Path,
    *,
    create: bool,
    target_directory: bool,
) -> None:
    """Reject symbolic links unless explicitly excluded."""
    target = tmp_path / "target"
    if target_directory:
        target.mkdir()
    else:
        _ = target.write_bytes(data=b"outside upload directory")
    directory = tmp_path / "project"
    directory.mkdir()
    (directory / "link").symlink_to(
        target=target, target_is_directory=target_directory
    )
    with pytest.raises(expected_exception=ValueError, match="symbolic links"):
        await _upload(
            client=upload_client,
            create=create,
            directory=directory,
            exclude=(),
            contents=None,
            file_contents=None,
            zip_file=None,
        )
    assert len(mock_coderpad_api.calls) == 0
    await _upload(
        client=upload_client,
        create=create,
        directory=directory,
        exclude=("link",),
        contents=None,
        file_contents=None,
        zip_file=None,
    )
    assert _archive_contents(router=mock_coderpad_api) == {}
