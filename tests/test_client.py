"""Tests for the CoderPad client."""

import httpx
import respx

from coderpad_api import AuthenticatedClient


class TestAuthenticatedClient:
    """Tests for ``AuthenticatedClient``."""

    @staticmethod
    def test_default_base_url() -> None:
        """The default base URL is the CoderPad Interview API."""
        client = AuthenticatedClient(
            base_url="https://api.interview.coderpad.io",
            token="test-key",
        )
        httpx_client = client.get_httpx_client()
        assert httpx_client.base_url == httpx.URL(
            url="https://api.interview.coderpad.io"
        )

    @staticmethod
    def test_custom_base_url() -> None:
        """A custom base URL can be provided."""
        client = AuthenticatedClient(
            base_url="https://custom.example.com",
            token="test-key",
        )
        httpx_client = client.get_httpx_client()
        assert httpx_client.base_url == httpx.URL(
            url="https://custom.example.com"
        )

    @staticmethod
    def test_auth_header() -> None:
        """The auth header is set with the Bearer prefix."""
        client = AuthenticatedClient(
            base_url="https://api.interview.coderpad.io",
            token="test-key",
        )
        httpx_client = client.get_httpx_client()
        assert httpx_client.headers["Authorization"] == "Bearer test-key"

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
