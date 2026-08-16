Changelog
=========

.. towncrier release notes start

2026.08.16
----------

- Add typed synchronous and asynchronous CoderPad Screen clients covering
  campaigns, invitations, tests, reports, pagination, regions, and webhooks.

- Add synchronous and asynchronous organization user listing, with optional
  server-side email filtering.

- Validate client form requests against request-body definitions in the bundled
  OpenAPI specification during tests.

- API resource types are now strict, frozen Pydantic v2 models.  Responses are
  validated with ``model_validate`` and request models support
  ``model_dump``.  Beartype continues to provide runtime type checking
  alongside Pydantic.

2026.07.24
----------

- Expose the optional ``ai_assist_custom_system_prompt`` field on question
  responses so custom AI Assist prompts can be read and synchronized.

2026.07.22.1
------------

- Add ``ai_assist_custom_system_prompt`` to ``questions.update`` so AI Assist
  system prompts can be synchronized for existing questions.

2026.07.22
----------

- Add synchronous and asynchronous support for retrieving and replaying per-file pad editor history.

- Support empirically observed API response variants for binary files, organization metadata, pad interviewer notifications, and question custom databases.

- Add an ``ai_assist_custom_system_prompt`` parameter to ``questions.create``
  to configure AI Assist's system prompt for a question.

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
