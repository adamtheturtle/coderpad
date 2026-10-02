"""Maintainer helpers for preparing shared OpenAPI changes for review."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import TypeGuard

from beartype import beartype
from beartype.door import TypeHint

from coderpad.json_types import JsonValue

_PADS_COLLECTION_PATH = "/api/pads/"
_PADS_ITEM_PATH = "/api/pads/{id}"


class _Arguments(argparse.Namespace):
    """Parsed command-line arguments."""

    source: Path
    target: Path


@beartype
def _is_object_mapping(value: object, /) -> TypeGuard[dict[str, JsonValue]]:
    """Return whether a JSON value is an object mapping."""
    return TypeHint(hint=dict[str, JsonValue]).is_bearable(obj=value)


@beartype
def _as_string_key_mapping(value: object, /) -> dict[str, JsonValue] | None:
    """Return a mapping when ``value`` is a JSON object."""
    if not _is_object_mapping(value):
        return None
    return value


@beartype
def apply_postman_corrections(spec: dict[str, JsonValue]) -> list[str]:
    """Move a misplaced ``PUT`` onto ``/api/pads/{id}``.

    Postman exports have historically placed the modify-pad ``PUT`` under
    the ``/api/pads/`` collection path instead of ``/api/pads/{id}``.

    Args:
        spec: An OpenAPI document dictionary.

    Returns:
        Human-readable notes describing applied corrections.
    """
    notes: list[str] = []
    paths_value = spec.get("paths")
    if not _is_object_mapping(paths_value):
        return notes
    collection_value = paths_value.get(_PADS_COLLECTION_PATH)
    if not _is_object_mapping(collection_value):
        return notes
    put_operation: JsonValue = collection_value.pop("put", None)
    if put_operation is None:
        return notes
    target_value = paths_value.get(_PADS_ITEM_PATH)
    if not _is_object_mapping(target_value):
        paths_value[_PADS_ITEM_PATH] = {"put": put_operation}
        notes.append(
            f"Replaced non-object {_PADS_ITEM_PATH} and installed PUT",
        )
        return notes
    if "put" in target_value:
        notes.append(
            f"Removed duplicate PUT from {_PADS_COLLECTION_PATH}; "
            f"{_PADS_ITEM_PATH} already defines put",
        )
        return notes
    target_value["put"] = put_operation
    notes.append(
        f"Moved PUT from {_PADS_COLLECTION_PATH} to {_PADS_ITEM_PATH}",
    )
    return notes


@beartype
def run_sync(*, arguments: list[str]) -> int:
    """Run the OpenAPI sync entry point.

    Args:
        arguments: Command-line arguments excluding the program name.

    Returns:
        Process exit code.
    """
    parser = argparse.ArgumentParser(
        description=(
            "Normalize a Postman-exported CoderPad OpenAPI document "
            "for review in adamtheturtle/coderpad-openapi."
        ),
    )
    _ = parser.add_argument(
        "source",
        type=Path,
        help="Path to a Postman-exported OpenAPI JSON file",
    )
    _ = parser.add_argument(
        "--target",
        type=Path,
        required=True,
        help="Output path for the normalized export to review",
    )
    args = parser.parse_args(args=arguments, namespace=_Arguments())
    loaded: object = json.loads(s=args.source.read_text(encoding="utf-8"))
    spec = _as_string_key_mapping(loaded)
    if spec is None:
        message = "OpenAPI document root must be a JSON object"
        raise SystemExit(message)
    notes = apply_postman_corrections(spec=spec)
    _ = args.target.write_text(
        data=json.dumps(obj=spec, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    for note in notes:
        _ = sys.stderr.write(f"{note}\n")
    if not bool(notes):
        _ = sys.stderr.write("No Postman path corrections needed.\n")
    _ = sys.stderr.write(
        "Review contract changes in adamtheturtle/coderpad-openapi. "
        "Retain manually maintained question variant definitions.\n",
    )
    _ = sys.stdout.write(f"{args.target}\n")
    return 0
