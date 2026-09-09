"""Tests for the OpenAPI sync maintainer helpers."""

from __future__ import annotations

import json
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

from coderpad._openapi_sync import apply_postman_corrections, run_sync

if TYPE_CHECKING:
    from coderpad._json_types import JsonValue


def test_apply_postman_corrections_moves_put() -> None:
    """A PUT under ``/api/pads/`` is moved to ``/api/pads/{id}``."""
    collection_path: dict[str, JsonValue] = {
        "get": {"summary": "list"},
        "put": {"summary": "modify"},
    }
    item_path: dict[str, JsonValue] = {
        "get": {"summary": "get one"},
    }
    paths: dict[str, JsonValue] = {
        "/api/pads/": collection_path,
        "/api/pads/{id}": item_path,
    }
    document: dict[str, JsonValue] = {
        "openapi": "3.0.0",
        "paths": paths,
    }
    notes = apply_postman_corrections(spec=document)
    assert any("Moved PUT" in note for note in notes)
    assert "put" not in collection_path
    put_operation = item_path["put"]
    assert isinstance(put_operation, dict)
    assert put_operation.get("summary") == "modify"


def test_apply_postman_corrections_skips_when_paths_missing() -> None:
    """No corrections run when ``paths`` is absent or not an object."""
    assert not bool(apply_postman_corrections(spec={"openapi": "3.0.0"}))
    assert not bool(
        apply_postman_corrections(
            spec={"openapi": "3.0.0", "paths": []},
        )
    )


def test_apply_postman_corrections_skips_when_collection_missing() -> None:
    """No corrections run when the pads collection path is absent."""
    assert not bool(
        apply_postman_corrections(
            spec={
                "openapi": "3.0.0",
                "paths": {"/api/pads/{id}": {"get": {}}},
            },
        )
    )


def test_apply_postman_corrections_skips_when_put_absent() -> None:
    """No corrections run when the collection path has no PUT."""
    assert not bool(
        apply_postman_corrections(
            spec={
                "openapi": "3.0.0",
                "paths": {
                    "/api/pads/": {"get": {}},
                    "/api/pads/{id}": {"get": {}},
                },
            },
        )
    )


def test_apply_postman_corrections_replaces_non_object_item_path() -> None:
    """A non-object pads item path is replaced when installing PUT."""
    paths: dict[str, JsonValue] = {
        "/api/pads/": {"put": {"summary": "modify"}},
        "/api/pads/{id}": "not-an-object",
    }
    notes = apply_postman_corrections(
        spec={"openapi": "3.0.0", "paths": paths},
    )
    assert any("Replaced non-object" in note for note in notes)
    assert paths["/api/pads/{id}"] == {"put": {"summary": "modify"}}


def test_apply_postman_corrections_removes_duplicate_put() -> None:
    """A duplicate collection PUT is dropped when the item already has one."""
    collection_path: dict[str, JsonValue] = {
        "put": {"summary": "duplicate"}
    }
    item_path: dict[str, JsonValue] = {
        "put": {"summary": "canonical"}
    }
    paths: dict[str, JsonValue] = {
        "/api/pads/": collection_path,
        "/api/pads/{id}": item_path,
    }
    notes = apply_postman_corrections(
        spec={"openapi": "3.0.0", "paths": paths},
    )
    assert any("Removed duplicate PUT" in note for note in notes)
    assert "put" not in collection_path
    assert item_path == {"put": {"summary": "canonical"}}


def test_main_writes_normalized_spec(tmp_path: Path) -> None:
    """The sync entry point writes a corrected OpenAPI document."""
    source = tmp_path / "export.json"
    target = tmp_path / "openapi.json"
    _ = source.write_text(
        data=json.dumps(
            obj={
                "openapi": "3.0.0",
                "paths": {
                    "/api/pads/": {"put": {"summary": "modify"}},
                    "/api/pads/{id}": {},
                },
            },
        ),
        encoding="utf-8",
    )
    exit_code = run_sync(
        arguments=[str(object=source), "--target", str(object=target)],
        repo_root=tmp_path,
    )
    assert exit_code == 0
    written = json.loads(s=target.read_text(encoding="utf-8"))
    assert "put" in written["paths"]["/api/pads/{id}"]


def test_main_reports_when_no_corrections_needed(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """The sync entry point reports when no path corrections apply."""
    source = tmp_path / "export.json"
    target = tmp_path / "openapi.json"
    _ = source.write_text(
        data=json.dumps(
            obj={
                "openapi": "3.0.0",
                "paths": {
                    "/api/pads/": {"get": {}},
                    "/api/pads/{id}": {"get": {}},
                },
            },
        ),
        encoding="utf-8",
    )
    exit_code = run_sync(
        arguments=[str(object=source), "--target", str(object=target)],
        repo_root=tmp_path,
    )
    assert exit_code == 0
    captured = capsys.readouterr()
    assert "No Postman path corrections needed." in captured.err


def test_main_rejects_non_object_root(tmp_path: Path) -> None:
    """A non-object OpenAPI root fails fast."""
    source = tmp_path / "export.json"
    _ = source.write_text(data="[]", encoding="utf-8")
    with pytest.raises(expected_exception=SystemExit):
        _ = run_sync(
            arguments=[
                str(object=source),
                "--target",
                str(object=tmp_path / "out"),
            ],
            repo_root=tmp_path,
        )
