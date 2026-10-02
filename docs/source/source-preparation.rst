Preparing question sources
==========================

``coderpad.sources.prepare_source`` reads a single UTF-8 file or prepares an isolated project directory without credentials or network requests.
Use the returned content for both previews and SDK uploads.
The helper is also available as ``coderpad.prepare_source``.

Supply exactly one of ``file=`` and ``directory=``.
For a single file, ``contents`` preserves the text exactly, including empty files, a UTF-8 byte order mark, CRLF, and trailing white space.
For a directory, ``directory`` contains a staged copy of the selected files with their original bytes.
Binary files are supported in directory sources.
``files`` contains deterministic POSIX paths relative to the source directory, or the single file's name.

Keep previews and uploads inside the preparation context.
The staged directory is deleted when the context exits, including when an upload raises an exception.
Changes to the original files after preparation do not affect the staged copy.
Preparation finishes reading or staging the selected files before yielding control to the caller.
It does not provide an atomic snapshot of a directory being modified concurrently.

.. code-block:: python

   """Preview and upload the same prepared project."""

   from pathlib import Path
   from tempfile import TemporaryDirectory

   from coderpad import CoderPad, prepare_source

   with TemporaryDirectory() as temporary:
       project = Path(temporary).resolve()
       _ = (project / "main.py").write_bytes(data=b"print('hello')\r\n")
       _ = (project / ".gitignore").write_text(data="*.pyc\n", encoding="utf-8")
       _ = (project / "main.pyc").write_bytes(data=b"generated")
       with prepare_source(
           directory=project,
           respect_gitignore=True,
           excludes=(".gitignore",),
       ) as source:
           assert source.files == ("main.py",)
           assert source.directory is not None
           assert (
               source.directory / "main.py"
           ).read_bytes() == b"print('hello')\r\n"
           with CoderPad(api_key="your-api-key") as client:
               client.questions.update(
                   question_id="123",
                   contents=source.contents,
                   directory=source.directory,
               )

The same arguments work with ``questions.create`` and the asynchronous client.
Preparation itself is synchronous local file system work.
For a dry run, inspect the prepared content and skip the client call.
A CLI adapter can pass its source paths and exclusions to this helper, enable ``respect_gitignore=True``, print ``files``, and pass ``contents`` and ``directory`` to the SDK.
Question IDs, repository metadata, and source transformations remain the consumer's responsibility.

Selection rules
---------------

* ``respect_gitignore=False`` is the default.
  Set it to ``True`` to enable nested Git ignore rules for directory sources.
  For single-file sources this option has no effect.
* Inside Git, rules are inherited from the nearest Git root down to the source directory.
  A linked working tree's ``.git`` file also identifies its root.
  Outside Git, rules start at the source directory, excluding unrelated parent rules.
* Patterns are relative to the directory containing their ``.gitignore`` file.
  Later matches override earlier ones, and deeper rules override inherited rules.
  Ignored directories are pruned, so children cannot restore themselves beneath an ignored parent.
  This also applies when the explicitly supplied source directory has an ignored ancestor below the Git root.
* Rules apply regardless of whether a file is tracked.
  Global Git excludes and ``.git/info/exclude`` are not read.
* ``excludes`` accepts ordered Git ignore patterns relative to the source directory.
  It is available only for directory sources and applies even when ``respect_gitignore=False``.
  Later negations can undo earlier exclusions in this list, but cannot restore a path already pruned by Git ignore rules or Git metadata exclusion.
* ``.git`` entries are always excluded, at every depth.
  Other hidden files, including ``.gitignore``, are included unless excluded.
  ZIP files are included by default; use ``excludes=("*.zip",)`` to omit them.
* Selected symbolic links, symbolic links in source paths, and special files are rejected.
  Excluded symbolic links are skipped.
  Enabled ``.gitignore`` files cannot be symbolic links.
  Empty directory selections fail, while empty single files are valid.

Existing directory uploads
--------------------------

Calling ``questions.create(directory=...)`` or ``questions.update(directory=...)`` directly retains its existing behavior: it uploads every file without this helper's selection policy.
The preparation helper does not change those methods or duplicate their serialization.
Passing a prepared directory still uses the SDK's ZIP importer, including the server's project configuration generation.

API
---

.. automodule:: coderpad.sources
   :members:
   :exclude-members: __init__
