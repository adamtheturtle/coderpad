from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_api_organization_pads_response_200 import (
    GetApiOrganizationPadsResponse200,
)
from ...types import Response


def _get_kwargs() -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/organization/pads",
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> GetApiOrganizationPadsResponse200 | None:
    if response.status_code == 200:
        response_200 = GetApiOrganizationPadsResponse200.from_dict(
            response.json()
        )

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[GetApiOrganizationPadsResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[GetApiOrganizationPadsResponse200]:
    r"""Retrieve pad info for entire company

     This endpoint is similar to the _Get a list of pads_ operation, except that it returns all the pads
    in your organization. To access this endpoint, your user must be an organization owner, or your
    organization must allow all pads to be visible to its users. This last setting is default on, but
    you can [email us](https://mailto:support@coderpad.io) to disable this feature.

    The endpoint also performs sorting and pagination identically to _Get a list of pads_.

    ```
    curl \
      -H 'Authorization: Token token=\"8af9a3412559d803707937250dc1569d\"' \
      \"https://app.coderpad.io/api/organization/pads?sort=updated_at,desc\"

     ```

    Returns:
    ``` json
    {
      \"status\": \"OK\",
      \"pads\": [
        {
          \"id\": \"PP7J474P\",
          \"title\": \"JavaScript Test\",
          \"owner_email\": \"kristin@coderpad.io\",
          \"language\": \"javascript\",
          \"participants\": [\"Kristin\", \"Guest 104\"],
          \"contents\": \"var _ = require('underscore');\n...\",
          \"private\": false,
          \"execution_enabled\": true,
          \"events\": \"https://app.coderpad.io/api/pads/PP7J474P/events\",
          \"notes\": \"Brenda did a fantastic job talking through the prompt ...\",
          \"created_at\": \"2018-02-13T02:06:30Z\",
          \"updated_at\": \"2018-02-13T06:21:26Z\",
          \"ended_at\": null,
          \"url\": \"https://coderpad.io/PP7J474P\",
          \"playback\": \"https://coderpad.io/PP7J474P/playback\",
          \"history\": \"https://coderpadproject.firebaseio.com/PP7J474P/history.json\",
          \"drawing\": \"https://storage.googleapis.com/...\",
          \"team\": {
            \"id\": \"68264172-5a54-4ac3-962b-cb8d1ad15d05\",
            \"name\": \"Main Team\"
          }
        }
        // ... followed by a list of the rest of the pads in the organization
      ],
      \"next_page\": \"https://app.coderpad.io/api/organization/pads?sort=updated_at,desc&page=2\",
      \"total\": 512
    }

     ```

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetApiOrganizationPadsResponse200]
    """
    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
) -> GetApiOrganizationPadsResponse200 | None:
    r"""Retrieve pad info for entire company

     This endpoint is similar to the _Get a list of pads_ operation, except that it returns all the pads
    in your organization. To access this endpoint, your user must be an organization owner, or your
    organization must allow all pads to be visible to its users. This last setting is default on, but
    you can [email us](https://mailto:support@coderpad.io) to disable this feature.

    The endpoint also performs sorting and pagination identically to _Get a list of pads_.

    ```
    curl \
      -H 'Authorization: Token token=\"8af9a3412559d803707937250dc1569d\"' \
      \"https://app.coderpad.io/api/organization/pads?sort=updated_at,desc\"

     ```

    Returns:
    ``` json
    {
      \"status\": \"OK\",
      \"pads\": [
        {
          \"id\": \"PP7J474P\",
          \"title\": \"JavaScript Test\",
          \"owner_email\": \"kristin@coderpad.io\",
          \"language\": \"javascript\",
          \"participants\": [\"Kristin\", \"Guest 104\"],
          \"contents\": \"var _ = require('underscore');\n...\",
          \"private\": false,
          \"execution_enabled\": true,
          \"events\": \"https://app.coderpad.io/api/pads/PP7J474P/events\",
          \"notes\": \"Brenda did a fantastic job talking through the prompt ...\",
          \"created_at\": \"2018-02-13T02:06:30Z\",
          \"updated_at\": \"2018-02-13T06:21:26Z\",
          \"ended_at\": null,
          \"url\": \"https://coderpad.io/PP7J474P\",
          \"playback\": \"https://coderpad.io/PP7J474P/playback\",
          \"history\": \"https://coderpadproject.firebaseio.com/PP7J474P/history.json\",
          \"drawing\": \"https://storage.googleapis.com/...\",
          \"team\": {
            \"id\": \"68264172-5a54-4ac3-962b-cb8d1ad15d05\",
            \"name\": \"Main Team\"
          }
        }
        // ... followed by a list of the rest of the pads in the organization
      ],
      \"next_page\": \"https://app.coderpad.io/api/organization/pads?sort=updated_at,desc&page=2\",
      \"total\": 512
    }

     ```

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetApiOrganizationPadsResponse200
    """
    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[GetApiOrganizationPadsResponse200]:
    r"""Retrieve pad info for entire company

     This endpoint is similar to the _Get a list of pads_ operation, except that it returns all the pads
    in your organization. To access this endpoint, your user must be an organization owner, or your
    organization must allow all pads to be visible to its users. This last setting is default on, but
    you can [email us](https://mailto:support@coderpad.io) to disable this feature.

    The endpoint also performs sorting and pagination identically to _Get a list of pads_.

    ```
    curl \
      -H 'Authorization: Token token=\"8af9a3412559d803707937250dc1569d\"' \
      \"https://app.coderpad.io/api/organization/pads?sort=updated_at,desc\"

     ```

    Returns:
    ``` json
    {
      \"status\": \"OK\",
      \"pads\": [
        {
          \"id\": \"PP7J474P\",
          \"title\": \"JavaScript Test\",
          \"owner_email\": \"kristin@coderpad.io\",
          \"language\": \"javascript\",
          \"participants\": [\"Kristin\", \"Guest 104\"],
          \"contents\": \"var _ = require('underscore');\n...\",
          \"private\": false,
          \"execution_enabled\": true,
          \"events\": \"https://app.coderpad.io/api/pads/PP7J474P/events\",
          \"notes\": \"Brenda did a fantastic job talking through the prompt ...\",
          \"created_at\": \"2018-02-13T02:06:30Z\",
          \"updated_at\": \"2018-02-13T06:21:26Z\",
          \"ended_at\": null,
          \"url\": \"https://coderpad.io/PP7J474P\",
          \"playback\": \"https://coderpad.io/PP7J474P/playback\",
          \"history\": \"https://coderpadproject.firebaseio.com/PP7J474P/history.json\",
          \"drawing\": \"https://storage.googleapis.com/...\",
          \"team\": {
            \"id\": \"68264172-5a54-4ac3-962b-cb8d1ad15d05\",
            \"name\": \"Main Team\"
          }
        }
        // ... followed by a list of the rest of the pads in the organization
      ],
      \"next_page\": \"https://app.coderpad.io/api/organization/pads?sort=updated_at,desc&page=2\",
      \"total\": 512
    }

     ```

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetApiOrganizationPadsResponse200]
    """
    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
) -> GetApiOrganizationPadsResponse200 | None:
    r"""Retrieve pad info for entire company

     This endpoint is similar to the _Get a list of pads_ operation, except that it returns all the pads
    in your organization. To access this endpoint, your user must be an organization owner, or your
    organization must allow all pads to be visible to its users. This last setting is default on, but
    you can [email us](https://mailto:support@coderpad.io) to disable this feature.

    The endpoint also performs sorting and pagination identically to _Get a list of pads_.

    ```
    curl \
      -H 'Authorization: Token token=\"8af9a3412559d803707937250dc1569d\"' \
      \"https://app.coderpad.io/api/organization/pads?sort=updated_at,desc\"

     ```

    Returns:
    ``` json
    {
      \"status\": \"OK\",
      \"pads\": [
        {
          \"id\": \"PP7J474P\",
          \"title\": \"JavaScript Test\",
          \"owner_email\": \"kristin@coderpad.io\",
          \"language\": \"javascript\",
          \"participants\": [\"Kristin\", \"Guest 104\"],
          \"contents\": \"var _ = require('underscore');\n...\",
          \"private\": false,
          \"execution_enabled\": true,
          \"events\": \"https://app.coderpad.io/api/pads/PP7J474P/events\",
          \"notes\": \"Brenda did a fantastic job talking through the prompt ...\",
          \"created_at\": \"2018-02-13T02:06:30Z\",
          \"updated_at\": \"2018-02-13T06:21:26Z\",
          \"ended_at\": null,
          \"url\": \"https://coderpad.io/PP7J474P\",
          \"playback\": \"https://coderpad.io/PP7J474P/playback\",
          \"history\": \"https://coderpadproject.firebaseio.com/PP7J474P/history.json\",
          \"drawing\": \"https://storage.googleapis.com/...\",
          \"team\": {
            \"id\": \"68264172-5a54-4ac3-962b-cb8d1ad15d05\",
            \"name\": \"Main Team\"
          }
        }
        // ... followed by a list of the rest of the pads in the organization
      ],
      \"next_page\": \"https://app.coderpad.io/api/organization/pads?sort=updated_at,desc&page=2\",
      \"total\": 512
    }

     ```

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetApiOrganizationPadsResponse200
    """
    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
