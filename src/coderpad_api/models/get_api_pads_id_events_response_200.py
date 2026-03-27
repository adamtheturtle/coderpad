from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_api_pads_id_events_response_200_events_item import (
        GetApiPadsIdEventsResponse200EventsItem,
    )


T = TypeVar("T", bound="GetApiPadsIdEventsResponse200")


@_attrs_define
class GetApiPadsIdEventsResponse200:
    """
    Attributes:
        status (str | Unset):
        events (list[GetApiPadsIdEventsResponse200EventsItem] | Unset):
        total (int | Unset):
    """

    status: str | Unset = UNSET
    events: list[GetApiPadsIdEventsResponse200EventsItem] | Unset = UNSET
    total: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=dict
    )

    def to_dict(self) -> dict[str, Any]:
        status = self.status

        events: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.events, Unset):
            events = []
            for events_item_data in self.events:
                events_item = events_item_data.to_dict()
                events.append(events_item)

        total = self.total

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if status is not UNSET:
            field_dict["status"] = status
        if events is not UNSET:
            field_dict["events"] = events
        if total is not UNSET:
            field_dict["total"] = total

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.get_api_pads_id_events_response_200_events_item import (
            GetApiPadsIdEventsResponse200EventsItem,
        )

        d = dict(src_dict)
        status = d.pop("status", UNSET)

        _events = d.pop("events", UNSET)
        events: list[GetApiPadsIdEventsResponse200EventsItem] | Unset = UNSET
        if _events is not UNSET:
            events = []
            for events_item_data in _events:
                events_item = (
                    GetApiPadsIdEventsResponse200EventsItem.from_dict(
                        events_item_data
                    )
                )

                events.append(events_item)

        total = d.pop("total", UNSET)

        get_api_pads_id_events_response_200 = cls(
            status=status,
            events=events,
            total=total,
        )

        get_api_pads_id_events_response_200.additional_properties = d
        return get_api_pads_id_events_response_200

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
