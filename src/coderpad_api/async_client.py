"""Async CoderPad Interview API client."""

from __future__ import annotations

from http import HTTPStatus
from typing import Self

from beartype import beartype

from coderpad_api.exceptions import CoderPadError
from coderpad_api.transports import (
    AsyncHTTPXTransport,
    AsyncTransport,
    TransportResponse,
)
from coderpad_api.types import (
    Organization,
    OrganizationStats,
    Pad,
    PadEnvironment,
    PadEvent,
    PaginatedList,
    Question,
    Quota,
    SortOrder,
)


@beartype
class _AsyncNamespace:
    """Base class providing shared async request logic."""

    def __init__(
        self,
        *,
        transport: AsyncTransport,
        base_url: str,
        headers: dict[str, str],
    ) -> None:
        """Create a new async namespace.

        Args:
            transport: The async HTTP transport.
            base_url: The base URL for the API.
            headers: Headers to send with every request.
        """
        self.transport = transport
        self.base_url = base_url
        self.headers = headers

    async def _request(
        self,
        *,
        method: str,
        url: str,
        params: dict[str, str | int] | None = None,
        data: dict[str, str] | None = None,
    ) -> TransportResponse:
        """Make an async HTTP request.

        Args:
            method: The HTTP method.
            url: The URL path.
            params: Query parameters.
            data: Form data.

        Returns:
            The transport response.

        Raises:
            CoderPadError: If the response has an error
                status code.
        """
        response = await self.transport(
            method=method,
            url=self.base_url + url,
            headers=self.headers,
            params=params,
            data=data,
        )
        if response.status_code >= HTTPStatus.BAD_REQUEST:
            raise CoderPadError.from_response(response=response)
        return response


@beartype
class AsyncPadsNamespace(_AsyncNamespace):
    """Namespace for async pad operations."""

    async def list(
        self,
        *,
        sort: SortOrder | None = None,
        page: int | None = None,
    ) -> PaginatedList[Pad]:
        """Retrieve a list of pads.

        Args:
            sort: Sort order.
            page: Page number for pagination.

        Returns:
            The list of pads with pagination metadata.
        """
        params: dict[str, str | int] = {}
        if sort is not None:
            params["sort"] = sort.value
        if page is not None:
            params["page"] = page
        response = await self._request(
            method="GET",
            url="/api/pads/",
            params=params,
        )
        data = response.json()
        return PaginatedList(
            [Pad.from_dict(data=item) for item in data["pads"]],
            total=data["total"],
            next_page=data.get("next_page"),
        )

    async def create(
        self,
        *,
        title: str | None = None,
        language: str | None = None,
        contents: str | None = None,
        notes: str | None = None,
    ) -> Pad:
        """Create a new pad.

        Args:
            title: Title for the pad.
            language: Programming language for the pad.
            contents: Initial contents of the pad editor.
            notes: Private notes for the interviewer.

        Returns:
            The created pad.
        """
        data: dict[str, str] = {}
        if title is not None:
            data["title"] = title
        if language is not None:
            data["language"] = language
        if contents is not None:
            data["contents"] = contents
        if notes is not None:
            data["notes"] = notes
        response = await self._request(
            method="POST",
            url="/api/pads/",
            data=data,
        )
        return Pad.from_dict(data=response.json())

    async def get(self, *, pad_id: str) -> Pad:
        """Retrieve a pad by id.

        Args:
            pad_id: The id of the pad.

        Returns:
            The pad.
        """
        response = await self._request(
            method="GET",
            url=f"/api/pads/{pad_id}",
        )
        return Pad.from_dict(data=response.json())

    async def update(
        self,
        *,
        pad_id: str,
        title: str | None = None,
        language: str | None = None,
        contents: str | None = None,
        notes: str | None = None,
        ended: bool | None = None,
        deleted: bool | None = None,
    ) -> None:
        """Modify an existing pad.

        Args:
            pad_id: The id of the pad.
            title: New title for the pad.
            language: New programming language.
            contents: New contents of the pad editor.
            notes: New private notes.
            ended: Set to ``True`` to end the interview.
            deleted: Set to ``True`` to delete the pad.
        """
        data: dict[str, str] = {}
        if title is not None:
            data["title"] = title
        if language is not None:
            data["language"] = language
        if contents is not None:
            data["contents"] = contents
        if notes is not None:
            data["notes"] = notes
        if ended is not None:
            data["ended"] = "true" if ended else "false"
        if deleted is not None:
            data["deleted"] = "true" if deleted else "false"
        await self._request(
            method="PUT",
            url=f"/api/pads/{pad_id}",
            data=data,
        )

    async def get_events(
        self,
        *,
        pad_id: str,
        sort: SortOrder | None = None,
        page: int | None = None,
    ) -> PaginatedList[PadEvent]:
        """Retrieve a list of pad events.

        Args:
            pad_id: The id of the pad.
            sort: Sort order.
            page: Page number for pagination.

        Returns:
            The list of pad events with pagination
            metadata.
        """
        params: dict[str, str | int] = {}
        if sort is not None:
            params["sort"] = sort.value
        if page is not None:
            params["page"] = page
        response = await self._request(
            method="GET",
            url=f"/api/pads/{pad_id}/events",
            params=params,
        )
        data = response.json()
        return PaginatedList(
            [PadEvent.from_dict(data=item) for item in data["events"]],
            total=data["total"],
            next_page=data.get("next_page"),
        )

    async def get_environment(
        self,
        *,
        environment_id: str,
    ) -> PadEnvironment:
        """Retrieve pad environment information.

        Args:
            environment_id: The id of the pad environment.

        Returns:
            The pad environment.
        """
        response = await self._request(
            method="GET",
            url=f"/api/pad_environments/{environment_id}",
        )
        return PadEnvironment.from_dict(
            data=response.json(),
        )


@beartype
class AsyncQuestionsNamespace(_AsyncNamespace):
    """Namespace for async question operations."""

    async def list(
        self,
        *,
        sort: SortOrder | None = None,
        page: int | None = None,
    ) -> PaginatedList[Question]:
        """Retrieve a list of questions.

        Args:
            sort: Sort order.
            page: Page number for pagination.

        Returns:
            The list of questions with pagination
            metadata.
        """
        params: dict[str, str | int] = {}
        if sort is not None:
            params["sort"] = sort.value
        if page is not None:
            params["page"] = page
        response = await self._request(
            method="GET",
            url="/api/questions/",
            params=params,
        )
        data = response.json()
        return PaginatedList(
            [Question.from_dict(data=item) for item in data["questions"]],
            total=data["total"],
            next_page=data.get("next_page"),
        )

    async def create(
        self,
        *,
        title: str,
        language: str,
        description: str | None = None,
        contents: str | None = None,
        solution: str | None = None,
    ) -> Question:
        """Create a new question.

        Args:
            title: Title for the question.
            language: Programming language for the
                question.
            description: Notes about the question.
            contents: Text inserted into the interview
                session.
            solution: The solution to the question.

        Returns:
            The created question.
        """
        data: dict[str, str] = {
            "title": title,
            "language": language,
        }
        if description is not None:
            data["description"] = description
        if contents is not None:
            data["contents"] = contents
        if solution is not None:
            data["solution"] = solution
        response = await self._request(
            method="POST",
            url="/api/questions/",
            data=data,
        )
        return Question.from_dict(
            data=response.json(),
        )

    async def get(
        self,
        *,
        question_id: str,
    ) -> Question:
        """Retrieve a question by id.

        Args:
            question_id: The id of the question.

        Returns:
            The question.
        """
        response = await self._request(
            method="GET",
            url=f"/api/questions/{question_id}",
        )
        return Question.from_dict(
            data=response.json(),
        )

    async def update(
        self,
        *,
        question_id: str,
        title: str | None = None,
        language: str | None = None,
        description: str | None = None,
        contents: str | None = None,
        solution: str | None = None,
    ) -> None:
        """Modify an existing question.

        Args:
            question_id: The id of the question.
            title: New title for the question.
            language: New programming language.
            description: New description.
            contents: New contents.
            solution: New solution.
        """
        data: dict[str, str] = {}
        if title is not None:
            data["title"] = title
        if language is not None:
            data["language"] = language
        if description is not None:
            data["description"] = description
        if contents is not None:
            data["contents"] = contents
        if solution is not None:
            data["solution"] = solution
        await self._request(
            method="PUT",
            url=f"/api/questions/{question_id}",
            data=data,
        )

    async def delete(
        self,
        *,
        question_id: str,
    ) -> None:
        """Delete a question.

        Args:
            question_id: The id of the question.
        """
        await self._request(
            method="DELETE",
            url=f"/api/questions/{question_id}",
        )


@beartype
class AsyncOrganizationPadsNamespace(_AsyncNamespace):
    """Namespace for async organization pad operations."""

    async def list(
        self,
        *,
        sort: SortOrder | None = None,
        page: int | None = None,
    ) -> PaginatedList[Pad]:
        """Retrieve pads for the entire organization.

        Args:
            sort: Sort order.
            page: Page number for pagination.

        Returns:
            The list of pads with pagination metadata.
        """
        params: dict[str, str | int] = {}
        if sort is not None:
            params["sort"] = sort.value
        if page is not None:
            params["page"] = page
        response = await self._request(
            method="GET",
            url="/api/organization/pads",
            params=params,
        )
        data = response.json()
        return PaginatedList(
            [Pad.from_dict(data=item) for item in data["pads"]],
            total=data["total"],
            next_page=data.get("next_page"),
        )


@beartype
class AsyncOrganizationQuestionsNamespace(
    _AsyncNamespace,
):
    """Namespace for async organization question
    operations.
    """

    async def list(
        self,
        *,
        sort: SortOrder | None = None,
        page: int | None = None,
    ) -> PaginatedList[Question]:
        """Retrieve questions for the entire organization.

        Args:
            sort: Sort order.
            page: Page number for pagination.

        Returns:
            The list of questions with pagination
            metadata.
        """
        params: dict[str, str | int] = {}
        if sort is not None:
            params["sort"] = sort.value
        if page is not None:
            params["page"] = page
        response = await self._request(
            method="GET",
            url="/api/organization/questions",
            params=params,
        )
        data = response.json()
        return PaginatedList(
            [Question.from_dict(data=item) for item in data["questions"]],
            total=data["total"],
            next_page=data.get("next_page"),
        )


@beartype
class AsyncOrganizationNamespace(_AsyncNamespace):
    """Namespace for async organization operations."""

    def __init__(
        self,
        *,
        transport: AsyncTransport,
        base_url: str,
        headers: dict[str, str],
    ) -> None:
        """Create a new async organization namespace.

        Args:
            transport: The async HTTP transport.
            base_url: The base URL for the API.
            headers: Headers to send with every request.
        """
        super().__init__(
            transport=transport,
            base_url=base_url,
            headers=headers,
        )
        self.pads: AsyncOrganizationPadsNamespace = (
            AsyncOrganizationPadsNamespace(
                transport=transport,
                base_url=base_url,
                headers=headers,
            )
        )
        self.questions: AsyncOrganizationQuestionsNamespace = (
            AsyncOrganizationQuestionsNamespace(
                transport=transport,
                base_url=base_url,
                headers=headers,
            )
        )

    async def get(self) -> Organization:
        """Retrieve organization information.

        Returns:
            The organization details.
        """
        response = await self._request(
            method="GET",
            url="/api/organization",
        )
        return Organization.from_dict(
            data=response.json(),
        )

    async def get_stats(
        self,
        *,
        start_time: str | None = None,
        end_time: str | None = None,
    ) -> OrganizationStats:
        """Retrieve pad usage stats for the organization.

        Args:
            start_time: ISO 8601 start of the search
                window.
            end_time: ISO 8601 end of the search window.

        Returns:
            The usage statistics.
        """
        params: dict[str, str | int] = {}
        if start_time is not None:
            params["start_time"] = start_time
        if end_time is not None:
            params["end_time"] = end_time
        response = await self._request(
            method="GET",
            url="/api/organization/stats",
            params=params,
        )
        return OrganizationStats.from_dict(
            data=response.json(),
        )

    async def get_quota(self) -> Quota:
        """Retrieve quota information.

        Returns:
            The quota details.
        """
        response = await self._request(
            method="GET",
            url="/api/quota",
        )
        return Quota.from_dict(data=response.json())


@beartype
class AsyncCoderPadClient:
    """An async client for the CoderPad Interview API."""

    def __init__(
        self,
        *,
        api_key: str,
        base_url: str = ("https://api.interview.coderpad.io"),
        transport: AsyncTransport | None = None,
    ) -> None:
        """Create a new async CoderPad client.

        Args:
            api_key: The API key for authentication.
            base_url: The base URL for the API.
            transport: The async HTTP transport. Defaults
                to ``AsyncHTTPXTransport()``.
        """
        self.base_url = base_url
        resolved_transport = transport or AsyncHTTPXTransport()
        headers = {"Authorization": f"Bearer {api_key}"}
        self.pads: AsyncPadsNamespace = AsyncPadsNamespace(
            transport=resolved_transport,
            base_url=base_url,
            headers=headers,
        )
        self.questions: AsyncQuestionsNamespace = AsyncQuestionsNamespace(
            transport=resolved_transport,
            base_url=base_url,
            headers=headers,
        )
        if isinstance(
            resolved_transport,
            AsyncHTTPXTransport,
        ):
            self._aclose = resolved_transport.aclose
        else:

            async def _noop() -> None:
                """No-op close for transports without aclose."""

            self._aclose = _noop
        self.organization: AsyncOrganizationNamespace = (
            AsyncOrganizationNamespace(
                transport=resolved_transport,
                base_url=base_url,
                headers=headers,
            )
        )

    async def aclose(self) -> None:
        """Close the underlying transport."""
        await self._aclose()

    async def __aenter__(self) -> Self:
        """Enter the async context manager.

        Returns:
            This client instance.
        """
        return self

    async def __aexit__(
        self,
        _exc_type: type[BaseException] | None,
        _exc_val: BaseException | None,
        _exc_tb: object,
    ) -> None:
        """Exit the async context manager and close."""
        await self.aclose()
