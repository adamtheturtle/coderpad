|project|
=========

Installation
------------

.. code-block:: console

   $ pip install coderpad-py

This is tested on Python |minimum-python-version|\+.

Usage
-----

.. code-block:: python

   """Use the CoderPad API."""

   from coderpad.client import CoderPad

   client = CoderPad(api_key="your-api-key")
   assert callable(client.pads.create)
   assert callable(client.pads.list)
   assert callable(client.pads.get)
   assert callable(client.organization.get)

See the :doc:`api-reference` for full usage details.

Reference
---------

.. toctree::
   :maxdepth: 3

   api-reference
   openapi-spec
   contributing
   release-process
   changelog
