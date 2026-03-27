from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar(
    "T",
    bound="GetApiQuestionsResponse200QuestionsItemCandidateInstructionsItem",
)


@_attrs_define
class GetApiQuestionsResponse200QuestionsItemCandidateInstructionsItem:
    """
    Attributes:
        instructions (str | Unset):
        default_visible (bool | Unset):
    """

    instructions: str | Unset = UNSET
    default_visible: bool | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=dict
    )

    def to_dict(self) -> dict[str, Any]:
        instructions = self.instructions

        default_visible = self.default_visible

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if instructions is not UNSET:
            field_dict["instructions"] = instructions
        if default_visible is not UNSET:
            field_dict["default_visible"] = default_visible

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        instructions = d.pop("instructions", UNSET)

        default_visible = d.pop("default_visible", UNSET)

        get_api_questions_response_200_questions_item_candidate_instructions_item = cls(
            instructions=instructions,
            default_visible=default_visible,
        )

        get_api_questions_response_200_questions_item_candidate_instructions_item.additional_properties = d
        return get_api_questions_response_200_questions_item_candidate_instructions_item

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
