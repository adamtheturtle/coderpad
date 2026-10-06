"""Tests for independent Interview and Screen API-key introspection."""

from http import HTTPStatus

import pytest
import respx
from httpx import Response

from coderpad import SCREEN_US_BASE_URL, AsyncCoderPad, CoderPad
from coderpad.exceptions import AuthenticationError


def _routes(router: respx.MockRouter, *, name: str | None) -> None:
    """Register independent account responses for both products."""
    _ = router.get(url="https://app.coderpad.io/api/user").mock(
        return_value=Response(
            status_code=200,
            json={
                "name": name,
                "allow_pad_creation": False,
                "analytics_id": "",
            },
        )
    )
    _ = router.get(url=SCREEN_US_BASE_URL + "/assessment/api/v1.1/me").mock(
        return_value=Response(
            status_code=200,
            json={
                "organization_id": "org",
                "recruiter_id": "recruiter",
                "teams": [{"id": "team", "name": "", "is_default": True}],
            },
        )
    )


def _assert_headers(router: respx.MockRouter) -> None:
    """Each request uses its own API key and endpoint."""
    interview = router.routes[0].calls.last.request
    screen = router.routes[1].calls.last.request
    assert str(object=interview.url) == "https://app.coderpad.io/api/user"
    assert interview.headers["Authorization"] == 'Token token="interview-key"'
    assert interview.headers.get(key="API-Key") is None
    assert (
        str(object=screen.url)
        == SCREEN_US_BASE_URL + "/assessment/api/v1.1/me"
    )
    assert screen.headers["API-Key"] == "screen-key"
    assert screen.headers.get(key="Authorization") is None


@pytest.mark.parametrize(argnames="name", argvalues=[None, "", "Ada"])
def test_account_introspection(name: str | None) -> None:
    """Optional names and empty metadata survive synchronous decoding."""
    with respx.mock() as router:
        _routes(router=router, name=name)
        with CoderPad(
            api_key="interview-key", screen_api_key="screen-key"
        ) as client:
            user = client.user.get()
            account = client.screen.me()
        assert user.name == name
        assert user.allow_pad_creation is False
        assert user.analytics_id == ""
        assert account.organization_id == "org"
        assert account.recruiter_id == "recruiter"
        assert [team.model_dump() for team in account.teams] == [
            {"id": "team", "name": "", "is_default": True}
        ]
        _assert_headers(router=router)


@pytest.mark.asyncio
async def test_async_account_introspection() -> None:
    """Async calls use the same independent contracts."""
    with respx.mock() as router:
        _routes(router=router, name=None)
        async with AsyncCoderPad(
            api_key="interview-key", screen_api_key="screen-key"
        ) as client:
            user = await client.user.get()
            account = await client.screen.me()
        assert user.name is None
        assert user.allow_pad_creation is False
        assert account.teams[0].is_default is True
        _assert_headers(router=router)


@pytest.mark.parametrize(
    argnames="path",
    argvalues=[
        "https://app.coderpad.io/api/user",
        SCREEN_US_BASE_URL + "/assessment/api/v1.1/me",
    ],
)
def test_account_authentication_errors(path: str) -> None:
    """Invalid keys retain the existing authentication error hierarchy."""
    with respx.mock() as router:
        _ = router.get(url=path).mock(
            return_value=Response(
                status_code=401, json={"code": "unauthorized"}
            )
        )
        with CoderPad(api_key="bad", screen_api_key="bad") as client:
            operation = (
                client.user.get if path.endswith("/user") else client.screen.me
            )
            with pytest.raises(
                expected_exception=AuthenticationError
            ) as error:
                _ = operation()
            assert error.value.status_code == HTTPStatus.UNAUTHORIZED


@pytest.mark.asyncio
@pytest.mark.parametrize(
    argnames="path",
    argvalues=[
        "https://app.coderpad.io/api/user",
        SCREEN_US_BASE_URL + "/assessment/api/v1.1/me",
    ],
)
async def test_async_account_authentication_errors(path: str) -> None:
    """Async invalid keys retain the same authentication errors."""
    with respx.mock() as router:
        _ = router.get(url=path).mock(
            return_value=Response(
                status_code=401, json={"code": "unauthorized"}
            )
        )
        async with AsyncCoderPad(
            api_key="bad", screen_api_key="bad"
        ) as client:
            operation = (
                client.user.get if path.endswith("/user") else client.screen.me
            )
            with pytest.raises(
                expected_exception=AuthenticationError
            ) as error:
                _ = await operation()
            assert error.value.status_code == HTTPStatus.UNAUTHORIZED
