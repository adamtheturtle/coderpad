|Build Status|

coderpad-api-python
===================

Python library for the CoderPad Interview API.

Installation
------------

.. code-block:: shell

   pip install coderpad-api-python

This is tested on Python |minimum-python-version|\+.

Getting Started
---------------

.. code-block:: python

   """Use the CoderPad Interview API."""

   from coderpad_api import CoderPadClient

   client = CoderPadClient(api_key="your-api-key")

Full Documentation
------------------

See the `full documentation <https://adamtheturtle.github.io/coderpad-api-python/>`__.

.. |Build Status| image:: https://github.com/adamtheturtle/coderpad-api-python/actions/workflows/ci.yml/badge.svg?branch=main
   :target: https://github.com/adamtheturtle/coderpad-api-python/actions
.. |minimum-python-version| replace:: 3.13
