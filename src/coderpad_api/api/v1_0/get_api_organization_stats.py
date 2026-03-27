from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_api_organization_stats_response_200 import (
    GetApiOrganizationStatsResponse200,
)
from ...types import Response


def _get_kwargs() -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/organization/stats",
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> GetApiOrganizationStatsResponse200 | None:
    if response.status_code == 200:
        response_200 = GetApiOrganizationStatsResponse200.from_dict(
            response.json()
        )

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[GetApiOrganizationStatsResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[GetApiOrganizationStatsResponse200]:
    r"""Retrieve pad usage stats

     This endpoint returns statistics about how many pads the members of your organization have created.
    By default the endpoint will return information about the last 7 days, but you can configure the
    time range as well.

    | Parameter | Values |
    | --- | --- |
    | start_time | `datetime` An [ISO 8601 time string](http://www.w3.org/TR/NOTE-datetime), specifying
    the start of the search window. If this parameter is specified, you must set `end_time` as well, and
    vice versa. |
    | end_time | `datetime` An ISO 8601 time string specifying the end of the search window. |

    ```
    curl \
      -H 'Authorization: Token token=\"8af9a3412559d803707937250dc1569d\"' \
      \"https://app.coderpad.io/api/organization/stats?\
    start_time=2015-12-07T00:31:52Z&\
    end_time=2015-12-15T00:31:52Z\"

     ```

    Returns:
    ``` json
    {
      status: \"OK\",
      // The computed start/end times are always returned,
      // even with the default window
      start_time: 2023-07-23T12:27:05Z,
      end_time: 2023-07-31T12:27:05Z,
      pads_created: 137,
      users: [
        {
          email: \"person@place.com\",
          name: \"Person Surname\",
          pads_created: 7
        },
        {
          email: \"confidant@place.com\",
          name: \"Confidant Methodical\",
          pads_created: 0
        },
        // ... followed by the rest of the users in your org
      ]
    }

     ```

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetApiOrganizationStatsResponse200]
    """
    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
) -> GetApiOrganizationStatsResponse200 | None:
    r"""Retrieve pad usage stats

     This endpoint returns statistics about how many pads the members of your organization have created.
    By default the endpoint will return information about the last 7 days, but you can configure the
    time range as well.

    | Parameter | Values |
    | --- | --- |
    | start_time | `datetime` An [ISO 8601 time string](http://www.w3.org/TR/NOTE-datetime), specifying
    the start of the search window. If this parameter is specified, you must set `end_time` as well, and
    vice versa. |
    | end_time | `datetime` An ISO 8601 time string specifying the end of the search window. |

    ```
    curl \
      -H 'Authorization: Token token=\"8af9a3412559d803707937250dc1569d\"' \
      \"https://app.coderpad.io/api/organization/stats?\
    start_time=2015-12-07T00:31:52Z&\
    end_time=2015-12-15T00:31:52Z\"

     ```

    Returns:
    ``` json
    {
      status: \"OK\",
      // The computed start/end times are always returned,
      // even with the default window
      start_time: 2023-07-23T12:27:05Z,
      end_time: 2023-07-31T12:27:05Z,
      pads_created: 137,
      users: [
        {
          email: \"person@place.com\",
          name: \"Person Surname\",
          pads_created: 7
        },
        {
          email: \"confidant@place.com\",
          name: \"Confidant Methodical\",
          pads_created: 0
        },
        // ... followed by the rest of the users in your org
      ]
    }

     ```

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetApiOrganizationStatsResponse200
    """
    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[GetApiOrganizationStatsResponse200]:
    r"""Retrieve pad usage stats

     This endpoint returns statistics about how many pads the members of your organization have created.
    By default the endpoint will return information about the last 7 days, but you can configure the
    time range as well.

    | Parameter | Values |
    | --- | --- |
    | start_time | `datetime` An [ISO 8601 time string](http://www.w3.org/TR/NOTE-datetime), specifying
    the start of the search window. If this parameter is specified, you must set `end_time` as well, and
    vice versa. |
    | end_time | `datetime` An ISO 8601 time string specifying the end of the search window. |

    ```
    curl \
      -H 'Authorization: Token token=\"8af9a3412559d803707937250dc1569d\"' \
      \"https://app.coderpad.io/api/organization/stats?\
    start_time=2015-12-07T00:31:52Z&\
    end_time=2015-12-15T00:31:52Z\"

     ```

    Returns:
    ``` json
    {
      status: \"OK\",
      // The computed start/end times are always returned,
      // even with the default window
      start_time: 2023-07-23T12:27:05Z,
      end_time: 2023-07-31T12:27:05Z,
      pads_created: 137,
      users: [
        {
          email: \"person@place.com\",
          name: \"Person Surname\",
          pads_created: 7
        },
        {
          email: \"confidant@place.com\",
          name: \"Confidant Methodical\",
          pads_created: 0
        },
        // ... followed by the rest of the users in your org
      ]
    }

     ```

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetApiOrganizationStatsResponse200]
    """
    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
) -> GetApiOrganizationStatsResponse200 | None:
    r"""Retrieve pad usage stats

     This endpoint returns statistics about how many pads the members of your organization have created.
    By default the endpoint will return information about the last 7 days, but you can configure the
    time range as well.

    | Parameter | Values |
    | --- | --- |
    | start_time | `datetime` An [ISO 8601 time string](http://www.w3.org/TR/NOTE-datetime), specifying
    the start of the search window. If this parameter is specified, you must set `end_time` as well, and
    vice versa. |
    | end_time | `datetime` An ISO 8601 time string specifying the end of the search window. |

    ```
    curl \
      -H 'Authorization: Token token=\"8af9a3412559d803707937250dc1569d\"' \
      \"https://app.coderpad.io/api/organization/stats?\
    start_time=2015-12-07T00:31:52Z&\
    end_time=2015-12-15T00:31:52Z\"

     ```

    Returns:
    ``` json
    {
      status: \"OK\",
      // The computed start/end times are always returned,
      // even with the default window
      start_time: 2023-07-23T12:27:05Z,
      end_time: 2023-07-31T12:27:05Z,
      pads_created: 137,
      users: [
        {
          email: \"person@place.com\",
          name: \"Person Surname\",
          pads_created: 7
        },
        {
          email: \"confidant@place.com\",
          name: \"Confidant Methodical\",
          pads_created: 0
        },
        // ... followed by the rest of the users in your org
      ]
    }

     ```

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetApiOrganizationStatsResponse200
    """
    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
