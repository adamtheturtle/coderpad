"""Opaque cursor pagination through both Interview transports."""

from urllib.parse import parse_qs

import pytest
import respx
from httpx import Request, Response

from coderpad import AsyncCoderPad, CoderPad, SortOrder
from coderpad._pagination import next_page_position

_ORIGIN = "https://interview.example.com"
_CURSOR = "opaque+/=token"


def _pages(*, router: respx.MockRouter) -> list[Request]:
    """A cursor followed by a nonconsecutive legacy page."""
    requests: list[Request] = []
    responses = iter(
        [
            Response(
                status_code=200,
                json={
                    "pads": [],
                    "total": 0,
                    "next_page": _ORIGIN
                    + "/api/pads/?cursor=opaque%2B%2F%3Dtoken&page=99",
                },
            ),
            Response(
                status_code=200,
                json={
                    "pads": [],
                    "total": 0,
                    "next_page": "/api/pads/?page=7",
                },
            ),
            Response(
                status_code=200,
                json={"pads": [], "total": 0, "next_page": None},
            ),
        ]
    )

    def respond(request: Request) -> Response:
        """Record the typed request and return the next page."""
        requests.append(request)
        return next(responses)

    _ = router.get(url=_ORIGIN + "/api/pads/").mock(side_effect=respond)
    return requests


def _assert_requests(*, requests: list[Request]) -> None:
    """Check exact cursor decoding and authorization origin."""
    assert [
        parse_qs(qs=request.url.query.decode()) for request in requests
    ] == [
        {"sort": ["created_at,desc"], "page": ["1"]},
        {"cursor": [_CURSOR]},
        {"sort": ["created_at,desc"], "page": ["7"]},
    ]
    assert requests[-1].headers["Authorization"] == 'Token token="key"'


def test_cursor_enumeration() -> None:
    """Enumeration follows cursor and numeric links instead of
    incrementing.
    """
    with respx.mock() as router:
        requests = _pages(router=router)
        with CoderPad(api_key="key", base_url=_ORIGIN) as client:
            # pylint: disable-next=use-implicit-booleaness-not-comparison
            assert list(client.pads.all(sort=SortOrder.CREATED_AT_DESC)) == []
        _assert_requests(requests=requests)


@pytest.mark.asyncio
async def test_async_cursor_enumeration() -> None:
    """Async enumeration follows identical links and query parameters."""
    with respx.mock() as router:
        requests = _pages(router=router)
        async with AsyncCoderPad(api_key="key", base_url=_ORIGIN) as client:
            assert [
                pad
                async for pad in client.pads.all(
                    sort=SortOrder.CREATED_AT_DESC
                )
            ] == []
        _assert_requests(requests=requests)


@pytest.mark.parametrize(
    argnames="url",
    argvalues=[
        "https://evil.example.com/api/pads/?cursor=secret",
        "http://interview.example.com/api/pads/?cursor=secret",
        "https://key@interview.example.com/api/pads/?cursor=secret",
        "/api/questions/?cursor=secret",
        "/api/pads/?cursor=secret#fragment",
        "/api/pads/?cursor=first&cursor=second",
        "/api/pads/?page=0",
        "/api/pads/?page=-1",
        "/api/pads/?page=word",
        "/api/pads/?page=1&page=2",
        "/api/pads/",
    ],
)
def test_invalid_pagination_link(url: str) -> None:
    """Other origins and malformed positions fail before any
    request.
    """
    with pytest.raises(
        expected_exception=ValueError, match="Pagination link"
    ) as error:
        _ = next_page_position(
            next_page=url, base_url=_ORIGIN, path="/api/pads/"
        )
    assert str(object=error.value).startswith("Pagination link")


def test_blank_cursor_is_opaque() -> None:
    """A supplied empty cursor is preserved rather than interpreted."""
    assert next_page_position(
        next_page="?cursor=", base_url=_ORIGIN, path="/api/pads/"
    ) == ("", None)


@pytest.mark.asyncio
async def test_explicit_cursor_overrides_page_and_sort() -> None:
    """Both list methods send only the caller's opaque cursor."""
    expected_call_count = 2
    with respx.mock() as router:
        route = router.get(url=_ORIGIN + "/api/pads/").mock(
            return_value=Response(
                status_code=200,
                json={"pads": [], "total": 0, "next_page": None},
            )
        )
        with CoderPad(api_key="key", base_url=_ORIGIN) as client:
            _ = client.pads.list(
                sort=SortOrder.UPDATED_AT_ASC, page=99, cursor=_CURSOR
            )
        assert parse_qs(qs=route.calls.last.request.url.query.decode()) == {
            "cursor": [_CURSOR]
        }
        async with AsyncCoderPad(api_key="key", base_url=_ORIGIN) as client:
            _ = await client.pads.list(
                sort=SortOrder.UPDATED_AT_ASC, page=99, cursor=_CURSOR
            )
        assert parse_qs(qs=route.calls.last.request.url.query.decode()) == {
            "cursor": [_CURSOR]
        }
        assert route.call_count == expected_call_count
