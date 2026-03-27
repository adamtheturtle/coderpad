from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_api_organization_users_response_200 import (
    GetApiOrganizationUsersResponse200,
)
from ...types import Response


def _get_kwargs() -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/organization/users",
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> GetApiOrganizationUsersResponse200 | None:
    if response.status_code == 200:
        response_200 = GetApiOrganizationUsersResponse200.from_dict(
            response.json()
        )

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[GetApiOrganizationUsersResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[GetApiOrganizationUsersResponse200]:
    r"""Retrieve company users

     This endpoint is similar to [<i>GET /api/organization</i>](#d2fa48b3-dbfe-4b9b-af97-9a4df8562f1e),
    except that it returns only the users list of that organization. If the `email` attribute is set, it
    returns only the user corresponding to that email.

    ```
    curl \
      -H 'Authorization: Token token=\"8af9a3412559d803707937250dc1569d\"' \
      \"https://app.coderpad.io/api/organization/pads?email=buddy@company.io\"

     ```

    Returns:
    ```
    {
        \"status\": \"OK\",
        \"users\": [
            {
                \"email\": \"buddy@company.io\",
                \"name\": \"Buddy\",
                \"teams\": [
                    \"68264172-5a54-4ac3-962b-cb8d1ad15d05\",
                    \"ddc4ce0a-93ec-4bad-9a1a-3d2db96f6220\"
                ]
            }
        ]
    }

     ```

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetApiOrganizationUsersResponse200]
    """
    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
) -> GetApiOrganizationUsersResponse200 | None:
    r"""Retrieve company users

     This endpoint is similar to [<i>GET /api/organization</i>](#d2fa48b3-dbfe-4b9b-af97-9a4df8562f1e),
    except that it returns only the users list of that organization. If the `email` attribute is set, it
    returns only the user corresponding to that email.

    ```
    curl \
      -H 'Authorization: Token token=\"8af9a3412559d803707937250dc1569d\"' \
      \"https://app.coderpad.io/api/organization/pads?email=buddy@company.io\"

     ```

    Returns:
    ```
    {
        \"status\": \"OK\",
        \"users\": [
            {
                \"email\": \"buddy@company.io\",
                \"name\": \"Buddy\",
                \"teams\": [
                    \"68264172-5a54-4ac3-962b-cb8d1ad15d05\",
                    \"ddc4ce0a-93ec-4bad-9a1a-3d2db96f6220\"
                ]
            }
        ]
    }

     ```

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetApiOrganizationUsersResponse200
    """
    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[GetApiOrganizationUsersResponse200]:
    r"""Retrieve company users

     This endpoint is similar to [<i>GET /api/organization</i>](#d2fa48b3-dbfe-4b9b-af97-9a4df8562f1e),
    except that it returns only the users list of that organization. If the `email` attribute is set, it
    returns only the user corresponding to that email.

    ```
    curl \
      -H 'Authorization: Token token=\"8af9a3412559d803707937250dc1569d\"' \
      \"https://app.coderpad.io/api/organization/pads?email=buddy@company.io\"

     ```

    Returns:
    ```
    {
        \"status\": \"OK\",
        \"users\": [
            {
                \"email\": \"buddy@company.io\",
                \"name\": \"Buddy\",
                \"teams\": [
                    \"68264172-5a54-4ac3-962b-cb8d1ad15d05\",
                    \"ddc4ce0a-93ec-4bad-9a1a-3d2db96f6220\"
                ]
            }
        ]
    }

     ```

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetApiOrganizationUsersResponse200]
    """
    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
) -> GetApiOrganizationUsersResponse200 | None:
    r"""Retrieve company users

     This endpoint is similar to [<i>GET /api/organization</i>](#d2fa48b3-dbfe-4b9b-af97-9a4df8562f1e),
    except that it returns only the users list of that organization. If the `email` attribute is set, it
    returns only the user corresponding to that email.

    ```
    curl \
      -H 'Authorization: Token token=\"8af9a3412559d803707937250dc1569d\"' \
      \"https://app.coderpad.io/api/organization/pads?email=buddy@company.io\"

     ```

    Returns:
    ```
    {
        \"status\": \"OK\",
        \"users\": [
            {
                \"email\": \"buddy@company.io\",
                \"name\": \"Buddy\",
                \"teams\": [
                    \"68264172-5a54-4ac3-962b-cb8d1ad15d05\",
                    \"ddc4ce0a-93ec-4bad-9a1a-3d2db96f6220\"
                ]
            }
        ]
    }

     ```

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetApiOrganizationUsersResponse200
    """
    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
