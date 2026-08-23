#!/usr/bin/env python3
"""Normalize a Postman-exported OpenAPI document into ``openapi.json``.

CoderPad does not publish a stable OpenAPI URL. Maintainers export the
Interview API collection from Postman, then run this script to apply the
known path corrections described in ``docs/source/openapi-spec.rst`` and
write the result to the repository root.
"""

from __future__ import annotations

import sys
from pathlib import Path

from coderpad._openapi_sync import run_sync

_REPO_ROOT = Path(__file__).resolve().parents[1]

if __name__ == "__main__":
    raise SystemExit(run_sync(arguments=sys.argv[1:], repo_root=_REPO_ROOT))
