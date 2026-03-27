from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_api_pads_id_events_response_200 import (
    GetApiPadsIdEventsResponse200,
)
from ...types import Response


def _get_kwargs(
    id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/pads/{id}/events".format(
            id=quote(str(id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> GetApiPadsIdEventsResponse200 | None:
    if response.status_code == 200:
        response_200 = GetApiPadsIdEventsResponse200.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[GetApiPadsIdEventsResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: str,
    *,
    client: AuthenticatedClient,
) -> Response[GetApiPadsIdEventsResponse200]:
    r"""Retrieve a list of pad events

     Returns detail about important **events** that transpired throughout the lifetime of the pad. It is
    represented as an array of objects with the following fields:

    | Field | Description |
    | --- | --- |
    | message | `string` The human-readable string version of the event. |
    | kind | `string`Can be one of:  <br>  <br>\- `joined`: when a user browses to a pad  <br>\- `left`:
    when a user closes the browser tab  <br>\- `ran`: when a user executes code  <br>\- `enabled`: when
    the pad owner enables code execution  <br>\- `disabled`: when the pad owner disables code execution
    <br>\- `ended`: when the pad owner ends the interview |
    | metadata | `string` Additional information associated with the event. In the case of a `ran`
    event, this will be the programming language run, for `joined` this can be `invisible` if a user
    joins in spectator mode. |
    | user_name | `string` Name of the user performing the event, will always be present. |
    | user_email | `string` If the user is logged in, this will be their email at the time of the event.
    |
    | created_at | `datetime` When the event occurred. |

    This endpoint supports sorting and pagination similar to the `/api/pads/` endpoint.

    Args:
        id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetApiPadsIdEventsResponse200]
    """
    kwargs = _get_kwargs(
        id=id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: str,
    *,
    client: AuthenticatedClient,
) -> GetApiPadsIdEventsResponse200 | None:
    r"""Retrieve a list of pad events

     Returns detail about important **events** that transpired throughout the lifetime of the pad. It is
    represented as an array of objects with the following fields:

    | Field | Description |
    | --- | --- |
    | message | `string` The human-readable string version of the event. |
    | kind | `string`Can be one of:  <br>  <br>\- `joined`: when a user browses to a pad  <br>\- `left`:
    when a user closes the browser tab  <br>\- `ran`: when a user executes code  <br>\- `enabled`: when
    the pad owner enables code execution  <br>\- `disabled`: when the pad owner disables code execution
    <br>\- `ended`: when the pad owner ends the interview |
    | metadata | `string` Additional information associated with the event. In the case of a `ran`
    event, this will be the programming language run, for `joined` this can be `invisible` if a user
    joins in spectator mode. |
    | user_name | `string` Name of the user performing the event, will always be present. |
    | user_email | `string` If the user is logged in, this will be their email at the time of the event.
    |
    | created_at | `datetime` When the event occurred. |

    This endpoint supports sorting and pagination similar to the `/api/pads/` endpoint.

    Args:
        id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetApiPadsIdEventsResponse200
    """
    return sync_detailed(
        id=id,
        client=client,
    ).parsed


async def asyncio_detailed(
    id: str,
    *,
    client: AuthenticatedClient,
) -> Response[GetApiPadsIdEventsResponse200]:
    r"""Retrieve a list of pad events

     Returns detail about important **events** that transpired throughout the lifetime of the pad. It is
    represented as an array of objects with the following fields:

    | Field | Description |
    | --- | --- |
    | message | `string` The human-readable string version of the event. |
    | kind | `string`Can be one of:  <br>  <br>\- `joined`: when a user browses to a pad  <br>\- `left`:
    when a user closes the browser tab  <br>\- `ran`: when a user executes code  <br>\- `enabled`: when
    the pad owner enables code execution  <br>\- `disabled`: when the pad owner disables code execution
    <br>\- `ended`: when the pad owner ends the interview |
    | metadata | `string` Additional information associated with the event. In the case of a `ran`
    event, this will be the programming language run, for `joined` this can be `invisible` if a user
    joins in spectator mode. |
    | user_name | `string` Name of the user performing the event, will always be present. |
    | user_email | `string` If the user is logged in, this will be their email at the time of the event.
    |
    | created_at | `datetime` When the event occurred. |

    This endpoint supports sorting and pagination similar to the `/api/pads/` endpoint.

    Args:
        id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetApiPadsIdEventsResponse200]
    """
    kwargs = _get_kwargs(
        id=id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: str,
    *,
    client: AuthenticatedClient,
) -> GetApiPadsIdEventsResponse200 | None:
    r"""Retrieve a list of pad events

     Returns detail about important **events** that transpired throughout the lifetime of the pad. It is
    represented as an array of objects with the following fields:

    | Field | Description |
    | --- | --- |
    | message | `string` The human-readable string version of the event. |
    | kind | `string`Can be one of:  <br>  <br>\- `joined`: when a user browses to a pad  <br>\- `left`:
    when a user closes the browser tab  <br>\- `ran`: when a user executes code  <br>\- `enabled`: when
    the pad owner enables code execution  <br>\- `disabled`: when the pad owner disables code execution
    <br>\- `ended`: when the pad owner ends the interview |
    | metadata | `string` Additional information associated with the event. In the case of a `ran`
    event, this will be the programming language run, for `joined` this can be `invisible` if a user
    joins in spectator mode. |
    | user_name | `string` Name of the user performing the event, will always be present. |
    | user_email | `string` If the user is logged in, this will be their email at the time of the event.
    |
    | created_at | `datetime` When the event occurred. |

    This endpoint supports sorting and pagination similar to the `/api/pads/` endpoint.

    Args:
        id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetApiPadsIdEventsResponse200
    """
    return (
        await asyncio_detailed(
            id=id,
            client=client,
        )
    ).parsed
