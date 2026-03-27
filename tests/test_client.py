"""Tests for the CoderPad client."""

import httpx
import respx

from coderpad_api import CoderPadClient


class TestCoderPadClient:
    """Tests for ``CoderPadClient``."""

    @staticmethod
    def test_default_base_url() -> None:
        """The default base URL is the CoderPad Interview API."""
        client = CoderPadClient(api_key="test-key")
        assert client.base_url == "https://api.interview.coderpad.io"

    @staticmethod
    def test_custom_base_url() -> None:
        """A custom base URL can be provided."""
        client = CoderPadClient(
            api_key="test-key",
            base_url="https://custom.example.com",
        )
        assert client.base_url == "https://custom.example.com"

    @staticmethod
    def test_mock_api_available(
        fixture_mock_coderpad_api: respx.MockRouter,
    ) -> None:
        """The mock API fixture provides a working mock router."""
        assert fixture_mock_coderpad_api.calls.call_count == 0
        response = httpx.get(
            url="https://api.interview.coderpad.io/api/pads/",
        )
        assert response.is_success
        assert fixture_mock_coderpad_api.calls.call_count == 1
