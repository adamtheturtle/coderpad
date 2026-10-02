"""Prepare real file system sources through the public API."""

import os
from contextlib import ExitStack
from pathlib import Path

import pytest

from coderpad import PreparedSource, prepare_source


def _write_files(*, root: Path, files: dict[str, bytes]) -> None:
    """Build a synthetic tree without replacing file system functions."""
    for name, data in files.items():
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        _ = path.write_bytes(data=data)


def _prepared_files(*, source: PreparedSource) -> dict[str, bytes]:
    """Read selected content while the preparation context is active."""
    assert source.directory is not None
    return {
        name: (source.directory / name).read_bytes() for name in source.files
    }


@pytest.mark.parametrize(
    argnames="data", argvalues=[b"", b"\xef\xbb\xbftext \r\n\r\n"]
)
def test_single_file(tmp_path: Path, data: bytes) -> None:
    """Preserve empty files, BOMs, CRLF, and white space exactly."""
    path = tmp_path / "main.py"
    _ = path.write_bytes(data=data)
    with prepare_source(file=path) as source:
        assert source == PreparedSource(
            contents=data.decode(encoding="utf-8"),
            directory=None,
            files=("main.py",),
        )
    assert path.read_bytes() == data


def test_directory_snapshot(tmp_path: Path) -> None:
    """Preview and upload share a byte-preserving isolated snapshot."""
    expected = {
        ".gitignore": b"*.bin\n",
        ".hidden": b"",
        "nested/data.bin": bytes(range(256)),
        "nested/main.py": b"pass\r\n",
        "archive.zip": b"included by default",
    }
    _write_files(root=tmp_path, files=expected)
    _write_files(
        root=tmp_path,
        files={".git/config": b"never upload", "nested/.git": b"metadata"},
    )
    with prepare_source(directory=tmp_path) as source:
        assert source.contents is None
        assert source.files == tuple(sorted(expected))
        assert _prepared_files(source=source) == expected
        _ = (tmp_path / "nested/main.py").write_bytes(data=b"changed later")
        assert _prepared_files(source=source) == expected
        assert source.directory is not None
        staged = source.directory
    assert staged.exists() is False
    assert (tmp_path / "nested/main.py").read_bytes() == b"changed later"


def test_cleanup_after_caller_failure(tmp_path: Path) -> None:
    """Remove the staging directory even when an upload fails."""
    _write_files(root=tmp_path, files={"main.py": b"pass"})
    staged: Path | None = None
    with (  # noqa: PT012 - Capture the staged path before the caller fails.
        pytest.raises(expected_exception=RuntimeError, match="upload failed"),
        prepare_source(directory=tmp_path) as source,
    ):
        assert source.directory is not None
        staged = source.directory
        msg = "upload failed"
        raise RuntimeError(msg)
    assert staged is not None
    assert staged.exists() is False
    assert (tmp_path / "main.py").read_bytes() == b"pass"


@pytest.mark.parametrize(argnames="worktree", argvalues=[True, False])
def test_inherited_and_nested_rules(tmp_path: Path, *, worktree: bool) -> None:
    """Find the nearest Git root and apply deeper relative negations."""
    root = tmp_path / "repo"
    _write_files(
        root=root,
        files={
            ".git" if worktree else ".git/config": b"synthetic metadata",
            ".gitignore": b"*.tmp\nignored/\n!ignored/\n",
            "project/.gitignore": b"!keep.tmp\n",
            "project/keep.tmp": b"keep",
            "project/drop.tmp": b"drop",
            "project/nested/.gitignore": b"/local.py\n",
            "project/nested/local.py": b"drop",
            "project/local.py": b"keep",
            "project/ignored/keep.py": b"keep",
        },
    )
    with prepare_source(
        directory=root / "project", respect_gitignore=True
    ) as source:
        assert source.files == (
            ".gitignore",
            "ignored/keep.py",
            "keep.tmp",
            "local.py",
            "nested/.gitignore",
        )


def test_non_git_rules(tmp_path: Path) -> None:
    """Ignore unrelated parent rules outside a Git repository."""
    _write_files(
        root=tmp_path,
        files={
            ".gitignore": b"*\n",
            "project/.gitignore": b"*.tmp\ncache/\n",
            "project/main.py": b"keep",
            "project/drop.tmp": b"drop",
            "project/cache/.gitignore": b"!keep.py\n",
            "project/cache/keep.py": b"pruned",
            "project/nested/keep.py": b"keep",
        },
    )
    with prepare_source(
        directory=tmp_path / "project", respect_gitignore=True
    ) as source:
        assert source.files == (".gitignore", "main.py", "nested/keep.py")


def test_final_exclusions(tmp_path: Path) -> None:
    """Final exclusions override ignores but cannot revive pruned
    files.
    """
    _write_files(
        root=tmp_path,
        files={
            ".gitignore": b"*.tmp\n!keep.tmp\n",
            "drop.tmp": b"drop",
            "keep.tmp": b"drop explicitly",
            "keep.zip": b"keep by final negation",
            "drop.zip": b"drop explicitly",
            "main.py": b"keep",
        },
    )
    with prepare_source(
        directory=tmp_path,
        respect_gitignore=True,
        excludes=("keep.tmp", "!drop.tmp", "*.zip", "!keep.zip"),
    ) as source:
        assert source.files == (".gitignore", "keep.zip", "main.py")


@pytest.mark.parametrize(
    argnames="suffix", argvalues=["project", "project/nested"]
)
def test_ignored_upload_root(tmp_path: Path, suffix: str) -> None:
    """Explicit nested roots cannot bypass ignored ancestors."""
    _write_files(
        root=tmp_path,
        files={
            ".git/config": b"synthetic",
            ".gitignore": b"project/\n",
            "project/.gitignore": b"!nested/\n",
            "project/nested/main.py": b"pass",
        },
    )
    with (
        pytest.raises(
            expected_exception=ValueError, match="No files selected"
        ),
        ExitStack() as stack,
    ):
        _ = stack.enter_context(
            cm=prepare_source(
                directory=tmp_path / suffix, respect_gitignore=True
            )
        )


@pytest.mark.parametrize(
    argnames="kind", argvalues=["file", "directory", "broken", "ignore"]
)
def test_selected_symlinks(tmp_path: Path, kind: str) -> None:
    """Selected links and enabled ignore-file links are rejected."""
    root = tmp_path / "source"
    root.mkdir()
    target = tmp_path / "target"
    if kind == "directory":
        target.mkdir()
    elif kind != "broken":
        _ = target.write_bytes(data=b"outside")
    (root / (".gitignore" if kind == "ignore" else "link")).symlink_to(
        target=target, target_is_directory=kind == "directory"
    )
    with (
        pytest.raises(expected_exception=ValueError, match="Symbolic links"),
        ExitStack() as stack,
    ):
        _ = stack.enter_context(
            cm=prepare_source(directory=root, respect_gitignore=True)
        )


@pytest.mark.parametrize(argnames="directory", argvalues=[True, False])
def test_source_symlink_ancestor(tmp_path: Path, *, directory: bool) -> None:
    """Reject links in the supplied source path before resolving it."""
    root = tmp_path / "source"
    _write_files(root=root, files={"main.py": b"pass"})
    link = tmp_path / "alias"
    link.symlink_to(target=root, target_is_directory=True)
    with (
        pytest.raises(expected_exception=ValueError, match="Symbolic links"),
        ExitStack() as stack,
    ):
        _ = stack.enter_context(
            cm=prepare_source(
                directory=link if directory else None,
                file=None if directory else link / "main.py",
            )
        )


def test_ignored_links(tmp_path: Path) -> None:
    """Excluded links are skipped without copying their targets."""
    _write_files(
        root=tmp_path, files={"main.py": b"pass", ".gitignore": b"ignored\n"}
    )
    for name in ("ignored", "excluded", ".git"):
        (tmp_path / name).symlink_to(target=tmp_path / "absent")
    with prepare_source(
        directory=tmp_path, respect_gitignore=True, excludes=("excluded",)
    ) as source:
        assert source.files == (".gitignore", "main.py")


def test_special_file() -> None:
    """Reject a real device before attempting to read it."""
    with (
        pytest.raises(
            expected_exception=ValueError, match="Only regular files"
        ),
        ExitStack() as stack,
    ):
        _ = stack.enter_context(cm=prepare_source(file=Path(os.devnull)))


def test_source_validation(tmp_path: Path) -> None:
    """Reject absent/conflicting sources and file-only exclusions."""
    with (
        pytest.raises(expected_exception=ValueError, match="exactly one"),
        ExitStack() as stack,
    ):
        _ = stack.enter_context(cm=prepare_source())
    with (
        pytest.raises(expected_exception=ValueError, match="exactly one"),
        ExitStack() as stack,
    ):
        _ = stack.enter_context(
            cm=prepare_source(directory=tmp_path, file=tmp_path)
        )
    with (
        pytest.raises(
            expected_exception=ValueError, match="excludes requires"
        ),
        ExitStack() as stack,
    ):
        _ = stack.enter_context(
            cm=prepare_source(file=tmp_path, excludes=("*.py",))
        )
    with (
        pytest.raises(
            expected_exception=ValueError, match="Only regular files"
        ),
        ExitStack() as stack,
    ):
        _ = stack.enter_context(cm=prepare_source(file=tmp_path))
    with (
        pytest.raises(
            expected_exception=ValueError, match="No files selected"
        ),
        ExitStack() as stack,
    ):
        _ = stack.enter_context(cm=prepare_source(directory=tmp_path))
    path = tmp_path / "main.py"
    _ = path.write_bytes(data=b"pass")
    with (
        pytest.raises(expected_exception=ValueError, match="Not a directory"),
        ExitStack() as stack,
    ):
        _ = stack.enter_context(cm=prepare_source(directory=path))


@pytest.mark.parametrize(argnames="directory", argvalues=[True, False])
def test_missing_source(tmp_path: Path, *, directory: bool) -> None:
    """Report missing source paths without network access."""
    path = tmp_path / "absent"
    with (
        pytest.raises(expected_exception=FileNotFoundError),
        ExitStack() as stack,
    ):
        _ = stack.enter_context(
            cm=prepare_source(
                directory=path if directory else None,
                file=None if directory else path,
            )
        )


@pytest.mark.parametrize(argnames="directory", argvalues=[True, False])
def test_invalid_utf8(tmp_path: Path, *, directory: bool) -> None:
    """Only text sources and enabled ignore rules require UTF-8."""
    path = tmp_path / ".gitignore"
    _ = path.write_bytes(data=b"\xff")
    with (
        pytest.raises(expected_exception=UnicodeDecodeError),
        ExitStack() as stack,
    ):
        _ = stack.enter_context(
            cm=prepare_source(
                directory=tmp_path if directory else None,
                file=None if directory else path,
                respect_gitignore=True,
            )
        )
    with prepare_source(directory=tmp_path) as source:
        assert _prepared_files(source=source) == {".gitignore": b"\xff"}
