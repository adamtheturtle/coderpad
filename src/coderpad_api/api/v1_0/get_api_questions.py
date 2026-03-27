from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_api_questions_response_200 import GetApiQuestionsResponse200
from ...types import Response


def _get_kwargs() -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/questions/",
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> GetApiQuestionsResponse200 | None:
    if response.status_code == 200:
        response_200 = GetApiQuestionsResponse200.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[GetApiQuestionsResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[GetApiQuestionsResponse200]:
    r"""Retrieve a list of questions

     Fetch a list of all of your questions. Returns all fields that an individual _Get question by id_
    request does.

    ```
    curl \
      -H 'Authorization: Token token=\"8af9a3412559d803707937250dc1569d\"' \
      https://app.coderpad.io/api/questions?sort=updated_at,desc

     ```

    `index` takes an optional `sort` parameter, which allows you to sort by either the `created_at` or
    `updated_at` fields on the questions. Adding a comma will allow you to change the sort direction,
    which is `desc` by default. For example, to sort your questions by `updated_at` from oldest to
    newest, specify `updated_at,asc`.

    If no `sort` parameter is provided, `created_at,desc` is assumed.

    The method also returns paginated results - no more than 50 per request. If you want more, follow
    the `next_page` or `prev_page` urls if present. The API also returns a `total` count to give you a
    sense of how many questions exist.

    ``` json
    {
      \"status\": \"OK\",
      \"questions\": [
        // ... your questions, with the same data format as in `show`
      ],
      \"next_page\": \"https://app.coderpad.io/api/question?sort=updated_at,desc&page=2\",
      \"total\": 420
    }

     ```

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetApiQuestionsResponse200]
    """
    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
) -> GetApiQuestionsResponse200 | None:
    r"""Retrieve a list of questions

     Fetch a list of all of your questions. Returns all fields that an individual _Get question by id_
    request does.

    ```
    curl \
      -H 'Authorization: Token token=\"8af9a3412559d803707937250dc1569d\"' \
      https://app.coderpad.io/api/questions?sort=updated_at,desc

     ```

    `index` takes an optional `sort` parameter, which allows you to sort by either the `created_at` or
    `updated_at` fields on the questions. Adding a comma will allow you to change the sort direction,
    which is `desc` by default. For example, to sort your questions by `updated_at` from oldest to
    newest, specify `updated_at,asc`.

    If no `sort` parameter is provided, `created_at,desc` is assumed.

    The method also returns paginated results - no more than 50 per request. If you want more, follow
    the `next_page` or `prev_page` urls if present. The API also returns a `total` count to give you a
    sense of how many questions exist.

    ``` json
    {
      \"status\": \"OK\",
      \"questions\": [
        // ... your questions, with the same data format as in `show`
      ],
      \"next_page\": \"https://app.coderpad.io/api/question?sort=updated_at,desc&page=2\",
      \"total\": 420
    }

     ```

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetApiQuestionsResponse200
    """
    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[GetApiQuestionsResponse200]:
    r"""Retrieve a list of questions

     Fetch a list of all of your questions. Returns all fields that an individual _Get question by id_
    request does.

    ```
    curl \
      -H 'Authorization: Token token=\"8af9a3412559d803707937250dc1569d\"' \
      https://app.coderpad.io/api/questions?sort=updated_at,desc

     ```

    `index` takes an optional `sort` parameter, which allows you to sort by either the `created_at` or
    `updated_at` fields on the questions. Adding a comma will allow you to change the sort direction,
    which is `desc` by default. For example, to sort your questions by `updated_at` from oldest to
    newest, specify `updated_at,asc`.

    If no `sort` parameter is provided, `created_at,desc` is assumed.

    The method also returns paginated results - no more than 50 per request. If you want more, follow
    the `next_page` or `prev_page` urls if present. The API also returns a `total` count to give you a
    sense of how many questions exist.

    ``` json
    {
      \"status\": \"OK\",
      \"questions\": [
        // ... your questions, with the same data format as in `show`
      ],
      \"next_page\": \"https://app.coderpad.io/api/question?sort=updated_at,desc&page=2\",
      \"total\": 420
    }

     ```

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetApiQuestionsResponse200]
    """
    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
) -> GetApiQuestionsResponse200 | None:
    r"""Retrieve a list of questions

     Fetch a list of all of your questions. Returns all fields that an individual _Get question by id_
    request does.

    ```
    curl \
      -H 'Authorization: Token token=\"8af9a3412559d803707937250dc1569d\"' \
      https://app.coderpad.io/api/questions?sort=updated_at,desc

     ```

    `index` takes an optional `sort` parameter, which allows you to sort by either the `created_at` or
    `updated_at` fields on the questions. Adding a comma will allow you to change the sort direction,
    which is `desc` by default. For example, to sort your questions by `updated_at` from oldest to
    newest, specify `updated_at,asc`.

    If no `sort` parameter is provided, `created_at,desc` is assumed.

    The method also returns paginated results - no more than 50 per request. If you want more, follow
    the `next_page` or `prev_page` urls if present. The API also returns a `total` count to give you a
    sense of how many questions exist.

    ``` json
    {
      \"status\": \"OK\",
      \"questions\": [
        // ... your questions, with the same data format as in `show`
      ],
      \"next_page\": \"https://app.coderpad.io/api/question?sort=updated_at,desc&page=2\",
      \"total\": 420
    }

     ```

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetApiQuestionsResponse200
    """
    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
