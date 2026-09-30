"""Question variant JSON contract tests."""

import json

import pytest
import respx

from coderpad import Language, QuestionVariantFileContent
from coderpad.async_client import AsyncCoderPad
from coderpad.exceptions import NotFoundError
from coderpad.json_types import JsonValue
from coderpad.transports import TransportResponse

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


@pytest.mark.asyncio
@respx.mock
async def test_variant_crud() -> None:
    """All five operations use nested routes and JSON mutations."""
    listing = respx.get(url=_BASE).respond(json={"variants": [_VARIANT]})
    showing = respx.get(url=_BASE + "/7").respond(json=_VARIANT)
    creating = respx.post(url=_BASE).respond(json=_VARIANT)
    updating = respx.put(url=_BASE + "/7").respond(json=_VARIANT)
    deleting = respx.delete(url=_BASE + "/7").respond(status_code=204)
    async with AsyncCoderPad(api_key="variant-key") as client:
        variants = await client.questions.variants.list(question_id=42)
        assert [variant.id for variant in variants] == [7]
        variant = await client.questions.variants.get(
            question_id=42, variant_id=7
        )
        assert variant.contents == "puts 1"
        assert variant.project_template_id is None
        assert variant.project_template_slug is None
        assert variant.display == "Ruby"
        created = await client.questions.variants.create(
            question_id=42,
            language="ruby",
            contents="",
            solution="puts 2",
        )
        assert created == variant
        updated = await client.questions.variants.update(
            question_id=42,
            variant_id=7,
            language="python3",
        )
        assert updated.id == variant.id
        await client.questions.variants.delete(question_id=42, variant_id=7)
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
@pytest.mark.asyncio
@respx.mock
async def test_explicit_code_state(contents: str | None) -> None:
    """Blank code and default-code resets retain their distinct JSON
    values.
    """
    route = respx.put(url=_BASE + "/7").respond(json=_VARIANT)
    async with AsyncCoderPad(api_key="key") as client:
        _ = await client.questions.variants.update(
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
@pytest.mark.asyncio
@respx.mock
async def test_file_payload(
    files: list[QuestionVariantFileContent] | str,
) -> None:
    """File payloads retain overlay flags and decoded paths."""
    route = respx.post(url=_BASE).respond(json=_VARIANT)
    async with AsyncCoderPad(api_key="key") as client:
        _ = await client.questions.variants.create(
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
@pytest.mark.asyncio
async def test_conflicting_sources(contents: str | None) -> None:
    """Explicit contents conflict with files even when blank or null."""
    async with AsyncCoderPad(api_key="key") as client:
        with pytest.raises(
            expected_exception=ValueError, match="cannot be combined"
        ):
            _ = await client.questions.variants.create(
                question_id=42,
                language="react",
                contents=contents,
                file_contents=[],
            )


@pytest.mark.asyncio
@respx.mock
async def test_flat_list_and_file_response() -> None:
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
    async with AsyncCoderPad(api_key="key") as client:
        variants = await client.questions.variants.list(question_id=42)
    assert variants[0].file_contents is not None
    assert variants[0].file_contents[0].hidden is True
    assert variants[0].file_contents == [
        QuestionVariantFileContent(
            path="src/hello world.jsx",
            contents="",
            hidden=True,
        )
    ]


@pytest.mark.asyncio
@respx.mock
async def test_variant_error() -> None:
    """Nested request errors use the existing exception mapping."""
    _ = respx.get(url=_BASE + "/7").respond(
        status_code=404, json={"error": "missing"}
    )
    async with AsyncCoderPad(api_key="key") as client:
        with pytest.raises(expected_exception=NotFoundError):
            _ = await client.questions.variants.get(
                question_id=42, variant_id=7
            )


class _FormOnlyTransport:
    """A legacy custom transport that still supports question
    operations.
    """

    async def __call__(
        self,
        *,
        method: str,
        url: str,
        headers: dict[str, str],
        params: dict[str, str | int] | None,
        data: dict[str, str] | None,
        files: dict[str, tuple[str, bytes, str]] | None,
    ) -> TransportResponse:
        """Return an empty library using the legacy form signature."""
        del method, url, headers, params, data, files
        return TransportResponse(
            status_code=200, headers={}, content=b'{"questions":[],"total":0}'
        )


class _KeywordJSONTransport:
    """A custom transport accepting JSON through keyword arguments."""

    async def __call__(self, **kwargs: object) -> TransportResponse:
        """Confirm that an enum environment is encoded as its language key."""
        assert kwargs["json"] == {"language": "ruby"}
        return TransportResponse(
            status_code=200,
            headers={},
            content=json.dumps(obj=_VARIANT).encode(),
        )


@pytest.mark.asyncio
async def test_legacy_custom_transport() -> None:
    """Legacy form operations work and variants fail before a request."""
    async with AsyncCoderPad(
        api_key="key", transport=_FormOnlyTransport()
    ) as client:
        page = await client.questions.list()
        assert page.total == 0
        with pytest.raises(expected_exception=TypeError, match="JSON-capable"):
            _ = client.questions.variants


@pytest.mark.asyncio
async def test_custom_keyword_json_transport() -> None:
    """Custom keyword transports can create variants with language
    values.
    """
    async with AsyncCoderPad(
        api_key="key", transport=_KeywordJSONTransport()
    ) as client:
        variant = await client.questions.variants.create(
            question_id=42, language=Language.RUBY
        )
        assert variant.language == "ruby"
