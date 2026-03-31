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

   """Example usage."""

   import sys

   from coderpad.client import CoderPad

   client = CoderPad(api_key="your-api-key")
   pad = client.pads.create(title="Interview", language="python")
   sys.stdout.write(pad.title)
   for listed_pad in client.pads.list():
       sys.stdout.write(listed_pad.title)
   org = client.organization.get()
   sys.stdout.write(org.organization_name)

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
