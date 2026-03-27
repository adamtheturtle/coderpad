from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.put_api_questions_id_response_200 import (
    PutApiQuestionsIdResponse200,
)
from ...types import Response


def _get_kwargs(
    id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/api/questions/{id}".format(
            id=quote(str(id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> PutApiQuestionsIdResponse200 | None:
    if response.status_code == 200:
        response_200 = PutApiQuestionsIdResponse200.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[PutApiQuestionsIdResponse200]:
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
) -> Response[PutApiQuestionsIdResponse200]:
    r"""Modify a question

     Modifies an existing question. You can specify any of the valid parameters to `create`.

    ```
    curl \
      -X PUT --data description=\"We've noticed candidates from the West coast have substantial
    experience with avocados, so this question is worth less points now.\" \
      -H 'Authorization: Token token=\"8af9a3412559d803707937250dc1569d\"' \
      https://app.coderpad.io/api/questions/42

     ```

    Args:
        id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PutApiQuestionsIdResponse200]
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
) -> PutApiQuestionsIdResponse200 | None:
    r"""Modify a question

     Modifies an existing question. You can specify any of the valid parameters to `create`.

    ```
    curl \
      -X PUT --data description=\"We've noticed candidates from the West coast have substantial
    experience with avocados, so this question is worth less points now.\" \
      -H 'Authorization: Token token=\"8af9a3412559d803707937250dc1569d\"' \
      https://app.coderpad.io/api/questions/42

     ```

    Args:
        id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PutApiQuestionsIdResponse200
    """
    return sync_detailed(
        id=id,
        client=client,
    ).parsed


async def asyncio_detailed(
    id: str,
    *,
    client: AuthenticatedClient,
) -> Response[PutApiQuestionsIdResponse200]:
    r"""Modify a question

     Modifies an existing question. You can specify any of the valid parameters to `create`.

    ```
    curl \
      -X PUT --data description=\"We've noticed candidates from the West coast have substantial
    experience with avocados, so this question is worth less points now.\" \
      -H 'Authorization: Token token=\"8af9a3412559d803707937250dc1569d\"' \
      https://app.coderpad.io/api/questions/42

     ```

    Args:
        id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PutApiQuestionsIdResponse200]
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
) -> PutApiQuestionsIdResponse200 | None:
    r"""Modify a question

     Modifies an existing question. You can specify any of the valid parameters to `create`.

    ```
    curl \
      -X PUT --data description=\"We've noticed candidates from the West coast have substantial
    experience with avocados, so this question is worth less points now.\" \
      -H 'Authorization: Token token=\"8af9a3412559d803707937250dc1569d\"' \
      https://app.coderpad.io/api/questions/42

     ```

    Args:
        id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PutApiQuestionsIdResponse200
    """
    return (
        await asyncio_detailed(
            id=id,
            client=client,
        )
    ).parsed
