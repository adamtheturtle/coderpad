from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetApiQuotaResponse200")


@_attrs_define
class GetApiQuotaResponse200:
    """
    Attributes:
        status (str | Unset):
        trial_expires_at (datetime.datetime | Unset):
        pads_used (int | Unset):
        quota_reset_at (datetime.datetime | Unset):
        unlimited (bool | Unset):
        overages_enabled (bool | Unset):
    """

    status: str | Unset = UNSET
    trial_expires_at: datetime.datetime | Unset = UNSET
    pads_used: int | Unset = UNSET
    quota_reset_at: datetime.datetime | Unset = UNSET
    unlimited: bool | Unset = UNSET
    overages_enabled: bool | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=dict
    )

    def to_dict(self) -> dict[str, Any]:
        status = self.status

        trial_expires_at: str | Unset = UNSET
        if not isinstance(self.trial_expires_at, Unset):
            trial_expires_at = self.trial_expires_at.isoformat()

        pads_used = self.pads_used

        quota_reset_at: str | Unset = UNSET
        if not isinstance(self.quota_reset_at, Unset):
            quota_reset_at = self.quota_reset_at.isoformat()

        unlimited = self.unlimited

        overages_enabled = self.overages_enabled

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if status is not UNSET:
            field_dict["status"] = status
        if trial_expires_at is not UNSET:
            field_dict["trial_expires_at"] = trial_expires_at
        if pads_used is not UNSET:
            field_dict["pads_used"] = pads_used
        if quota_reset_at is not UNSET:
            field_dict["quota_reset_at"] = quota_reset_at
        if unlimited is not UNSET:
            field_dict["unlimited"] = unlimited
        if overages_enabled is not UNSET:
            field_dict["overages_enabled"] = overages_enabled

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        status = d.pop("status", UNSET)

        _trial_expires_at = d.pop("trial_expires_at", UNSET)
        trial_expires_at: datetime.datetime | Unset
        if isinstance(_trial_expires_at, Unset):
            trial_expires_at = UNSET
        else:
            trial_expires_at = isoparse(_trial_expires_at)

        pads_used = d.pop("pads_used", UNSET)

        _quota_reset_at = d.pop("quota_reset_at", UNSET)
        quota_reset_at: datetime.datetime | Unset
        if isinstance(_quota_reset_at, Unset):
            quota_reset_at = UNSET
        else:
            quota_reset_at = isoparse(_quota_reset_at)

        unlimited = d.pop("unlimited", UNSET)

        overages_enabled = d.pop("overages_enabled", UNSET)

        get_api_quota_response_200 = cls(
            status=status,
            trial_expires_at=trial_expires_at,
            pads_used=pads_used,
            quota_reset_at=quota_reset_at,
            unlimited=unlimited,
            overages_enabled=overages_enabled,
        )

        get_api_quota_response_200.additional_properties = d
        return get_api_quota_response_200

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
