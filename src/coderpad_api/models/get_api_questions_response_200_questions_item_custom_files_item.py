from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar(
    "T", bound="GetApiQuestionsResponse200QuestionsItemCustomFilesItem"
)


@_attrs_define
class GetApiQuestionsResponse200QuestionsItemCustomFilesItem:
    """
    Attributes:
        id (str | Unset):
        title (str | Unset):
        description (str | Unset):
        filename (str | Unset):
        filesize (str | Unset):
    """

    id: str | Unset = UNSET
    title: str | Unset = UNSET
    description: str | Unset = UNSET
    filename: str | Unset = UNSET
    filesize: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=dict
    )

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        title = self.title

        description = self.description

        filename = self.filename

        filesize = self.filesize

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if title is not UNSET:
            field_dict["title"] = title
        if description is not UNSET:
            field_dict["description"] = description
        if filename is not UNSET:
            field_dict["filename"] = filename
        if filesize is not UNSET:
            field_dict["filesize"] = filesize

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        id = d.pop("id", UNSET)

        title = d.pop("title", UNSET)

        description = d.pop("description", UNSET)

        filename = d.pop("filename", UNSET)

        filesize = d.pop("filesize", UNSET)

        get_api_questions_response_200_questions_item_custom_files_item = cls(
            id=id,
            title=title,
            description=description,
            filename=filename,
            filesize=filesize,
        )

        get_api_questions_response_200_questions_item_custom_files_item.additional_properties = d
        return get_api_questions_response_200_questions_item_custom_files_item

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
