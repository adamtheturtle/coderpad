"""Tests for `coderpad` organization asynchronous client."""

from http import HTTPStatus

import pytest
import respx

from coderpad.async_client import AsyncCoderPad
from coderpad.exceptions import NotFoundError
from coderpad.transports import (
    TransportResponse,
)
from coderpad.types import (
    OrganizationUser,
    SortOrder,
)


@pytest.mark.asyncio
async def test_get_quota(
    async_coderpad_client: AsyncCoderPad,
) -> None:
    """Quota information can be retrieved."""
    result = await async_coderpad_client.organization.get_quota()
    assert result.pads_used >= 0


@pytest.mark.asyncio
async def test_get_organization(
    async_coderpad_client: AsyncCoderPad,
) -> None:
    """Organization information can be retrieved."""
    result = await async_coderpad_client.organization.get()
    assert bool(result.organization_name)


@pytest.mark.asyncio
async def test_get_organization_stats(
    async_coderpad_client: AsyncCoderPad,
) -> None:
    """Organization stats can be retrieved."""
    result = await async_coderpad_client.organization.get_stats()
    assert result.pads_created >= 0


@pytest.mark.asyncio
async def test_get_organization_stats_with_params(
    async_coderpad_client: AsyncCoderPad,
) -> None:
    """Organization stats can be filtered by time."""
    result = await async_coderpad_client.organization.get_stats(
        start_time="2023-07-01T00:00:00Z",
        end_time="2023-07-31T00:00:00Z",
    )
    assert result.pads_created >= 0


@pytest.mark.asyncio
async def test_list_organization_pads(
    async_coderpad_client: AsyncCoderPad,
) -> None:
    """Organization pads can be listed."""
    result = await async_coderpad_client.organization.pads.list()
    assert result.total >= 0


@pytest.mark.asyncio
async def test_list_organization_pads_with_params(
    async_coderpad_client: AsyncCoderPad,
) -> None:
    """Organization pads can be listed with optional arguments."""
    result = await async_coderpad_client.organization.pads.list(
        sort=SortOrder.UPDATED_AT_ASC,
        page=1,
    )
    assert result.total >= 0


@pytest.mark.asyncio
async def test_list_organization_questions(
    async_coderpad_client: AsyncCoderPad,
) -> None:
    """Organization questions can be listed."""
    result = await async_coderpad_client.organization.questions.list()
    assert result.total >= 0
    assert result[0].ai_assist_custom_system_prompt == "Only provide hints."


@pytest.mark.asyncio
async def test_list_org_questions_with_params(
    async_coderpad_client: AsyncCoderPad,
) -> None:
    """Organization questions can be listed with optional
    arguments.
    """
    result = await async_coderpad_client.organization.questions.list(
        sort=SortOrder.CREATED_AT_DESC,
        page=1,
    )
    assert result.total >= 0


@pytest.mark.asyncio
async def test_list_organization_users(
    async_coderpad_client: AsyncCoderPad,
) -> None:
    """Organization users can be listed and decoded."""
    result = await async_coderpad_client.organization.users.list()
    assert bool(result)
    assert all(isinstance(item, OrganizationUser) for item in result)


@pytest.mark.asyncio
async def test_list_organization_users_with_email(
    async_coderpad_client: AsyncCoderPad,
    mock_coderpad_api: respx.MockRouter,
) -> None:
    """Organization users can be filtered by email."""
    email = "buddy@company.io"
    result = await async_coderpad_client.organization.users.list(
        email=email,
    )
    request = mock_coderpad_api.calls.last.request
    assert request.url.params["email"] == email
    assert all(isinstance(item, OrganizationUser) for item in result)


@pytest.mark.asyncio
async def test_list_organization_users_empty() -> None:
    """An empty organization user response decodes to an empty
    list.
    """

    async def _empty_transport(
        *,
        method: str,
        url: str,
        headers: dict[str, str],
        params: (dict[str, str | int] | None),
        data: dict[str, str] | None,
        files: (dict[str, tuple[str, bytes, str]] | None),
    ) -> TransportResponse:
        """Return an empty successful user response."""
        del method, url, headers, params, data, files
        return TransportResponse(
            status_code=HTTPStatus.OK,
            headers={},
            content=b'{"status": "OK", "users": []}',
        )

    client = AsyncCoderPad(api_key="test-key", transport=_empty_transport)
    assert await client.organization.users.list() == []


@pytest.mark.asyncio
async def test_list_organization_users_maps_http_errors() -> None:
    """Organization user HTTP failures use the client error
    hierarchy.
    """

    async def _error_transport(
        *,
        method: str,
        url: str,
        headers: dict[str, str],
        params: (dict[str, str | int] | None),
        data: dict[str, str] | None,
        files: (dict[str, tuple[str, bytes, str]] | None),
    ) -> TransportResponse:
        """Return a not-found user response."""
        del method, url, headers, params, data, files
        return TransportResponse(
            status_code=HTTPStatus.NOT_FOUND,
            headers={},
            content=b"Not Found",
        )

    client = AsyncCoderPad(api_key="test-key", transport=_error_transport)
    with pytest.raises(expected_exception=NotFoundError):
        await client.organization.users.list()
