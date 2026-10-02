OpenAPI Spec
============

The canonical, community-maintained specification lives in `coderpad-openapi`_.
This SDK consumes ``spec/openapi.json`` through the ``spec`` Git submodule.
The Git tree records an immutable commit, initially ``e1d67d75cc8fde40ee1f0f382793b2172302c6e3``.
The shared repository preserves the original MIT license in ``spec/LICENSE``.

.. _coderpad-openapi: https://github.com/adamtheturtle/coderpad-openapi

Initialize the dependency before running tests:

.. code-block:: console

   $ git submodule update --init spec

CI resolves the submodule during checkout.
Tests and documentation examples read the local file without downloading it.
Installed SDK operations do not depend on the specification.

The original specification was created from the CoderPad API at ``https://app.coderpad.io``.

The spec was exported using Postman's export to OpenAPI feature.

The exported spec required manual corrections.
Postman's export grouped the ``PUT`` (modify pad) operation under the ``/api/pads/`` collection path instead of ``/api/pads/{id}``.
This was because the Postman collection used a literal URL rather than a ``:id`` path variable.
The spec has been corrected to place the ``PUT`` operation under ``/api/pads/{id}``.

The shared spec also includes the question variant endpoints, which are absent from the Postman export.
These additions describe JSON requests, starter files, and response fields that accept null values in the live API.
Project variants return ``language: null`` and identify their environment using project template metadata.

Updating the specification pin
------------------------------

Propose API contract changes in ``coderpad-openapi`` first.
After those changes are reviewed and merged, update this consumer to a reviewed full commit SHA:

.. code-block:: console

   $ git -C spec fetch origin
   $ git -C spec checkout REVIEWED_COMMIT_SHA
   $ git add spec
   $ uv run --group=dev pytest

Review the upstream diff with any SDK model or request changes.
Commit the new pin together with the relevant synthetic regression tests.
After pulling a pin update, run ``git submodule update --init spec`` again.
Do not maintain a separate root ``openapi.json`` here.

Preparing an upstream refresh
-----------------------------

CoderPad does not publish a stable OpenAPI download URL.
To prepare a proposed shared specification refresh:

#. Export the Interview API collection from Postman as OpenAPI JSON.
#. Run the maintainer script against that export:

   .. code-block:: console

      $ python scripts/sync_openapi.py /path/to/postman-export.json --target /tmp/normalized-openapi.json

   The script requires an explicit output path and applies the known Postman path correction above.
   It does not change the specification pin.
#. Compare the output with the shared specification and propose the reviewed changes in ``coderpad-openapi``.
   Retain the manually maintained question variant paths and component schema definitions that the export lacks.
#. After the shared changes merge, update the pin here and keep the empirically observed response fields below and synthetic fixtures in sync.

Empirically observed response fields
------------------------------------

CoderPad responses can include fields that are not currently described by the published specification.
The client preserves the following structures observed in live API responses:

* binary pad-environment files, whose ``contents`` value is ``null``;
* project question variants, whose ``language`` value is ``null`` and whose environment is identified by project template metadata;
* pad interviewer-access restrictions and interviewer notifications;
* question custom databases and their structured table definitions; and
* organization identifiers and raw child-organization mappings.

The organization SSO sign-in URL is also conditional and may be omitted when single sign-on is not supported.
These extensions are covered by synthetic fixtures so that no account-specific response data is stored in the project.

Changelog and review process
----------------------------

When a maintainer adds support for a new undocumented response or request shape, the pull request should include:

* a towncrier news fragment describing the user-visible parsing or typing change;
* a reviewed shared specification change and pin update for any API contract changes;
* an update to the empirically observed response fields list above; and
* synthetic regression tests (see :doc:`contributing`).
