OpenAPI Spec
============

The OpenAPI spec used to generate this library was created from the CoderPad API at ``https://app.coderpad.io``.

The spec was exported using Postman's export to OpenAPI feature.

The exported spec required manual corrections.
Postman's export grouped the ``PUT`` (modify pad) operation under the ``/api/pads/`` collection path instead of ``/api/pads/{id}``.
This was because the Postman collection used a literal URL rather than a ``:id`` path variable.
The spec has been corrected to place the ``PUT`` operation under ``/api/pads/{id}``.

Empirically observed response fields
------------------------------------

CoderPad responses can include fields that are not currently described by
the published specification. The client preserves the following structures
observed in live API responses:

* binary pad-environment files, whose ``contents`` value is ``null``;
* pad interviewer-access restrictions and interviewer notifications;
* question custom databases and their structured table definitions; and
* organization identifiers and raw child-organization mappings.

The organization SSO sign-in URL is also conditional and may be omitted when
single sign-on is not supported. These extensions are covered by synthetic
fixtures so that no account-specific response data is stored in the project.
