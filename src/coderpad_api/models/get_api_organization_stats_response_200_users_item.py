from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetApiOrganizationStatsResponse200UsersItem")


@_attrs_define
class GetApiOrganizationStatsResponse200UsersItem:
    """
    Attributes:
        email (str | Unset):
        name (str | Unset):
        pads_created (int | Unset):
    """

    email: str | Unset = UNSET
    name: str | Unset = UNSET
    pads_created: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=dict
    )

    def to_dict(self) -> dict[str, Any]:
        email = self.email

        name = self.name

        pads_created = self.pads_created

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if email is not UNSET:
            field_dict["email"] = email
        if name is not UNSET:
            field_dict["name"] = name
        if pads_created is not UNSET:
            field_dict["pads_created"] = pads_created

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        email = d.pop("email", UNSET)

        name = d.pop("name", UNSET)

        pads_created = d.pop("pads_created", UNSET)

        get_api_organization_stats_response_200_users_item = cls(
            email=email,
            name=name,
            pads_created=pads_created,
        )

        get_api_organization_stats_response_200_users_item.additional_properties = d
        return get_api_organization_stats_response_200_users_item

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
