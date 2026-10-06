"""Fixtures for CoderPad model tests."""

import pytest

from coderpad._dict_types import TeamDict


@pytest.fixture(name="team_dict")
def fixture_team_dict() -> TeamDict:
    """Return fresh sample team data."""
    return {"id": "team-1", "name": "Backend"}
