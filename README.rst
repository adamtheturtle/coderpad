|Build Status| |PyPI|

coderpad-py
===========

Python library for the CoderPad Interview API.

Installation
------------

.. code-block:: shell

   pip install coderpad-py

This is tested on Python |minimum-python-version|\+.

Getting Started
---------------

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
   for user in client.organization.users.list():
       sys.stdout.write(user.email)

The organization users endpoint also supports server-side email filtering:

.. code-block:: python

   """Filter organization users by email."""

   from coderpad.client import CoderPad

   client = CoderPad(api_key="your-api-key")
   users = client.organization.users.list(email="person@example.com")

The equivalent asynchronous operation is
``await client.organization.users.list(email="person@example.com")``.

Full Documentation
------------------

See the `full documentation <https://adamtheturtle.github.io/coderpad-api-python/>`__.

.. |Build Status| image:: https://github.com/adamtheturtle/coderpad-api-python/actions/workflows/ci.yml/badge.svg?branch=main
   :target: https://github.com/adamtheturtle/coderpad-api-python/actions
.. |PyPI| image:: https://badge.fury.io/py/coderpad-py.svg
   :target: https://badge.fury.io/py/coderpad-py
.. |minimum-python-version| replace:: 3.13
