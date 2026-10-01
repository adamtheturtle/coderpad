API Reference
=============

.. automodule:: coderpad.client
   :undoc-members:
   :members:

.. automodule:: coderpad.async_client
   :undoc-members:
   :members:

.. automodule:: coderpad.screen
   :undoc-members:
   :members:

.. automodule:: coderpad.async_screen
   :undoc-members:
   :members:

.. automodule:: coderpad.screen_types
   :undoc-members:
   :members:
   :exclude-members: __init__, model_config

Question variants
-----------------

Use ``client.questions.variants`` (also available on ``AsyncCoderPad``): ``list(question_id=...)``, ``get(question_id=..., variant_id=...)``, ``create(question_id=..., language=...)``, ``update(question_id=..., variant_id=...)`` and ``delete(question_id=..., variant_id=...)``.
All five operations use JSON endpoints nested under the question.
Custom Interview transports must accept the ``json`` keyword.

Create accepts a language key such as ``ruby`` or a project template slug such as ``react``.
Project variant responses have ``language=None``.
Use ``project_template_slug`` and ``project_template_id`` to identify their environment.
Omitting ``contents`` preserves code on update, ``contents=""`` writes a blank starter file, and ``contents=None`` restores the language default.
Changing environment clears code unless replacement code or files are supplied.

``file_contents`` accepts a sequence of ``QuestionVariantFileContent`` models or a JSON string.
File paths are already decoded in responses.
``hidden`` and ``deleted`` flags are preserved.
Files overlay the template on create and replace variant files on update; ``file_contents=[]`` resets a template variant on update.
The server prevents deleting ``.cpad`` and requires at least one remaining file.
``contents`` and ``file_contents`` cannot be combined, including explicit null code.
``solution`` sets the variant's reference solution.

.. automodule:: coderpad.transports
   :undoc-members:
   :members:

.. automodule:: coderpad.types
   :undoc-members:
   :members:
   :exclude-members: __init__, model_config

.. automodule:: coderpad.json_types
   :undoc-members:
   :members:

.. automodule:: coderpad.exceptions
   :undoc-members:
   :members:
