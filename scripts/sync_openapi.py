#!/usr/bin/env python3
"""Normalize a Postman-exported OpenAPI document for shared review.

CoderPad does not publish a stable OpenAPI URL. Maintainers export the
Interview API collection from Postman, then run this script to apply the
known path corrections described in ``docs/source/openapi-spec.rst`` and
write the result to an explicit target for review in coderpad-openapi.
"""

from __future__ import annotations

import sys

from coderpad._openapi_sync import run_sync

if __name__ == "__main__":
    raise SystemExit(run_sync(arguments=sys.argv[1:]))
