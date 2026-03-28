"""CoderPad Interview API client."""

from __future__ import annotations

import httpx
from beartype import beartype

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
class PadsNamespace:
    """Namespace for pad operations."""

    def __init__(self, *, client: httpx.Client) -> None:
        """Create a new pads namespace.

        Args:
            client: The HTTP client.
        """
        self.client = client

    def list(
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
        response = self.client.get(
            url="/api/pads/",
            params=params,
        )
        response.raise_for_status()
        data = response.json()
        return PaginatedList(
            [Pad.from_dict(data=item) for item in data["pads"]],
            total=data["total"],
            next_page=data.get("next_page"),
        )

    def create(
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
        response = self.client.post(
            url="/api/pads/",
            data=data,
        )
        response.raise_for_status()
        return Pad.from_dict(data=response.json())

    def get(self, *, pad_id: str) -> Pad:
        """Retrieve a pad by id.

        Args:
            pad_id: The id of the pad.

        Returns:
            The pad.
        """
        response = self.client.get(
            url=f"/api/pads/{pad_id}",
        )
        response.raise_for_status()
        return Pad.from_dict(data=response.json())

    def update(
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
        response = self.client.put(
            url=f"/api/pads/{pad_id}",
            data=data,
        )
        response.raise_for_status()

    def get_events(
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
            The list of pad events with pagination metadata.
        """
        params: dict[str, str | int] = {}
        if sort is not None:
            params["sort"] = sort.value
        if page is not None:
            params["page"] = page
        response = self.client.get(
            url=f"/api/pads/{pad_id}/events",
            params=params,
        )
        response.raise_for_status()
        data = response.json()
        return PaginatedList(
            [PadEvent.from_dict(data=item) for item in data["events"]],
            total=data["total"],
            next_page=data.get("next_page"),
        )

    def get_environment(
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
        response = self.client.get(
            url=f"/api/pad_environments/{environment_id}",
        )
        response.raise_for_status()
        return PadEnvironment.from_dict(
            data=response.json(),
        )


@beartype
class QuestionsNamespace:
    """Namespace for question operations."""

    def __init__(self, *, client: httpx.Client) -> None:
        """Create a new questions namespace.

        Args:
            client: The HTTP client.
        """
        self.client = client

    def list(
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
            The list of questions with pagination metadata.
        """
        params: dict[str, str | int] = {}
        if sort is not None:
            params["sort"] = sort.value
        if page is not None:
            params["page"] = page
        response = self.client.get(
            url="/api/questions/",
            params=params,
        )
        response.raise_for_status()
        data = response.json()
        return PaginatedList(
            [Question.from_dict(data=item) for item in data["questions"]],
            total=data["total"],
            next_page=data.get("next_page"),
        )

    def create(
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
            language: Programming language for the question.
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
        response = self.client.post(
            url="/api/questions/",
            data=data,
        )
        response.raise_for_status()
        return Question.from_dict(
            data=response.json(),
        )

    def get(
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
        response = self.client.get(
            url=f"/api/questions/{question_id}",
        )
        response.raise_for_status()
        return Question.from_dict(
            data=response.json(),
        )

    def update(
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
        response = self.client.put(
            url=f"/api/questions/{question_id}",
            data=data,
        )
        response.raise_for_status()

    def delete(
        self,
        *,
        question_id: str,
    ) -> None:
        """Delete a question.

        Args:
            question_id: The id of the question.
        """
        response = self.client.delete(
            url=f"/api/questions/{question_id}",
        )
        response.raise_for_status()


@beartype
class OrganizationPadsNamespace:
    """Namespace for organization pad operations."""

    def __init__(self, *, client: httpx.Client) -> None:
        """Create a new organization pads namespace.

        Args:
            client: The HTTP client.
        """
        self.client = client

    def list(
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
        response = self.client.get(
            url="/api/organization/pads",
            params=params,
        )
        response.raise_for_status()
        data = response.json()
        return PaginatedList(
            [Pad.from_dict(data=item) for item in data["pads"]],
            total=data["total"],
            next_page=data.get("next_page"),
        )


@beartype
class OrganizationQuestionsNamespace:
    """Namespace for organization question operations."""

    def __init__(self, *, client: httpx.Client) -> None:
        """Create a new organization questions namespace.

        Args:
            client: The HTTP client.
        """
        self.client = client

    def list(
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
            The list of questions with pagination metadata.
        """
        params: dict[str, str | int] = {}
        if sort is not None:
            params["sort"] = sort.value
        if page is not None:
            params["page"] = page
        response = self.client.get(
            url="/api/organization/questions",
            params=params,
        )
        response.raise_for_status()
        data = response.json()
        return PaginatedList(
            [Question.from_dict(data=item) for item in data["questions"]],
            total=data["total"],
            next_page=data.get("next_page"),
        )


@beartype
class OrganizationNamespace:
    """Namespace for organization operations."""

    def __init__(self, *, client: httpx.Client) -> None:
        """Create a new organization namespace.

        Args:
            client: The HTTP client.
        """
        self.client = client
        self.pads: OrganizationPadsNamespace = OrganizationPadsNamespace(
            client=client,
        )
        self.questions: OrganizationQuestionsNamespace = (
            OrganizationQuestionsNamespace(client=client)
        )

    def get(self) -> Organization:
        """Retrieve organization information.

        Returns:
            The organization details.
        """
        response = self.client.get(
            url="/api/organization",
        )
        response.raise_for_status()
        return Organization.from_dict(
            data=response.json(),
        )

    def get_stats(
        self,
        *,
        start_time: str | None = None,
        end_time: str | None = None,
    ) -> OrganizationStats:
        """Retrieve pad usage stats for the organization.

        Args:
            start_time: ISO 8601 start of the search window.
            end_time: ISO 8601 end of the search window.

        Returns:
            The usage statistics.
        """
        params: dict[str, str] = {}
        if start_time is not None:
            params["start_time"] = start_time
        if end_time is not None:
            params["end_time"] = end_time
        response = self.client.get(
            url="/api/organization/stats",
            params=params,
        )
        response.raise_for_status()
        return OrganizationStats.from_dict(
            data=response.json(),
        )

    def get_quota(self) -> Quota:
        """Retrieve quota information.

        Returns:
            The quota details.
        """
        response = self.client.get(url="/api/quota")
        response.raise_for_status()
        return Quota.from_dict(data=response.json())


@beartype
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
        http_client = httpx.Client(
            base_url=base_url,
            headers={"Authorization": f"Bearer {api_key}"},
        )
        self.pads: PadsNamespace = PadsNamespace(client=http_client)
        self.questions: QuestionsNamespace = QuestionsNamespace(
            client=http_client,
        )
        self.organization: OrganizationNamespace = OrganizationNamespace(
            client=http_client,
        )
