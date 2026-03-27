from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetApiQuestionsResponse200QuestionsItemTestCasesItem")


@_attrs_define
class GetApiQuestionsResponse200QuestionsItemTestCasesItem:
    """
    Attributes:
        id (int | Unset):
        return_value (str | Unset):
        visible (bool | Unset):
        arguments (list[str] | Unset):
    """

    id: int | Unset = UNSET
    return_value: str | Unset = UNSET
    visible: bool | Unset = UNSET
    arguments: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=dict
    )

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        return_value = self.return_value

        visible = self.visible

        arguments: list[str] | Unset = UNSET
        if not isinstance(self.arguments, Unset):
            arguments = self.arguments

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if return_value is not UNSET:
            field_dict["return_value"] = return_value
        if visible is not UNSET:
            field_dict["visible"] = visible
        if arguments is not UNSET:
            field_dict["arguments"] = arguments

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        id = d.pop("id", UNSET)

        return_value = d.pop("return_value", UNSET)

        visible = d.pop("visible", UNSET)

        arguments = cast("list[str]", d.pop("arguments", UNSET))

        get_api_questions_response_200_questions_item_test_cases_item = cls(
            id=id,
            return_value=return_value,
            visible=visible,
            arguments=arguments,
        )

        get_api_questions_response_200_questions_item_test_cases_item.additional_properties = d
        return get_api_questions_response_200_questions_item_test_cases_item

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
