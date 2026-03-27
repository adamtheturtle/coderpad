from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_api_pad_environments_id_response_200_file_contents_item import (
        GetApiPadEnvironmentsIdResponse200FileContentsItem,
    )


T = TypeVar("T", bound="GetApiPadEnvironmentsIdResponse200")


@_attrs_define
class GetApiPadEnvironmentsIdResponse200:
    """
    Attributes:
        status (str | Unset):
        id (int | Unset):
        pad_id (int | Unset):
        question_id (None | Unset):
        example_question_id (None | Unset):
        language (str | Unset):
        file_contents
    (list[GetApiPadEnvironmentsIdResponse200FileContentsItem] | Unset):
        created_at (datetime.datetime | Unset):
        updated_at (datetime.datetime | Unset):
    """

    status: str | Unset = UNSET
    id: int | Unset = UNSET
    pad_id: int | Unset = UNSET
    question_id: None | Unset = UNSET
    example_question_id: None | Unset = UNSET
    language: str | Unset = UNSET
    file_contents: (
        list[GetApiPadEnvironmentsIdResponse200FileContentsItem] | Unset
    ) = UNSET
    created_at: datetime.datetime | Unset = UNSET
    updated_at: datetime.datetime | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=dict
    )

    def to_dict(self) -> dict[str, Any]:
        status = self.status

        id = self.id

        pad_id = self.pad_id

        question_id = self.question_id

        example_question_id = self.example_question_id

        language = self.language

        file_contents: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.file_contents, Unset):
            file_contents = []
            for file_contents_item_data in self.file_contents:
                file_contents_item = file_contents_item_data.to_dict()
                file_contents.append(file_contents_item)

        created_at: str | Unset = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        updated_at: str | Unset = UNSET
        if not isinstance(self.updated_at, Unset):
            updated_at = self.updated_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if status is not UNSET:
            field_dict["status"] = status
        if id is not UNSET:
            field_dict["id"] = id
        if pad_id is not UNSET:
            field_dict["pad_id"] = pad_id
        if question_id is not UNSET:
            field_dict["question_id"] = question_id
        if example_question_id is not UNSET:
            field_dict["example_question_id"] = example_question_id
        if language is not UNSET:
            field_dict["language"] = language
        if file_contents is not UNSET:
            field_dict["file_contents"] = file_contents
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.get_api_pad_environments_id_response_200_file_contents_item import (
            GetApiPadEnvironmentsIdResponse200FileContentsItem,
        )

        d = dict(src_dict)
        status = d.pop("status", UNSET)

        id = d.pop("id", UNSET)

        pad_id = d.pop("pad_id", UNSET)

        question_id = d.pop("question_id", UNSET)

        example_question_id = d.pop("example_question_id", UNSET)

        language = d.pop("language", UNSET)

        _file_contents = d.pop("file_contents", UNSET)
        file_contents: (
            list[GetApiPadEnvironmentsIdResponse200FileContentsItem] | Unset
        ) = UNSET
        if _file_contents is not UNSET:
            file_contents = []
            for file_contents_item_data in _file_contents:
                file_contents_item = GetApiPadEnvironmentsIdResponse200FileContentsItem.from_dict(
                    file_contents_item_data
                )

                file_contents.append(file_contents_item)

        _created_at = d.pop("created_at", UNSET)
        created_at: datetime.datetime | Unset
        if isinstance(_created_at, Unset):
            created_at = UNSET
        else:
            created_at = isoparse(_created_at)

        _updated_at = d.pop("updated_at", UNSET)
        updated_at: datetime.datetime | Unset
        if isinstance(_updated_at, Unset):
            updated_at = UNSET
        else:
            updated_at = isoparse(_updated_at)

        get_api_pad_environments_id_response_200 = cls(
            status=status,
            id=id,
            pad_id=pad_id,
            question_id=question_id,
            example_question_id=example_question_id,
            language=language,
            file_contents=file_contents,
            created_at=created_at,
            updated_at=updated_at,
        )

        get_api_pad_environments_id_response_200.additional_properties = d
        return get_api_pad_environments_id_response_200

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
