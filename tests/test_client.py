"""Tests for the CoderPad client."""

import respx

from coderpad_api.client import CoderPadClient
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
    def test_mock_api_available(
        fixture_mock_coderpad_api: respx.MockRouter,
        fixture_coderpad_client: CoderPadClient,
    ) -> None:
        """The mock API fixture provides a working mock router."""
        assert fixture_mock_coderpad_api.calls.call_count == 0
        fixture_coderpad_client.list_pads()
        assert fixture_mock_coderpad_api.calls.call_count == 1


class TestListPads:
    """Tests for ``CoderPadClient.list_pads``."""

    @staticmethod
    def test_list_pads(
        fixture_coderpad_client: CoderPadClient,
    ) -> None:
        """Pads can be listed."""
        result = fixture_coderpad_client.list_pads()
        assert isinstance(result, list)

    @staticmethod
    def test_list_pads_with_sort(
        fixture_coderpad_client: CoderPadClient,
    ) -> None:
        """Pads can be listed with a sort parameter."""
        result = fixture_coderpad_client.list_pads(
            sort=SortOrder.UPDATED_AT_DESC,
        )
        assert isinstance(result, list)

    @staticmethod
    def test_list_pads_with_page(
        fixture_coderpad_client: CoderPadClient,
    ) -> None:
        """Pads can be listed with a page parameter."""
        result = fixture_coderpad_client.list_pads(page=2)
        assert isinstance(result, list)


class TestCreatePad:
    """Tests for ``CoderPadClient.create_pad``."""

    @staticmethod
    def test_create_pad(
        fixture_coderpad_client: CoderPadClient,
    ) -> None:
        """A pad can be created."""
        result = fixture_coderpad_client.create_pad(
            title="Test Pad",
            language="python",
        )
        assert result.id

    @staticmethod
    def test_create_pad_all_params(
        fixture_coderpad_client: CoderPadClient,
    ) -> None:
        """A pad can be created with all parameters."""
        result = fixture_coderpad_client.create_pad(
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
        result = fixture_coderpad_client.create_pad()
        assert result.id


class TestGetPad:
    """Tests for ``CoderPadClient.get_pad``."""

    @staticmethod
    def test_get_pad(
        fixture_coderpad_client: CoderPadClient,
    ) -> None:
        """A pad can be retrieved by id."""
        result = fixture_coderpad_client.get_pad(
            pad_id="ABC1234",
        )
        assert result.id


class TestUpdatePad:
    """Tests for ``CoderPadClient.update_pad``."""

    @staticmethod
    def test_update_pad(
        fixture_coderpad_client: CoderPadClient,
    ) -> None:
        """A pad can be updated."""
        fixture_coderpad_client.update_pad(
            pad_id="ABC1234",
            title="Updated Title",
        )

    @staticmethod
    def test_update_pad_no_title(
        fixture_coderpad_client: CoderPadClient,
    ) -> None:
        """A pad can be updated without a title."""
        fixture_coderpad_client.update_pad(
            pad_id="ABC1234",
            language="python",
        )

    @staticmethod
    def test_update_pad_all_params(
        fixture_coderpad_client: CoderPadClient,
    ) -> None:
        """A pad can be updated with all parameters."""
        fixture_coderpad_client.update_pad(
            pad_id="ABC1234",
            title="Updated Title",
            language="python",
            contents="print('hello')",
            notes="Notes",
            ended=True,
            deleted=False,
        )


class TestGetPadEvents:
    """Tests for ``CoderPadClient.get_pad_events``."""

    @staticmethod
    def test_get_pad_events(
        fixture_coderpad_client: CoderPadClient,
    ) -> None:
        """Pad events can be retrieved."""
        result = fixture_coderpad_client.get_pad_events(
            pad_id="ABC1234",
        )
        assert isinstance(result, list)

    @staticmethod
    def test_get_pad_events_with_params(
        fixture_coderpad_client: CoderPadClient,
    ) -> None:
        """Pad events can be retrieved with sort and page."""
        result = fixture_coderpad_client.get_pad_events(
            pad_id="ABC1234",
            sort=SortOrder.CREATED_AT_ASC,
            page=1,
        )
        assert isinstance(result, list)


class TestGetPadEnvironment:
    """Tests for ``CoderPadClient.get_pad_environment``."""

    @staticmethod
    def test_get_pad_environment(
        fixture_coderpad_client: CoderPadClient,
    ) -> None:
        """A pad environment can be retrieved."""
        result = fixture_coderpad_client.get_pad_environment(
            environment_id="123",
        )
        assert result.id


class TestListQuestions:
    """Tests for ``CoderPadClient.list_questions``."""

    @staticmethod
    def test_list_questions(
        fixture_coderpad_client: CoderPadClient,
    ) -> None:
        """Questions can be listed."""
        result = fixture_coderpad_client.list_questions()
        assert isinstance(result, list)

    @staticmethod
    def test_list_questions_with_params(
        fixture_coderpad_client: CoderPadClient,
    ) -> None:
        """Questions can be listed with sort and page."""
        result = fixture_coderpad_client.list_questions(
            sort=SortOrder.UPDATED_AT_DESC,
            page=1,
        )
        assert isinstance(result, list)


class TestCreateQuestion:
    """Tests for ``CoderPadClient.create_question``."""

    @staticmethod
    def test_create_question(
        fixture_coderpad_client: CoderPadClient,
    ) -> None:
        """A question can be created."""
        result = fixture_coderpad_client.create_question(
            title="Test Question",
            language="python",
        )
        assert result.id

    @staticmethod
    def test_create_question_all_params(
        fixture_coderpad_client: CoderPadClient,
    ) -> None:
        """A question can be created with all parameters."""
        result = fixture_coderpad_client.create_question(
            title="Test Question",
            language="python",
            description="A description",
            contents="def solve(): pass",
            solution="def solve(): return 42",
        )
        assert result.id


class TestGetQuestion:
    """Tests for ``CoderPadClient.get_question``."""

    @staticmethod
    def test_get_question(
        fixture_coderpad_client: CoderPadClient,
    ) -> None:
        """A question can be retrieved by id."""
        result = fixture_coderpad_client.get_question(
            question_id="123",
        )
        assert result.id


class TestUpdateQuestion:
    """Tests for ``CoderPadClient.update_question``."""

    @staticmethod
    def test_update_question(
        fixture_coderpad_client: CoderPadClient,
    ) -> None:
        """A question can be updated."""
        fixture_coderpad_client.update_question(
            question_id="123",
            title="Updated Question",
        )

    @staticmethod
    def test_update_question_no_title(
        fixture_coderpad_client: CoderPadClient,
    ) -> None:
        """A question can be updated without a title."""
        fixture_coderpad_client.update_question(
            question_id="123",
            language="ruby",
        )

    @staticmethod
    def test_update_question_all_params(
        fixture_coderpad_client: CoderPadClient,
    ) -> None:
        """A question can be updated with all parameters."""
        fixture_coderpad_client.update_question(
            question_id="123",
            title="Updated",
            language="ruby",
            description="New desc",
            contents="puts 'hi'",
            solution="puts 'answer'",
        )


class TestDeleteQuestion:
    """Tests for ``CoderPadClient.delete_question``."""

    @staticmethod
    def test_delete_question(
        fixture_coderpad_client: CoderPadClient,
    ) -> None:
        """A question can be deleted."""
        fixture_coderpad_client.delete_question(
            question_id="123",
        )


class TestGetQuota:
    """Tests for ``CoderPadClient.get_quota``."""

    @staticmethod
    def test_get_quota(
        fixture_coderpad_client: CoderPadClient,
    ) -> None:
        """Quota information can be retrieved."""
        result = fixture_coderpad_client.get_quota()
        assert result.pads_used >= 0


class TestGetOrganization:
    """Tests for ``CoderPadClient.get_organization``."""

    @staticmethod
    def test_get_organization(
        fixture_coderpad_client: CoderPadClient,
    ) -> None:
        """Organization information can be retrieved."""
        result = fixture_coderpad_client.get_organization()
        assert result.organization_name


class TestGetOrganizationStats:
    """Tests for ``CoderPadClient.get_organization_stats``."""

    @staticmethod
    def test_get_organization_stats(
        fixture_coderpad_client: CoderPadClient,
    ) -> None:
        """Organization stats can be retrieved."""
        result = fixture_coderpad_client.get_organization_stats()
        assert result.pads_created >= 0

    @staticmethod
    def test_get_organization_stats_with_params(
        fixture_coderpad_client: CoderPadClient,
    ) -> None:
        """Organization stats can be filtered by time range."""
        result = fixture_coderpad_client.get_organization_stats(
            start_time="2023-07-01T00:00:00Z",
            end_time="2023-07-31T00:00:00Z",
        )
        assert result.pads_created >= 0


class TestListOrganizationPads:
    """Tests for ``CoderPadClient.list_organization_pads``."""

    @staticmethod
    def test_list_organization_pads(
        fixture_coderpad_client: CoderPadClient,
    ) -> None:
        """Organization pads can be listed."""
        result = fixture_coderpad_client.list_organization_pads()
        assert isinstance(result, list)

    @staticmethod
    def test_list_organization_pads_with_params(
        fixture_coderpad_client: CoderPadClient,
    ) -> None:
        """Organization pads can be listed with optional arguments."""
        result = fixture_coderpad_client.list_organization_pads(
            sort=SortOrder.UPDATED_AT_ASC,
            page=1,
        )
        assert isinstance(result, list)


class TestListOrganizationQuestions:
    """Tests for ``CoderPadClient.list_organization_questions``."""

    @staticmethod
    def test_list_organization_questions(
        fixture_coderpad_client: CoderPadClient,
    ) -> None:
        """Organization questions can be listed."""
        result = fixture_coderpad_client.list_organization_questions()
        assert isinstance(result, list)

    @staticmethod
    def test_list_organization_questions_with_params(
        fixture_coderpad_client: CoderPadClient,
    ) -> None:
        """Organization questions can be listed with optional
        arguments.
        """
        result = fixture_coderpad_client.list_organization_questions(
            sort=SortOrder.CREATED_AT_DESC,
            page=1,
        )
        assert isinstance(result, list)
