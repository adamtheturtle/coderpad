from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...types import Response


def _get_kwargs() -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/pads/",
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | None:
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Any]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[Any]:
    r"""Create a pad

     Create a new pad. You can set some initial conditions as well.

    ```
    curl \
      --data title=\"Rob Zombie's Interview\" \
      --data language=\"ruby\" \
      --data contents=\"print 'Hello, World'\" \
      --data notes=\"Your private notes\" \
      -H 'Authorization: Token token=\"8af9a3412559d803707937250dc1569d\"' \
      https://app.coderpad.io/api/pads

     ```

    Returns:
    ``` json
    {
      \"status\": \"OK\",
      \"id\": \"AFQ2K9A3\",
      \"title\": \"Rob Zombie's Interview\",
      \"owner_email\": \"fbueller@gmail.com\",
      \"language\": \"ruby\",
      \"participants\": [\"vincent\"],
      \"contents\": \"print 'Hello, World'\",
      \"notes\": \"Your private notes\",
      \"events\": \"https://app.coderpad.io/api/pads/AFQ2K9A3/events\",
      \"private\": false,
      \"execution_enabled\": true,
      \"created_at\": \"2014-11-14T03:02:45Z\",
      \"updated_at\": \"2014-11-14T03:02:45Z\",
      \"ended_at\": null,
      \"url\": \"https://coderpad.io/AFQ2K9A3\",
      \"playback\": \"https://coderpad.io/AFQ2K9A3/playback\",
      \"history\": \"https://coderpad.firebaseio.com/AFQ2K9A3/history.json\",
      \"drawing\": null,
      \"pad_environment_ids\": [
        1234567,
        7654321
      ],
      \"active_environment_id\": 1234567,
      \"team\": {
        \"id\": \"68264172-5a54-4ac3-962b-cb8d1ad15d05\",
        \"name\": \"Main Team\"
      }
    }

     ```

    This method can return a quota exceeded error if you are over your used pad limit for the month.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """
    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[Any]:
    r"""Create a pad

     Create a new pad. You can set some initial conditions as well.

    ```
    curl \
      --data title=\"Rob Zombie's Interview\" \
      --data language=\"ruby\" \
      --data contents=\"print 'Hello, World'\" \
      --data notes=\"Your private notes\" \
      -H 'Authorization: Token token=\"8af9a3412559d803707937250dc1569d\"' \
      https://app.coderpad.io/api/pads

     ```

    Returns:
    ``` json
    {
      \"status\": \"OK\",
      \"id\": \"AFQ2K9A3\",
      \"title\": \"Rob Zombie's Interview\",
      \"owner_email\": \"fbueller@gmail.com\",
      \"language\": \"ruby\",
      \"participants\": [\"vincent\"],
      \"contents\": \"print 'Hello, World'\",
      \"notes\": \"Your private notes\",
      \"events\": \"https://app.coderpad.io/api/pads/AFQ2K9A3/events\",
      \"private\": false,
      \"execution_enabled\": true,
      \"created_at\": \"2014-11-14T03:02:45Z\",
      \"updated_at\": \"2014-11-14T03:02:45Z\",
      \"ended_at\": null,
      \"url\": \"https://coderpad.io/AFQ2K9A3\",
      \"playback\": \"https://coderpad.io/AFQ2K9A3/playback\",
      \"history\": \"https://coderpad.firebaseio.com/AFQ2K9A3/history.json\",
      \"drawing\": null,
      \"pad_environment_ids\": [
        1234567,
        7654321
      ],
      \"active_environment_id\": 1234567,
      \"team\": {
        \"id\": \"68264172-5a54-4ac3-962b-cb8d1ad15d05\",
        \"name\": \"Main Team\"
      }
    }

     ```

    This method can return a quota exceeded error if you are over your used pad limit for the month.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """
    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
