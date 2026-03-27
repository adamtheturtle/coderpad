from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_api_questions_response_200_questions_item import (
        GetApiQuestionsResponse200QuestionsItem,
    )


T = TypeVar("T", bound="GetApiQuestionsResponse200")


@_attrs_define
class GetApiQuestionsResponse200:
    """
    Attributes:
        status (str | Unset):
        questions (list[GetApiQuestionsResponse200QuestionsItem] | Unset):
        next_page (str | Unset):
        total (int | Unset):
    """

    status: str | Unset = UNSET
    questions: list[GetApiQuestionsResponse200QuestionsItem] | Unset = UNSET
    next_page: str | Unset = UNSET
    total: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=dict
    )

    def to_dict(self) -> dict[str, Any]:
        status = self.status

        questions: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.questions, Unset):
            questions = []
            for questions_item_data in self.questions:
                questions_item = questions_item_data.to_dict()
                questions.append(questions_item)

        next_page = self.next_page

        total = self.total

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if status is not UNSET:
            field_dict["status"] = status
        if questions is not UNSET:
            field_dict["questions"] = questions
        if next_page is not UNSET:
            field_dict["next_page"] = next_page
        if total is not UNSET:
            field_dict["total"] = total

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.get_api_questions_response_200_questions_item import (
            GetApiQuestionsResponse200QuestionsItem,
        )

        d = dict(src_dict)
        status = d.pop("status", UNSET)

        _questions = d.pop("questions", UNSET)
        questions: list[GetApiQuestionsResponse200QuestionsItem] | Unset = (
            UNSET
        )
        if _questions is not UNSET:
            questions = []
            for questions_item_data in _questions:
                questions_item = (
                    GetApiQuestionsResponse200QuestionsItem.from_dict(
                        questions_item_data
                    )
                )

                questions.append(questions_item)

        next_page = d.pop("next_page", UNSET)

        total = d.pop("total", UNSET)

        get_api_questions_response_200 = cls(
            status=status,
            questions=questions,
            next_page=next_page,
            total=total,
        )

        get_api_questions_response_200.additional_properties = d
        return get_api_questions_response_200

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
