"""Tests for the OpenAPI sync maintainer helpers."""

import json
from pathlib import Path

import pytest

from coderpad._openapi_sync import apply_postman_corrections, run_sync


def test_apply_postman_corrections_moves_put() -> None:
    """A PUT under ``/api/pads/`` is moved to ``/api/pads/{id}``."""
    paths: dict[str, dict[str, object]] = {
        "/api/pads/": {
            "get": {"summary": "list"},
            "put": {"summary": "modify"},
        },
        "/api/pads/{id}": {
            "get": {"summary": "get one"},
        },
    }
    document: dict[str, object] = {
        "openapi": "3.0.0",
        "paths": paths,
    }
    notes = apply_postman_corrections(spec=document)
    assert any("Moved PUT" in note for note in notes)
    assert "put" not in paths["/api/pads/"]
    pad_item = paths["/api/pads/{id}"]
    put_operation = pad_item["put"]
    assert isinstance(put_operation, dict)
    assert put_operation["summary"] == "modify"


def test_main_writes_normalized_spec(tmp_path: Path) -> None:
    """The CLI writes a corrected OpenAPI document to the target path."""
    source = tmp_path / "export.json"
    target = tmp_path / "openapi.json"
    source.write_text(
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
        argv=[str(object=source), "--target", str(object=target)],
        repo_root=tmp_path,
    )
    assert exit_code == 0
    written = json.loads(s=target.read_text(encoding="utf-8"))
    assert "put" in written["paths"]["/api/pads/{id}"]


def test_main_rejects_non_object_root(tmp_path: Path) -> None:
    """A non-object OpenAPI root fails fast."""
    source = tmp_path / "export.json"
    source.write_text(data="[]", encoding="utf-8")
    with pytest.raises(expected_exception=SystemExit):
        run_sync(
            argv=[
                str(object=source),
                "--target",
                str(object=tmp_path / "out"),
            ],
            repo_root=tmp_path,
        )
