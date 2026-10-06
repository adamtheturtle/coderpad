"""Tests for `coderpad` pagination models."""

from coderpad.screen_types import ScreenPagination, ScreenTestsPage
from coderpad.types import (
    PaginatedList,
)


def test_paginated_list_repr() -> None:
    """The string representation shows length, total, and next
    page.
    """
    pads: PaginatedList[str] = PaginatedList(
        ["a", "b"],
        total=10,
        next_page="https://example.com/page2",
    )
    assert (
        repr(pads) == "PaginatedList(len=2, total=10, "
        "next_page='https://example.com/page2')"
    )


def test_repr_without_next_page() -> None:
    """The string representation shows None when there is no next page."""
    pads: PaginatedList[str] = PaginatedList([], total=0, next_page=None)
    assert repr(pads) == "PaginatedList(len=0, total=0, next_page=None)"


def test_screen_tests_page_repr() -> None:
    """The string representation shows test count and pagination."""
    page = ScreenTestsPage(
        tests=[],
        pagination=ScreenPagination(
            start=0,
            limit=25,
            total=100,
            has_more_items=True,
            next_start=25,
        ),
    )
    assert repr(page) == (
        "ScreenTestsPage(tests=0, pagination=ScreenPagination("
        "start=0, limit=25, total=100, has_more_items=True, "
        "next_start=25))"
    )


def test_repr_without_pagination() -> None:
    """The string representation shows None pagination when absent."""
    page = ScreenTestsPage(tests=[], pagination=None)
    assert repr(page) == "ScreenTestsPage(tests=0, pagination=None)"
