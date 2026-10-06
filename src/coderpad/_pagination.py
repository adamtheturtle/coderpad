"""Validate API pagination links without forwarding credentials."""

from urllib.parse import parse_qs, urljoin, urlsplit

from beartype import beartype


@beartype
def next_page_position(
    *,
    next_page: str,
    base_url: str,
    path: str,
) -> tuple[str | None, int | None]:
    """Extract an opaque cursor or legacy page from the same API
    endpoint.
    """
    expected = urlsplit(url=base_url + path)
    target = urlsplit(url=urljoin(base=base_url + path, url=next_page))
    if (target.scheme, target.netloc, target.path.rstrip("/")) != (
        expected.scheme,
        expected.netloc,
        expected.path.rstrip("/"),
    ) or bool(target.fragment):
        message = "Pagination link must refer to the configured API endpoint."
        raise ValueError(message)
    query = parse_qs(qs=target.query, keep_blank_values=True)
    cursor = query.get("cursor")
    if cursor is not None and len(cursor) == 1:
        return cursor[0], None
    page = query.get("page")
    if (
        cursor is None
        and page is not None
        and len(page) == 1
        and page[0].isdecimal()
        and int(page[0]) > 0
    ):
        return None, int(page[0])
    message = "Pagination link must contain one cursor or positive page."
    raise ValueError(message)


@beartype
def next_page_number(
    *,
    next_page: str,
    base_url: str,
    path: str,
    after_page: int,
) -> int:
    """Follow a numeric link on endpoints without cursor pagination."""
    _, page = next_page_position(
        next_page=next_page, base_url=base_url, path=path
    )
    if page is None or page <= after_page:
        message = (
            "This endpoint requires an advancing numeric pagination link."
        )
        raise ValueError(message)
    return page
