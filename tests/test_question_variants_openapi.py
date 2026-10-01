"""Question variant contracts in the bundled OpenAPI document."""

import pytest

from coderpad import QuestionVariant, QuestionVariantFileContent
from coderpad.async_client import AsyncCoderPad
from coderpad.client import CoderPad
from tests.openapi_mock import JSONMapping

_PROJECT_TEMPLATE_ID = 12


@pytest.mark.parametrize(
    argnames="model",
    argvalues=[QuestionVariant, QuestionVariantFileContent],
)
def test_response_schema_matches_model(
    openapi_spec: JSONMapping,
    model: type[QuestionVariant] | type[QuestionVariantFileContent],
) -> None:
    """The response schema preserves required fields and null values."""
    components = openapi_spec["components"]
    assert isinstance(components, dict)
    schemas = components["schemas"]
    assert isinstance(schemas, dict)
    expected = model.model_json_schema(
        ref_template="#/components/schemas/{model}"
    )
    _ = expected.pop("$defs", None)
    assert schemas[model.__name__] == expected


def test_project_variant_from_spec(coderpad_client: CoderPad) -> None:
    """The synchronous client parses project examples served by the
    spec.
    """
    variants = coderpad_client.questions.variants.list(question_id=42)
    variant = coderpad_client.questions.variants.get(
        question_id=42, variant_id=7
    )
    assert variants == [variant]
    assert variant.language is None
    assert variant.project_template_slug == "multifile_python"
    assert variant.project_template_id == _PROJECT_TEMPLATE_ID
    assert variant.file_contents == [
        QuestionVariantFileContent(
            path="main.py", contents="print('hello')\n"
        ),
    ]


@pytest.mark.asyncio
async def test_async_project_variant_from_spec(
    async_coderpad_client: AsyncCoderPad,
) -> None:
    """The asynchronous client parses project examples served by the
    spec.
    """
    variants = await async_coderpad_client.questions.variants.list(
        question_id=42
    )
    variant = await async_coderpad_client.questions.variants.get(
        question_id=42, variant_id=7
    )
    assert variants == [variant]
    assert variant.language is None
    assert variant.project_template_slug == "multifile_python"
    assert variant.project_template_id == _PROJECT_TEMPLATE_ID
    assert variant.file_contents == [
        QuestionVariantFileContent(
            path="main.py", contents="print('hello')\n"
        ),
    ]
