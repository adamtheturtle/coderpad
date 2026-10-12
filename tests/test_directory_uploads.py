"""Directory uploads use the ZIP importer through each question API."""

from collections.abc import AsyncGenerator, Awaitable, Sequence
from contextlib import asynccontextmanager
from email import policy
from email.parser import BytesParser
from io import BytesIO
from pathlib import Path
from shutil import copytree, ignore_patterns
from zipfile import ZipFile

import pytest
import respx

from coderpad.async_client import AsyncCoderPad
from coderpad.client import CoderPad
from coderpad.types import Question, QuestionFileContent


@asynccontextmanager
async def _upload_client(
    *,
    client_type: type[CoderPad] | type[AsyncCoderPad],
) -> AsyncGenerator[CoderPad | AsyncCoderPad]:
    """Construct the selected client and close it after the test."""
    client = client_type(
        api_key="test-key", base_url="https://app.coderpad.io"
    )
    if isinstance(client, AsyncCoderPad):
        async with client:
            yield client
    else:
        with client:
            yield client


async def _upload(
    *,
    client: CoderPad | AsyncCoderPad,
    create: bool,
    directory: Path,
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
            contents=contents,
            file_contents=file_contents,
            zip_file=zip_file,
        )
    else:
        result = client.questions.update(
            question_id="123",
            directory=directory,
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
@pytest.mark.parametrize(
    argnames="client_type",
    argvalues=[CoderPad, AsyncCoderPad],
    ids=["sync", "async"],
)
@pytest.mark.parametrize(argnames="create", argvalues=[True, False])
async def test_directory_preserves_files(
    client_type: type[CoderPad] | type[AsyncCoderPad],
    mock_coderpad_api: respx.MockRouter,
    tmp_path: Path,
    *,
    create: bool,
) -> None:
    """Preserve nested paths, hidden files, binary bytes and empty
    files.
    """
    async with _upload_client(client_type=client_type) as upload_client:
        expected = {
            ".cpad": b'{"targets": {}}\n',
            "nested/main.py": "print('caf\u00e9')\r\n".encode(),
            "nested/image.bin": bytes(range(256)),
            "empty.txt": b"",
            "uv.lock": b"include all files",
            "node_modules/dependency.js": b"include dependencies",
            "__pycache__/main.pyc": b"include generated files",
        }
        for name, data in expected.items():
            path = tmp_path / name
            path.parent.mkdir(parents=True, exist_ok=True)
            _ = path.write_bytes(data=data)
        await _upload(
            client=upload_client,
            create=create,
            directory=tmp_path,
            contents=None,
            file_contents=None,
            zip_file=None,
        )
        assert _archive_contents(router=mock_coderpad_api) == expected


@pytest.mark.asyncio
@pytest.mark.parametrize(
    argnames="client_type",
    argvalues=[CoderPad, AsyncCoderPad],
    ids=["sync", "async"],
)
@pytest.mark.parametrize(argnames="create", argvalues=[True, False])
async def test_staged_directory(
    client_type: type[CoderPad] | type[AsyncCoderPad],
    mock_coderpad_api: respx.MockRouter,
    tmp_path: Path,
    *,
    create: bool,
) -> None:
    """Callers can filter files with ``copytree`` before uploading."""
    async with _upload_client(client_type=client_type) as upload_client:
        source = tmp_path / "source"
        source.mkdir()
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
            path = source / name
            path.parent.mkdir(parents=True, exist_ok=True)
            _ = path.write_bytes(data=b"data")
        directory = Path(
            copytree(
                src=source,
                dst=tmp_path / "upload",
                ignore=ignore_patterns(
                    "node_modules",
                    "*.egg-info",
                    "*.pyc",
                    "uv.lock",
                    "private",
                ),
            )
        )
        await _upload(
            client=upload_client,
            create=create,
            directory=directory,
            contents=None,
            file_contents=None,
            zip_file=None,
        )
        assert _archive_contents(router=mock_coderpad_api) == {
            "main.py": b"data",
            "nested/keep.py": b"data",
        }


@pytest.mark.asyncio
@pytest.mark.parametrize(
    argnames="client_type",
    argvalues=[CoderPad, AsyncCoderPad],
    ids=["sync", "async"],
)
@pytest.mark.parametrize(argnames="create", argvalues=[True, False])
async def test_empty_directory(
    client_type: type[CoderPad] | type[AsyncCoderPad],
    mock_coderpad_api: respx.MockRouter,
    tmp_path: Path,
    *,
    create: bool,
) -> None:
    """An empty directory still produces a valid ZIP upload."""
    async with _upload_client(client_type=client_type) as upload_client:
        await _upload(
            client=upload_client,
            create=create,
            directory=tmp_path,
            contents=None,
            file_contents=None,
            zip_file=None,
        )
        assert _archive_contents(router=mock_coderpad_api) == {}


@pytest.mark.asyncio
@pytest.mark.parametrize(
    argnames="client_type",
    argvalues=[CoderPad, AsyncCoderPad],
    ids=["sync", "async"],
)
@pytest.mark.parametrize(argnames="create", argvalues=[True, False])
@pytest.mark.parametrize(argnames="existing_file", argvalues=[True, False])
async def test_invalid_directory(
    client_type: type[CoderPad] | type[AsyncCoderPad],
    mock_coderpad_api: respx.MockRouter,
    tmp_path: Path,
    *,
    create: bool,
    existing_file: bool,
) -> None:
    """Reject missing directories and regular files before HTTP
    requests.
    """
    async with _upload_client(client_type=client_type) as upload_client:
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
                contents=None,
                file_contents=None,
                zip_file=None,
            )
        assert len(mock_coderpad_api.calls) == 0


@pytest.mark.asyncio
@pytest.mark.parametrize(
    argnames="client_type",
    argvalues=[CoderPad, AsyncCoderPad],
    ids=["sync", "async"],
)
@pytest.mark.parametrize(argnames="create", argvalues=[True, False])
@pytest.mark.parametrize(
    argnames="source", argvalues=["contents", "file_contents", "zip_file"]
)
async def test_conflicting_directory_content(
    client_type: type[CoderPad] | type[AsyncCoderPad],
    mock_coderpad_api: respx.MockRouter,
    tmp_path: Path,
    source: str,
    *,
    create: bool,
) -> None:
    """Even empty content sources conflict with a directory upload."""
    async with _upload_client(client_type=client_type) as upload_client:
        with pytest.raises(expected_exception=ValueError, match="directory"):
            await _upload(
                client=upload_client,
                create=create,
                directory=tmp_path,
                contents="" if source == "contents" else None,
                file_contents=[] if source == "file_contents" else None,
                zip_file=tmp_path / "unused.zip"
                if source == "zip_file"
                else None,
            )
        assert len(mock_coderpad_api.calls) == 0


@pytest.mark.asyncio
@pytest.mark.parametrize(
    argnames="client_type",
    argvalues=[CoderPad, AsyncCoderPad],
    ids=["sync", "async"],
)
@pytest.mark.parametrize(argnames="create", argvalues=[True, False])
@pytest.mark.parametrize(argnames="target_directory", argvalues=[True, False])
async def test_directory_symlinks(
    client_type: type[CoderPad] | type[AsyncCoderPad],
    mock_coderpad_api: respx.MockRouter,
    tmp_path: Path,
    *,
    create: bool,
    target_directory: bool,
) -> None:
    """Reject symbolic links before making an upload request."""
    async with _upload_client(client_type=client_type) as upload_client:
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
        with pytest.raises(
            expected_exception=ValueError, match="symbolic links"
        ):
            await _upload(
                client=upload_client,
                create=create,
                directory=directory,
                contents=None,
                file_contents=None,
                zip_file=None,
            )
        assert len(mock_coderpad_api.calls) == 0
