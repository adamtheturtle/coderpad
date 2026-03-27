from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...types import Response


def _get_kwargs() -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/organization/questions",
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
    r"""Retrieve question info for entire company

     This endpoint is similar to [<i>GET /api/questions</i>](#d2fa48b3-dbfe-4b9b-af97-9a4df8562f1e),
    except that it returns all the questions in your organization visible to you. You’ll see your own
    questions as well as colleagues’ questions where the `shared` boolean is set to `true`. If you are
    an organization owner, you can see every question in the organization.

    The endpoint also performs sorting and pagination identically to [<i>GET
    /api/questions</i>](#d2fa48b3-dbfe-4b9b-af97-9a4df8562f1e).

    ```
    curl \
      -H 'Authorization: Token token=\"8af9a3412559d803707937250dc1569d\"' \
      \"https://app.coderpad.io/api/organization/questions?sort=updated_at,desc\"

     ```

    Returns:
    ```
    {
      \"status\": \"OK\",
      \"questions\": [
        {
          \"id\": 12,
          \"title\": \"Are avocados fruity?\",
          \"owner_email\": \"alice@fruits-party.io\",
          \"language\": \"ruby\",
          \"description\": \"Fruit puzzler round 2?\",
          \"contents\": \"def is_fruity?(thing);\\n  end\\n\",
          \"shared\": true,
          \"used\": 0,
          \"created_at\": \"2019-01-28T22:08:09Z\",
          \"updated_at\": \"2019-01-28T22:08:09Z\"
        }
        // ... followed by the rest of the questions in the organization visible to you
      ],
      \"next_page\": \"https://app.coderpad.io/api/organization/questions?sort=updated_at,desc&page=2\",
      \"total\": 256
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
    r"""Retrieve question info for entire company

     This endpoint is similar to [<i>GET /api/questions</i>](#d2fa48b3-dbfe-4b9b-af97-9a4df8562f1e),
    except that it returns all the questions in your organization visible to you. You’ll see your own
    questions as well as colleagues’ questions where the `shared` boolean is set to `true`. If you are
    an organization owner, you can see every question in the organization.

    The endpoint also performs sorting and pagination identically to [<i>GET
    /api/questions</i>](#d2fa48b3-dbfe-4b9b-af97-9a4df8562f1e).

    ```
    curl \
      -H 'Authorization: Token token=\"8af9a3412559d803707937250dc1569d\"' \
      \"https://app.coderpad.io/api/organization/questions?sort=updated_at,desc\"

     ```

    Returns:
    ```
    {
      \"status\": \"OK\",
      \"questions\": [
        {
          \"id\": 12,
          \"title\": \"Are avocados fruity?\",
          \"owner_email\": \"alice@fruits-party.io\",
          \"language\": \"ruby\",
          \"description\": \"Fruit puzzler round 2?\",
          \"contents\": \"def is_fruity?(thing);\\n  end\\n\",
          \"shared\": true,
          \"used\": 0,
          \"created_at\": \"2019-01-28T22:08:09Z\",
          \"updated_at\": \"2019-01-28T22:08:09Z\"
        }
        // ... followed by the rest of the questions in the organization visible to you
      ],
      \"next_page\": \"https://app.coderpad.io/api/organization/questions?sort=updated_at,desc&page=2\",
      \"total\": 256
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
