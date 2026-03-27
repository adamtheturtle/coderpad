from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetApiPadEnvironmentsIdResponse200FileContentsItem")


@_attrs_define
class GetApiPadEnvironmentsIdResponse200FileContentsItem:
    """
    Attributes:
        path (str | Unset):
        contents (str | Unset):
        history (str | Unset):
    """

    path: str | Unset = UNSET
    contents: str | Unset = UNSET
    history: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=dict
    )

    def to_dict(self) -> dict[str, Any]:
        path = self.path

        contents = self.contents

        history = self.history

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if path is not UNSET:
            field_dict["path"] = path
        if contents is not UNSET:
            field_dict["contents"] = contents
        if history is not UNSET:
            field_dict["history"] = history

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        path = d.pop("path", UNSET)

        contents = d.pop("contents", UNSET)

        history = d.pop("history", UNSET)

        get_api_pad_environments_id_response_200_file_contents_item = cls(
            path=path,
            contents=contents,
            history=history,
        )

        get_api_pad_environments_id_response_200_file_contents_item.additional_properties = d
        return get_api_pad_environments_id_response_200_file_contents_item

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
