from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...types import Response


def _get_kwargs() -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
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
    r"""Retrieve a list of pads

     Fetch a list of all of your pads. Returns everything that an individual _Get pads by id_ request
    does. The only caveat is that the values of fields in the index view are not guaranteed to be 100%
    real-time. Generally, they should be no more than a minute behind, but if you absolutely require the
    latest value in a pad, please use the individual _Get pads by id_ endpoint.

    ```
    curl \
      -H 'Authorization: Token token=\"8af9a3412559d803707937250dc1569d\"' \
      <a class=&#x27;preserveHtml&#x27; class=&#x27;preserveHtml&#x27; target=\"_blank\"
    rel=\"noreferrer noopener\" href=\"https://app.coderpad.io/api/pads?sort=updated_at,descThis\">https
    ://app.coderpad.io/api/pads?sort=updated_at,desc</a>

     ```

    This API endpoint takes an optional `sort` parameter, which allows you to sort by either the
    `created_at` or `updated_at` fields on your pads. Adding a comma will allow you to change the sort
    direction, which is `desc` by default. For example, to sort your pads by `updated_at` from oldest to
    newest, specify `updated_at,asc`.

    If no `sort` parameter is provided, `created_at,desc` is assumed.

    The method also returns paginated results - no more than 50 per request. If you want more, follow
    the `next_page` or `prev_page` urls if present. The API also returns a `total` count to give you a
    sense of how many pads you have created.

    ``` json
    {
      \"status\": \"OK\",
      \"pads\": [
        // ... your pads, with the same data format as in `show`
      ],
      \"next_page\": \"https://app.coderpad.io/api/pads?sort=updated_at,desc&page=2\",
      \"total\": 420
    }

     ```

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
    r"""Retrieve a list of pads

     Fetch a list of all of your pads. Returns everything that an individual _Get pads by id_ request
    does. The only caveat is that the values of fields in the index view are not guaranteed to be 100%
    real-time. Generally, they should be no more than a minute behind, but if you absolutely require the
    latest value in a pad, please use the individual _Get pads by id_ endpoint.

    ```
    curl \
      -H 'Authorization: Token token=\"8af9a3412559d803707937250dc1569d\"' \
      <a class=&#x27;preserveHtml&#x27; class=&#x27;preserveHtml&#x27; target=\"_blank\"
    rel=\"noreferrer noopener\" href=\"https://app.coderpad.io/api/pads?sort=updated_at,descThis\">https
    ://app.coderpad.io/api/pads?sort=updated_at,desc</a>

     ```

    This API endpoint takes an optional `sort` parameter, which allows you to sort by either the
    `created_at` or `updated_at` fields on your pads. Adding a comma will allow you to change the sort
    direction, which is `desc` by default. For example, to sort your pads by `updated_at` from oldest to
    newest, specify `updated_at,asc`.

    If no `sort` parameter is provided, `created_at,desc` is assumed.

    The method also returns paginated results - no more than 50 per request. If you want more, follow
    the `next_page` or `prev_page` urls if present. The API also returns a `total` count to give you a
    sense of how many pads you have created.

    ``` json
    {
      \"status\": \"OK\",
      \"pads\": [
        // ... your pads, with the same data format as in `show`
      ],
      \"next_page\": \"https://app.coderpad.io/api/pads?sort=updated_at,desc&page=2\",
      \"total\": 420
    }

     ```

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """
    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
