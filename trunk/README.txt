repoze.sphinx.autointerface README
==================================

Overview
--------

Thie package defines an extension for the
`Sphinx <http://sphinx.pocool.org>`_ documentation system.  The extension
allows generation of API documentation by introspection of
`zope.interface <http://pypi.python.org/pypi/zope.interface>`_ instances in 
code.


Installation
------------

Install via `easy_install
<http://peak.telecommunity.com/DevCenter/EasyInstall>`_::

 $ bin/easy_install repoze.sphinx.autointerface

or any other means which gets the package on your ``PYTHONPATH``.


Registering the Extension
-------------------------

Add ``repoze.sphinx.autointerface`` to the ``extensions`` list in the
``conf.py`` of the Sphinx documentation for your product.  E.g.::

 extensions = ['sphinx.ext.autodoc',
               'sphinx.ext.doctest',
               'repoze.sphinx.autointerface',
              ]


Using the Extension
-------------------

At appropriate points in your document, call out the interface
autodocs via::

  .. autointerface:: yourpackage.interfaces.IFoo

Output from the directive includes

- the fully-qualified interface name
- any base interfaces
- the doctstring from the interface, rendered as reSTX.
- the members of the interface (methods and attributes).

  * For each attribute, the output includes the attribute name
    and its description.
  * For each method, the output includes the method name, its signature,
    and its docstring (also rendered as reSTX).
