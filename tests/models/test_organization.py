"""Tests for `coderpad` organization models."""

from typing import TYPE_CHECKING

import pytest
from pydantic import ValidationError

from coderpad.types import (
    Organization,
    OrganizationStats,
    OrganizationStatsUser,
    OrganizationUser,
    Quota,
    Team,
)
from tests.models.helpers import team_dict

if TYPE_CHECKING:
    from coderpad._dict_types import (
        OrganizationDict,
        OrganizationStatsDict,
        OrganizationStatsUserDict,
        OrganizationUserDict,
        QuotaDict,
    )


def test_team_from_dict() -> None:
    """A Team can be created from a dictionary."""
    data = team_dict()
    result = Team.from_dict(data=data)
    assert result.id == data["id"]
    assert result.name == data["name"]


def test_pydantic_validation_and_serialization() -> None:
    """Models validate strictly, ignore new API fields, and
    serialize.
    """
    team = Team.model_validate(
        obj={"id": "team-1", "name": "Backend", "future_field": True},
    )
    assert team.model_dump() == {"id": "team-1", "name": "Backend"}
    with pytest.raises(expected_exception=ValidationError):
        _ = Team.model_validate(obj={"id": 1, "name": "Backend"})
    with (
        pytest.MonkeyPatch.context() as monkeypatch,
        pytest.raises(expected_exception=ValidationError),
    ):
        monkeypatch.setattr(
            target=team,
            name="name",
            value="Frontend",
        )


def test_organization_user_from_dict() -> None:
    """An OrganizationUser can be created from a dictionary."""
    data: OrganizationUserDict = {
        "email": "u@example.com",
        "name": "User",
        "teams": ["Backend"],
    }
    result = OrganizationUser.from_dict(data=data)
    assert result.email == data["email"]
    assert result.name == data["name"]
    assert result.teams == data["teams"]


def test_organization_stats_user_from_dict() -> None:
    """An OrganizationStatsUser can be created from a dictionary."""
    data: OrganizationStatsUserDict = {
        "email": "u@example.com",
        "name": "User",
        "pads_created": 5,
    }
    result = OrganizationStatsUser.from_dict(data=data)
    assert result.email == data["email"]
    assert result.name == data["name"]
    assert result.pads_created == data["pads_created"]


def test_quota_from_dict() -> None:
    """A Quota can be created from a dictionary."""
    data: QuotaDict = {
        "trial_expires_at": "2024-01-01T00:00:00Z",
        "pads_used": 10,
        "quota_reset_at": "2024-02-01T00:00:00Z",
        "unlimited": False,
        "overages_enabled": True,
    }
    result = Quota.from_dict(data=data)
    assert result.trial_expires_at == data["trial_expires_at"]
    assert result.pads_used == data["pads_used"]
    assert result.quota_reset_at == data["quota_reset_at"]
    assert result.unlimited == data["unlimited"]
    assert result.overages_enabled == data["overages_enabled"]


def test_organization_from_dict() -> None:
    """An Organization can be created from a dictionary."""
    data: OrganizationDict = {
        "id": 123,
        "organization_name": "Acme",
        "user_count": 5,
        "users": [
            {"email": "u@example.com", "name": "User", "teams": ["BE"]},
        ],
        "organization_default_language": "python",
        "single_sign_on_supported": True,
        "single_sign_in_url": "https://sso.example.com",
        "teams": [team_dict()],
        "child_organizations": [{"id": 456, "name": "Subsidiary"}],
    }
    result = Organization.from_dict(data=data)
    assert result.organization_name == data["organization_name"]
    assert result.user_count == data["user_count"]
    assert len(result.users) == len(data["users"])
    assert (
        result.organization_default_language
        == data["organization_default_language"]
    )
    assert result.single_sign_on_supported == data["single_sign_on_supported"]
    assert "single_sign_in_url" in data
    assert result.single_sign_in_url == data["single_sign_in_url"]
    assert len(result.teams) == len(data["teams"])
    assert "id" in data
    assert result.id == data["id"]
    assert "child_organizations" in data
    assert result.child_organizations == data["child_organizations"]


def test_from_dict_without_sso_url_or_observed_fields() -> None:
    """An Organization can omit conditional and observed fields."""
    data: OrganizationDict = {
        "organization_name": "Acme",
        "user_count": 0,
        "users": [],
        "organization_default_language": "python",
        "single_sign_on_supported": False,
        "teams": [],
    }
    result = Organization.from_dict(data=data)
    assert result.single_sign_in_url is None
    assert result.id is None
    assert not bool(result.child_organizations)


def test_organization_stats_from_dict() -> None:
    """An OrganizationStats can be created from a
    dictionary.
    """
    data: OrganizationStatsDict = {
        "start_time": "2023-01-01T00:00:00Z",
        "end_time": "2023-02-01T00:00:00Z",
        "pads_created": 42,
        "users": [
            {
                "email": "u@example.com",
                "name": "User",
                "pads_created": 10,
            },
        ],
    }
    result = OrganizationStats.from_dict(data=data)
    assert result.start_time == data["start_time"]
    assert result.end_time == data["end_time"]
    assert result.pads_created == data["pads_created"]
    assert len(result.users) == len(data["users"])
