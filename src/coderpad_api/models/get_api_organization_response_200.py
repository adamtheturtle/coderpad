from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_api_organization_response_200_teams_item import (
        GetApiOrganizationResponse200TeamsItem,
    )
    from ..models.get_api_organization_response_200_users_item import (
        GetApiOrganizationResponse200UsersItem,
    )


T = TypeVar("T", bound="GetApiOrganizationResponse200")


@_attrs_define
class GetApiOrganizationResponse200:
    """
    Attributes:
        status (str | Unset):
        organization_name (str | Unset):
        user_count (int | Unset):
        users (list[GetApiOrganizationResponse200UsersItem] | Unset):
        organization_default_language (str | Unset):
        single_sign_on_supported (bool | Unset):
        single_sign_in_url (str | Unset):
        teams (list[GetApiOrganizationResponse200TeamsItem] | Unset):
    """

    status: str | Unset = UNSET
    organization_name: str | Unset = UNSET
    user_count: int | Unset = UNSET
    users: list[GetApiOrganizationResponse200UsersItem] | Unset = UNSET
    organization_default_language: str | Unset = UNSET
    single_sign_on_supported: bool | Unset = UNSET
    single_sign_in_url: str | Unset = UNSET
    teams: list[GetApiOrganizationResponse200TeamsItem] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=dict
    )

    def to_dict(self) -> dict[str, Any]:
        status = self.status

        organization_name = self.organization_name

        user_count = self.user_count

        users: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.users, Unset):
            users = []
            for users_item_data in self.users:
                users_item = users_item_data.to_dict()
                users.append(users_item)

        organization_default_language = self.organization_default_language

        single_sign_on_supported = self.single_sign_on_supported

        single_sign_in_url = self.single_sign_in_url

        teams: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.teams, Unset):
            teams = []
            for teams_item_data in self.teams:
                teams_item = teams_item_data.to_dict()
                teams.append(teams_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if status is not UNSET:
            field_dict["status"] = status
        if organization_name is not UNSET:
            field_dict["organization_name"] = organization_name
        if user_count is not UNSET:
            field_dict["user_count"] = user_count
        if users is not UNSET:
            field_dict["users"] = users
        if organization_default_language is not UNSET:
            field_dict["organization_default_language"] = (
                organization_default_language
            )
        if single_sign_on_supported is not UNSET:
            field_dict["single_sign_on_supported"] = single_sign_on_supported
        if single_sign_in_url is not UNSET:
            field_dict["single_sign_in_url"] = single_sign_in_url
        if teams is not UNSET:
            field_dict["teams"] = teams

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.get_api_organization_response_200_teams_item import (
            GetApiOrganizationResponse200TeamsItem,
        )
        from ..models.get_api_organization_response_200_users_item import (
            GetApiOrganizationResponse200UsersItem,
        )

        d = dict(src_dict)
        status = d.pop("status", UNSET)

        organization_name = d.pop("organization_name", UNSET)

        user_count = d.pop("user_count", UNSET)

        _users = d.pop("users", UNSET)
        users: list[GetApiOrganizationResponse200UsersItem] | Unset = UNSET
        if _users is not UNSET:
            users = []
            for users_item_data in _users:
                users_item = GetApiOrganizationResponse200UsersItem.from_dict(
                    users_item_data
                )

                users.append(users_item)

        organization_default_language = d.pop(
            "organization_default_language", UNSET
        )

        single_sign_on_supported = d.pop("single_sign_on_supported", UNSET)

        single_sign_in_url = d.pop("single_sign_in_url", UNSET)

        _teams = d.pop("teams", UNSET)
        teams: list[GetApiOrganizationResponse200TeamsItem] | Unset = UNSET
        if _teams is not UNSET:
            teams = []
            for teams_item_data in _teams:
                teams_item = GetApiOrganizationResponse200TeamsItem.from_dict(
                    teams_item_data
                )

                teams.append(teams_item)

        get_api_organization_response_200 = cls(
            status=status,
            organization_name=organization_name,
            user_count=user_count,
            users=users,
            organization_default_language=organization_default_language,
            single_sign_on_supported=single_sign_on_supported,
            single_sign_in_url=single_sign_in_url,
            teams=teams,
        )

        get_api_organization_response_200.additional_properties = d
        return get_api_organization_response_200

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
