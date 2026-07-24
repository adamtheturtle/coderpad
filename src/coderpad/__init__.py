"""A library for the CoderPad Interview and Screen APIs."""

from coderpad.async_client import AsyncCoderPad
from coderpad.client import CoderPad
from coderpad.screen import SCREEN_EU_BASE_URL, SCREEN_US_BASE_URL
from coderpad.screen_types import (
    ScreenCampaign,
    ScreenInvitation,
    ScreenInvitationResult,
    ScreenPagination,
    ScreenReport,
    ScreenSkillResult,
    ScreenTechnologyResult,
    ScreenTest,
    ScreenTestQuestion,
    ScreenTestsPage,
    ScreenWebhook,
)

__all__ = [
    "SCREEN_EU_BASE_URL",
    "SCREEN_US_BASE_URL",
    "AsyncCoderPad",
    "CoderPad",
    "ScreenCampaign",
    "ScreenInvitation",
    "ScreenInvitationResult",
    "ScreenPagination",
    "ScreenReport",
    "ScreenSkillResult",
    "ScreenTechnologyResult",
    "ScreenTest",
    "ScreenTestQuestion",
    "ScreenTestsPage",
    "ScreenWebhook",
]
