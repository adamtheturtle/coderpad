"""Tests for the async CoderPad client."""

from http import HTTPStatus
from pathlib import Path

import pytest

from coderpad_api.async_client import AsyncCoderPadClient
from coderpad_api.exceptions import NotFoundError
from coderpad_api.transports import (
    AsyncHTTPXTransport,
    AsyncTransport,
    TransportResponse,
)
from coderpad_api.types import QuestionFileContent, SortOrder


class TestAsyncCoderPadClient:
    """Tests for ``AsyncCoderPadClient``."""

    @staticmethod
    def test_default_base_url() -> None:
        """The default base URL is the CoderPad Interview API."""
        client = AsyncCoderPadClient(api_key="test-key")
        assert client.base_url == "https://api.interview.coderpad.io"

    @staticmethod
    def test_custom_base_url() -> None:
        """A custom base URL can be provided."""
        client = AsyncCoderPadClient(
            api_key="test-key",
            base_url="https://custom.example.com",
        )
        assert client.base_url == "https://custom.example.com"

    @staticmethod
    @pytest.mark.asyncio
    async def test_custom_transport(
        mock_coderpad_api: object,
    ) -> None:
        """A custom transport can be provided."""
        del mock_coderpad_api
        transport = AsyncHTTPXTransport()
        client = AsyncCoderPadClient(
            api_key="test-key",
            transport=transport,
        )
        result = await client.pads.list()
        assert result.total >= 0

    @staticmethod
    @pytest.mark.asyncio
    async def test_mock_api_available(
        async_coderpad_client: AsyncCoderPadClient,
    ) -> None:
        """The mock API fixture provides a working mock."""
        result = await async_coderpad_client.pads.list()
        assert result.total >= 0

    @staticmethod
    @pytest.mark.asyncio
    async def test_aclose() -> None:
        """The client can be closed."""
        client = AsyncCoderPadClient(api_key="test-key")
        await client.aclose()

    @staticmethod
    @pytest.mark.asyncio
    async def test_async_context_manager() -> None:
        """The client can be used as an async context manager."""
        async with AsyncCoderPadClient(
            api_key="test-key",
        ) as client:
            assert isinstance(client, AsyncCoderPadClient)

    @staticmethod
    @pytest.mark.asyncio
    async def test_close_transport_without_aclose() -> None:
        """Closing works when transport has no aclose."""

        class _NoCloseTransport:
            """A transport without an aclose method."""

            async def __call__(
                self,
                *,
                method: str,
                url: str,
                headers: dict[str, str],
                params: (dict[str, str | int] | None) = None,
                data: dict[str, str] | None = None,
                files: (dict[str, tuple[str, bytes, str]] | None) = None,
            ) -> TransportResponse:  # pragma: no cover
                """Make a request."""
                raise NotImplementedError

        client = AsyncCoderPadClient(
            api_key="test-key",
            transport=_NoCloseTransport(),
        )
        await client.aclose()


class TestAsyncHTTPXTransport:
    """Tests for ``AsyncHTTPXTransport``."""

    @staticmethod
    def test_is_async_transport() -> None:
        """AsyncHTTPXTransport satisfies AsyncTransport."""
        assert isinstance(
            AsyncHTTPXTransport(),
            AsyncTransport,
        )

    @staticmethod
    @pytest.mark.asyncio
    async def test_aclose() -> None:
        """The transport can be closed."""
        transport = AsyncHTTPXTransport()
        await transport.aclose()

    @staticmethod
    @pytest.mark.asyncio
    async def test_async_context_manager() -> None:
        """The transport can be used as an async context manager."""
        async with AsyncHTTPXTransport() as transport:
            assert isinstance(
                transport,
                AsyncHTTPXTransport,
            )


class TestAsyncListPads:
    """Tests for ``AsyncCoderPadClient.pads.list``."""

    @staticmethod
    @pytest.mark.asyncio
    async def test_list_pads(
        async_coderpad_client: AsyncCoderPadClient,
    ) -> None:
        """Pads can be listed."""
        result = await async_coderpad_client.pads.list()
        assert result.total >= 0

    @staticmethod
    @pytest.mark.asyncio
    async def test_list_pads_with_sort(
        async_coderpad_client: AsyncCoderPadClient,
    ) -> None:
        """Pads can be listed with a sort parameter."""
        result = await async_coderpad_client.pads.list(
            sort=SortOrder.UPDATED_AT_DESC,
        )
        assert result.total >= 0

    @staticmethod
    @pytest.mark.asyncio
    async def test_list_pads_with_page(
        async_coderpad_client: AsyncCoderPadClient,
    ) -> None:
        """Pads can be listed with a page parameter."""
        result = await async_coderpad_client.pads.list(
            page=2,
        )
        assert result.total >= 0


class TestAsyncCreatePad:
    """Tests for ``AsyncCoderPadClient.pads.create``."""

    @staticmethod
    @pytest.mark.asyncio
    async def test_create_pad(
        async_coderpad_client: AsyncCoderPadClient,
    ) -> None:
        """A pad can be created."""
        result = await async_coderpad_client.pads.create(
            title="Test Pad",
            language="python",
        )
        assert result.id

    @staticmethod
    @pytest.mark.asyncio
    async def test_create_pad_all_params(
        async_coderpad_client: AsyncCoderPadClient,
    ) -> None:
        """A pad can be created with all parameters."""
        result = await async_coderpad_client.pads.create(
            title="Test Pad",
            language="python",
            contents="print('hello')",
            notes="Private notes",
        )
        assert result.id

    @staticmethod
    @pytest.mark.asyncio
    async def test_create_pad_minimal(
        async_coderpad_client: AsyncCoderPadClient,
    ) -> None:
        """A pad can be created with no parameters."""
        result = await async_coderpad_client.pads.create()
        assert result.id


class TestAsyncGetPad:
    """Tests for ``AsyncCoderPadClient.pads.get``."""

    @staticmethod
    @pytest.mark.asyncio
    async def test_get_pad(
        async_coderpad_client: AsyncCoderPadClient,
    ) -> None:
        """A pad can be retrieved by id."""
        result = await async_coderpad_client.pads.get(
            pad_id="ABC1234",
        )
        assert result.id


class TestAsyncUpdatePad:
    """Tests for ``AsyncCoderPadClient.pads.update``."""

    @staticmethod
    @pytest.mark.asyncio
    async def test_update_pad(
        async_coderpad_client: AsyncCoderPadClient,
    ) -> None:
        """A pad can be updated."""
        await async_coderpad_client.pads.update(
            pad_id="ABC1234",
            title="Updated Title",
        )

    @staticmethod
    @pytest.mark.asyncio
    async def test_update_pad_no_title(
        async_coderpad_client: AsyncCoderPadClient,
    ) -> None:
        """A pad can be updated without a title."""
        await async_coderpad_client.pads.update(
            pad_id="ABC1234",
            language="python",
        )

    @staticmethod
    @pytest.mark.asyncio
    async def test_update_pad_all_params(
        async_coderpad_client: AsyncCoderPadClient,
    ) -> None:
        """A pad can be updated with all parameters."""
        await async_coderpad_client.pads.update(
            pad_id="ABC1234",
            title="Updated Title",
            language="python",
            contents="print('hello')",
            notes="Notes",
            ended=True,
            deleted=False,
        )


class TestAsyncGetPadEvents:
    """Tests for ``AsyncCoderPadClient.pads.get_events``."""

    @staticmethod
    @pytest.mark.asyncio
    async def test_get_pad_events(
        async_coderpad_client: AsyncCoderPadClient,
    ) -> None:
        """Pad events can be retrieved."""
        result = await async_coderpad_client.pads.get_events(
            pad_id="ABC1234",
        )
        assert result.total >= 0

    @staticmethod
    @pytest.mark.asyncio
    async def test_get_pad_events_with_params(
        async_coderpad_client: AsyncCoderPadClient,
    ) -> None:
        """Pad events can be retrieved with sort and page."""
        result = await async_coderpad_client.pads.get_events(
            pad_id="ABC1234",
            sort=SortOrder.CREATED_AT_ASC,
            page=1,
        )
        assert result.total >= 0


class TestAsyncGetPadEnvironment:
    """Tests for ``AsyncCoderPadClient.pads.get_environment``."""

    @staticmethod
    @pytest.mark.asyncio
    async def test_get_pad_environment(
        async_coderpad_client: AsyncCoderPadClient,
    ) -> None:
        """A pad environment can be retrieved."""
        result = await async_coderpad_client.pads.get_environment(
            environment_id="123",
        )
        assert result.id


class TestAsyncListQuestions:
    """Tests for ``AsyncCoderPadClient.questions.list``."""

    @staticmethod
    @pytest.mark.asyncio
    async def test_list_questions(
        async_coderpad_client: AsyncCoderPadClient,
    ) -> None:
        """Questions can be listed."""
        result = await async_coderpad_client.questions.list()
        assert result.total >= 0

    @staticmethod
    @pytest.mark.asyncio
    async def test_list_questions_with_params(
        async_coderpad_client: AsyncCoderPadClient,
    ) -> None:
        """Questions can be listed with sort and page."""
        result = await async_coderpad_client.questions.list(
            sort=SortOrder.UPDATED_AT_DESC,
            page=1,
        )
        assert result.total >= 0


class TestAsyncCreateQuestion:
    """Tests for ``AsyncCoderPadClient.questions.create``."""

    @staticmethod
    @pytest.mark.asyncio
    async def test_create_question(
        async_coderpad_client: AsyncCoderPadClient,
    ) -> None:
        """A question can be created."""
        result = await async_coderpad_client.questions.create(
            title="Test Question",
            language="python",
        )
        assert result.id

    @staticmethod
    @pytest.mark.asyncio
    async def test_create_question_all_params(
        async_coderpad_client: AsyncCoderPadClient,
    ) -> None:
        """A question can be created with all parameters."""
        result = await async_coderpad_client.questions.create(
            title="Test Question",
            language="python",
            description="A description",
            contents="def solve(): pass",
            solution="def solve(): return 42",
        )
        assert result.id

    @staticmethod
    @pytest.mark.asyncio
    async def test_create_question_with_file_contents(
        async_coderpad_client: AsyncCoderPadClient,
    ) -> None:
        """A question can be created with file contents."""
        result = await async_coderpad_client.questions.create(
            title="Multi-file Question",
            language="multifile_python",
            file_contents=[
                QuestionFileContent(
                    path="main.py",
                    contents="print('hello')",
                ),
                QuestionFileContent(
                    path="lib/utils.py",
                    contents="def helper(): pass",
                ),
            ],
        )
        assert result.id

    @staticmethod
    @pytest.mark.asyncio
    async def test_create_question_with_zip_file(
        async_coderpad_client: AsyncCoderPadClient,
        tmp_path: Path,
    ) -> None:
        """A question can be created with a zip file."""
        zip_path = tmp_path / "project.zip"
        zip_path.write_bytes(data=b"PK\x03\x04fake-zip")
        result = await async_coderpad_client.questions.create(
            title="Zip Question",
            language="multifile_java",
            zip_file=zip_path,
        )
        assert result.id

    @staticmethod
    @pytest.mark.asyncio
    async def test_create_file_contents_with_contents_error() -> None:
        """Combining file_contents with contents raises ValueError."""
        client = AsyncCoderPadClient(api_key="test-key")
        with pytest.raises(
            expected_exception=ValueError,
            match="Cannot combine 'file_contents' with 'contents'",
        ):
            await client.questions.create(
                title="Test",
                language="python",
                contents="print('hi')",
                file_contents=[
                    QuestionFileContent(
                        path="main.py",
                        contents="print('hi')",
                    ),
                ],
            )

    @staticmethod
    @pytest.mark.asyncio
    async def test_create_file_contents_with_zip_file_error(
        tmp_path: Path,
    ) -> None:
        """Combining file_contents with zip_file raises ValueError."""
        client = AsyncCoderPadClient(api_key="test-key")
        zip_path = tmp_path / "project.zip"
        zip_path.write_bytes(data=b"PK\x03\x04fake-zip")
        with pytest.raises(
            expected_exception=ValueError,
            match="Cannot combine 'file_contents' with 'zip_file'",
        ):
            await client.questions.create(
                title="Test",
                language="python",
                file_contents=[
                    QuestionFileContent(
                        path="main.py",
                        contents="print('hi')",
                    ),
                ],
                zip_file=zip_path,
            )


class TestAsyncGetQuestion:
    """Tests for ``AsyncCoderPadClient.questions.get``."""

    @staticmethod
    @pytest.mark.asyncio
    async def test_get_question(
        async_coderpad_client: AsyncCoderPadClient,
    ) -> None:
        """A question can be retrieved by id."""
        result = await async_coderpad_client.questions.get(
            question_id="123",
        )
        assert result.id


class TestAsyncUpdateQuestion:
    """Tests for ``AsyncCoderPadClient.questions.update``."""

    @staticmethod
    @pytest.mark.asyncio
    async def test_update_question(
        async_coderpad_client: AsyncCoderPadClient,
    ) -> None:
        """A question can be updated."""
        await async_coderpad_client.questions.update(
            question_id="123",
            title="Updated Question",
        )

    @staticmethod
    @pytest.mark.asyncio
    async def test_update_question_no_title(
        async_coderpad_client: AsyncCoderPadClient,
    ) -> None:
        """A question can be updated without a title."""
        await async_coderpad_client.questions.update(
            question_id="123",
            language="ruby",
        )

    @staticmethod
    @pytest.mark.asyncio
    async def test_update_question_all_params(
        async_coderpad_client: AsyncCoderPadClient,
    ) -> None:
        """A question can be updated with all params."""
        await async_coderpad_client.questions.update(
            question_id="123",
            title="Updated",
            language="ruby",
            description="New desc",
            contents="puts 'hi'",
            solution="puts 'answer'",
        )

    @staticmethod
    @pytest.mark.asyncio
    async def test_update_question_with_file_contents(
        async_coderpad_client: AsyncCoderPadClient,
    ) -> None:
        """A question can be updated with file contents."""
        await async_coderpad_client.questions.update(
            question_id="123",
            file_contents=[
                QuestionFileContent(
                    path="main.py",
                    contents="print('updated')",
                ),
            ],
        )

    @staticmethod
    @pytest.mark.asyncio
    async def test_update_question_with_zip_file(
        async_coderpad_client: AsyncCoderPadClient,
        tmp_path: Path,
    ) -> None:
        """A question can be updated with a zip file."""
        zip_path = tmp_path / "project.zip"
        zip_path.write_bytes(data=b"PK\x03\x04fake-zip")
        await async_coderpad_client.questions.update(
            question_id="123",
            zip_file=zip_path,
        )

    @staticmethod
    @pytest.mark.asyncio
    async def test_update_file_contents_with_contents_error() -> None:
        """Combining file_contents with contents raises ValueError."""
        client = AsyncCoderPadClient(api_key="test-key")
        with pytest.raises(
            expected_exception=ValueError,
            match="Cannot combine 'file_contents' with 'contents'",
        ):
            await client.questions.update(
                question_id="123",
                contents="print('hi')",
                file_contents=[
                    QuestionFileContent(
                        path="main.py",
                        contents="print('hi')",
                    ),
                ],
            )

    @staticmethod
    @pytest.mark.asyncio
    async def test_update_file_contents_with_zip_file_error(
        tmp_path: Path,
    ) -> None:
        """Combining file_contents with zip_file raises ValueError."""
        client = AsyncCoderPadClient(api_key="test-key")
        zip_path = tmp_path / "project.zip"
        zip_path.write_bytes(data=b"PK\x03\x04fake-zip")
        with pytest.raises(
            expected_exception=ValueError,
            match="Cannot combine 'file_contents' with 'zip_file'",
        ):
            await client.questions.update(
                question_id="123",
                file_contents=[
                    QuestionFileContent(
                        path="main.py",
                        contents="print('hi')",
                    ),
                ],
                zip_file=zip_path,
            )


class TestAsyncDeleteQuestion:
    """Tests for ``AsyncCoderPadClient.questions.delete``."""

    @staticmethod
    @pytest.mark.asyncio
    async def test_delete_question(
        async_coderpad_client: AsyncCoderPadClient,
    ) -> None:
        """A question can be deleted."""
        await async_coderpad_client.questions.delete(
            question_id="123",
        )


class TestAsyncGetQuota:
    """Tests for ``AsyncCoderPadClient.organization.get_quota``."""

    @staticmethod
    @pytest.mark.asyncio
    async def test_get_quota(
        async_coderpad_client: AsyncCoderPadClient,
    ) -> None:
        """Quota information can be retrieved."""
        result = await async_coderpad_client.organization.get_quota()
        assert result.pads_used >= 0


class TestAsyncGetOrganization:
    """Tests for ``AsyncCoderPadClient.organization.get``."""

    @staticmethod
    @pytest.mark.asyncio
    async def test_get_organization(
        async_coderpad_client: AsyncCoderPadClient,
    ) -> None:
        """Organization information can be retrieved."""
        result = await async_coderpad_client.organization.get()
        assert result.organization_name


class TestAsyncGetOrganizationStats:
    """Tests for ``AsyncCoderPadClient.organization.get_stats``."""

    @staticmethod
    @pytest.mark.asyncio
    async def test_get_organization_stats(
        async_coderpad_client: AsyncCoderPadClient,
    ) -> None:
        """Organization stats can be retrieved."""
        result = await async_coderpad_client.organization.get_stats()
        assert result.pads_created >= 0

    @staticmethod
    @pytest.mark.asyncio
    async def test_get_organization_stats_with_params(
        async_coderpad_client: AsyncCoderPadClient,
    ) -> None:
        """Organization stats can be filtered by time."""
        result = await async_coderpad_client.organization.get_stats(
            start_time="2023-07-01T00:00:00Z",
            end_time="2023-07-31T00:00:00Z",
        )
        assert result.pads_created >= 0


class TestAsyncListOrganizationPads:
    """Tests for organization pads list."""

    @staticmethod
    @pytest.mark.asyncio
    async def test_list_organization_pads(
        async_coderpad_client: AsyncCoderPadClient,
    ) -> None:
        """Organization pads can be listed."""
        result = await async_coderpad_client.organization.pads.list()
        assert result.total >= 0

    @staticmethod
    @pytest.mark.asyncio
    async def test_list_organization_pads_with_params(
        async_coderpad_client: AsyncCoderPadClient,
    ) -> None:
        """Organization pads can be listed with optional arguments."""
        result = await async_coderpad_client.organization.pads.list(
            sort=SortOrder.UPDATED_AT_ASC,
            page=1,
        )
        assert result.total >= 0


class TestAsyncListOrganizationQuestions:
    """Tests for organization questions list."""

    @staticmethod
    @pytest.mark.asyncio
    async def test_list_organization_questions(
        async_coderpad_client: AsyncCoderPadClient,
    ) -> None:
        """Organization questions can be listed."""
        result = await async_coderpad_client.organization.questions.list()
        assert result.total >= 0

    @staticmethod
    @pytest.mark.asyncio
    async def test_list_org_questions_with_params(
        async_coderpad_client: AsyncCoderPadClient,
    ) -> None:
        """Organization questions can be listed with optional
        arguments.
        """
        result = await async_coderpad_client.organization.questions.list(
            sort=SortOrder.CREATED_AT_DESC,
            page=1,
        )
        assert result.total >= 0


class TestAsyncExceptionHandling:
    """Tests for async exception handling."""

    @staticmethod
    @pytest.mark.asyncio
    async def test_client_raises_specific_exception() -> None:
        """The async client raises specific exceptions."""

        async def _error_transport(
            *,
            method: str,
            url: str,
            headers: dict[str, str],
            params: (dict[str, str | int] | None) = None,
            data: dict[str, str] | None = None,
            files: (dict[str, tuple[str, bytes, str]] | None) = None,
        ) -> TransportResponse:
            """Return a 404 response."""
            del method, url, headers, params, data, files
            return TransportResponse(
                status_code=HTTPStatus.NOT_FOUND,
                headers={},
                content=b"Not Found",
            )

        client = AsyncCoderPadClient(
            api_key="test-key",
            transport=_error_transport,
        )
        with pytest.raises(
            expected_exception=NotFoundError,
        ):
            await client.pads.get(pad_id="nonexistent")
