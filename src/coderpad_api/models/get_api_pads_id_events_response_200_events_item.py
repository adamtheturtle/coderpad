from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetApiPadsIdEventsResponse200EventsItem")


@_attrs_define
class GetApiPadsIdEventsResponse200EventsItem:
    """
    Attributes:
        message (str | Unset):
        kind (str | Unset):
        metadata (None | Unset):
        user_name (None | Unset):
        user_email (None | Unset):
        created_at (datetime.datetime | Unset):
    """

    message: str | Unset = UNSET
    kind: str | Unset = UNSET
    metadata: None | Unset = UNSET
    user_name: None | Unset = UNSET
    user_email: None | Unset = UNSET
    created_at: datetime.datetime | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=dict
    )

    def to_dict(self) -> dict[str, Any]:
        message = self.message

        kind = self.kind

        metadata = self.metadata

        user_name = self.user_name

        user_email = self.user_email

        created_at: str | Unset = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if message is not UNSET:
            field_dict["message"] = message
        if kind is not UNSET:
            field_dict["kind"] = kind
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if user_name is not UNSET:
            field_dict["user_name"] = user_name
        if user_email is not UNSET:
            field_dict["user_email"] = user_email
        if created_at is not UNSET:
            field_dict["created_at"] = created_at

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        message = d.pop("message", UNSET)

        kind = d.pop("kind", UNSET)

        metadata = d.pop("metadata", UNSET)

        user_name = d.pop("user_name", UNSET)

        user_email = d.pop("user_email", UNSET)

        _created_at = d.pop("created_at", UNSET)
        created_at: datetime.datetime | Unset
        if isinstance(_created_at, Unset):
            created_at = UNSET
        else:
            created_at = isoparse(_created_at)

        get_api_pads_id_events_response_200_events_item = cls(
            message=message,
            kind=kind,
            metadata=metadata,
            user_name=user_name,
            user_email=user_email,
            created_at=created_at,
        )

        get_api_pads_id_events_response_200_events_item.additional_properties = d
        return get_api_pads_id_events_response_200_events_item

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
