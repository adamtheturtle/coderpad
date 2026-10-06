"""Tests for `coderpad` questions asynchronous client."""

import json
from pathlib import Path
from urllib.parse import parse_qs

import pytest
import respx

from coderpad.async_client import AsyncCoderPad
from coderpad.types import (
    CandidateInstruction,
    Language,
    QuestionFileContent,
    SortOrder,
)


@pytest.mark.asyncio
async def test_list_questions(
    async_coderpad_client: AsyncCoderPad,
) -> None:
    """Questions can be listed."""
    result = await async_coderpad_client.questions.list()
    assert result.total >= 0
    assert result[0].ai_assist_custom_system_prompt == "Only provide hints."


@pytest.mark.asyncio
async def test_list_questions_with_params(
    async_coderpad_client: AsyncCoderPad,
) -> None:
    """Questions can be listed with sort and page."""
    result = await async_coderpad_client.questions.list(
        sort=SortOrder.UPDATED_AT_DESC,
        page=1,
    )
    assert result.total >= 0


@pytest.mark.asyncio
async def test_create_question(
    async_coderpad_client: AsyncCoderPad,
) -> None:
    """A question can be created."""
    result = await async_coderpad_client.questions.create(
        title="Test Question",
        language="python",
    )
    assert bool(result.id)
    assert result.ai_assist_custom_system_prompt == "Only provide hints."


@pytest.mark.asyncio
async def test_create_question_all_params(
    async_coderpad_client: AsyncCoderPad,
) -> None:
    """A question can be created with all parameters."""
    result = await async_coderpad_client.questions.create(
        title="Test Question",
        language="python",
        description="A description",
        contents="def solve(): pass",
        solution="def solve(): return 42",
        ai_assist_custom_system_prompt="Only provide hints.",
        candidate_instructions=[
            CandidateInstruction(
                instructions="Part 1",
                name="First step",
                default_visible=True,
            ),
            CandidateInstruction(instructions="Part 2"),
        ],
    )
    assert bool(result.id)


@pytest.mark.asyncio
async def test_create_question_with_language_enum(
    async_coderpad_client: AsyncCoderPad,
) -> None:
    """A question can be created with a Language enum."""
    result = await async_coderpad_client.questions.create(
        title="Test Question",
        language=Language.PYTHON,
    )
    assert bool(result.id)


@pytest.mark.asyncio
async def test_create_question_with_file_contents(
    async_coderpad_client: AsyncCoderPad,
) -> None:
    """A question can be created with file contents."""
    result = await async_coderpad_client.questions.create(
        title="Multi-file Question",
        language=Language.MULTIFILE_PYTHON,
        file_contents=[
            QuestionFileContent(
                path="main.py",
                contents="print('hello')",
            ),
            QuestionFileContent(
                path="lib/utils.py",
                contents="def helper(): pass",
            ),
        ],
    )
    assert bool(result.id)


@pytest.mark.asyncio
async def test_create_question_with_zip_file(
    async_coderpad_client: AsyncCoderPad,
    tmp_path: Path,
) -> None:
    """A question can be created with a zip file."""
    zip_path = tmp_path / "project.zip"
    _ = zip_path.write_bytes(data=b"PK\x03\x04fake-zip")
    result = await async_coderpad_client.questions.create(
        title="Zip Question",
        language=Language.MULTIFILE_JAVA,
        zip_file=zip_path,
    )
    assert bool(result.id)


@pytest.mark.asyncio
async def test_create_question_candidate_instructions_body(
    async_coderpad_client: AsyncCoderPad,
    mock_coderpad_api: respx.MockRouter,
) -> None:
    """Candidate instructions are serialized into the form body."""
    await async_coderpad_client.questions.create(
        title="Live Question",
        language="python",
        ai_assist_custom_system_prompt="Only provide hints.",
        candidate_instructions=[
            CandidateInstruction(
                instructions="Part 1",
                name="First step",
                default_visible=True,
            ),
            CandidateInstruction(instructions="Part 2"),
        ],
    )
    request = mock_coderpad_api.calls.last.request
    sent = parse_qs(qs=request.content.decode())
    assert sent["question[ai_assist_custom_system_prompt]"] == [
        "Only provide hints.",
    ]
    assert json.loads(
        s=sent["question[candidate_instructions]"][0],
    ) == [
        {
            "instructions": "Part 1",
            "name": "First step",
            "default_visible": True,
        },
        {"instructions": "Part 2", "default_visible": False},
    ]


@pytest.mark.asyncio
async def test_create_question_rejects_multiple_content_sources(
    async_coderpad_client: AsyncCoderPad,
    tmp_path: Path,
) -> None:
    """Creating with multiple content sources raises ValueError."""
    zip_path = tmp_path / "project.zip"
    _ = zip_path.write_bytes(data=b"PK\x03\x04fake-zip")
    with pytest.raises(
        expected_exception=ValueError,
        match="at most one of contents, file_contents, zip_file",
    ):
        await async_coderpad_client.questions.create(
            title="Conflict",
            language="python",
            contents="print(1)",
            file_contents=[
                QuestionFileContent(path="main.py", contents="x"),
            ],
        )
    with pytest.raises(expected_exception=ValueError, match="zip_file"):
        await async_coderpad_client.questions.create(
            title="Conflict",
            language="python",
            contents="print(1)",
            zip_file=zip_path,
        )


@pytest.mark.asyncio
async def test_get_question(
    async_coderpad_client: AsyncCoderPad,
) -> None:
    """A question can be retrieved by id."""
    result = await async_coderpad_client.questions.get(
        question_id="123",
    )
    assert bool(result.id)
    assert result.ai_assist_custom_system_prompt == "Only provide hints."


@pytest.mark.asyncio
async def test_update_question(
    async_coderpad_client: AsyncCoderPad,
) -> None:
    """A question can be updated."""
    await async_coderpad_client.questions.update(
        question_id="123",
        title="Updated Question",
    )


@pytest.mark.asyncio
async def test_update_question_no_title(
    async_coderpad_client: AsyncCoderPad,
) -> None:
    """A question can be updated without a title."""
    await async_coderpad_client.questions.update(
        question_id="123",
        language="ruby",
    )


@pytest.mark.asyncio
async def test_update_question_all_params(
    async_coderpad_client: AsyncCoderPad,
) -> None:
    """A question can be updated with all params."""
    await async_coderpad_client.questions.update(
        question_id="123",
        title="Updated",
        language="ruby",
        description="New desc",
        contents="puts 'hi'",
        solution="puts 'answer'",
        ai_assist_custom_system_prompt="Only provide hints.",
        candidate_instructions=[
            CandidateInstruction(
                instructions="Part 1",
                name="First step",
                default_visible=True,
            ),
            CandidateInstruction(instructions="Part 2"),
        ],
    )


@pytest.mark.asyncio
async def test_update_question_with_file_contents(
    async_coderpad_client: AsyncCoderPad,
) -> None:
    """A question can be updated with file contents."""
    await async_coderpad_client.questions.update(
        question_id="123",
        file_contents=[
            QuestionFileContent(
                path="main.py",
                contents="print('updated')",
            ),
        ],
    )


@pytest.mark.asyncio
async def test_update_question_with_zip_file(
    async_coderpad_client: AsyncCoderPad,
    tmp_path: Path,
) -> None:
    """A question can be updated with a zip file."""
    zip_path = tmp_path / "project.zip"
    _ = zip_path.write_bytes(data=b"PK\x03\x04fake-zip")
    await async_coderpad_client.questions.update(
        question_id="123",
        zip_file=zip_path,
    )


@pytest.mark.asyncio
async def test_update_question_candidate_instructions_body(
    async_coderpad_client: AsyncCoderPad,
    mock_coderpad_api: respx.MockRouter,
) -> None:
    """Candidate instructions are serialized into the form body."""
    await async_coderpad_client.questions.update(
        question_id="123",
        candidate_instructions=[
            CandidateInstruction(
                instructions="Part 1",
                name="First step",
                default_visible=True,
            ),
            CandidateInstruction(instructions="Part 2"),
        ],
    )
    request = mock_coderpad_api.calls.last.request
    sent = parse_qs(qs=request.content.decode())
    assert json.loads(
        s=sent["question[candidate_instructions]"][0],
    ) == [
        {
            "instructions": "Part 1",
            "name": "First step",
            "default_visible": True,
        },
        {"instructions": "Part 2", "default_visible": False},
    ]


@pytest.mark.asyncio
async def test_update_question_ai_assist_system_prompt_body(
    async_coderpad_client: AsyncCoderPad,
    mock_coderpad_api: respx.MockRouter,
) -> None:
    """AI Assist's system prompt is serialized into the form body."""
    await async_coderpad_client.questions.update(
        question_id="123",
        ai_assist_custom_system_prompt="Only provide hints.",
    )
    request = mock_coderpad_api.calls.last.request
    sent = parse_qs(qs=request.content.decode())
    assert sent["question[ai_assist_custom_system_prompt]"] == [
        "Only provide hints.",
    ]


@pytest.mark.asyncio
async def test_update_question_rejects_multiple_content_sources(
    async_coderpad_client: AsyncCoderPad,
    tmp_path: Path,
) -> None:
    """Updating with multiple content sources raises ValueError."""
    zip_path = tmp_path / "project.zip"
    _ = zip_path.write_bytes(data=b"PK\x03\x04fake-zip")
    with pytest.raises(expected_exception=ValueError, match="at most one"):
        await async_coderpad_client.questions.update(
            question_id="1",
            contents="print(1)",
            zip_file=zip_path,
        )


@pytest.mark.asyncio
async def test_delete_question(
    async_coderpad_client: AsyncCoderPad,
) -> None:
    """A question can be deleted."""
    await async_coderpad_client.questions.delete(
        question_id="123",
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(argnames="shared", argvalues=[None, False, True])
async def test_question_sharing_and_database(
    async_coderpad_client: AsyncCoderPad,
    mock_coderpad_api: respx.MockRouter,
    *,
    shared: bool | None,
) -> None:
    """Question writes preserve optional sharing and database
    association.
    """
    _ = await async_coderpad_client.questions.create(
        title="Question",
        language="python",
        shared=shared,
        custom_database_id=12,
    )
    create_body = parse_qs(
        qs=mock_coderpad_api.calls.last.request.content.decode()
    )
    expected_create = {
        "question[title]": ["Question"],
        "question[language]": ["python"],
        "question[custom_database_id]": ["12"],
    }
    if shared is not None:
        expected_create["question[shared]"] = [str(object=shared).lower()]
    assert create_body == expected_create
    await async_coderpad_client.questions.update(
        question_id="123",
        shared=shared,
        custom_database_id=12,
    )
    update_body = parse_qs(
        qs=mock_coderpad_api.calls.last.request.content.decode()
    )
    expected_update = {"question[custom_database_id]": ["12"]}
    if shared is not None:
        expected_update["question[shared]"] = [str(object=shared).lower()]
    assert update_body == expected_update


@pytest.mark.asyncio
async def test_project_question_file_overlays(
    async_coderpad_client: AsyncCoderPad,
    mock_coderpad_api: respx.MockRouter,
) -> None:
    """Parent files preserve hidden, removal, and path-only entries."""
    files = [
        QuestionFileContent(
            path="hidden.py", contents="secret", hidden=True, deleted=False
        ),
        QuestionFileContent(path="obsolete.py", deleted=True),
        QuestionFileContent(path="empty.py", contents="", hidden=False),
    ]
    _ = await async_coderpad_client.questions.create(
        title="Project", language="python", file_contents=files
    )
    create_body = parse_qs(
        qs=mock_coderpad_api.calls.last.request.content.decode()
    )
    expected = [
        {
            "path": "hidden.py",
            "contents": "secret",
            "hidden": True,
            "deleted": False,
        },
        {"path": "obsolete.py", "deleted": True},
        {"path": "empty.py", "contents": "", "hidden": False},
    ]
    assert json.loads(s=create_body["question[file_contents]"][0]) == expected
    await async_coderpad_client.questions.update(
        question_id="123", file_contents=files
    )
    update_body = parse_qs(
        qs=mock_coderpad_api.calls.last.request.content.decode()
    )
    assert json.loads(s=update_body["question[file_contents]"][0]) == expected
    await async_coderpad_client.questions.update(
        question_id="123", file_contents=[]
    )
    empty_body = parse_qs(
        qs=mock_coderpad_api.calls.last.request.content.decode()
    )
    assert empty_body == {"question[file_contents]": ["[]"]}
