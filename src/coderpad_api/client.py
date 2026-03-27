"""CoderPad Interview API client."""

import httpx

from coderpad_api._types import (
    ListPadsResponse,
    ListQuestionsResponse,
    OrganizationResponse,
    OrganizationStatsResponse,
    PadEnvironmentResponse,
    PadEventsResponse,
    PadResponse,
    QuestionResponse,
    QuotaResponse,
    StatusResponse,
)


class CoderPadClient:
    """A client for the CoderPad Interview API."""

    def __init__(
        self,
        *,
        api_key: str,
        base_url: str = "https://api.interview.coderpad.io",
    ) -> None:
        """Create a new CoderPad client.

        Args:
            api_key: The API key for authentication.
            base_url: The base URL for the API.
        """
        self.base_url = base_url
        self._client = httpx.Client(
            base_url=base_url,
            headers={"Authorization": f"Bearer {api_key}"},
        )

    def list_pads(
        self,
        *,
        sort: str | None = None,
        page: int | None = None,
    ) -> ListPadsResponse:
        """Retrieve a list of pads.

        Args:
            sort: Sort order, e.g. ``"updated_at,desc"``.
            page: Page number for pagination.

        Returns:
            The JSON response containing pads, next_page,
            and total.
        """
        params: dict[str, str | int] = {}
        if sort is not None:
            params["sort"] = sort
        if page is not None:
            params["page"] = page
        response = self._client.get(
            url="/api/pads/",
            params=params,
        )
        response.raise_for_status()
        return ListPadsResponse.from_dict(data=response.json())

    def create_pad(
        self,
        *,
        title: str | None = None,
        language: str | None = None,
        contents: str | None = None,
        notes: str | None = None,
    ) -> PadResponse:
        """Create a new pad.

        Args:
            title: Title for the pad.
            language: Programming language for the pad.
            contents: Initial contents of the pad editor.
            notes: Private notes for the interviewer.

        Returns:
            The JSON response containing the created pad.
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
        response = self._client.post(
            url="/api/pads/",
            data=data,
        )
        response.raise_for_status()
        return PadResponse.from_dict(data=response.json())

    def get_pad(self, *, pad_id: str) -> PadResponse:
        """Retrieve a pad by id.

        Args:
            pad_id: The id of the pad.

        Returns:
            The JSON response containing the pad details.
        """
        response = self._client.get(
            url=f"/api/pads/{pad_id}",
        )
        response.raise_for_status()
        return PadResponse.from_dict(data=response.json())

    def update_pad(
        self,
        *,
        pad_id: str,
        title: str | None = None,
        language: str | None = None,
        contents: str | None = None,
        notes: str | None = None,
        ended: bool | None = None,
        deleted: bool | None = None,
    ) -> StatusResponse:
        """Modify an existing pad.

        Args:
            pad_id: The id of the pad.
            title: New title for the pad.
            language: New programming language.
            contents: New contents of the pad editor.
            notes: New private notes.
            ended: Set to ``True`` to end the interview.
            deleted: Set to ``True`` to delete the pad.

        Returns:
            The JSON response.
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
        response = self._client.put(
            url=f"/api/pads/{pad_id}",
            data=data,
        )
        response.raise_for_status()
        return StatusResponse.from_dict(data=response.json())

    def get_pad_events(
        self,
        *,
        pad_id: str,
        sort: str | None = None,
        page: int | None = None,
    ) -> PadEventsResponse:
        """Retrieve a list of pad events.

        Args:
            pad_id: The id of the pad.
            sort: Sort order, e.g. ``"created_at,asc"``.
            page: Page number for pagination.

        Returns:
            The JSON response containing events and total.
        """
        params: dict[str, str | int] = {}
        if sort is not None:
            params["sort"] = sort
        if page is not None:
            params["page"] = page
        response = self._client.get(
            url=f"/api/pads/{pad_id}/events",
            params=params,
        )
        response.raise_for_status()
        return PadEventsResponse.from_dict(
            data=response.json(),
        )

    def get_pad_environment(
        self,
        *,
        environment_id: str,
    ) -> PadEnvironmentResponse:
        """Retrieve pad environment information.

        Args:
            environment_id: The id of the pad environment.

        Returns:
            The JSON response containing the environment
            details.
        """
        response = self._client.get(
            url=f"/api/pad_environments/{environment_id}",
        )
        response.raise_for_status()
        return PadEnvironmentResponse.from_dict(
            data=response.json(),
        )

    def list_questions(
        self,
        *,
        sort: str | None = None,
        page: int | None = None,
    ) -> ListQuestionsResponse:
        """Retrieve a list of questions.

        Args:
            sort: Sort order, e.g. ``"updated_at,desc"``.
            page: Page number for pagination.

        Returns:
            The JSON response containing questions,
            next_page, and total.
        """
        params: dict[str, str | int] = {}
        if sort is not None:
            params["sort"] = sort
        if page is not None:
            params["page"] = page
        response = self._client.get(
            url="/api/questions/",
            params=params,
        )
        response.raise_for_status()
        return ListQuestionsResponse.from_dict(
            data=response.json(),
        )

    def create_question(
        self,
        *,
        title: str,
        language: str,
        description: str | None = None,
        contents: str | None = None,
        solution: str | None = None,
    ) -> QuestionResponse:
        """Create a new question.

        Args:
            title: Title for the question.
            language: Programming language for the question.
            description: Notes about the question.
            contents: Text inserted into the interview
                session.
            solution: The solution to the question.

        Returns:
            The JSON response containing the created
            question.
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
        response = self._client.post(
            url="/api/questions/",
            data=data,
        )
        response.raise_for_status()
        return QuestionResponse.from_dict(
            data=response.json(),
        )

    def get_question(
        self,
        *,
        question_id: str,
    ) -> QuestionResponse:
        """Retrieve a question by id.

        Args:
            question_id: The id of the question.

        Returns:
            The JSON response containing the question
            details.
        """
        response = self._client.get(
            url=f"/api/questions/{question_id}",
        )
        response.raise_for_status()
        return QuestionResponse.from_dict(
            data=response.json(),
        )

    def update_question(
        self,
        *,
        question_id: str,
        title: str | None = None,
        language: str | None = None,
        description: str | None = None,
        contents: str | None = None,
        solution: str | None = None,
    ) -> StatusResponse:
        """Modify an existing question.

        Args:
            question_id: The id of the question.
            title: New title for the question.
            language: New programming language.
            description: New description.
            contents: New contents.
            solution: New solution.

        Returns:
            The JSON response.
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
        response = self._client.put(
            url=f"/api/questions/{question_id}",
            data=data,
        )
        response.raise_for_status()
        return StatusResponse.from_dict(data=response.json())

    def delete_question(
        self,
        *,
        question_id: str,
    ) -> StatusResponse:
        """Delete a question.

        Args:
            question_id: The id of the question.

        Returns:
            The JSON response.
        """
        response = self._client.delete(
            url=f"/api/questions/{question_id}",
        )
        response.raise_for_status()
        return StatusResponse.from_dict(data=response.json())

    def get_quota(self) -> QuotaResponse:
        """Retrieve quota information.

        Returns:
            The JSON response containing quota details.
        """
        response = self._client.get(url="/api/quota")
        response.raise_for_status()
        return QuotaResponse.from_dict(data=response.json())

    def get_organization(self) -> OrganizationResponse:
        """Retrieve organization information.

        Returns:
            The JSON response containing organization
            details.
        """
        response = self._client.get(
            url="/api/organization",
        )
        response.raise_for_status()
        return OrganizationResponse.from_dict(
            data=response.json(),
        )

    def get_organization_stats(
        self,
        *,
        start_time: str | None = None,
        end_time: str | None = None,
    ) -> OrganizationStatsResponse:
        """Retrieve pad usage stats for the organization.

        Args:
            start_time: ISO 8601 start of the search window.
            end_time: ISO 8601 end of the search window.

        Returns:
            The JSON response containing usage statistics.
        """
        params: dict[str, str] = {}
        if start_time is not None:
            params["start_time"] = start_time
        if end_time is not None:
            params["end_time"] = end_time
        response = self._client.get(
            url="/api/organization/stats",
            params=params,
        )
        response.raise_for_status()
        return OrganizationStatsResponse.from_dict(
            data=response.json(),
        )

    def list_organization_pads(
        self,
        *,
        sort: str | None = None,
        page: int | None = None,
    ) -> ListPadsResponse:
        """Retrieve pads for the entire organization.

        Args:
            sort: Sort order, e.g. ``"updated_at,desc"``.
            page: Page number for pagination.

        Returns:
            The JSON response containing pads, next_page,
            and total.
        """
        params: dict[str, str | int] = {}
        if sort is not None:
            params["sort"] = sort
        if page is not None:
            params["page"] = page
        response = self._client.get(
            url="/api/organization/pads",
            params=params,
        )
        response.raise_for_status()
        return ListPadsResponse.from_dict(
            data=response.json(),
        )

    def list_organization_questions(
        self,
        *,
        sort: str | None = None,
        page: int | None = None,
    ) -> ListQuestionsResponse:
        """Retrieve questions for the entire organization.

        Args:
            sort: Sort order, e.g. ``"updated_at,desc"``.
            page: Page number for pagination.

        Returns:
            The JSON response containing questions,
            next_page, and total.
        """
        params: dict[str, str | int] = {}
        if sort is not None:
            params["sort"] = sort
        if page is not None:
            params["page"] = page
        response = self._client.get(
            url="/api/organization/questions",
            params=params,
        )
        response.raise_for_status()
        return ListQuestionsResponse.from_dict(
            data=response.json(),
        )
