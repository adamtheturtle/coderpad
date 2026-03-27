from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_api_organization_stats_response_200_users_item import (
        GetApiOrganizationStatsResponse200UsersItem,
    )


T = TypeVar("T", bound="GetApiOrganizationStatsResponse200")


@_attrs_define
class GetApiOrganizationStatsResponse200:
    """
    Attributes:
        status (str | Unset):
        start_time (datetime.datetime | Unset):
        end_time (datetime.datetime | Unset):
        pads_created (int | Unset):
        users (list[GetApiOrganizationStatsResponse200UsersItem] | Unset):
    """

    status: str | Unset = UNSET
    start_time: datetime.datetime | Unset = UNSET
    end_time: datetime.datetime | Unset = UNSET
    pads_created: int | Unset = UNSET
    users: list[GetApiOrganizationStatsResponse200UsersItem] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=dict
    )

    def to_dict(self) -> dict[str, Any]:
        status = self.status

        start_time: str | Unset = UNSET
        if not isinstance(self.start_time, Unset):
            start_time = self.start_time.isoformat()

        end_time: str | Unset = UNSET
        if not isinstance(self.end_time, Unset):
            end_time = self.end_time.isoformat()

        pads_created = self.pads_created

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
        if start_time is not UNSET:
            field_dict["start_time"] = start_time
        if end_time is not UNSET:
            field_dict["end_time"] = end_time
        if pads_created is not UNSET:
            field_dict["pads_created"] = pads_created
        if users is not UNSET:
            field_dict["users"] = users

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.get_api_organization_stats_response_200_users_item import (
            GetApiOrganizationStatsResponse200UsersItem,
        )

        d = dict(src_dict)
        status = d.pop("status", UNSET)

        _start_time = d.pop("start_time", UNSET)
        start_time: datetime.datetime | Unset
        if isinstance(_start_time, Unset):
            start_time = UNSET
        else:
            start_time = isoparse(_start_time)

        _end_time = d.pop("end_time", UNSET)
        end_time: datetime.datetime | Unset
        if isinstance(_end_time, Unset):
            end_time = UNSET
        else:
            end_time = isoparse(_end_time)

        pads_created = d.pop("pads_created", UNSET)

        _users = d.pop("users", UNSET)
        users: list[GetApiOrganizationStatsResponse200UsersItem] | Unset = (
            UNSET
        )
        if _users is not UNSET:
            users = []
            for users_item_data in _users:
                users_item = (
                    GetApiOrganizationStatsResponse200UsersItem.from_dict(
                        users_item_data
                    )
                )

                users.append(users_item)

        get_api_organization_stats_response_200 = cls(
            status=status,
            start_time=start_time,
            end_time=end_time,
            pads_created=pads_created,
            users=users,
        )

        get_api_organization_stats_response_200.additional_properties = d
        return get_api_organization_stats_response_200

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
