"""Question variant JSON contract tests."""

import json

import pytest
import respx

from coderpad import QuestionVariantFileContent
from coderpad.client import CoderPad
from coderpad.exceptions import NotFoundError
from coderpad.json_types import JsonValue

_BASE = "https://app.coderpad.io/api/questions/42/variants"
_VARIANT: dict[str, JsonValue] = {
    "id": 7,
    "question_id": 42,
    "language": "ruby",
    "project_template_id": None,
    "project_template_slug": None,
    "display": "Ruby",
    "contents": "puts 1",
    "file_contents": None,
    "solution": "puts 2",
    "created_at": "2026-09-30T10:00:00Z",
    "updated_at": "2026-09-30T10:00:00Z",
}


@respx.mock
def test_variant_crud() -> None:
    """All five operations use nested routes and JSON mutations."""
    listing = respx.get(url=_BASE).respond(json={"variants": [_VARIANT]})
    showing = respx.get(url=_BASE + "/7").respond(json=_VARIANT)
    creating = respx.post(url=_BASE).respond(json=_VARIANT)
    updating = respx.put(url=_BASE + "/7").respond(json=_VARIANT)
    deleting = respx.delete(url=_BASE + "/7").respond(status_code=204)
    with CoderPad(api_key="variant-key") as client:
        variants = client.questions.variants.list(question_id=42)
        assert [variant.id for variant in variants] == [7]
        variant = client.questions.variants.get(question_id=42, variant_id=7)
        assert variant.contents == "puts 1"
        assert variant.project_template_id is None
        assert variant.project_template_slug is None
        assert variant.display == "Ruby"
        created = client.questions.variants.create(
            question_id=42,
            language="ruby",
            contents="",
            solution="puts 2",
        )
        assert created == variant
        updated = client.questions.variants.update(
            question_id=42,
            variant_id=7,
            language="python3",
        )
        assert updated.id == variant.id
        client.questions.variants.delete(question_id=42, variant_id=7)
    assert listing.call_count == 1
    assert showing.call_count == 1
    assert deleting.call_count == 1
    assert json.loads(s=creating.calls.last.request.content) == {
        "language": "ruby",
        "contents": "",
        "solution": "puts 2",
    }
    assert json.loads(s=updating.calls.last.request.content) == {
        "language": "python3"
    }
    assert (
        creating.calls.last.request.headers["content-type"]
        == "application/json"
    )
    assert (
        creating.calls.last.request.headers["authorization"]
        == 'Token token="variant-key"'
    )


@pytest.mark.parametrize(argnames="contents", argvalues=["", None])
@respx.mock
def test_explicit_code_state(contents: str | None) -> None:
    """Blank code and default-code resets retain their distinct JSON
    values.
    """
    route = respx.put(url=_BASE + "/7").respond(json=_VARIANT)
    with CoderPad(api_key="key") as client:
        _ = client.questions.variants.update(
            question_id=42,
            variant_id=7,
            contents=contents,
        )
    assert json.loads(s=route.calls.last.request.content) == {
        "contents": contents
    }


@pytest.mark.parametrize(
    argnames="files",
    argvalues=[
        [],
        [
            QuestionVariantFileContent(
                path="hello world.jsx",
                contents="hello",
                hidden=True,
            )
        ],
        [QuestionVariantFileContent(path="old.jsx", deleted=True)],
        "[]",
    ],
)
@respx.mock
def test_file_payload(files: list[QuestionVariantFileContent] | str) -> None:
    """File payloads retain overlay flags and decoded paths."""
    route = respx.post(url=_BASE).respond(json=_VARIANT)
    with CoderPad(api_key="key") as client:
        _ = client.questions.variants.create(
            question_id=42,
            language="react",
            file_contents=files,
        )
    expected = (
        files
        if isinstance(files, str)
        else [file.model_dump(exclude_none=True) for file in files]
    )
    assert json.loads(s=route.calls.last.request.content) == {
        "language": "react",
        "file_contents": expected,
    }


@pytest.mark.parametrize(argnames="contents", argvalues=["", None])
def test_conflicting_sources(contents: str | None) -> None:
    """Explicit contents conflict with files even when blank or null."""
    with (
        CoderPad(api_key="key") as client,
        pytest.raises(
            expected_exception=ValueError, match="cannot be combined"
        ),
    ):
        _ = client.questions.variants.create(
            question_id=42,
            language="react",
            contents=contents,
            file_contents=[],
        )


@respx.mock
def test_flat_list_and_file_response() -> None:
    """An unwrapped list decodes file metadata and literal paths."""
    payload: dict[str, JsonValue] = {
        **_VARIANT,
        "file_contents": [
            {
                "path": "src/hello world.jsx",
                "contents": "",
                "hidden": True,
            }
        ],
    }
    _ = respx.get(url=_BASE).respond(json=[payload])
    with CoderPad(api_key="key") as client:
        variants = client.questions.variants.list(question_id=42)
    assert variants[0].file_contents is not None
    assert variants[0].file_contents[0].hidden is True
    assert variants[0].file_contents == [
        QuestionVariantFileContent(
            path="src/hello world.jsx",
            contents="",
            hidden=True,
        )
    ]


@respx.mock
def test_variant_error() -> None:
    """Nested request errors use the existing exception mapping."""
    _ = respx.get(url=_BASE + "/7").respond(
        status_code=404, json={"error": "missing"}
    )
    with (
        CoderPad(api_key="key") as client,
        pytest.raises(expected_exception=NotFoundError),
    ):
        _ = client.questions.variants.get(question_id=42, variant_id=7)
