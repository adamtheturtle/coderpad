OpenAPI Spec
============

The OpenAPI spec used to generate this library was created from the CoderPad API at ``https://api.interview.coderpad.io``.

The spec was exported using Postman's export to OpenAPI feature.

The exported spec required manual corrections.
Postman's export grouped the ``PUT`` (modify pad) operation under the ``/api/pads/`` collection path instead of ``/api/pads/{id}``.
This was because the Postman collection used a hardcoded URL rather than a ``:id`` path variable.
The spec has been corrected to place the ``PUT`` operation under ``/api/pads/{id}``.
