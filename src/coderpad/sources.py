"""Prepare local question sources without credentials or network
access.
"""

import stat
from collections.abc import Generator, Iterator, Sequence
from contextlib import contextmanager
from dataclasses import dataclass
from os.path import relpath
from pathlib import Path
from shutil import copyfile
from tempfile import TemporaryDirectory

from beartype import beartype
from pathspec import GitIgnoreSpec


def _reject_symlinks(path: Path) -> None:
    """Reject symbolic links in the path and its ancestors before resolving
    it.
    """
    for component in (path, *path.parents):
        if component.is_symlink():
            msg = f"Symbolic links are not supported: {component}"
            raise ValueError(msg)


def _rules(directory: Path) -> tuple[tuple[Path, GitIgnoreSpec], ...]:
    """Read one directory's ignore rules without following symbolic
    links.
    """
    ignore_file = directory / ".gitignore"
    if ignore_file.is_symlink():
        _reject_symlinks(path=ignore_file)
    if ignore_file.is_file():
        return (
            (
                directory,
                GitIgnoreSpec.from_lines(
                    lines=ignore_file.read_text(encoding="utf-8").splitlines(),
                ),
            ),
        )
    return ()


def _inherited_rules(
    directory: Path,
) -> tuple[tuple[Path, GitIgnoreSpec], ...] | None:
    """Inherit rules from the nearest Git root, or start at the source."""
    for candidate in (directory, *directory.parents):
        if (candidate / ".git").exists():
            bases = [directory]
            while bases[-1] != candidate:
                bases.append(bases[-1].parent)
            rules: list[tuple[Path, GitIgnoreSpec]] = []
            for base in reversed(bases):
                if _is_ignored(path=base, rules=rules, suffix="/"):
                    return None
                rules.extend(_rules(directory=base))
            return tuple(rules)
    return _rules(directory=directory)


def _is_ignored(
    path: Path,
    rules: Sequence[tuple[Path, GitIgnoreSpec]],
    *,
    suffix: str,
) -> bool:
    """Apply the last matching rule from the deepest matching ignore
    file.
    """
    ignored = False
    for base, spec in rules:
        match = spec.check_file(
            file=Path(relpath(path=path, start=base)).as_posix() + suffix
        )
        if match.include is not None:
            ignored = match.include
    return ignored


def _require_regular_file(path: Path) -> None:
    """Reject devices, pipes, and other special files before reading."""
    if not stat.S_ISREG(path.stat().st_mode):
        msg = f"Only regular files are supported: {path}"
        raise ValueError(msg)


def _selected_files(
    *, directory: Path, excludes: Sequence[str], respect_gitignore: bool
) -> tuple[Path, ...]:
    """Select regular files using layered Git ignores and final exclusions."""
    exclusion_spec = GitIgnoreSpec.from_lines(lines=excludes)

    def walk(
        parent: Path, rules: tuple[tuple[Path, GitIgnoreSpec], ...]
    ) -> Iterator[Path]:
        """Traverse selected directories without following links."""
        for path in sorted(parent.iterdir()):
            if path.name.casefold() == ".git":
                continue
            is_directory = path.is_dir()
            suffix = "/" if is_directory else ""
            relative = (
                Path(relpath(path=path, start=directory)).as_posix() + suffix
            )
            if exclusion_spec.match_file(file=relative):
                continue
            if _is_ignored(path=path, rules=rules, suffix=suffix):
                continue
            _reject_symlinks(path=path)
            if is_directory:
                yield from walk(
                    parent=path,
                    rules=(*rules, *_rules(directory=path))
                    if respect_gitignore
                    else rules,
                )
            else:
                _require_regular_file(path=path)
                yield Path(relpath(path=path, start=directory))

    inherited = (
        _inherited_rules(directory=directory) if respect_gitignore else ()
    )
    if inherited is None:
        return ()
    return tuple(walk(parent=directory, rules=inherited))


@beartype
@dataclass(frozen=True)
class PreparedSource:
    """Prepared question content and its selected file paths.

    Attributes:
        contents: Exact UTF-8 text for a single-file source, otherwise None.
        directory: Isolated project directory, otherwise None. It exists only
            inside the context returned by :func:`prepare_source`.
        files: Selected POSIX paths relative to the input directory, or the
            input file's name for a single-file source.
    """

    contents: str | None
    directory: Path | None
    files: tuple[str, ...]


@contextmanager
@beartype
def prepare_source(
    *,
    directory: Path | None = None,
    file: Path | None = None,
    excludes: Sequence[str] = (),
    respect_gitignore: bool = False,
) -> Generator[PreparedSource]:
    """Read a UTF-8 file or stage a selected project without API calls.

    Args:
        directory: Project directory. Mutually exclusive with file.
        file: Single UTF-8 source file. Mutually exclusive with directory.
        excludes: Ordered Git ignore patterns relative to the project root.
            Available only with directory. Exclusions cannot restore files
            pruned by Git ignore rules or Git metadata exclusion.
        respect_gitignore: Read nested Git ignore rules, inheriting rules from
            the nearest Git root. Outside Git, start at directory. False
            ignores these rules. Git metadata is always excluded.

    Yields:
        Prepared content for previews and the client's upload methods.
        Staged files preserve bytes and are removed on context exit,
        including when the caller raises an exception.

    Raises:
        ValueError: Invalid source combination, selected symbolic link,
            special file, or empty directory selection.
        OSError: A source or ignore file cannot be read or staged.
        UnicodeError: A single file or enabled Git ignore file is not UTF-8.
    """
    if directory is not None and file is not None:
        msg = "Provide exactly one of directory or file."
        raise ValueError(msg)
    if file is not None and len(excludes) > 0:
        msg = "excludes requires directory."
        raise ValueError(msg)
    if file is not None:
        _reject_symlinks(path=file.absolute())
        _require_regular_file(path=file)
        # Decode bytes to avoid read_text universal-newline conversion.
        contents = file.read_bytes().decode(encoding="utf-8")
        yield PreparedSource(
            contents=contents, directory=None, files=(file.name,)
        )
        return
    if directory is None:
        msg = "Provide exactly one of directory or file."
        raise ValueError(msg)
    _reject_symlinks(path=directory.absolute())
    directory = directory.resolve(strict=True)
    if not directory.is_dir():
        msg = f"Not a directory: {directory}"
        raise ValueError(msg)
    files = _selected_files(
        directory=directory,
        excludes=excludes,
        respect_gitignore=respect_gitignore,
    )
    if len(files) == 0:
        msg = "No files selected for upload."
        raise ValueError(msg)
    with TemporaryDirectory(prefix="coderpad-source-") as temporary:
        staged = Path(temporary).resolve() / "project"
        staged.mkdir()
        for relative in files:
            source = directory / relative
            _reject_symlinks(path=source)
            target = staged / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            # Do not follow links introduced after selection. The client also
            # rejects symbolic links present in the staged tree.
            _ = copyfile(src=source, dst=target, follow_symlinks=False)
            _reject_symlinks(path=target)
        yield PreparedSource(
            contents=None,
            directory=staged,
            files=tuple(path.as_posix() for path in files),
        )
