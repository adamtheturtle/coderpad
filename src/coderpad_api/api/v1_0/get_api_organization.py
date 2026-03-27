from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_api_organization_response_200 import (
    GetApiOrganizationResponse200,
)
from ...types import Response


def _get_kwargs() -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/organization",
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> GetApiOrganizationResponse200 | None:
    if response.status_code == 200:
        response_200 = GetApiOrganizationResponse200.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[GetApiOrganizationResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[GetApiOrganizationResponse200]:
    r"""Retrieve account info

     This endpoint returns basic information about your organization, including whether or not your
    organization makes use of a single-sign-on service for authentication.

    ```
    curl \
      -H 'Authorization: Token token=\"8af9a3412559d803707937250dc1569d\"' \
      https://app.coderpad.io/api/organization

     ```

    Returns:
    ``` json
    {
      \"status\": \"OK\",
      \"organization_name\": \"ACME Computing\",
      \"user_count\": 137,
      \"users\": [
        {
          \"email\": \"wile@acme.com\",
          \"name\": \"Wile Coyote\",
          \"teams\": [
            \"68264172-5a54-4ac3-962b-cb8d1ad15d05\",
            \"4a0f61a3-3013-49f5-9eb7-9f83712a49bf\"
          ]
        }
        // ... followed by the rest of the users in your org.
      ],
      \"default_language\": \"erlang\", // default language for new users in your organization
      \"single_sign_on_supported\": true, // users will be directed to login via the single sign in
    portal
      \"single_sign_in_url\": acme.coderpad.io, // the url for that portal.
      \"teams\": [ // The teams names and ids
        {
          \"id\": \"68264172-5a54-4ac3-962b-cb8d1ad15d05\",
          \"name\": \"Main Team\"
        },
        {
          \"id\": \"4a0f61a3-3013-49f5-9eb7-9f83712a49bf\",
          \"name\": \"Second Team\"
        },
        {
          \"id\": \"ddc4ce0a-93ec-4bad-9a1a-3d2db96f6220\",
          \"name\": \"Third Team\"
        }
      ]
    }

     ```

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetApiOrganizationResponse200]
    """
    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
) -> GetApiOrganizationResponse200 | None:
    r"""Retrieve account info

     This endpoint returns basic information about your organization, including whether or not your
    organization makes use of a single-sign-on service for authentication.

    ```
    curl \
      -H 'Authorization: Token token=\"8af9a3412559d803707937250dc1569d\"' \
      https://app.coderpad.io/api/organization

     ```

    Returns:
    ``` json
    {
      \"status\": \"OK\",
      \"organization_name\": \"ACME Computing\",
      \"user_count\": 137,
      \"users\": [
        {
          \"email\": \"wile@acme.com\",
          \"name\": \"Wile Coyote\",
          \"teams\": [
            \"68264172-5a54-4ac3-962b-cb8d1ad15d05\",
            \"4a0f61a3-3013-49f5-9eb7-9f83712a49bf\"
          ]
        }
        // ... followed by the rest of the users in your org.
      ],
      \"default_language\": \"erlang\", // default language for new users in your organization
      \"single_sign_on_supported\": true, // users will be directed to login via the single sign in
    portal
      \"single_sign_in_url\": acme.coderpad.io, // the url for that portal.
      \"teams\": [ // The teams names and ids
        {
          \"id\": \"68264172-5a54-4ac3-962b-cb8d1ad15d05\",
          \"name\": \"Main Team\"
        },
        {
          \"id\": \"4a0f61a3-3013-49f5-9eb7-9f83712a49bf\",
          \"name\": \"Second Team\"
        },
        {
          \"id\": \"ddc4ce0a-93ec-4bad-9a1a-3d2db96f6220\",
          \"name\": \"Third Team\"
        }
      ]
    }

     ```

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetApiOrganizationResponse200
    """
    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[GetApiOrganizationResponse200]:
    r"""Retrieve account info

     This endpoint returns basic information about your organization, including whether or not your
    organization makes use of a single-sign-on service for authentication.

    ```
    curl \
      -H 'Authorization: Token token=\"8af9a3412559d803707937250dc1569d\"' \
      https://app.coderpad.io/api/organization

     ```

    Returns:
    ``` json
    {
      \"status\": \"OK\",
      \"organization_name\": \"ACME Computing\",
      \"user_count\": 137,
      \"users\": [
        {
          \"email\": \"wile@acme.com\",
          \"name\": \"Wile Coyote\",
          \"teams\": [
            \"68264172-5a54-4ac3-962b-cb8d1ad15d05\",
            \"4a0f61a3-3013-49f5-9eb7-9f83712a49bf\"
          ]
        }
        // ... followed by the rest of the users in your org.
      ],
      \"default_language\": \"erlang\", // default language for new users in your organization
      \"single_sign_on_supported\": true, // users will be directed to login via the single sign in
    portal
      \"single_sign_in_url\": acme.coderpad.io, // the url for that portal.
      \"teams\": [ // The teams names and ids
        {
          \"id\": \"68264172-5a54-4ac3-962b-cb8d1ad15d05\",
          \"name\": \"Main Team\"
        },
        {
          \"id\": \"4a0f61a3-3013-49f5-9eb7-9f83712a49bf\",
          \"name\": \"Second Team\"
        },
        {
          \"id\": \"ddc4ce0a-93ec-4bad-9a1a-3d2db96f6220\",
          \"name\": \"Third Team\"
        }
      ]
    }

     ```

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetApiOrganizationResponse200]
    """
    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
) -> GetApiOrganizationResponse200 | None:
    r"""Retrieve account info

     This endpoint returns basic information about your organization, including whether or not your
    organization makes use of a single-sign-on service for authentication.

    ```
    curl \
      -H 'Authorization: Token token=\"8af9a3412559d803707937250dc1569d\"' \
      https://app.coderpad.io/api/organization

     ```

    Returns:
    ``` json
    {
      \"status\": \"OK\",
      \"organization_name\": \"ACME Computing\",
      \"user_count\": 137,
      \"users\": [
        {
          \"email\": \"wile@acme.com\",
          \"name\": \"Wile Coyote\",
          \"teams\": [
            \"68264172-5a54-4ac3-962b-cb8d1ad15d05\",
            \"4a0f61a3-3013-49f5-9eb7-9f83712a49bf\"
          ]
        }
        // ... followed by the rest of the users in your org.
      ],
      \"default_language\": \"erlang\", // default language for new users in your organization
      \"single_sign_on_supported\": true, // users will be directed to login via the single sign in
    portal
      \"single_sign_in_url\": acme.coderpad.io, // the url for that portal.
      \"teams\": [ // The teams names and ids
        {
          \"id\": \"68264172-5a54-4ac3-962b-cb8d1ad15d05\",
          \"name\": \"Main Team\"
        },
        {
          \"id\": \"4a0f61a3-3013-49f5-9eb7-9f83712a49bf\",
          \"name\": \"Second Team\"
        },
        {
          \"id\": \"ddc4ce0a-93ec-4bad-9a1a-3d2db96f6220\",
          \"name\": \"Third Team\"
        }
      ]
    }

     ```

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetApiOrganizationResponse200
    """
    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
