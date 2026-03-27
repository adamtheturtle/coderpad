from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...types import Response


def _get_kwargs(
    id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/questions/{id}".format(
            id=quote(str(id), safe=""),
        ),
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
    id: str,
    *,
    client: AuthenticatedClient,
) -> Response[Any]:
    r"""Retrieve a question by id

     Returns details about a particular question. You can view questions visible to you, which includes
    your own questions as well as colleagues’ questions where `shared` is set to `true`. If you’re an
    organization owner, you can view all questions in the organization.

    ```
    curl \
      -H 'Authorization: Token token=\"8af9a3412559d803707937250dc1569d\"' \
      https://app.coderpad.io/api/questions/42

     ```

    Yields:
    ``` json
    {
      \"status\": \"OK\",
      \"id\": 42,
      \"title\": \"Are fruits tomatoes?\",
      \"author_name\": \"Molly Macadamia\",
      \"owner_email\": \"molly@macadamia.net\",
      \"language\": \"postgresql\",
      \"description\": \"Use SQL magic to discover the answer.\",
      \"contents\": \"SELECT * FROM fruits;\n\",
      \"shared\": true,
      \"used\": 0,
      \"created_at\": \"2019-01-25T02:07:12Z\",
      \"updated_at\": \"2019-01-25T02:07:12Z\"
    }

     ```

    Fields returned:

    | Field | Description |
    | --- | --- |
    | id | `string` Primary key for the object. Use this to query or modify this resource later. |
    | title | `string` User-assigned title of the question. |
    | author_name | `string` Name of the person who authored this question. This is the same person as
    the owner referenced by owner_email. |
    | owner_email | `string` Email address of the person who owns the question. |
    | language | `string` Chosen language for the question. One of a [set list](#Languages). |
    | description | `string` Notes for yourself (or colleagues) on what this question is about, and what
    good and bad answers might look like. |
    | contents | `string`User-assigned question contents. This text is inserted into your interview
    session if you choose to use this question. |
    | shared | `boolean` Specifies whether this question is shared with the user’s organization.
    Defaults to `true`. |
    | used | `int` A counter counting the number of times this question was used to create pads. |
    | created_at | `datetime` The time when the question was created, in UTC ISO 8601, like
    `2019-01-30T00:22:55.520Z`. |
    | updated_at | `datetime` Similarly, the time when the question was last updated. |

    Args:
        id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """
    kwargs = _get_kwargs(
        id=id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    id: str,
    *,
    client: AuthenticatedClient,
) -> Response[Any]:
    r"""Retrieve a question by id

     Returns details about a particular question. You can view questions visible to you, which includes
    your own questions as well as colleagues’ questions where `shared` is set to `true`. If you’re an
    organization owner, you can view all questions in the organization.

    ```
    curl \
      -H 'Authorization: Token token=\"8af9a3412559d803707937250dc1569d\"' \
      https://app.coderpad.io/api/questions/42

     ```

    Yields:
    ``` json
    {
      \"status\": \"OK\",
      \"id\": 42,
      \"title\": \"Are fruits tomatoes?\",
      \"author_name\": \"Molly Macadamia\",
      \"owner_email\": \"molly@macadamia.net\",
      \"language\": \"postgresql\",
      \"description\": \"Use SQL magic to discover the answer.\",
      \"contents\": \"SELECT * FROM fruits;\n\",
      \"shared\": true,
      \"used\": 0,
      \"created_at\": \"2019-01-25T02:07:12Z\",
      \"updated_at\": \"2019-01-25T02:07:12Z\"
    }

     ```

    Fields returned:

    | Field | Description |
    | --- | --- |
    | id | `string` Primary key for the object. Use this to query or modify this resource later. |
    | title | `string` User-assigned title of the question. |
    | author_name | `string` Name of the person who authored this question. This is the same person as
    the owner referenced by owner_email. |
    | owner_email | `string` Email address of the person who owns the question. |
    | language | `string` Chosen language for the question. One of a [set list](#Languages). |
    | description | `string` Notes for yourself (or colleagues) on what this question is about, and what
    good and bad answers might look like. |
    | contents | `string`User-assigned question contents. This text is inserted into your interview
    session if you choose to use this question. |
    | shared | `boolean` Specifies whether this question is shared with the user’s organization.
    Defaults to `true`. |
    | used | `int` A counter counting the number of times this question was used to create pads. |
    | created_at | `datetime` The time when the question was created, in UTC ISO 8601, like
    `2019-01-30T00:22:55.520Z`. |
    | updated_at | `datetime` Similarly, the time when the question was last updated. |

    Args:
        id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """
    kwargs = _get_kwargs(
        id=id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
