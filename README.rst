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

   """Use the CoderPad Interview API."""

   from coderpad_api.client import CoderPadClient

   client = CoderPadClient(api_key="your-api-key")
   assert client.base_url == "https://api.interview.coderpad.io"

Full Documentation
------------------

See the `full documentation <https://adamtheturtle.github.io/coderpad-api-python/>`__.

.. |Build Status| image:: https://github.com/adamtheturtle/coderpad-api-python/actions/workflows/ci.yml/badge.svg?branch=main
   :target: https://github.com/adamtheturtle/coderpad-api-python/actions
.. |PyPI| image:: https://badge.fury.io/py/coderpad-py.svg
   :target: https://badge.fury.io/py/coderpad-py
.. |minimum-python-version| replace:: 3.13
