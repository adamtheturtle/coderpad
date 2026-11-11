"""Catalog requests preserve new metadata and keep identifiers in one
path segment.
"""

import httpx
import pytest
import respx

from coderpad import AsyncCoderPad, AuthenticationError, CoderPad
from coderpad.json_types import JsonValue


@pytest.mark.asyncio
@pytest.mark.parametrize(
    argnames="client_type", argvalues=[CoderPad, AsyncCoderPad]
)
async def test_language_catalog(
    client_type: type[CoderPad] | type[AsyncCoderPad],
) -> None:
    """Return complete catalog and starter metadata without narrowing
    fields.
    """
    payload = {
        "status": "OK",
        "environments": [
            {"slug": "multifile_python", "new_metadata": [1, None]}
        ],
    }
    client = client_type(api_key="test-key")
    with respx.mock() as router:
        listing = router.get(url="https://app.coderpad.io/api/languages").mock(
            return_value=httpx.Response(status_code=200, json=payload)
        )
        detail = router.get(
            url="https://app.coderpad.io/api/languages/multifile_python"
        ).mock(
            return_value=httpx.Response(
                status_code=200, json={"starter": {"main.py": ""}}
            )
        )
        assert await _language(client=client, language=None) == payload
        assert await _language(client=client, language="multifile_python") == {
            "starter": {"main.py": ""}
        }
        assert listing.calls.last.request.method == "GET"
        assert (
            detail.calls.last.request.headers["Authorization"]
            == 'Token token="test-key"'
        )
        for language in ("", ".", ".."):
            with pytest.raises(
                expected_exception=ValueError, match="identifier"
            ):
                await _language(client=client, language=language)
        _ = router.get(url="https://app.coderpad.io/api/languages").mock(
            return_value=httpx.Response(
                status_code=401, json={"status": "ERROR"}
            )
        )
        with pytest.raises(expected_exception=AuthenticationError):
            await _language(client=client, language=None)
    if isinstance(client, AsyncCoderPad):
        await client.aclose()
    else:
        client.close()


async def _language(
    client: CoderPad | AsyncCoderPad, language: str | None
) -> JsonValue:
    """Read through either public client with its declared result type."""
    if isinstance(client, AsyncCoderPad):
        return (
            await client.languages.list()
            if language is None
            else await client.languages.get(language=language)
        )
    return (
        client.languages.list()
        if language is None
        else client.languages.get(language=language)
    )
