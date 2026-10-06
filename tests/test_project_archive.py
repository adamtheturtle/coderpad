"""Screen project archives preserve bytes, credentials, and errors."""

import asyncio
from typing import NoReturn
from uuid import UUID

import httpx
import pytest
import respx

from coderpad import SCREEN_EU_BASE_URL, AsyncCoderPad, CoderPad
from coderpad.exceptions import CoderPadError

_QUESTION_ID = "12345678-1234-1234-1234-123456789012"
_URL = (
    f"{SCREEN_EU_BASE_URL}/assessment/api/v1.1/tests/11/"
    f"questions/{_QUESTION_ID}/project"
)
_ARCHIVE = b"\x1f\x8b\x00\xff\x80candidate archive\x00"
_QUESTION_IDS: list[str | UUID] = [_QUESTION_ID, UUID(hex=_QUESTION_ID)]


def _assert_request(*, request: httpx.Request) -> None:
    """Assert the dedicated binary endpoint and independent
    credentials.
    """
    assert request.method == "GET"
    assert str(object=request.url) == _URL
    assert request.content == b""
    assert request.headers.get(key="Authorization") is None
    assert request.headers["API-Key"] == "screen-key"
    assert request.extensions["timeout"] == {
        "connect": 0.125,
        "read": 0.125,
        "write": 0.125,
        "pool": 0.125,
    }


@pytest.mark.parametrize(argnames="question_id", argvalues=_QUESTION_IDS)
def test_archive(question_id: str | UUID) -> None:
    """Return unchanged bytes through the configured timeout."""
    with respx.mock() as router:
        route = router.get(url=_URL).respond(
            status_code=200, content=_ARCHIVE, content_type="application/gzip"
        )
        with CoderPad(
            api_key="interview-key",
            screen_api_key="screen-key",
            screen_base_url=SCREEN_EU_BASE_URL,
            timeout=0.125,
        ) as client:
            result = client.screen.tests.project_archive(
                test_id=11, question_id=question_id
            )
        assert result == _ARCHIVE
        assert route.call_count == 1
        _assert_request(request=route.calls.last.request)


@pytest.mark.asyncio
@pytest.mark.parametrize(argnames="question_id", argvalues=_QUESTION_IDS)
async def test_async_archive(question_id: str | UUID) -> None:
    """Asynchronous downloads have identical bytes, paths, and
    timeouts.
    """
    with respx.mock() as router:
        route = router.get(url=_URL).respond(
            status_code=200, content=_ARCHIVE, content_type="application/gzip"
        )
        async with AsyncCoderPad(
            api_key="interview-key",
            screen_api_key="screen-key",
            screen_base_url=SCREEN_EU_BASE_URL,
            timeout=0.125,
        ) as client:
            result = await client.screen.tests.project_archive(
                test_id=11, question_id=question_id
            )
        assert result == _ARCHIVE
        assert route.call_count == 1
        _assert_request(request=route.calls.last.request)


@pytest.mark.parametrize(argnames="status", argvalues=[400, 404])
def test_archive_api_errors(status: int) -> None:
    """JSON errors retain the public exception contract rather than
    bytes.
    """
    with respx.mock() as router:
        route = router.get(url=_URL).respond(
            status_code=status, json={"message": "Unavailable"}
        )
        with (
            CoderPad(
                api_key="interview-key",
                screen_api_key="screen-key",
                screen_base_url=SCREEN_EU_BASE_URL,
            ) as client,
            pytest.raises(expected_exception=CoderPadError) as error,
        ):
            _ = client.screen.tests.project_archive(
                test_id=11, question_id=_QUESTION_ID
            )
        assert error.value.status_code == status
        assert route.call_count == 1


@pytest.mark.asyncio
@pytest.mark.parametrize(argnames="status", argvalues=[400, 404])
async def test_async_archive_api_errors(status: int) -> None:
    """Asynchronous HTTP errors use the same public exception contract."""
    with respx.mock() as router:
        route = router.get(url=_URL).respond(
            status_code=status, json={"message": "Unavailable"}
        )
        async with AsyncCoderPad(
            api_key="interview-key",
            screen_api_key="screen-key",
            screen_base_url=SCREEN_EU_BASE_URL,
        ) as client:
            with pytest.raises(expected_exception=CoderPadError) as error:
                _ = await client.screen.tests.project_archive(
                    test_id=11, question_id=_QUESTION_ID
                )
        assert error.value.status_code == status
        assert route.call_count == 1


@pytest.mark.parametrize(
    argnames=("test_id", "question_id"),
    argvalues=[(0, _QUESTION_ID), (11, "invalid/path")],
)
def test_archive_invalid_identity(test_id: int, question_id: str) -> None:
    """Malformed identities fail before any network request."""
    with (
        respx.mock() as router,
        CoderPad(
            api_key="interview-key", screen_api_key="screen-key"
        ) as client,
    ):
        with pytest.raises(
            expected_exception=ValueError, match=r"positive integer|UUID"
        ):
            _ = client.screen.tests.project_archive(
                test_id=test_id, question_id=question_id
            )
        assert router.calls.call_count == 0


@pytest.mark.asyncio
@pytest.mark.parametrize(
    argnames=("test_id", "question_id"),
    argvalues=[(0, _QUESTION_ID), (11, "invalid/path")],
)
async def test_async_archive_invalid_identity(
    test_id: int, question_id: str
) -> None:
    """Asynchronous invalid identities also fail before networking."""
    with respx.mock() as router:
        async with AsyncCoderPad(
            api_key="interview-key", screen_api_key="screen-key"
        ) as client:
            with pytest.raises(
                expected_exception=ValueError, match=r"positive integer|UUID"
            ):
                _ = await client.screen.tests.project_archive(
                    test_id=test_id, question_id=question_id
                )
        assert router.calls.call_count == 0


def test_archive_timeout() -> None:
    """Timeouts propagate without retrying archive generation."""
    with respx.mock() as router:
        route = router.get(url=_URL).mock(
            side_effect=httpx.ReadTimeout(message="Slow generation")
        )
        with (
            CoderPad(
                api_key="interview-key",
                screen_api_key="screen-key",
                screen_base_url=SCREEN_EU_BASE_URL,
            ) as client,
            pytest.raises(expected_exception=httpx.ReadTimeout),
        ):
            _ = client.screen.tests.project_archive(
                test_id=11, question_id=_QUESTION_ID
            )
        assert route.call_count == 1


@pytest.mark.asyncio
@pytest.mark.parametrize(
    argnames="failure", argvalues=["timeout", "cancellation"]
)
async def test_async_archive_transport_errors(failure: str) -> None:
    """Timeouts and task cancellation propagate without retries."""
    attempts: list[str] = []

    async def interrupt(request: httpx.Request) -> NoReturn:
        """Interrupt the real HTTP transport during archive generation."""
        attempts.append(str(object=request.url))
        if failure == "timeout":
            raise httpx.ReadTimeout(message="Slow generation")
        raise asyncio.CancelledError

    exception = (
        httpx.ReadTimeout if failure == "timeout" else asyncio.CancelledError
    )
    with respx.mock(assert_all_called=False) as router:
        _ = router.get(url=_URL).mock(side_effect=interrupt)
        async with AsyncCoderPad(
            api_key="interview-key",
            screen_api_key="screen-key",
            screen_base_url=SCREEN_EU_BASE_URL,
        ) as client:
            with pytest.raises(expected_exception=exception):
                _ = await client.screen.tests.project_archive(
                    test_id=11, question_id=_QUESTION_ID
                )
        assert attempts == [_URL]
