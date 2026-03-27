from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_api_organization_users_response_200_users_item import (
        GetApiOrganizationUsersResponse200UsersItem,
    )


T = TypeVar("T", bound="GetApiOrganizationUsersResponse200")


@_attrs_define
class GetApiOrganizationUsersResponse200:
    """
    Attributes:
        status (str | Unset):
        users (list[GetApiOrganizationUsersResponse200UsersItem] | Unset):
    """

    status: str | Unset = UNSET
    users: list[GetApiOrganizationUsersResponse200UsersItem] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=dict
    )

    def to_dict(self) -> dict[str, Any]:
        status = self.status

        users: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.users, Unset):
            users = []
            for users_item_data in self.users:
                users_item = users_item_data.to_dict()
                users.append(users_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if status is not UNSET:
            field_dict["status"] = status
        if users is not UNSET:
            field_dict["users"] = users

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.get_api_organization_users_response_200_users_item import (
            GetApiOrganizationUsersResponse200UsersItem,
        )

        d = dict(src_dict)
        status = d.pop("status", UNSET)

        _users = d.pop("users", UNSET)
        users: list[GetApiOrganizationUsersResponse200UsersItem] | Unset = (
            UNSET
        )
        if _users is not UNSET:
            users = []
            for users_item_data in _users:
                users_item = (
                    GetApiOrganizationUsersResponse200UsersItem.from_dict(
                        users_item_data
                    )
                )

                users.append(users_item)

        get_api_organization_users_response_200 = cls(
            status=status,
            users=users,
        )

        get_api_organization_users_response_200.additional_properties = d
        return get_api_organization_users_response_200

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
