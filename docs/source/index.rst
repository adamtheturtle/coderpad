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
   pad = client.pads.create(title="Interview", language="python")
   assert pad.title == "Interview"
   pads = client.pads.list()
   assert len(pads) > 0
   org = client.organization.get()
   assert org.organization_name

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
