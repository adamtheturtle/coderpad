|project|
=========

Installation
------------

.. code-block:: console

   $ pip install coderpad-py

This is tested on Python |minimum-python-version|\+.

Usage
-----

.. code-block:: python3

   from coderpad.client import CoderPad

   client = CoderPad(api_key="your-api-key")
   pad = client.pads.create(title="Interview", language="python")
   pads = client.pads.list()
   org = client.organization.get()

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
