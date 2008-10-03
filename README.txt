repoze.sphinx.autointerface README
==================================

Overview
--------

Thie package defines an extension for the
`Sphinx <http://sphinx.pocool.org>`_ documentation system.

Installation
------------

Install via ``easy_install`` or any other mechanism to get the
package on the path.

Registering the Extension
-------------------------

Add ``repoze.sphinx.autointerface`` to the ``conf.py`` of the docs
section of your product.

Using the Extension
-------------------

At appropriate points in your document, call out the interface
autodocs via::

  .. autoinclude:: yourpackage.interfaces.IFoo
     :members:
