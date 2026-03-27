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
        "url": "/api/pads/{id}".format(
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
    r"""Retrieve a pad by id

     Returns detail about a particular pad. Doing a straightforward curl like so:

    ```
    curl \
      -H 'Authorization: Token token=\"c\"' \
      https://app.coderpad.io/api/pads/DM32JWG2

     ```

    Yields:
    ``` json
    {
      status: \"OK\",
      id: \"DM32JWG2\",
      title: \"Ruby Test\",
      owner_email: \"fbueller@gmail.com\",
      language: \"ruby\",
      participants: [
        \"vincent\",
        \"Guest 405\"
      ],
      contents: \"5.times do\n  puts 'Hello, World!'\nend\n\",
      notes: \"Greg was a *very* gregarious candidate, whom...\"
      events: \"https://app.coderpad.io/api/pads/DM32JWG2/events\",
      private: false,
      execution_enabled: true,
      created_at: \"2014-11-14T03:02:45Z\",
      updated_at: \"2014-11-14T03:06:39Z\",
      ended_at:   \"2014-11-14T03:06:39Z\",
      url: \"https://coderpad.io/DM32JWG2\",
      playback: \"https://coderpad.io/DM32JWG2/playback\",
      drawing: \"https://storage.googleapis.com/...\",
      pad_environment_ids: [
        1234567,
        7654321
      ],
      active_environment_id: 1234567,
      team: {
        id: \"68264172-5a54-4ac3-962b-cb8d1ad15d05\",
        name: \"Main Team\"
      }
    }

     ```

    Fields returned:

    | **Field** | **Description** |
    | --- | --- |
    | id | `string` Primary key for the object. Use this to query or modify this resource later. |
    | title | `string` User-assigned title of the pad. |
    | owner_email | `string` Email address of the owner of the pad. Will usually just be your email! |
    | language | `string` Chosen language for the pad. [Full list is here](#Languages). |
    | participants | `array` The self-reported names of the participants. |
    | contents | `string` Latest contents of the pad editor. Updates in real-time. For pads that support
    multiple environments, this will be nil, and you can get the contents for each environment at the
    pad_environments endpoint. |
    | notes | `string` Markdown-formatted notes taken by the interviewer. |
    | events | `string` A link to an API endpoint containing a log of events created by users during the
    pad session. [See <i>Get a list of pad events</i> below.](#c1a6a910-8b73-4f56-a929-3947c571af35). |
    | private | `boolean` Whether the pad is viewable by guests, ie whether the [waiting
    room](https://coderpad.io/resources/docs/interview/pads/settings/#waiting-room) is enabled or not.
    Private pads will essentially 404 unless you are authorized to view the pad. Defaults to `false`. |
    | execution_enabled | `boolean` Whether to allow running code in this pad. When set to false, this
    hides the right-hand side of the pad interface. Defaults to `true`. |
    | created_at | `datetime` When the pad was created, in UTC ISO 8601, like
    `2015-01-30T00:22:55.520Z`. |
    | updated_at | `datetime` Similarly, when the pad was last updated. |
    | ended_at | `datetime` The time when the interview was ended. `null` if it has not ended yet. |
    | url | `string` Convenience field to link human users to the editing interface for this pad. |
    | playback | `string` Convenience field to link human users to the playback interface for this pad.
    |
    | drawing | `string` A URL where you can download the final state of a drawing made with Drawing
    Mode. These URLs are signed URLs that are valid for 5 minutes, after which you will need to make
    another request to our API to get a fresh signed URL. |
    | pad_environment_ids | `array` An array of IDs which can be used to fetch the environment details
    from the pad_environments endpoint. [See <i>Get pad environment information</i>
    below](#4458345f-f2a1-44b1-921b-d79445cbe365). |
    | active_environment_id | `string` The ID of the currently active environment. |
    | question_ids | `string` An array of question Ids for questions used in the pad. |
    | team | `{ id: string, name: string }` An object describing the team the pad is linked to. |

    All values returned by this request are real-time as of the moment you request them.

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
    r"""Retrieve a pad by id

     Returns detail about a particular pad. Doing a straightforward curl like so:

    ```
    curl \
      -H 'Authorization: Token token=\"c\"' \
      https://app.coderpad.io/api/pads/DM32JWG2

     ```

    Yields:
    ``` json
    {
      status: \"OK\",
      id: \"DM32JWG2\",
      title: \"Ruby Test\",
      owner_email: \"fbueller@gmail.com\",
      language: \"ruby\",
      participants: [
        \"vincent\",
        \"Guest 405\"
      ],
      contents: \"5.times do\n  puts 'Hello, World!'\nend\n\",
      notes: \"Greg was a *very* gregarious candidate, whom...\"
      events: \"https://app.coderpad.io/api/pads/DM32JWG2/events\",
      private: false,
      execution_enabled: true,
      created_at: \"2014-11-14T03:02:45Z\",
      updated_at: \"2014-11-14T03:06:39Z\",
      ended_at:   \"2014-11-14T03:06:39Z\",
      url: \"https://coderpad.io/DM32JWG2\",
      playback: \"https://coderpad.io/DM32JWG2/playback\",
      drawing: \"https://storage.googleapis.com/...\",
      pad_environment_ids: [
        1234567,
        7654321
      ],
      active_environment_id: 1234567,
      team: {
        id: \"68264172-5a54-4ac3-962b-cb8d1ad15d05\",
        name: \"Main Team\"
      }
    }

     ```

    Fields returned:

    | **Field** | **Description** |
    | --- | --- |
    | id | `string` Primary key for the object. Use this to query or modify this resource later. |
    | title | `string` User-assigned title of the pad. |
    | owner_email | `string` Email address of the owner of the pad. Will usually just be your email! |
    | language | `string` Chosen language for the pad. [Full list is here](#Languages). |
    | participants | `array` The self-reported names of the participants. |
    | contents | `string` Latest contents of the pad editor. Updates in real-time. For pads that support
    multiple environments, this will be nil, and you can get the contents for each environment at the
    pad_environments endpoint. |
    | notes | `string` Markdown-formatted notes taken by the interviewer. |
    | events | `string` A link to an API endpoint containing a log of events created by users during the
    pad session. [See <i>Get a list of pad events</i> below.](#c1a6a910-8b73-4f56-a929-3947c571af35). |
    | private | `boolean` Whether the pad is viewable by guests, ie whether the [waiting
    room](https://coderpad.io/resources/docs/interview/pads/settings/#waiting-room) is enabled or not.
    Private pads will essentially 404 unless you are authorized to view the pad. Defaults to `false`. |
    | execution_enabled | `boolean` Whether to allow running code in this pad. When set to false, this
    hides the right-hand side of the pad interface. Defaults to `true`. |
    | created_at | `datetime` When the pad was created, in UTC ISO 8601, like
    `2015-01-30T00:22:55.520Z`. |
    | updated_at | `datetime` Similarly, when the pad was last updated. |
    | ended_at | `datetime` The time when the interview was ended. `null` if it has not ended yet. |
    | url | `string` Convenience field to link human users to the editing interface for this pad. |
    | playback | `string` Convenience field to link human users to the playback interface for this pad.
    |
    | drawing | `string` A URL where you can download the final state of a drawing made with Drawing
    Mode. These URLs are signed URLs that are valid for 5 minutes, after which you will need to make
    another request to our API to get a fresh signed URL. |
    | pad_environment_ids | `array` An array of IDs which can be used to fetch the environment details
    from the pad_environments endpoint. [See <i>Get pad environment information</i>
    below](#4458345f-f2a1-44b1-921b-d79445cbe365). |
    | active_environment_id | `string` The ID of the currently active environment. |
    | question_ids | `string` An array of question Ids for questions used in the pad. |
    | team | `{ id: string, name: string }` An object describing the team the pad is linked to. |

    All values returned by this request are real-time as of the moment you request them.

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
