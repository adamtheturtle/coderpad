from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_api_quota_response_200 import GetApiQuotaResponse200
from ...types import Response


def _get_kwargs() -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/quota",
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> GetApiQuotaResponse200 | None:
    if response.status_code == 200:
        response_200 = GetApiQuotaResponse200.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[GetApiQuotaResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
) -> Response[GetApiQuotaResponse200]:
    r"""Retrieve quota information

     This endpoint returns basic information about your organization’s monthly pad quota (or your quota,
    if you are not a part of an organization). For example, if you are a user in an organization with a
    monthly quota of 120 pads, the following:

    ```
    curl \
      -H 'Authorization: Token token=\"8af9a3412559d803707937250dc1569d\"' \
      https://app.coderpad.io/api/quota

     ```

    Returns:
    ``` json
    {
      \"status\": \"OK\",
      \"trial_expires_at\": \"2018-01-30T16:16:00.000-08:00\",
      \"pads_used\": 33,
      \"quota_reset_at\": \"2018-01-25T14:51:37.084-08:00\",
      \"unlimited\": false,
      \"pads_remaining\": 87,
      \"billing_cycle_pad_limit\": 120
    }

     ```

    Fields returned:

    | Field | Description |
    | --- | --- |
    | trial_expires_at | `datetime` The date your trial will expire, or has expired, in UTC ISO 8601
    format (e.g., `2018-01-25T14:51:37.084-08:00`). |
    | pads_used | `int` The number of pads used during the current billing cycle. |
    | quota_reset_at | `datetime` The date, in UTC ISO 8601, that your quota was last reset. Pad quotas
    are reset every billing cycle. |
    | unlimited | `boolean` Indicates whether your billing plan allows for unmetered usage. |
    | pads_remaining | `int` The number of pads remaining for the current billing cycle. Not returned if
    `unlimited` is true. |
    | billing_cycle_pad_limit | `int` The total number of pads allocated for the billing cycle. Not
    returned if `unlimited` is true. |

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetApiQuotaResponse200]
    """
    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
) -> GetApiQuotaResponse200 | None:
    r"""Retrieve quota information

     This endpoint returns basic information about your organization’s monthly pad quota (or your quota,
    if you are not a part of an organization). For example, if you are a user in an organization with a
    monthly quota of 120 pads, the following:

    ```
    curl \
      -H 'Authorization: Token token=\"8af9a3412559d803707937250dc1569d\"' \
      https://app.coderpad.io/api/quota

     ```

    Returns:
    ``` json
    {
      \"status\": \"OK\",
      \"trial_expires_at\": \"2018-01-30T16:16:00.000-08:00\",
      \"pads_used\": 33,
      \"quota_reset_at\": \"2018-01-25T14:51:37.084-08:00\",
      \"unlimited\": false,
      \"pads_remaining\": 87,
      \"billing_cycle_pad_limit\": 120
    }

     ```

    Fields returned:

    | Field | Description |
    | --- | --- |
    | trial_expires_at | `datetime` The date your trial will expire, or has expired, in UTC ISO 8601
    format (e.g., `2018-01-25T14:51:37.084-08:00`). |
    | pads_used | `int` The number of pads used during the current billing cycle. |
    | quota_reset_at | `datetime` The date, in UTC ISO 8601, that your quota was last reset. Pad quotas
    are reset every billing cycle. |
    | unlimited | `boolean` Indicates whether your billing plan allows for unmetered usage. |
    | pads_remaining | `int` The number of pads remaining for the current billing cycle. Not returned if
    `unlimited` is true. |
    | billing_cycle_pad_limit | `int` The total number of pads allocated for the billing cycle. Not
    returned if `unlimited` is true. |

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetApiQuotaResponse200
    """
    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
) -> Response[GetApiQuotaResponse200]:
    r"""Retrieve quota information

     This endpoint returns basic information about your organization’s monthly pad quota (or your quota,
    if you are not a part of an organization). For example, if you are a user in an organization with a
    monthly quota of 120 pads, the following:

    ```
    curl \
      -H 'Authorization: Token token=\"8af9a3412559d803707937250dc1569d\"' \
      https://app.coderpad.io/api/quota

     ```

    Returns:
    ``` json
    {
      \"status\": \"OK\",
      \"trial_expires_at\": \"2018-01-30T16:16:00.000-08:00\",
      \"pads_used\": 33,
      \"quota_reset_at\": \"2018-01-25T14:51:37.084-08:00\",
      \"unlimited\": false,
      \"pads_remaining\": 87,
      \"billing_cycle_pad_limit\": 120
    }

     ```

    Fields returned:

    | Field | Description |
    | --- | --- |
    | trial_expires_at | `datetime` The date your trial will expire, or has expired, in UTC ISO 8601
    format (e.g., `2018-01-25T14:51:37.084-08:00`). |
    | pads_used | `int` The number of pads used during the current billing cycle. |
    | quota_reset_at | `datetime` The date, in UTC ISO 8601, that your quota was last reset. Pad quotas
    are reset every billing cycle. |
    | unlimited | `boolean` Indicates whether your billing plan allows for unmetered usage. |
    | pads_remaining | `int` The number of pads remaining for the current billing cycle. Not returned if
    `unlimited` is true. |
    | billing_cycle_pad_limit | `int` The total number of pads allocated for the billing cycle. Not
    returned if `unlimited` is true. |

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetApiQuotaResponse200]
    """
    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
) -> GetApiQuotaResponse200 | None:
    r"""Retrieve quota information

     This endpoint returns basic information about your organization’s monthly pad quota (or your quota,
    if you are not a part of an organization). For example, if you are a user in an organization with a
    monthly quota of 120 pads, the following:

    ```
    curl \
      -H 'Authorization: Token token=\"8af9a3412559d803707937250dc1569d\"' \
      https://app.coderpad.io/api/quota

     ```

    Returns:
    ``` json
    {
      \"status\": \"OK\",
      \"trial_expires_at\": \"2018-01-30T16:16:00.000-08:00\",
      \"pads_used\": 33,
      \"quota_reset_at\": \"2018-01-25T14:51:37.084-08:00\",
      \"unlimited\": false,
      \"pads_remaining\": 87,
      \"billing_cycle_pad_limit\": 120
    }

     ```

    Fields returned:

    | Field | Description |
    | --- | --- |
    | trial_expires_at | `datetime` The date your trial will expire, or has expired, in UTC ISO 8601
    format (e.g., `2018-01-25T14:51:37.084-08:00`). |
    | pads_used | `int` The number of pads used during the current billing cycle. |
    | quota_reset_at | `datetime` The date, in UTC ISO 8601, that your quota was last reset. Pad quotas
    are reset every billing cycle. |
    | unlimited | `boolean` Indicates whether your billing plan allows for unmetered usage. |
    | pads_remaining | `int` The number of pads remaining for the current billing cycle. Not returned if
    `unlimited` is true. |
    | billing_cycle_pad_limit | `int` The total number of pads allocated for the billing cycle. Not
    returned if `unlimited` is true. |

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetApiQuotaResponse200
    """
    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
