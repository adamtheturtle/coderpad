from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_api_organization_pads_response_200_pads_item_team import (
        GetApiOrganizationPadsResponse200PadsItemTeam,
    )


T = TypeVar("T", bound="GetApiOrganizationPadsResponse200PadsItem")


@_attrs_define
class GetApiOrganizationPadsResponse200PadsItem:
    """
    Attributes:
        id (str | Unset):
        title (str | Unset):
        state (str | Unset):
        owner_email (str | Unset):
        language (None | Unset):
        private (bool | Unset):
        execution_enabled (bool | Unset):
        contents (None | Unset):
        participants (list[str] | Unset):
        events (str | Unset):
        notes (str | Unset):
        created_at (datetime.datetime | Unset):
        updated_at (datetime.datetime | Unset):
        ended_at (None | Unset):
        url (str | Unset):
        playback (str | Unset):
        history (str | Unset):
        drawing (None | Unset):
        type_ (str | Unset):
        question_ids (list[int] | Unset):
        pad_environment_ids (list[int] | Unset):
        active_environment_id (int | Unset):
        team (GetApiOrganizationPadsResponse200PadsItemTeam | Unset):
    """

    id: str | Unset = UNSET
    title: str | Unset = UNSET
    state: str | Unset = UNSET
    owner_email: str | Unset = UNSET
    language: None | Unset = UNSET
    private: bool | Unset = UNSET
    execution_enabled: bool | Unset = UNSET
    contents: None | Unset = UNSET
    participants: list[str] | Unset = UNSET
    events: str | Unset = UNSET
    notes: str | Unset = UNSET
    created_at: datetime.datetime | Unset = UNSET
    updated_at: datetime.datetime | Unset = UNSET
    ended_at: None | Unset = UNSET
    url: str | Unset = UNSET
    playback: str | Unset = UNSET
    history: str | Unset = UNSET
    drawing: None | Unset = UNSET
    type_: str | Unset = UNSET
    question_ids: list[int] | Unset = UNSET
    pad_environment_ids: list[int] | Unset = UNSET
    active_environment_id: int | Unset = UNSET
    team: GetApiOrganizationPadsResponse200PadsItemTeam | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=dict
    )

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        title = self.title

        state = self.state

        owner_email = self.owner_email

        language = self.language

        private = self.private

        execution_enabled = self.execution_enabled

        contents = self.contents

        participants: list[str] | Unset = UNSET
        if not isinstance(self.participants, Unset):
            participants = self.participants

        events = self.events

        notes = self.notes

        created_at: str | Unset = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        updated_at: str | Unset = UNSET
        if not isinstance(self.updated_at, Unset):
            updated_at = self.updated_at.isoformat()

        ended_at = self.ended_at

        url = self.url

        playback = self.playback

        history = self.history

        drawing = self.drawing

        type_ = self.type_

        question_ids: list[int] | Unset = UNSET
        if not isinstance(self.question_ids, Unset):
            question_ids = self.question_ids

        pad_environment_ids: list[int] | Unset = UNSET
        if not isinstance(self.pad_environment_ids, Unset):
            pad_environment_ids = self.pad_environment_ids

        active_environment_id = self.active_environment_id

        team: dict[str, Any] | Unset = UNSET
        if not isinstance(self.team, Unset):
            team = self.team.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if title is not UNSET:
            field_dict["title"] = title
        if state is not UNSET:
            field_dict["state"] = state
        if owner_email is not UNSET:
            field_dict["owner_email"] = owner_email
        if language is not UNSET:
            field_dict["language"] = language
        if private is not UNSET:
            field_dict["private"] = private
        if execution_enabled is not UNSET:
            field_dict["execution_enabled"] = execution_enabled
        if contents is not UNSET:
            field_dict["contents"] = contents
        if participants is not UNSET:
            field_dict["participants"] = participants
        if events is not UNSET:
            field_dict["events"] = events
        if notes is not UNSET:
            field_dict["notes"] = notes
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at
        if ended_at is not UNSET:
            field_dict["ended_at"] = ended_at
        if url is not UNSET:
            field_dict["url"] = url
        if playback is not UNSET:
            field_dict["playback"] = playback
        if history is not UNSET:
            field_dict["history"] = history
        if drawing is not UNSET:
            field_dict["drawing"] = drawing
        if type_ is not UNSET:
            field_dict["type"] = type_
        if question_ids is not UNSET:
            field_dict["question_ids"] = question_ids
        if pad_environment_ids is not UNSET:
            field_dict["pad_environment_ids"] = pad_environment_ids
        if active_environment_id is not UNSET:
            field_dict["active_environment_id"] = active_environment_id
        if team is not UNSET:
            field_dict["team"] = team

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.get_api_organization_pads_response_200_pads_item_team import (
            GetApiOrganizationPadsResponse200PadsItemTeam,
        )

        d = dict(src_dict)
        id = d.pop("id", UNSET)

        title = d.pop("title", UNSET)

        state = d.pop("state", UNSET)

        owner_email = d.pop("owner_email", UNSET)

        language = d.pop("language", UNSET)

        private = d.pop("private", UNSET)

        execution_enabled = d.pop("execution_enabled", UNSET)

        contents = d.pop("contents", UNSET)

        participants = cast("list[str]", d.pop("participants", UNSET))

        events = d.pop("events", UNSET)

        notes = d.pop("notes", UNSET)

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

        ended_at = d.pop("ended_at", UNSET)

        url = d.pop("url", UNSET)

        playback = d.pop("playback", UNSET)

        history = d.pop("history", UNSET)

        drawing = d.pop("drawing", UNSET)

        type_ = d.pop("type", UNSET)

        question_ids = cast("list[int]", d.pop("question_ids", UNSET))

        pad_environment_ids = cast(
            "list[int]", d.pop("pad_environment_ids", UNSET)
        )

        active_environment_id = d.pop("active_environment_id", UNSET)

        _team = d.pop("team", UNSET)
        team: GetApiOrganizationPadsResponse200PadsItemTeam | Unset
        if isinstance(_team, Unset):
            team = UNSET
        else:
            team = GetApiOrganizationPadsResponse200PadsItemTeam.from_dict(
                _team
            )

        get_api_organization_pads_response_200_pads_item = cls(
            id=id,
            title=title,
            state=state,
            owner_email=owner_email,
            language=language,
            private=private,
            execution_enabled=execution_enabled,
            contents=contents,
            participants=participants,
            events=events,
            notes=notes,
            created_at=created_at,
            updated_at=updated_at,
            ended_at=ended_at,
            url=url,
            playback=playback,
            history=history,
            drawing=drawing,
            type_=type_,
            question_ids=question_ids,
            pad_environment_ids=pad_environment_ids,
            active_environment_id=active_environment_id,
            team=team,
        )

        get_api_organization_pads_response_200_pads_item.additional_properties = d
        return get_api_organization_pads_response_200_pads_item

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
