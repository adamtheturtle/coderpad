"""Tests for the CoderPad client."""

from http import HTTPStatus
from pathlib import Path

import pytest

from coderpad.client import CoderPad
from coderpad.exceptions import (
    AuthenticationError,
    BadRequestError,
    CoderPadError,
    ForbiddenError,
    NotFoundError,
    RateLimitError,
    ServerError,
)
from coderpad.transports import (
    HTTPStatusError,
    HTTPXTransport,
    Transport,
    TransportResponse,
)
from coderpad.types import QuestionFileContent, SortOrder


class TestCoderPad:
    """Tests for ``CoderPad``."""

    @staticmethod
    def test_default_base_url() -> None:
        """The default base URL is the CoderPad Interview API."""
        client = CoderPad(api_key="test-key")
        assert client.base_url == "https://api.interview.coderpad.io"

    @staticmethod
    def test_custom_base_url() -> None:
        """A custom base URL can be provided."""
        client = CoderPad(
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
        client = CoderPad(
            api_key="test-key",
            transport=transport,
        )
        result = client.pads.list()
        assert result.total >= 0

    @staticmethod
    def test_mock_api_available(
        coderpad_client: CoderPad,
    ) -> None:
        """The mock API fixture provides a working mock router."""
        result = coderpad_client.pads.list()
        assert result.total >= 0

    @staticmethod
    def test_close() -> None:
        """The client can be closed."""
        client = CoderPad(api_key="test-key")
        client.close()

    @staticmethod
    def test_context_manager() -> None:
        """The client can be used as a context manager."""
        with CoderPad(api_key="test-key") as client:
            assert isinstance(client, CoderPad)

    @staticmethod
    def test_close_transport_without_close() -> None:
        """Closing works when the transport has no close method."""

        class _NoCloseTransport:
            """A transport without a close method."""

            def __call__(
                self,
                *,
                method: str,
                url: str,
                headers: dict[str, str],
                params: dict[str, str | int] | None = None,
                data: dict[str, str] | None = None,
                files: (dict[str, tuple[str, bytes, str]] | None) = None,
            ) -> TransportResponse:  # pragma: no cover
                """Make a request."""
                raise NotImplementedError

        client = CoderPad(
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
        error_content = b"Not Found"
        response = TransportResponse(
            status_code=HTTPStatus.NOT_FOUND,
            headers={},
            content=error_content,
        )
        with pytest.raises(expected_exception=HTTPStatusError) as exc_info:
            response.raise_for_status()
        assert exc_info.value.status_code == HTTPStatus.NOT_FOUND
        assert exc_info.value.content == error_content

    @staticmethod
    def test_raise_for_status_ok() -> None:
        """A success status code does not raise."""
        response = TransportResponse(
            status_code=HTTPStatus.OK,
            headers={},
            content=b"{}",
        )
        response.raise_for_status()


class TestExceptionHierarchy:
    """Tests for the custom exception hierarchy."""

    @staticmethod
    def test_bad_request() -> None:
        """A 400 response raises BadRequestError."""
        response = TransportResponse(
            status_code=HTTPStatus.BAD_REQUEST,
            headers={},
            content=b"Bad Request",
        )
        exc = CoderPadError.from_response(response=response)
        assert isinstance(exc, BadRequestError)
        assert exc.status_code == HTTPStatus.BAD_REQUEST
        assert exc.content == b"Bad Request"
        assert exc.response is response

    @staticmethod
    def test_authentication_error() -> None:
        """A 401 response raises AuthenticationError."""
        response = TransportResponse(
            status_code=HTTPStatus.UNAUTHORIZED,
            headers={},
            content=b"Unauthorized",
        )
        exc = CoderPadError.from_response(response=response)
        assert isinstance(exc, AuthenticationError)

    @staticmethod
    def test_forbidden_error() -> None:
        """A 403 response raises ForbiddenError."""
        response = TransportResponse(
            status_code=HTTPStatus.FORBIDDEN,
            headers={},
            content=b"Forbidden",
        )
        exc = CoderPadError.from_response(response=response)
        assert isinstance(exc, ForbiddenError)

    @staticmethod
    def test_not_found_error() -> None:
        """A 404 response raises NotFoundError."""
        response = TransportResponse(
            status_code=HTTPStatus.NOT_FOUND,
            headers={},
            content=b"Not Found",
        )
        exc = CoderPadError.from_response(response=response)
        assert isinstance(exc, NotFoundError)

    @staticmethod
    def test_rate_limit_error() -> None:
        """A 429 response raises RateLimitError."""
        response = TransportResponse(
            status_code=HTTPStatus.TOO_MANY_REQUESTS,
            headers={},
            content=b"Too Many Requests",
        )
        exc = CoderPadError.from_response(response=response)
        assert isinstance(exc, RateLimitError)

    @staticmethod
    def test_server_error() -> None:
        """A 500 response raises ServerError."""
        response = TransportResponse(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            headers={},
            content=b"Internal Server Error",
        )
        exc = CoderPadError.from_response(response=response)
        assert isinstance(exc, ServerError)

    @staticmethod
    def test_unmapped_status_code() -> None:
        """An unmapped status code raises CoderPadError."""
        response = TransportResponse(
            status_code=HTTPStatus.IM_A_TEAPOT,
            headers={},
            content=b"I'm a teapot",
        )
        exc = CoderPadError.from_response(response=response)
        assert isinstance(exc, CoderPadError)
        assert not isinstance(
            exc,
            (
                BadRequestError,
                AuthenticationError,
                ForbiddenError,
                NotFoundError,
                RateLimitError,
                ServerError,
            ),
        )
        assert exc.status_code == HTTPStatus.IM_A_TEAPOT

    @staticmethod
    def test_nonstandard_status_code() -> None:
        """A non-standard status code raises CoderPadError."""
        nonstandard_status = 999
        response = TransportResponse(
            status_code=nonstandard_status,
            headers={},
            content=b"Unknown",
        )
        exc = CoderPadError.from_response(response=response)
        assert isinstance(exc, CoderPadError)
        assert not isinstance(
            exc,
            (
                BadRequestError,
                AuthenticationError,
                ForbiddenError,
                NotFoundError,
                RateLimitError,
                ServerError,
            ),
        )
        assert exc.status_code == nonstandard_status

    @staticmethod
    def test_all_subclasses_are_coderpad_errors() -> None:
        """All specific exceptions are CoderPadError subclasses."""
        response = TransportResponse(
            status_code=HTTPStatus.NOT_FOUND,
            headers={},
            content=b"Not Found",
        )
        exc = CoderPadError.from_response(response=response)
        assert isinstance(exc, CoderPadError)

    @staticmethod
    def test_subclass_without_status_code() -> None:
        """A subclass without a status_code is not registered."""

        class _CustomError(CoderPadError):
            """A custom error without a mapped status code."""

        # Verify from_response never returns _CustomError for
        # any common status code.
        for code in (
            HTTPStatus.BAD_REQUEST,
            HTTPStatus.UNAUTHORIZED,
            HTTPStatus.FORBIDDEN,
            HTTPStatus.NOT_FOUND,
            HTTPStatus.IM_A_TEAPOT,
            HTTPStatus.TOO_MANY_REQUESTS,
            HTTPStatus.INTERNAL_SERVER_ERROR,
        ):
            response = TransportResponse(
                status_code=code,
                headers={},
                content=b"",
            )
            exc = CoderPadError.from_response(response=response)
            assert not isinstance(exc, _CustomError)

    @staticmethod
    def test_error_message() -> None:
        """The exception message includes the status code."""
        response = TransportResponse(
            status_code=HTTPStatus.NOT_FOUND,
            headers={},
            content=b"Not Found",
        )
        exc = CoderPadError.from_response(response=response)
        assert exc.args[0] == "HTTP 404"

    @staticmethod
    def test_client_raises_specific_exception() -> None:
        """The client raises specific exceptions for error responses."""

        def _error_transport(
            *,
            method: str,
            url: str,
            headers: dict[str, str],
            params: dict[str, str | int] | None = None,
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

        client = CoderPad(
            api_key="test-key",
            transport=_error_transport,
        )
        with pytest.raises(expected_exception=NotFoundError):
            client.pads.get(pad_id="nonexistent")


class TestListPads:
    """Tests for ``CoderPad.pads.list``."""

    @staticmethod
    def test_list_pads(
        coderpad_client: CoderPad,
    ) -> None:
        """Pads can be listed."""
        result = coderpad_client.pads.list()
        assert result.total >= 0

    @staticmethod
    def test_list_pads_with_sort(
        coderpad_client: CoderPad,
    ) -> None:
        """Pads can be listed with a sort parameter."""
        result = coderpad_client.pads.list(
            sort=SortOrder.UPDATED_AT_DESC,
        )
        assert result.total >= 0

    @staticmethod
    def test_list_pads_with_page(
        coderpad_client: CoderPad,
    ) -> None:
        """Pads can be listed with a page parameter."""
        result = coderpad_client.pads.list(page=2)
        assert result.total >= 0


class TestCreatePad:
    """Tests for ``CoderPad.pads.create``."""

    @staticmethod
    def test_create_pad(
        coderpad_client: CoderPad,
    ) -> None:
        """A pad can be created."""
        result = coderpad_client.pads.create(
            title="Test Pad",
            language="python",
        )
        assert result.id

    @staticmethod
    def test_create_pad_all_params(
        coderpad_client: CoderPad,
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
        coderpad_client: CoderPad,
    ) -> None:
        """A pad can be created with no parameters."""
        result = coderpad_client.pads.create()
        assert result.id


class TestGetPad:
    """Tests for ``CoderPad.pads.get``."""

    @staticmethod
    def test_get_pad(
        coderpad_client: CoderPad,
    ) -> None:
        """A pad can be retrieved by id."""
        result = coderpad_client.pads.get(
            pad_id="ABC1234",
        )
        assert result.id


class TestUpdatePad:
    """Tests for ``CoderPad.pads.update``."""

    @staticmethod
    def test_update_pad(
        coderpad_client: CoderPad,
    ) -> None:
        """A pad can be updated."""
        coderpad_client.pads.update(
            pad_id="ABC1234",
            title="Updated Title",
        )

    @staticmethod
    def test_update_pad_no_title(
        coderpad_client: CoderPad,
    ) -> None:
        """A pad can be updated without a title."""
        coderpad_client.pads.update(
            pad_id="ABC1234",
            language="python",
        )

    @staticmethod
    def test_update_pad_all_params(
        coderpad_client: CoderPad,
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
    """Tests for ``CoderPad.pads.get_events``."""

    @staticmethod
    def test_get_pad_events(
        coderpad_client: CoderPad,
    ) -> None:
        """Pad events can be retrieved."""
        result = coderpad_client.pads.get_events(
            pad_id="ABC1234",
        )
        assert result.total >= 0

    @staticmethod
    def test_get_pad_events_with_params(
        coderpad_client: CoderPad,
    ) -> None:
        """Pad events can be retrieved with sort and page."""
        result = coderpad_client.pads.get_events(
            pad_id="ABC1234",
            sort=SortOrder.CREATED_AT_ASC,
            page=1,
        )
        assert result.total >= 0


class TestGetPadEnvironment:
    """Tests for ``CoderPad.pads.get_environment``."""

    @staticmethod
    def test_get_pad_environment(
        coderpad_client: CoderPad,
    ) -> None:
        """A pad environment can be retrieved."""
        result = coderpad_client.pads.get_environment(
            environment_id="123",
        )
        assert result.id


class TestListQuestions:
    """Tests for ``CoderPad.questions.list``."""

    @staticmethod
    def test_list_questions(
        coderpad_client: CoderPad,
    ) -> None:
        """Questions can be listed."""
        result = coderpad_client.questions.list()
        assert result.total >= 0

    @staticmethod
    def test_list_questions_with_params(
        coderpad_client: CoderPad,
    ) -> None:
        """Questions can be listed with sort and page."""
        result = coderpad_client.questions.list(
            sort=SortOrder.UPDATED_AT_DESC,
            page=1,
        )
        assert result.total >= 0


class TestCreateQuestion:
    """Tests for ``CoderPad.questions.create``."""

    @staticmethod
    def test_create_question(
        coderpad_client: CoderPad,
    ) -> None:
        """A question can be created."""
        result = coderpad_client.questions.create(
            title="Test Question",
            language="python",
        )
        assert result.id

    @staticmethod
    def test_create_question_all_params(
        coderpad_client: CoderPad,
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

    @staticmethod
    def test_create_question_with_file_contents(
        coderpad_client: CoderPad,
    ) -> None:
        """A question can be created with file contents."""
        result = coderpad_client.questions.create(
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
    def test_create_question_with_zip_file(
        coderpad_client: CoderPad,
        tmp_path: Path,
    ) -> None:
        """A question can be created with a zip file."""
        zip_path = tmp_path / "project.zip"
        zip_path.write_bytes(data=b"PK\x03\x04fake-zip")
        result = coderpad_client.questions.create(
            title="Zip Question",
            language="multifile_java",
            zip_file=zip_path,
        )
        assert result.id


class TestGetQuestion:
    """Tests for ``CoderPad.questions.get``."""

    @staticmethod
    def test_get_question(
        coderpad_client: CoderPad,
    ) -> None:
        """A question can be retrieved by id."""
        result = coderpad_client.questions.get(
            question_id="123",
        )
        assert result.id


class TestUpdateQuestion:
    """Tests for ``CoderPad.questions.update``."""

    @staticmethod
    def test_update_question(
        coderpad_client: CoderPad,
    ) -> None:
        """A question can be updated."""
        coderpad_client.questions.update(
            question_id="123",
            title="Updated Question",
        )

    @staticmethod
    def test_update_question_no_title(
        coderpad_client: CoderPad,
    ) -> None:
        """A question can be updated without a title."""
        coderpad_client.questions.update(
            question_id="123",
            language="ruby",
        )

    @staticmethod
    def test_update_question_all_params(
        coderpad_client: CoderPad,
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

    @staticmethod
    def test_update_question_with_file_contents(
        coderpad_client: CoderPad,
    ) -> None:
        """A question can be updated with file contents."""
        coderpad_client.questions.update(
            question_id="123",
            file_contents=[
                QuestionFileContent(
                    path="main.py",
                    contents="print('updated')",
                ),
            ],
        )

    @staticmethod
    def test_update_question_with_zip_file(
        coderpad_client: CoderPad,
        tmp_path: Path,
    ) -> None:
        """A question can be updated with a zip file."""
        zip_path = tmp_path / "project.zip"
        zip_path.write_bytes(data=b"PK\x03\x04fake-zip")
        coderpad_client.questions.update(
            question_id="123",
            zip_file=zip_path,
        )


class TestDeleteQuestion:
    """Tests for ``CoderPad.questions.delete``."""

    @staticmethod
    def test_delete_question(
        coderpad_client: CoderPad,
    ) -> None:
        """A question can be deleted."""
        coderpad_client.questions.delete(
            question_id="123",
        )


class TestGetQuota:
    """Tests for ``CoderPad.organization.get_quota``."""

    @staticmethod
    def test_get_quota(
        coderpad_client: CoderPad,
    ) -> None:
        """Quota information can be retrieved."""
        result = coderpad_client.organization.get_quota()
        assert result.pads_used >= 0


class TestGetOrganization:
    """Tests for ``CoderPad.organization.get``."""

    @staticmethod
    def test_get_organization(
        coderpad_client: CoderPad,
    ) -> None:
        """Organization information can be retrieved."""
        result = coderpad_client.organization.get()
        assert result.organization_name


class TestGetOrganizationStats:
    """Tests for ``CoderPad.organization.get_stats``."""

    @staticmethod
    def test_get_organization_stats(
        coderpad_client: CoderPad,
    ) -> None:
        """Organization stats can be retrieved."""
        result = coderpad_client.organization.get_stats()
        assert result.pads_created >= 0

    @staticmethod
    def test_get_organization_stats_with_params(
        coderpad_client: CoderPad,
    ) -> None:
        """Organization stats can be filtered by time range."""
        result = coderpad_client.organization.get_stats(
            start_time="2023-07-01T00:00:00Z",
            end_time="2023-07-31T00:00:00Z",
        )
        assert result.pads_created >= 0


class TestListOrganizationPads:
    """Tests for ``CoderPad.organization.pads.list``."""

    @staticmethod
    def test_list_organization_pads(
        coderpad_client: CoderPad,
    ) -> None:
        """Organization pads can be listed."""
        result = coderpad_client.organization.pads.list()
        assert result.total >= 0

    @staticmethod
    def test_list_organization_pads_with_params(
        coderpad_client: CoderPad,
    ) -> None:
        """Organization pads can be listed with optional arguments."""
        result = coderpad_client.organization.pads.list(
            sort=SortOrder.UPDATED_AT_ASC,
            page=1,
        )
        assert result.total >= 0


class TestListOrganizationQuestions:
    """Tests for ``CoderPad.organization.questions.list``."""

    @staticmethod
    def test_list_organization_questions(
        coderpad_client: CoderPad,
    ) -> None:
        """Organization questions can be listed."""
        result = coderpad_client.organization.questions.list()
        assert result.total >= 0

    @staticmethod
    def test_list_organization_questions_with_params(
        coderpad_client: CoderPad,
    ) -> None:
        """Organization questions can be listed with optional
        arguments.
        """
        result = coderpad_client.organization.questions.list(
            sort=SortOrder.CREATED_AT_DESC,
            page=1,
        )
        assert result.total >= 0
