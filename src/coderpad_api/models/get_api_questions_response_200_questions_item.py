from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_api_questions_response_200_questions_item_candidate_instructions_item import (
        GetApiQuestionsResponse200QuestionsItemCandidateInstructionsItem,
    )
    from ..models.get_api_questions_response_200_questions_item_custom_files_item import (
        GetApiQuestionsResponse200QuestionsItemCustomFilesItem,
    )
    from ..models.get_api_questions_response_200_questions_item_test_cases_item import (
        GetApiQuestionsResponse200QuestionsItemTestCasesItem,
    )


T = TypeVar("T", bound="GetApiQuestionsResponse200QuestionsItem")


@_attrs_define
class GetApiQuestionsResponse200QuestionsItem:
    """
    Attributes:
        id (int | Unset):
        title (str | Unset):
        owner_email (str | Unset):
        language (str | Unset):
        description (str | Unset):
        candidate_instructions
    (list[GetApiQuestionsResponse200QuestionsItemCandidateInstructionsItem]
    | Unset):
        contents (None | Unset):
        shared (bool | Unset):
        used (int | Unset):
        take_home (bool | Unset):
        test_cases_enabled (bool | Unset):
        solution (str | Unset):
        pad_type (str | Unset):
        is_draft (bool | Unset):
        author_name (str | Unset):
        organization_name (str | Unset):
        custom_files
    (list[GetApiQuestionsResponse200QuestionsItemCustomFilesItem] | Unset):
        public_take_home_setting_id (int | Unset):
        contents_for_test_cases (str | Unset):
        test_cases
    (list[GetApiQuestionsResponse200QuestionsItemTestCasesItem] | Unset):
        created_at (datetime.datetime | Unset):
        updated_at (datetime.datetime | Unset):
    """

    id: int | Unset = UNSET
    title: str | Unset = UNSET
    owner_email: str | Unset = UNSET
    language: str | Unset = UNSET
    description: str | Unset = UNSET
    candidate_instructions: (
        list[GetApiQuestionsResponse200QuestionsItemCandidateInstructionsItem]
        | Unset
    ) = UNSET
    contents: None | Unset = UNSET
    shared: bool | Unset = UNSET
    used: int | Unset = UNSET
    take_home: bool | Unset = UNSET
    test_cases_enabled: bool | Unset = UNSET
    solution: str | Unset = UNSET
    pad_type: str | Unset = UNSET
    is_draft: bool | Unset = UNSET
    author_name: str | Unset = UNSET
    organization_name: str | Unset = UNSET
    custom_files: (
        list[GetApiQuestionsResponse200QuestionsItemCustomFilesItem] | Unset
    ) = UNSET
    public_take_home_setting_id: int | Unset = UNSET
    contents_for_test_cases: str | Unset = UNSET
    test_cases: (
        list[GetApiQuestionsResponse200QuestionsItemTestCasesItem] | Unset
    ) = UNSET
    created_at: datetime.datetime | Unset = UNSET
    updated_at: datetime.datetime | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=dict
    )

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        title = self.title

        owner_email = self.owner_email

        language = self.language

        description = self.description

        candidate_instructions: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.candidate_instructions, Unset):
            candidate_instructions = []
            for (
                candidate_instructions_item_data
            ) in self.candidate_instructions:
                candidate_instructions_item = (
                    candidate_instructions_item_data.to_dict()
                )
                candidate_instructions.append(candidate_instructions_item)

        contents = self.contents

        shared = self.shared

        used = self.used

        take_home = self.take_home

        test_cases_enabled = self.test_cases_enabled

        solution = self.solution

        pad_type = self.pad_type

        is_draft = self.is_draft

        author_name = self.author_name

        organization_name = self.organization_name

        custom_files: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.custom_files, Unset):
            custom_files = []
            for custom_files_item_data in self.custom_files:
                custom_files_item = custom_files_item_data.to_dict()
                custom_files.append(custom_files_item)

        public_take_home_setting_id = self.public_take_home_setting_id

        contents_for_test_cases = self.contents_for_test_cases

        test_cases: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.test_cases, Unset):
            test_cases = []
            for test_cases_item_data in self.test_cases:
                test_cases_item = test_cases_item_data.to_dict()
                test_cases.append(test_cases_item)

        created_at: str | Unset = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        updated_at: str | Unset = UNSET
        if not isinstance(self.updated_at, Unset):
            updated_at = self.updated_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if title is not UNSET:
            field_dict["title"] = title
        if owner_email is not UNSET:
            field_dict["owner_email"] = owner_email
        if language is not UNSET:
            field_dict["language"] = language
        if description is not UNSET:
            field_dict["description"] = description
        if candidate_instructions is not UNSET:
            field_dict["candidate_instructions"] = candidate_instructions
        if contents is not UNSET:
            field_dict["contents"] = contents
        if shared is not UNSET:
            field_dict["shared"] = shared
        if used is not UNSET:
            field_dict["used"] = used
        if take_home is not UNSET:
            field_dict["take_home"] = take_home
        if test_cases_enabled is not UNSET:
            field_dict["test_cases_enabled"] = test_cases_enabled
        if solution is not UNSET:
            field_dict["solution"] = solution
        if pad_type is not UNSET:
            field_dict["pad_type"] = pad_type
        if is_draft is not UNSET:
            field_dict["is_draft"] = is_draft
        if author_name is not UNSET:
            field_dict["author_name"] = author_name
        if organization_name is not UNSET:
            field_dict["organization_name"] = organization_name
        if custom_files is not UNSET:
            field_dict["custom_files"] = custom_files
        if public_take_home_setting_id is not UNSET:
            field_dict["public_take_home_setting_id"] = (
                public_take_home_setting_id
            )
        if contents_for_test_cases is not UNSET:
            field_dict["contents_for_test_cases"] = contents_for_test_cases
        if test_cases is not UNSET:
            field_dict["test_cases"] = test_cases
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.get_api_questions_response_200_questions_item_candidate_instructions_item import (
            GetApiQuestionsResponse200QuestionsItemCandidateInstructionsItem,
        )
        from ..models.get_api_questions_response_200_questions_item_custom_files_item import (
            GetApiQuestionsResponse200QuestionsItemCustomFilesItem,
        )
        from ..models.get_api_questions_response_200_questions_item_test_cases_item import (
            GetApiQuestionsResponse200QuestionsItemTestCasesItem,
        )

        d = dict(src_dict)
        id = d.pop("id", UNSET)

        title = d.pop("title", UNSET)

        owner_email = d.pop("owner_email", UNSET)

        language = d.pop("language", UNSET)

        description = d.pop("description", UNSET)

        _candidate_instructions = d.pop("candidate_instructions", UNSET)
        candidate_instructions: (
            list[
                GetApiQuestionsResponse200QuestionsItemCandidateInstructionsItem
            ]
            | Unset
        ) = UNSET
        if _candidate_instructions is not UNSET:
            candidate_instructions = []
            for candidate_instructions_item_data in _candidate_instructions:
                candidate_instructions_item = GetApiQuestionsResponse200QuestionsItemCandidateInstructionsItem.from_dict(
                    candidate_instructions_item_data
                )

                candidate_instructions.append(candidate_instructions_item)

        contents = d.pop("contents", UNSET)

        shared = d.pop("shared", UNSET)

        used = d.pop("used", UNSET)

        take_home = d.pop("take_home", UNSET)

        test_cases_enabled = d.pop("test_cases_enabled", UNSET)

        solution = d.pop("solution", UNSET)

        pad_type = d.pop("pad_type", UNSET)

        is_draft = d.pop("is_draft", UNSET)

        author_name = d.pop("author_name", UNSET)

        organization_name = d.pop("organization_name", UNSET)

        _custom_files = d.pop("custom_files", UNSET)
        custom_files: (
            list[GetApiQuestionsResponse200QuestionsItemCustomFilesItem]
            | Unset
        ) = UNSET
        if _custom_files is not UNSET:
            custom_files = []
            for custom_files_item_data in _custom_files:
                custom_files_item = GetApiQuestionsResponse200QuestionsItemCustomFilesItem.from_dict(
                    custom_files_item_data
                )

                custom_files.append(custom_files_item)

        public_take_home_setting_id = d.pop(
            "public_take_home_setting_id", UNSET
        )

        contents_for_test_cases = d.pop("contents_for_test_cases", UNSET)

        _test_cases = d.pop("test_cases", UNSET)
        test_cases: (
            list[GetApiQuestionsResponse200QuestionsItemTestCasesItem] | Unset
        ) = UNSET
        if _test_cases is not UNSET:
            test_cases = []
            for test_cases_item_data in _test_cases:
                test_cases_item = GetApiQuestionsResponse200QuestionsItemTestCasesItem.from_dict(
                    test_cases_item_data
                )

                test_cases.append(test_cases_item)

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

        get_api_questions_response_200_questions_item = cls(
            id=id,
            title=title,
            owner_email=owner_email,
            language=language,
            description=description,
            candidate_instructions=candidate_instructions,
            contents=contents,
            shared=shared,
            used=used,
            take_home=take_home,
            test_cases_enabled=test_cases_enabled,
            solution=solution,
            pad_type=pad_type,
            is_draft=is_draft,
            author_name=author_name,
            organization_name=organization_name,
            custom_files=custom_files,
            public_take_home_setting_id=public_take_home_setting_id,
            contents_for_test_cases=contents_for_test_cases,
            test_cases=test_cases,
            created_at=created_at,
            updated_at=updated_at,
        )

        get_api_questions_response_200_questions_item.additional_properties = d
        return get_api_questions_response_200_questions_item

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
