"""CoderPad Interview API client."""

import httpx


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
