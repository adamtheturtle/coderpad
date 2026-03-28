"""Tests for the CoderPad client."""

import respx

from coderpad_api.client import CoderPadClient
from coderpad_api.types import PaginatedList, SortOrder


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
        fixture_coderpad_client: CoderPadClient,
    ) -> None:
        """The mock API fixture provides a working mock router."""
        assert fixture_mock_coderpad_api.calls.call_count == 0
        fixture_coderpad_client.pads.list()
        assert fixture_mock_coderpad_api.calls.call_count == 1


class TestListPads:
    """Tests for ``CoderPadClient.pads.list``."""

    @staticmethod
    def test_list_pads(
        fixture_coderpad_client: CoderPadClient,
    ) -> None:
        """Pads can be listed."""
        result = fixture_coderpad_client.pads.list()
        assert isinstance(result, PaginatedList)
        assert isinstance(result.total, int)

    @staticmethod
    def test_list_pads_with_sort(
        fixture_coderpad_client: CoderPadClient,
    ) -> None:
        """Pads can be listed with a sort parameter."""
        result = fixture_coderpad_client.pads.list(
            sort=SortOrder.UPDATED_AT_DESC,
        )
        assert isinstance(result, PaginatedList)

    @staticmethod
    def test_list_pads_with_page(
        fixture_coderpad_client: CoderPadClient,
    ) -> None:
        """Pads can be listed with a page parameter."""
        result = fixture_coderpad_client.pads.list(page=2)
        assert isinstance(result, PaginatedList)


class TestCreatePad:
    """Tests for ``CoderPadClient.pads.create``."""

    @staticmethod
    def test_create_pad(
        fixture_coderpad_client: CoderPadClient,
    ) -> None:
        """A pad can be created."""
        result = fixture_coderpad_client.pads.create(
            title="Test Pad",
            language="python",
        )
        assert result.id

    @staticmethod
    def test_create_pad_all_params(
        fixture_coderpad_client: CoderPadClient,
    ) -> None:
        """A pad can be created with all parameters."""
        result = fixture_coderpad_client.pads.create(
            title="Test Pad",
            language="python",
            contents="print('hello')",
            notes="Private notes",
        )
        assert result.id

    @staticmethod
    def test_create_pad_minimal(
        fixture_coderpad_client: CoderPadClient,
    ) -> None:
        """A pad can be created with no parameters."""
        result = fixture_coderpad_client.pads.create()
        assert result.id


class TestGetPad:
    """Tests for ``CoderPadClient.pads.get``."""

    @staticmethod
    def test_get_pad(
        fixture_coderpad_client: CoderPadClient,
    ) -> None:
        """A pad can be retrieved by id."""
        result = fixture_coderpad_client.pads.get(
            pad_id="ABC1234",
        )
        assert result.id


class TestUpdatePad:
    """Tests for ``CoderPadClient.pads.update``."""

    @staticmethod
    def test_update_pad(
        fixture_coderpad_client: CoderPadClient,
    ) -> None:
        """A pad can be updated."""
        fixture_coderpad_client.pads.update(
            pad_id="ABC1234",
            title="Updated Title",
        )

    @staticmethod
    def test_update_pad_no_title(
        fixture_coderpad_client: CoderPadClient,
    ) -> None:
        """A pad can be updated without a title."""
        fixture_coderpad_client.pads.update(
            pad_id="ABC1234",
            language="python",
        )

    @staticmethod
    def test_update_pad_all_params(
        fixture_coderpad_client: CoderPadClient,
    ) -> None:
        """A pad can be updated with all parameters."""
        fixture_coderpad_client.pads.update(
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
        fixture_coderpad_client: CoderPadClient,
    ) -> None:
        """Pad events can be retrieved."""
        result = fixture_coderpad_client.pads.get_events(
            pad_id="ABC1234",
        )
        assert isinstance(result, PaginatedList)

    @staticmethod
    def test_get_pad_events_with_params(
        fixture_coderpad_client: CoderPadClient,
    ) -> None:
        """Pad events can be retrieved with sort and page."""
        result = fixture_coderpad_client.pads.get_events(
            pad_id="ABC1234",
            sort=SortOrder.CREATED_AT_ASC,
            page=1,
        )
        assert isinstance(result, PaginatedList)


class TestGetPadEnvironment:
    """Tests for ``CoderPadClient.pads.get_environment``."""

    @staticmethod
    def test_get_pad_environment(
        fixture_coderpad_client: CoderPadClient,
    ) -> None:
        """A pad environment can be retrieved."""
        result = fixture_coderpad_client.pads.get_environment(
            environment_id="123",
        )
        assert result.id


class TestListQuestions:
    """Tests for ``CoderPadClient.questions.list``."""

    @staticmethod
    def test_list_questions(
        fixture_coderpad_client: CoderPadClient,
    ) -> None:
        """Questions can be listed."""
        result = fixture_coderpad_client.questions.list()
        assert isinstance(result, PaginatedList)

    @staticmethod
    def test_list_questions_with_params(
        fixture_coderpad_client: CoderPadClient,
    ) -> None:
        """Questions can be listed with sort and page."""
        result = fixture_coderpad_client.questions.list(
            sort=SortOrder.UPDATED_AT_DESC,
            page=1,
        )
        assert isinstance(result, PaginatedList)


class TestCreateQuestion:
    """Tests for ``CoderPadClient.questions.create``."""

    @staticmethod
    def test_create_question(
        fixture_coderpad_client: CoderPadClient,
    ) -> None:
        """A question can be created."""
        result = fixture_coderpad_client.questions.create(
            title="Test Question",
            language="python",
        )
        assert result.id

    @staticmethod
    def test_create_question_all_params(
        fixture_coderpad_client: CoderPadClient,
    ) -> None:
        """A question can be created with all parameters."""
        result = fixture_coderpad_client.questions.create(
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
        fixture_coderpad_client: CoderPadClient,
    ) -> None:
        """A question can be retrieved by id."""
        result = fixture_coderpad_client.questions.get(
            question_id="123",
        )
        assert result.id


class TestUpdateQuestion:
    """Tests for ``CoderPadClient.questions.update``."""

    @staticmethod
    def test_update_question(
        fixture_coderpad_client: CoderPadClient,
    ) -> None:
        """A question can be updated."""
        fixture_coderpad_client.questions.update(
            question_id="123",
            title="Updated Question",
        )

    @staticmethod
    def test_update_question_no_title(
        fixture_coderpad_client: CoderPadClient,
    ) -> None:
        """A question can be updated without a title."""
        fixture_coderpad_client.questions.update(
            question_id="123",
            language="ruby",
        )

    @staticmethod
    def test_update_question_all_params(
        fixture_coderpad_client: CoderPadClient,
    ) -> None:
        """A question can be updated with all parameters."""
        fixture_coderpad_client.questions.update(
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
        fixture_coderpad_client: CoderPadClient,
    ) -> None:
        """A question can be deleted."""
        fixture_coderpad_client.questions.delete(
            question_id="123",
        )


class TestGetQuota:
    """Tests for ``CoderPadClient.organization.get_quota``."""

    @staticmethod
    def test_get_quota(
        fixture_coderpad_client: CoderPadClient,
    ) -> None:
        """Quota information can be retrieved."""
        result = fixture_coderpad_client.organization.get_quota()
        assert result.pads_used >= 0


class TestGetOrganization:
    """Tests for ``CoderPadClient.organization.get``."""

    @staticmethod
    def test_get_organization(
        fixture_coderpad_client: CoderPadClient,
    ) -> None:
        """Organization information can be retrieved."""
        result = fixture_coderpad_client.organization.get()
        assert result.organization_name


class TestGetOrganizationStats:
    """Tests for ``CoderPadClient.organization.get_stats``."""

    @staticmethod
    def test_get_organization_stats(
        fixture_coderpad_client: CoderPadClient,
    ) -> None:
        """Organization stats can be retrieved."""
        result = fixture_coderpad_client.organization.get_stats()
        assert result.pads_created >= 0

    @staticmethod
    def test_get_organization_stats_with_params(
        fixture_coderpad_client: CoderPadClient,
    ) -> None:
        """Organization stats can be filtered by time range."""
        result = fixture_coderpad_client.organization.get_stats(
            start_time="2023-07-01T00:00:00Z",
            end_time="2023-07-31T00:00:00Z",
        )
        assert result.pads_created >= 0


class TestListOrganizationPads:
    """Tests for ``CoderPadClient.organization.pads.list``."""

    @staticmethod
    def test_list_organization_pads(
        fixture_coderpad_client: CoderPadClient,
    ) -> None:
        """Organization pads can be listed."""
        result = fixture_coderpad_client.organization.pads.list()
        assert isinstance(result, PaginatedList)

    @staticmethod
    def test_list_organization_pads_with_params(
        fixture_coderpad_client: CoderPadClient,
    ) -> None:
        """Organization pads can be listed with optional arguments."""
        result = fixture_coderpad_client.organization.pads.list(
            sort=SortOrder.UPDATED_AT_ASC,
            page=1,
        )
        assert isinstance(result, PaginatedList)


class TestListOrganizationQuestions:
    """Tests for ``CoderPadClient.organization.questions.list``."""

    @staticmethod
    def test_list_organization_questions(
        fixture_coderpad_client: CoderPadClient,
    ) -> None:
        """Organization questions can be listed."""
        result = fixture_coderpad_client.organization.questions.list()
        assert isinstance(result, PaginatedList)

    @staticmethod
    def test_list_organization_questions_with_params(
        fixture_coderpad_client: CoderPadClient,
    ) -> None:
        """Organization questions can be listed with optional
        arguments.
        """
        result = fixture_coderpad_client.organization.questions.list(
            sort=SortOrder.CREATED_AT_DESC,
            page=1,
        )
        assert isinstance(result, PaginatedList)
