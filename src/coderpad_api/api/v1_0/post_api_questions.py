from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...types import Response


def _get_kwargs() -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/questions/",
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
    r"""Create a question

     Create a new question.

    ```
    curl \
      --data title=\"Are avocados fruity?\" \
      --data description=\"Fruit puzzler round 2\" \
      --data language=\"ruby\" \
      --data contents=\"def is_fruity?(thing);\n  end\n\" \
      --data solution=\"This is the solution\" \
      --data candidate_instructions=\"[{'instructions': 'Implement the is_fruity method'}]\" \
      -H 'Authorization: Token token=\"8af9a3412559d803707937250dc1569d\"' \
      https://app.coderpad.io/api/questions

     ```

    returns the question just created:

    ``` json
    {
      \"status\": \"OK\",
      \"id\": 7,
      \"title\": \"Are avocados fruity?\",
      \"owner_email\": \"alice@fruits-party.io\",
      \"language\": \"ruby\",
      \"description\": \"Fruit puzzler round 2\",
      \"contents\": \"def is_fruity?(thing);\n  end\n\",
      \"shared\": true,
      \"used\": 0,
      \"created_at\": \"2019-01-28T21:21:16Z\",
      \"updated_at\": \"2019-01-28T21:21:16Z\"
    }

     ```

    The available paramters you have to configure are detailed below:

    | Field | Description |
    | --- | --- |
    | id | `string` Primary key for the object. Use this to query or modify this resource later. |
    | title | `string` Title for this question. |
    | language | `string` One of a [set list](#Languages). |
    | description | `string` Notes for yourself (or colleagues) on what this question is about, and what
    good and bad answers might look like. |
    | contents | `string` This text is inserted into your interview session if you choose to use this
    question. |

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
    r"""Create a question

     Create a new question.

    ```
    curl \
      --data title=\"Are avocados fruity?\" \
      --data description=\"Fruit puzzler round 2\" \
      --data language=\"ruby\" \
      --data contents=\"def is_fruity?(thing);\n  end\n\" \
      --data solution=\"This is the solution\" \
      --data candidate_instructions=\"[{'instructions': 'Implement the is_fruity method'}]\" \
      -H 'Authorization: Token token=\"8af9a3412559d803707937250dc1569d\"' \
      https://app.coderpad.io/api/questions

     ```

    returns the question just created:

    ``` json
    {
      \"status\": \"OK\",
      \"id\": 7,
      \"title\": \"Are avocados fruity?\",
      \"owner_email\": \"alice@fruits-party.io\",
      \"language\": \"ruby\",
      \"description\": \"Fruit puzzler round 2\",
      \"contents\": \"def is_fruity?(thing);\n  end\n\",
      \"shared\": true,
      \"used\": 0,
      \"created_at\": \"2019-01-28T21:21:16Z\",
      \"updated_at\": \"2019-01-28T21:21:16Z\"
    }

     ```

    The available paramters you have to configure are detailed below:

    | Field | Description |
    | --- | --- |
    | id | `string` Primary key for the object. Use this to query or modify this resource later. |
    | title | `string` Title for this question. |
    | language | `string` One of a [set list](#Languages). |
    | description | `string` Notes for yourself (or colleagues) on what this question is about, and what
    good and bad answers might look like. |
    | contents | `string` This text is inserted into your interview session if you choose to use this
    question. |

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """
    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
