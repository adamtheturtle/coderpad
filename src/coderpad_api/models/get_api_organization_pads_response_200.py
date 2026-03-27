from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_api_organization_pads_response_200_pads_item import (
        GetApiOrganizationPadsResponse200PadsItem,
    )


T = TypeVar("T", bound="GetApiOrganizationPadsResponse200")


@_attrs_define
class GetApiOrganizationPadsResponse200:
    """
    Attributes:
        status (str | Unset):
        pads (list[GetApiOrganizationPadsResponse200PadsItem] | Unset):
        next_page (str | Unset):
        total (int | Unset):
    """

    status: str | Unset = UNSET
    pads: list[GetApiOrganizationPadsResponse200PadsItem] | Unset = UNSET
    next_page: str | Unset = UNSET
    total: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=dict
    )

    def to_dict(self) -> dict[str, Any]:
        status = self.status

        pads: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.pads, Unset):
            pads = []
            for pads_item_data in self.pads:
                pads_item = pads_item_data.to_dict()
                pads.append(pads_item)

        next_page = self.next_page

        total = self.total

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if status is not UNSET:
            field_dict["status"] = status
        if pads is not UNSET:
            field_dict["pads"] = pads
        if next_page is not UNSET:
            field_dict["next_page"] = next_page
        if total is not UNSET:
            field_dict["total"] = total

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.get_api_organization_pads_response_200_pads_item import (
            GetApiOrganizationPadsResponse200PadsItem,
        )

        d = dict(src_dict)
        status = d.pop("status", UNSET)

        _pads = d.pop("pads", UNSET)
        pads: list[GetApiOrganizationPadsResponse200PadsItem] | Unset = UNSET
        if _pads is not UNSET:
            pads = []
            for pads_item_data in _pads:
                pads_item = (
                    GetApiOrganizationPadsResponse200PadsItem.from_dict(
                        pads_item_data
                    )
                )

                pads.append(pads_item)

        next_page = d.pop("next_page", UNSET)

        total = d.pop("total", UNSET)

        get_api_organization_pads_response_200 = cls(
            status=status,
            pads=pads,
            next_page=next_page,
            total=total,
        )

        get_api_organization_pads_response_200.additional_properties = d
        return get_api_organization_pads_response_200

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
