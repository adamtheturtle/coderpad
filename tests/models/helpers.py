"""Shared helpers for models tests."""

from coderpad._dict_types import (
    TeamDict,
)


def team_dict() -> TeamDict:
    """Sample TeamDict."""
    return {"id": "team-1", "name": "Backend"}
