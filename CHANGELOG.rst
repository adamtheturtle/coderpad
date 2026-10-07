Changelog
=========

.. towncrier release notes start

2026.10.07
----------

- Use a pinned ``coderpad-openapi`` Git submodule for the API contract.
  Contributors must initialize ``spec`` before running tests.
  The Postman normalization script now requires an explicit ``--target`` for changes proposed to the shared specification.

- Create Screen campaigns with typed question selections and optional settings that preserve team defaults.

- Add Screen question library reads, filtered pagination, and typed creation and updates.
  Keep response metadata separate from writable fields and preserve creation Location headers.

- Retrieve typed Screen question usage, answer, test-case, and score distribution insights.

- Upload raw Screen project archive bytes with exact content length, the 52428800 byte size limit, and typed temporary-file identifiers.

- Retrieve typed candidate Screen AI Assist conversations and preserve structured message output.

- Download candidate Screen project archives as binary ``tar.gz`` data with synchronous and asynchronous clients.

- Decode UUID question reports alongside integer question summaries.
  Expose typed answers, evaluations, warnings, session timers, and recruiter activity indicators.

- Add the optional ``allow_duplicate_invitations`` Screen invitation policy.
  Preserve omission and explicit false or true in both clients.

- Add typed Interview ``user.get()`` and Screen ``me()`` account introspection to both synchronous and asynchronous clients.

- Support pad access lists, ownership, waiting-room and execution controls, and take-home, team, and AI Assist creation settings.

- Preserve optional Interview highlights, structured outlines, transcripts, transcript availability, and review reports on pad retrieval.

- Add optional question sharing and custom database association to create and update requests in both clients.

- Preserve parent-question starter file overlays and variant summaries, including hidden files and template removals.

- Preserve candidate instruction step names in responses and question writes.
  Omit unnamed steps from the JSON name field.

- Filter and incrementally enumerate Interview questions, including repeatable pad types and question-specific title and usage sorting.

- Use ``https://screen.coderpad.io`` as the default US Screen API origin.
  Explicit base URL overrides and the EU origin remain supported.

- Follow opaque pad cursors and exact legacy page links while keeping API credentials scoped to the configured origin.

- Allow manual Screen invitations without candidate email or name.
  Require an address only when email delivery is explicitly enabled.

2026.10.01.1
------------

- Add directory uploads to synchronous and asynchronous question creation and updates, preserving ZIP importer behavior without temporary archives.

2026.10.01
----------

- Accept null languages in project question variant responses, preserving their template metadata and starter files in both synchronous and asynchronous clients.
  Document the question variant endpoints and their request and response schema definitions in the bundled OpenAPI spec.

2026.09.30
----------

- Validate paginated API response shapes before constructing client models.

- Type context manager traceback arguments precisely.

- Type decoded API error bodies using the shared JSON value domain.

- Validate CoderPad Screen response bodies as JSON values before decoding them.

- Add JSON question variant CRUD to the synchronous and asynchronous clients, including template files and distinct omitted, blank, and default starter-code states.

2026.09.07
----------

- Removed ``client.quota.get()``.
  Use ``client.organization.get_quota()``, which it only delegated to.

- Removed ``PadHistory.replay_to_file`` and ``coderpad.screen.save_screen_report``.
  Callers can write replayed contents or report bytes with ``pathlib.Path`` directly.

- Add synchronous and asynchronous HTTPX2 transports while retaining HTTPX as the default client family.

2026.08.23
----------

- Add ``pads.all()`` to iterate Interview pads across paginated responses.

- Add ``screen.tests.all()`` to iterate Screen tests across paginated responses.

- Expose ``prev_page`` on Interview API ``PaginatedList`` responses.

- Interview API types such as ``Pad``, ``Question``, and ``Language`` are now available from ``coderpad``.

- Exception classes such as ``CoderPadError`` and ``NotFoundError`` are now available from ``coderpad``.

- Documented which ``Question`` and ``Pad`` fields are writable versus read-only in a new "Writable and read-only fields" reference page.

- Validate that ``contents``, ``file_contents``, and ``zip_file`` are mutually exclusive on question create/update.

- Support configurable ``httpx`` timeouts on ``CoderPad`` and ``AsyncCoderPad``.

- Parse JSON API error bodies into optional ``CoderPadError.code`` and ``CoderPadError.message`` attributes.

- Added ``BadGatewayError``, ``ServiceUnavailableError``, and ``GatewayTimeoutError`` for HTTP 502, 503, and 504 responses.

- Defer Screen namespace initialization until first access on CoderPad clients.

- Fail fast with a clear error when Screen methods are called without a ``screen_api_key``.

- Support custom default headers on ``CoderPad`` and ``AsyncCoderPad``.

- Support configuring an ``httpx`` proxy on ``CoderPad`` and ``AsyncCoderPad``.

- Bump PyPI development status classifier from Planning to Beta.

- Fixed the README minimum Python version badge to match ``requires-python`` (3.12).

- Add Screen API usage documentation.

- Document the exception hierarchy in the Sphinx API reference.

- Add ``save_screen_report`` to write Screen report bytes to a file.

- ``SortOrder`` is now a ``StrEnum``, so its values work directly as query strings.

- ``Language`` is now a ``StrEnum``, so its values work directly in API requests.

- Add ``scripts/sync_openapi.py`` to normalize Postman OpenAPI exports into the bundled ``openapi.json``.

- Load API keys from ``CODERPAD_API_KEY`` and ``CODERPAD_SCREEN_API_KEY`` via ``from_env()``.

- ``PaginatedList`` and ``ScreenTestsPage`` now include concise ``__repr__`` output for debugging.

- Add ``tests.report_json`` (sync and async) returning a typed ``ScreenReport`` from the Screen test session payload.

- Document the public API stability policy.

- Add ``PadHistory.replay_to_file`` to write replayed editor contents to disk.

- Support configuring ``httpx`` connection pool limits on CoderPad clients.

- Document the maintainer workflow for empirically observed API variants and link it to towncrier news fragments and the API drift issue template.

- Add ``client.quota.get()`` as an alias for ``client.organization.get_quota()``.

- Validate that Screen invitations include ``candidate_email`` and ``candidate_name`` before send.

2026.08.16
----------

- Add typed synchronous and asynchronous CoderPad Screen clients covering campaigns, invitations, tests, reports, pagination, regions, and webhooks.

- Add synchronous and asynchronous organization user listing, with optional server-side email filtering.

- Validate client form requests against request-body definitions in the bundled OpenAPI specification during tests.

- API resource types are now strict, frozen Pydantic v2 models.
  Responses are validated with ``model_validate`` and request models support ``model_dump``.
  Beartype continues to provide runtime type checking alongside Pydantic.

2026.07.24
----------

- Expose the optional ``ai_assist_custom_system_prompt`` field on question responses so custom AI Assist prompts can be read and synchronized.

2026.07.22.1
------------

- Add ``ai_assist_custom_system_prompt`` to ``questions.update`` so AI Assist system prompts can be synchronized for existing questions.

2026.07.22
----------

- Add synchronous and asynchronous support for retrieving and replaying per-file pad editor history.

- Support empirically observed API response variants for binary files, organization metadata, pad interviewer notifications, and question custom databases.

- Add an ``ai_assist_custom_system_prompt`` parameter to ``questions.create`` to configure AI Assist's system prompt for a question.

2026.06.29
----------

- Add a ``candidate_instructions`` parameter to ``questions.create`` and ``questions.update`` so progressively-revealed candidate instruction blocks can be authored via the API.

2026.05.04
----------


2026.04.01
----------


2026.03.31.2
------------


- Removed support for Python 3.11.
- Changed default ``base_url`` from ``https://api.interview.coderpad.io`` to ``https://app.coderpad.io``.

2026.03.31.1
------------


2026.03.31
----------


2026.03.29.1
------------


2026.03.29
----------
