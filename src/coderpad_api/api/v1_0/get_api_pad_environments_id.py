from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_api_pad_environments_id_response_200 import (
    GetApiPadEnvironmentsIdResponse200,
)
from ...types import Response


def _get_kwargs(
    id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/pad_environments/{id}".format(
            id=quote(str(id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> GetApiPadEnvironmentsIdResponse200 | None:
    if response.status_code == 200:
        response_200 = GetApiPadEnvironmentsIdResponse200.from_dict(
            response.json()
        )

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[GetApiPadEnvironmentsIdResponse200]:
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
) -> Response[GetApiPadEnvironmentsIdResponse200]:
    r"""Retrieve pad environment information

     Returns detail about a particular pad environment. Doing a straightforward curl like so:

    ```
    curl \
      -H 'Authorization: Token token=\"8af9a3412559d803707937250dc1569d\"' \
      https://app.coderpad.io/api/pad_environments/42

     ```

    Yields:
    ``` json
    {
      \"status\": \"OK\",
      \"id\": 1,
      \"pad_id\": 3,
      \"question_id\": null,
      \"example_question_id\": null,
      \"language\": \"ruby\",
      \"file_contents\": [
        {
          \"path\": \"coderpad/main.rb\",
          \"contents\": \"5.times do\n  puts 'Hello, World!'\nend\n\"
        }
      ],
      \"created_at\": \"2022-09-12T13:49:45.390-07:00\",
      \"updated_at\": \"2022-09-12T13:50:42.058-07:00\"
    }

     ```

    Fields returned:

    | Field | Description |
    | --- | --- |
    | id | `string` Primary key for the object. Use this to query or modify this resource later. |
    | pad_id | `string` The pad this environment belongs to. |
    | question_id | `string` If this is a question environment, this is the identifier for the question,
    otherwise null. |
    | example_question_id | `string` If you used one of CoderPad's example questions in the pad
    environment, the ID will be listed in this field. Example: `examples/035-django-shopping-list`. |
    | language | `string` Chosen language for the pad environment. One of a [set list](#Languages). |
    | file_contents | `object` Returns latest contents of pad environment. Note: If the environment
    language is a multi-file framework or project, for each file in the project a separate object with
    “path\", ”contents”, and “history” will be returned. See the `file_contents` object table below for
    more info. |
    | created_at | `datetime` When the environment was created, in UTC ISO 8601, like
    `2015-01-30T00:22:55.520Z`. |
    | updated_at | `datetime` Similarly, when the environment was last updated. |

    The **file_contents** field contains information about the files associated with the environment. It
    is represented as an array of objects with the following fields:

    | Field | Description |
    | --- | --- |
    | path | `string` The path to the file. |
    | contents | `string` Initial contents of the file. Defaults to the example code for the
    language/file combination. |
    | history (optional) | `string` A URL that displays a JSON file that contains pad history
    information. This field will only be available once edits have been made to the pad. |

    All values returned by this endpoint are real-time as of the moment you request them.

    Args:
        id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetApiPadEnvironmentsIdResponse200]
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
) -> GetApiPadEnvironmentsIdResponse200 | None:
    r"""Retrieve pad environment information

     Returns detail about a particular pad environment. Doing a straightforward curl like so:

    ```
    curl \
      -H 'Authorization: Token token=\"8af9a3412559d803707937250dc1569d\"' \
      https://app.coderpad.io/api/pad_environments/42

     ```

    Yields:
    ``` json
    {
      \"status\": \"OK\",
      \"id\": 1,
      \"pad_id\": 3,
      \"question_id\": null,
      \"example_question_id\": null,
      \"language\": \"ruby\",
      \"file_contents\": [
        {
          \"path\": \"coderpad/main.rb\",
          \"contents\": \"5.times do\n  puts 'Hello, World!'\nend\n\"
        }
      ],
      \"created_at\": \"2022-09-12T13:49:45.390-07:00\",
      \"updated_at\": \"2022-09-12T13:50:42.058-07:00\"
    }

     ```

    Fields returned:

    | Field | Description |
    | --- | --- |
    | id | `string` Primary key for the object. Use this to query or modify this resource later. |
    | pad_id | `string` The pad this environment belongs to. |
    | question_id | `string` If this is a question environment, this is the identifier for the question,
    otherwise null. |
    | example_question_id | `string` If you used one of CoderPad's example questions in the pad
    environment, the ID will be listed in this field. Example: `examples/035-django-shopping-list`. |
    | language | `string` Chosen language for the pad environment. One of a [set list](#Languages). |
    | file_contents | `object` Returns latest contents of pad environment. Note: If the environment
    language is a multi-file framework or project, for each file in the project a separate object with
    “path\", ”contents”, and “history” will be returned. See the `file_contents` object table below for
    more info. |
    | created_at | `datetime` When the environment was created, in UTC ISO 8601, like
    `2015-01-30T00:22:55.520Z`. |
    | updated_at | `datetime` Similarly, when the environment was last updated. |

    The **file_contents** field contains information about the files associated with the environment. It
    is represented as an array of objects with the following fields:

    | Field | Description |
    | --- | --- |
    | path | `string` The path to the file. |
    | contents | `string` Initial contents of the file. Defaults to the example code for the
    language/file combination. |
    | history (optional) | `string` A URL that displays a JSON file that contains pad history
    information. This field will only be available once edits have been made to the pad. |

    All values returned by this endpoint are real-time as of the moment you request them.

    Args:
        id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetApiPadEnvironmentsIdResponse200
    """
    return sync_detailed(
        id=id,
        client=client,
    ).parsed


async def asyncio_detailed(
    id: str,
    *,
    client: AuthenticatedClient,
) -> Response[GetApiPadEnvironmentsIdResponse200]:
    r"""Retrieve pad environment information

     Returns detail about a particular pad environment. Doing a straightforward curl like so:

    ```
    curl \
      -H 'Authorization: Token token=\"8af9a3412559d803707937250dc1569d\"' \
      https://app.coderpad.io/api/pad_environments/42

     ```

    Yields:
    ``` json
    {
      \"status\": \"OK\",
      \"id\": 1,
      \"pad_id\": 3,
      \"question_id\": null,
      \"example_question_id\": null,
      \"language\": \"ruby\",
      \"file_contents\": [
        {
          \"path\": \"coderpad/main.rb\",
          \"contents\": \"5.times do\n  puts 'Hello, World!'\nend\n\"
        }
      ],
      \"created_at\": \"2022-09-12T13:49:45.390-07:00\",
      \"updated_at\": \"2022-09-12T13:50:42.058-07:00\"
    }

     ```

    Fields returned:

    | Field | Description |
    | --- | --- |
    | id | `string` Primary key for the object. Use this to query or modify this resource later. |
    | pad_id | `string` The pad this environment belongs to. |
    | question_id | `string` If this is a question environment, this is the identifier for the question,
    otherwise null. |
    | example_question_id | `string` If you used one of CoderPad's example questions in the pad
    environment, the ID will be listed in this field. Example: `examples/035-django-shopping-list`. |
    | language | `string` Chosen language for the pad environment. One of a [set list](#Languages). |
    | file_contents | `object` Returns latest contents of pad environment. Note: If the environment
    language is a multi-file framework or project, for each file in the project a separate object with
    “path\", ”contents”, and “history” will be returned. See the `file_contents` object table below for
    more info. |
    | created_at | `datetime` When the environment was created, in UTC ISO 8601, like
    `2015-01-30T00:22:55.520Z`. |
    | updated_at | `datetime` Similarly, when the environment was last updated. |

    The **file_contents** field contains information about the files associated with the environment. It
    is represented as an array of objects with the following fields:

    | Field | Description |
    | --- | --- |
    | path | `string` The path to the file. |
    | contents | `string` Initial contents of the file. Defaults to the example code for the
    language/file combination. |
    | history (optional) | `string` A URL that displays a JSON file that contains pad history
    information. This field will only be available once edits have been made to the pad. |

    All values returned by this endpoint are real-time as of the moment you request them.

    Args:
        id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetApiPadEnvironmentsIdResponse200]
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
) -> GetApiPadEnvironmentsIdResponse200 | None:
    r"""Retrieve pad environment information

     Returns detail about a particular pad environment. Doing a straightforward curl like so:

    ```
    curl \
      -H 'Authorization: Token token=\"8af9a3412559d803707937250dc1569d\"' \
      https://app.coderpad.io/api/pad_environments/42

     ```

    Yields:
    ``` json
    {
      \"status\": \"OK\",
      \"id\": 1,
      \"pad_id\": 3,
      \"question_id\": null,
      \"example_question_id\": null,
      \"language\": \"ruby\",
      \"file_contents\": [
        {
          \"path\": \"coderpad/main.rb\",
          \"contents\": \"5.times do\n  puts 'Hello, World!'\nend\n\"
        }
      ],
      \"created_at\": \"2022-09-12T13:49:45.390-07:00\",
      \"updated_at\": \"2022-09-12T13:50:42.058-07:00\"
    }

     ```

    Fields returned:

    | Field | Description |
    | --- | --- |
    | id | `string` Primary key for the object. Use this to query or modify this resource later. |
    | pad_id | `string` The pad this environment belongs to. |
    | question_id | `string` If this is a question environment, this is the identifier for the question,
    otherwise null. |
    | example_question_id | `string` If you used one of CoderPad's example questions in the pad
    environment, the ID will be listed in this field. Example: `examples/035-django-shopping-list`. |
    | language | `string` Chosen language for the pad environment. One of a [set list](#Languages). |
    | file_contents | `object` Returns latest contents of pad environment. Note: If the environment
    language is a multi-file framework or project, for each file in the project a separate object with
    “path\", ”contents”, and “history” will be returned. See the `file_contents` object table below for
    more info. |
    | created_at | `datetime` When the environment was created, in UTC ISO 8601, like
    `2015-01-30T00:22:55.520Z`. |
    | updated_at | `datetime` Similarly, when the environment was last updated. |

    The **file_contents** field contains information about the files associated with the environment. It
    is represented as an array of objects with the following fields:

    | Field | Description |
    | --- | --- |
    | path | `string` The path to the file. |
    | contents | `string` Initial contents of the file. Defaults to the example code for the
    language/file combination. |
    | history (optional) | `string` A URL that displays a JSON file that contains pad history
    information. This field will only be available once edits have been made to the pad. |

    All values returned by this endpoint are real-time as of the moment you request them.

    Args:
        id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetApiPadEnvironmentsIdResponse200
    """
    return (
        await asyncio_detailed(
            id=id,
            client=client,
        )
    ).parsed
