"""Project-pad payloads preserve overlays and the multipart ZIP
contract.
"""

import json
from collections.abc import Sequence
from pathlib import Path
from urllib.parse import parse_qs

import httpx
import pytest
import respx

from coderpad import AsyncCoderPad, CoderPad, Pad, QuestionFileContent
from tests.pad_fixtures import pad_payload


@pytest.mark.asyncio
@pytest.mark.parametrize(
    argnames="client_type", argvalues=[CoderPad, AsyncCoderPad]
)
@pytest.mark.parametrize(
    argnames="source", argvalues=["template", "files", "zip", "directory"]
)
@pytest.mark.parametrize(argnames="emails", argvalues=[None, []])
async def test_project_pad(
    client_type: type[CoderPad] | type[AsyncCoderPad],
    source: str,
    emails: list[str] | None,
    tmp_path: Path,
) -> None:
    """Exercise every content transport with nullable project response
    fields.
    """
    payload = pad_payload()
    payload.update(
        {"language": None, "contents": None, "pad_environment_ids": [42]}
    )
    archive = tmp_path / "project.zip"
    _ = archive.write_bytes(data=b"project archive")
    project = tmp_path / "project"
    project.mkdir()
    _ = (project / "main.py").write_text(data="print(1)")
    with respx.mock() as router:
        route = router.post(url="https://app.coderpad.io/api/pads/").mock(
            return_value=httpx.Response(status_code=200, json=payload)
        )
        client = client_type(api_key="test-key")
        pad = await _create(
            client=client,
            contents=None,
            question_id=None,
            language="multifile_python",
            file_contents=[
                QuestionFileContent(path="main.py", contents="", hidden=True),
                QuestionFileContent(path="old.py", deleted=True),
            ]
            if source == "files"
            else None,
            zip_file=archive if source == "zip" else None,
            directory=project if source == "directory" else None,
            allowed_interviewer_emails=emails,
        )
        if isinstance(client, AsyncCoderPad):
            await client.aclose()
        else:
            client.close()
        assert pad.language is None
        assert pad.contents is None
        assert pad.pad_environment_ids == [42]
        request = route.calls.last.request
        if source in {"zip", "directory"}:
            assert 'name="pad[zip_file]"' in request.content.decode(
                encoding="latin1"
            )
            assert 'name="pad[language]"' in request.content.decode(
                encoding="latin1"
            )
            assert b"question[" not in request.content
        else:
            data = (
                json.loads(s=request.content)["pad"]
                if emails is not None
                else {
                    name: values[0]
                    for name, values in parse_qs(
                        qs=request.content.decode()
                    ).items()
                }
            )
            assert data["language"] == "multifile_python"
            if source == "files":
                assert json.loads(s=data["file_contents"]) == [
                    {"path": "main.py", "contents": "", "hidden": True},
                    {"path": "old.py", "deleted": True},
                ]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    argnames="client_type", argvalues=[CoderPad, AsyncCoderPad]
)
@pytest.mark.parametrize(
    argnames="source", argvalues=["contents", "files", "zip", "directory"]
)
async def test_question_seed_rejects_starter_content(
    client_type: type[CoderPad] | type[AsyncCoderPad],
    source: str,
    tmp_path: Path,
) -> None:
    """Reject ambiguous creation before reading files or sending a request."""
    client = client_type(api_key="test-key")
    with pytest.raises(expected_exception=ValueError, match="question_id"):
        await _create(
            client=client,
            language=None,
            question_id=1,
            contents="" if source == "contents" else None,
            file_contents=[] if source == "files" else None,
            zip_file=tmp_path if source == "zip" else None,
            directory=tmp_path if source == "directory" else None,
            allowed_interviewer_emails=None,
        )
    if isinstance(client, AsyncCoderPad):
        await client.aclose()
    else:
        client.close()


async def _create(
    *,
    client: CoderPad | AsyncCoderPad,
    language: str | None,
    contents: str | None,
    question_id: int | None,
    file_contents: Sequence[QuestionFileContent] | None,
    zip_file: Path | None,
    directory: Path | None,
    allowed_interviewer_emails: list[str] | None,
) -> Pad:
    """Exercise each public client without losing its declared result type."""
    if isinstance(client, AsyncCoderPad):
        return await client.pads.create(
            language=language,
            contents=contents,
            question_id=question_id,
            file_contents=file_contents,
            zip_file=zip_file,
            directory=directory,
            allowed_interviewer_emails=allowed_interviewer_emails,
        )
    return client.pads.create(
        language=language,
        contents=contents,
        question_id=question_id,
        file_contents=file_contents,
        zip_file=zip_file,
        directory=directory,
        allowed_interviewer_emails=allowed_interviewer_emails,
    )
