"""Tests for the CoderPad client."""

import pytest

from coderpad_api.client import CoderPadClient
from coderpad_api.transports import (
    HTTPStatusError,
    HTTPXTransport,
    Transport,
    TransportResponse,
)
from coderpad_api.types import SortOrder


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
    def test_custom_transport(
        mock_coderpad_api: object,
    ) -> None:
        """A custom transport can be provided."""
        del mock_coderpad_api
        transport = HTTPXTransport()
        client = CoderPadClient(
            api_key="test-key",
            transport=transport,
        )
        result = client.pads.list()
        assert result.total >= 0

    @staticmethod
    def test_mock_api_available(
        coderpad_client: CoderPadClient,
    ) -> None:
        """The mock API fixture provides a working mock router."""
        result = coderpad_client.pads.list()
        assert result.total >= 0

    @staticmethod
    def test_close() -> None:
        """The client can be closed."""
        client = CoderPadClient(api_key="test-key")
        client.close()

    @staticmethod
    def test_context_manager() -> None:
        """The client can be used as a context manager."""
        with CoderPadClient(api_key="test-key") as client:
            assert isinstance(client, CoderPadClient)

    @staticmethod
    def test_close_transport_without_close() -> None:
        """Closing works when the transport has no close method."""

        class _NoCloseTransport:
            def __call__(
                self,
                *,
                method: str,
                url: str,
                headers: dict[str, str],
                params: dict[str, str | int] | None = None,
                data: dict[str, str] | None = None,
            ) -> TransportResponse:  # pragma: no cover
                raise NotImplementedError

        client = CoderPadClient(
            api_key="test-key",
            transport=_NoCloseTransport(),
        )
        client.close()


class TestHTTPXTransport:
    """Tests for ``HTTPXTransport``."""

    @staticmethod
    def test_is_transport() -> None:
        """HTTPXTransport satisfies the Transport protocol."""
        assert isinstance(HTTPXTransport(), Transport)

    @staticmethod
    def test_close() -> None:
        """The transport can be closed."""
        transport = HTTPXTransport()
        transport.close()

    @staticmethod
    def test_context_manager() -> None:
        """The transport can be used as a context manager."""
        with HTTPXTransport() as transport:
            assert isinstance(transport, HTTPXTransport)


class TestTransportResponse:
    """Tests for ``TransportResponse``."""

    @staticmethod
    def test_raise_for_status_error() -> None:
        """An error status code raises HTTPStatusError."""
        error_status_code = 404
        error_content = b"Not Found"
        response = TransportResponse(
            status_code=error_status_code,
            headers={},
            content=error_content,
        )
        with pytest.raises(expected_exception=HTTPStatusError) as exc_info:
            response.raise_for_status()
        assert exc_info.value.status_code == error_status_code
        assert exc_info.value.content == error_content

    @staticmethod
    def test_raise_for_status_ok() -> None:
        """A success status code does not raise."""
        response = TransportResponse(
            status_code=200,
            headers={},
            content=b"{}",
        )
        response.raise_for_status()


class TestListPads:
    """Tests for ``CoderPadClient.pads.list``."""

    @staticmethod
    def test_list_pads(
        coderpad_client: CoderPadClient,
    ) -> None:
        """Pads can be listed."""
        result = coderpad_client.pads.list()
        assert result.total >= 0

    @staticmethod
    def test_list_pads_with_sort(
        coderpad_client: CoderPadClient,
    ) -> None:
        """Pads can be listed with a sort parameter."""
        result = coderpad_client.pads.list(
            sort=SortOrder.UPDATED_AT_DESC,
        )
        assert result.total >= 0

    @staticmethod
    def test_list_pads_with_page(
        coderpad_client: CoderPadClient,
    ) -> None:
        """Pads can be listed with a page parameter."""
        result = coderpad_client.pads.list(page=2)
        assert result.total >= 0


class TestCreatePad:
    """Tests for ``CoderPadClient.pads.create``."""

    @staticmethod
    def test_create_pad(
        coderpad_client: CoderPadClient,
    ) -> None:
        """A pad can be created."""
        result = coderpad_client.pads.create(
            title="Test Pad",
            language="python",
        )
        assert result.id

    @staticmethod
    def test_create_pad_all_params(
        coderpad_client: CoderPadClient,
    ) -> None:
        """A pad can be created with all parameters."""
        result = coderpad_client.pads.create(
            title="Test Pad",
            language="python",
            contents="print('hello')",
            notes="Private notes",
        )
        assert result.id

    @staticmethod
    def test_create_pad_minimal(
        coderpad_client: CoderPadClient,
    ) -> None:
        """A pad can be created with no parameters."""
        result = coderpad_client.pads.create()
        assert result.id


class TestGetPad:
    """Tests for ``CoderPadClient.pads.get``."""

    @staticmethod
    def test_get_pad(
        coderpad_client: CoderPadClient,
    ) -> None:
        """A pad can be retrieved by id."""
        result = coderpad_client.pads.get(
            pad_id="ABC1234",
        )
        assert result.id


class TestUpdatePad:
    """Tests for ``CoderPadClient.pads.update``."""

    @staticmethod
    def test_update_pad(
        coderpad_client: CoderPadClient,
    ) -> None:
        """A pad can be updated."""
        coderpad_client.pads.update(
            pad_id="ABC1234",
            title="Updated Title",
        )

    @staticmethod
    def test_update_pad_no_title(
        coderpad_client: CoderPadClient,
    ) -> None:
        """A pad can be updated without a title."""
        coderpad_client.pads.update(
            pad_id="ABC1234",
            language="python",
        )

    @staticmethod
    def test_update_pad_all_params(
        coderpad_client: CoderPadClient,
    ) -> None:
        """A pad can be updated with all parameters."""
        coderpad_client.pads.update(
            pad_id="ABC1234",
            title="Updated Title",
            language="python",
            contents="print('hello')",
            notes="Notes",
            ended=True,
            deleted=False,
        )


class TestGetPadEvents:
    """Tests for ``CoderPadClient.pads.get_events``."""

    @staticmethod
    def test_get_pad_events(
        coderpad_client: CoderPadClient,
    ) -> None:
        """Pad events can be retrieved."""
        result = coderpad_client.pads.get_events(
            pad_id="ABC1234",
        )
        assert result.total >= 0

    @staticmethod
    def test_get_pad_events_with_params(
        coderpad_client: CoderPadClient,
    ) -> None:
        """Pad events can be retrieved with sort and page."""
        result = coderpad_client.pads.get_events(
            pad_id="ABC1234",
            sort=SortOrder.CREATED_AT_ASC,
            page=1,
        )
        assert result.total >= 0


class TestGetPadEnvironment:
    """Tests for ``CoderPadClient.pads.get_environment``."""

    @staticmethod
    def test_get_pad_environment(
        coderpad_client: CoderPadClient,
    ) -> None:
        """A pad environment can be retrieved."""
        result = coderpad_client.pads.get_environment(
            environment_id="123",
        )
        assert result.id


class TestListQuestions:
    """Tests for ``CoderPadClient.questions.list``."""

    @staticmethod
    def test_list_questions(
        coderpad_client: CoderPadClient,
    ) -> None:
        """Questions can be listed."""
        result = coderpad_client.questions.list()
        assert result.total >= 0

    @staticmethod
    def test_list_questions_with_params(
        coderpad_client: CoderPadClient,
    ) -> None:
        """Questions can be listed with sort and page."""
        result = coderpad_client.questions.list(
            sort=SortOrder.UPDATED_AT_DESC,
            page=1,
        )
        assert result.total >= 0


class TestCreateQuestion:
    """Tests for ``CoderPadClient.questions.create``."""

    @staticmethod
    def test_create_question(
        coderpad_client: CoderPadClient,
    ) -> None:
        """A question can be created."""
        result = coderpad_client.questions.create(
            title="Test Question",
            language="python",
        )
        assert result.id

    @staticmethod
    def test_create_question_all_params(
        coderpad_client: CoderPadClient,
    ) -> None:
        """A question can be created with all parameters."""
        result = coderpad_client.questions.create(
            title="Test Question",
            language="python",
            description="A description",
            contents="def solve(): pass",
            solution="def solve(): return 42",
        )
        assert result.id


class TestGetQuestion:
    """Tests for ``CoderPadClient.questions.get``."""

    @staticmethod
    def test_get_question(
        coderpad_client: CoderPadClient,
    ) -> None:
        """A question can be retrieved by id."""
        result = coderpad_client.questions.get(
            question_id="123",
        )
        assert result.id


class TestUpdateQuestion:
    """Tests for ``CoderPadClient.questions.update``."""

    @staticmethod
    def test_update_question(
        coderpad_client: CoderPadClient,
    ) -> None:
        """A question can be updated."""
        coderpad_client.questions.update(
            question_id="123",
            title="Updated Question",
        )

    @staticmethod
    def test_update_question_no_title(
        coderpad_client: CoderPadClient,
    ) -> None:
        """A question can be updated without a title."""
        coderpad_client.questions.update(
            question_id="123",
            language="ruby",
        )

    @staticmethod
    def test_update_question_all_params(
        coderpad_client: CoderPadClient,
    ) -> None:
        """A question can be updated with all parameters."""
        coderpad_client.questions.update(
            question_id="123",
            title="Updated",
            language="ruby",
            description="New desc",
            contents="puts 'hi'",
            solution="puts 'answer'",
        )


class TestDeleteQuestion:
    """Tests for ``CoderPadClient.questions.delete``."""

    @staticmethod
    def test_delete_question(
        coderpad_client: CoderPadClient,
    ) -> None:
        """A question can be deleted."""
        coderpad_client.questions.delete(
            question_id="123",
        )


class TestGetQuota:
    """Tests for ``CoderPadClient.organization.get_quota``."""

    @staticmethod
    def test_get_quota(
        coderpad_client: CoderPadClient,
    ) -> None:
        """Quota information can be retrieved."""
        result = coderpad_client.organization.get_quota()
        assert result.pads_used >= 0


class TestGetOrganization:
    """Tests for ``CoderPadClient.organization.get``."""

    @staticmethod
    def test_get_organization(
        coderpad_client: CoderPadClient,
    ) -> None:
        """Organization information can be retrieved."""
        result = coderpad_client.organization.get()
        assert result.organization_name


class TestGetOrganizationStats:
    """Tests for ``CoderPadClient.organization.get_stats``."""

    @staticmethod
    def test_get_organization_stats(
        coderpad_client: CoderPadClient,
    ) -> None:
        """Organization stats can be retrieved."""
        result = coderpad_client.organization.get_stats()
        assert result.pads_created >= 0

    @staticmethod
    def test_get_organization_stats_with_params(
        coderpad_client: CoderPadClient,
    ) -> None:
        """Organization stats can be filtered by time range."""
        result = coderpad_client.organization.get_stats(
            start_time="2023-07-01T00:00:00Z",
            end_time="2023-07-31T00:00:00Z",
        )
        assert result.pads_created >= 0


class TestListOrganizationPads:
    """Tests for ``CoderPadClient.organization.pads.list``."""

    @staticmethod
    def test_list_organization_pads(
        coderpad_client: CoderPadClient,
    ) -> None:
        """Organization pads can be listed."""
        result = coderpad_client.organization.pads.list()
        assert result.total >= 0

    @staticmethod
    def test_list_organization_pads_with_params(
        coderpad_client: CoderPadClient,
    ) -> None:
        """Organization pads can be listed with optional arguments."""
        result = coderpad_client.organization.pads.list(
            sort=SortOrder.UPDATED_AT_ASC,
            page=1,
        )
        assert result.total >= 0


class TestListOrganizationQuestions:
    """Tests for ``CoderPadClient.organization.questions.list``."""

    @staticmethod
    def test_list_organization_questions(
        coderpad_client: CoderPadClient,
    ) -> None:
        """Organization questions can be listed."""
        result = coderpad_client.organization.questions.list()
        assert result.total >= 0

    @staticmethod
    def test_list_organization_questions_with_params(
        coderpad_client: CoderPadClient,
    ) -> None:
        """Organization questions can be listed with optional
        arguments.
        """
        result = coderpad_client.organization.questions.list(
            sort=SortOrder.CREATED_AT_DESC,
            page=1,
        )
        assert result.total >= 0
