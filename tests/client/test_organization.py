"""Tests for `coderpad` organization client."""

from http import HTTPStatus

import pytest
import respx

from coderpad.client import CoderPad
from coderpad.exceptions import (
    NotFoundError,
)
from coderpad.transports import (
    TransportResponse,
)
from coderpad.types import (
    OrganizationUser,
    SortOrder,
)


def test_get_quota(
    coderpad_client: CoderPad,
) -> None:
    """Quota information can be retrieved."""
    result = coderpad_client.organization.get_quota()
    assert result.pads_used >= 0


def test_get_organization(
    coderpad_client: CoderPad,
) -> None:
    """Organization information can be retrieved."""
    result = coderpad_client.organization.get()
    assert bool(result.organization_name)


def test_get_organization_stats(
    coderpad_client: CoderPad,
) -> None:
    """Organization stats can be retrieved."""
    result = coderpad_client.organization.get_stats()
    assert result.pads_created >= 0


def test_get_organization_stats_with_params(
    coderpad_client: CoderPad,
) -> None:
    """Organization stats can be filtered by time range."""
    result = coderpad_client.organization.get_stats(
        start_time="2023-07-01T00:00:00Z",
        end_time="2023-07-31T00:00:00Z",
    )
    assert result.pads_created >= 0


def test_list_organization_pads(
    coderpad_client: CoderPad,
) -> None:
    """Organization pads can be listed."""
    result = coderpad_client.organization.pads.list()
    assert result.total >= 0


def test_list_organization_pads_with_params(
    coderpad_client: CoderPad,
) -> None:
    """Organization pads can be listed with optional arguments."""
    result = coderpad_client.organization.pads.list(
        sort=SortOrder.UPDATED_AT_ASC,
        page=1,
    )
    assert result.total >= 0


def test_list_organization_questions(
    coderpad_client: CoderPad,
) -> None:
    """Organization questions can be listed."""
    result = coderpad_client.organization.questions.list()
    assert result.total >= 0
    assert result[0].ai_assist_custom_system_prompt == "Only provide hints."


def test_list_organization_questions_with_params(
    coderpad_client: CoderPad,
) -> None:
    """Organization questions can be listed with optional
    arguments.
    """
    result = coderpad_client.organization.questions.list(
        sort=SortOrder.CREATED_AT_DESC,
        page=1,
    )
    assert result.total >= 0


def test_list_organization_users(
    coderpad_client: CoderPad,
) -> None:
    """Organization users can be listed and decoded."""
    result = coderpad_client.organization.users.list()
    assert bool(result)
    assert all(isinstance(item, OrganizationUser) for item in result)


def test_list_organization_users_with_email(
    coderpad_client: CoderPad,
    mock_coderpad_api: respx.MockRouter,
) -> None:
    """Organization users can be filtered by email."""
    email = "buddy@company.io"
    result = coderpad_client.organization.users.list(email=email)
    request = mock_coderpad_api.calls.last.request
    assert request.url.params["email"] == email
    assert all(isinstance(item, OrganizationUser) for item in result)


def test_list_organization_users_empty() -> None:
    """An empty organization user response decodes to an empty
    list.
    """

    def _empty_transport(
        *,
        method: str,
        url: str,
        headers: dict[str, str],
        params: dict[str, str | int] | None,
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

    client = CoderPad(api_key="test-key", transport=_empty_transport)
    assert client.organization.users.list() == []


def test_list_organization_users_rejects_invalid_response() -> None:
    """Organization users must be returned as a list of objects."""

    def _invalid_transport(
        *,
        method: str,
        url: str,
        headers: dict[str, str],
        params: dict[str, str | int] | None,
        data: dict[str, str] | None,
        files: (dict[str, tuple[str, bytes, str]] | None),
    ) -> TransportResponse:
        """Return a malformed successful user response."""
        del method, url, headers, params, data, files
        return TransportResponse(
            status_code=HTTPStatus.OK,
            headers={},
            content=b'{"status": "OK", "users": "invalid"}',
        )

    client = CoderPad(api_key="test-key", transport=_invalid_transport)
    with pytest.raises(expected_exception=TypeError):
        _ = client.organization.users.list()
    client.close()


def test_list_organization_users_maps_http_errors() -> None:
    """Organization user HTTP failures use the client error
    hierarchy.
    """

    def _error_transport(
        *,
        method: str,
        url: str,
        headers: dict[str, str],
        params: dict[str, str | int] | None,
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

    client = CoderPad(api_key="test-key", transport=_error_transport)
    with pytest.raises(expected_exception=NotFoundError):
        _ = client.organization.users.list()
