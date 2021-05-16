repoze.sphinx.autointerface README
==================================

.. image:: https://github.com/repoze/repoze.sphinx.autointerface/actions/workflows/ci-tests.yml/badge.svg
    :target: https://github.com/repoze/repoze.sphinx.autointerface/actions/workflows/ci-tests.yml

.. image:: https://img.shields.io/pypi/v/repoze.sphinx.autointerface.svg
    :target: https://pypi.python.org/pypi/repoze.sphinx.autointerface

.. image:: https://img.shields.io/pypi/pyversions/repoze.sphinx.autointerface.svg
    :target: https://pypi.python.org/pypi/repoze.sphinx.autointerface


Overview
--------

Thie package defines an extension for the
`Sphinx <https://www.sphinx-doc.org/en/master/>`_ documentation system.
The extension allows generation of API documentation by introspection of
`zope.interface <https://pypi.org/project/zope.interface/>`_ instances in
code.


Installation
------------

Install via ``pip``:

.. code-block:: bash

    pip install repoze.sphinx.autointerface


Registering the Extension
-------------------------

Add ``repoze.sphinx.autointerface`` to the ``extensions`` list in the
``conf.py`` of the Sphinx documentation for your product.

.. code-block:: python

    extensions = [
        "sphinx.ext.autodoc",
        "sphinx.ext.doctest",
        "repoze.sphinx.autointerface",
    ]


Using the Extension
-------------------

At appropriate points in your document, call out the autodoc interface.

.. code-block:: rst

    .. autointerface:: yourpackage.interfaces.IFoo

Output from the directive includes

- the fully-qualified interface name
- any base interfaces
- the docstring from the interface, rendered as reStructuredText
- the members of the interface (methods and attributes)

  * For each attribute, the output includes the attribute name
    and its description.
  * For each method, the output includes the method name, its signature,
    and its docstring (also rendered as reStructuredText).
