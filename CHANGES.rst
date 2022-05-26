repoze.sphinx.autointerface Changelog
=====================================

1.0.0 (2022-05-26)
------------------

- Remove sphinx.util.force_decode. Previously we hacked it in to support Python
  2 and Sphinx 3.x, but Sphinx 4.0 deprecated it and dropped Python 2 support.

- Replace Travis-CI with GitHub Actions

- Add support for Python 3.6, 3.7, 3.8, 3.9, 3.10, and PyPy3.

- Drop support for Python 2.7, 3.3, 3.4, 3.5, and PyPy.

- Update to work with newer Sphinx versions:

  * Sphinx.domains -> Sphinx.registry.domains
  * Sphinx.override_domain(D) -> Sphinx.add_domain(D, override=True)

- Drop support for Sphinx < 4.0.

0.8 (2016-03-28)
----------------

- Add support for Python 3.3, 3.4, and 3.5.

- Drop support for Python 2.6 and 3.2.

- Allow cross references using the ``:class:`` directive to use the
  ``.`` for "fuzzy" searching.  Thanks to Jason Madden for the patch.

0.7.1 (2012-09-15)
------------------

- Remove ``setup.py`` dependency on ``ez_setup.py``.

0.7.0 (2012-06-20)
------------------

- PyPy compatibility.

- Python 3.2+ compatibility.  Thanks to Arfrever for the patch.

- Include interface docs under the ``automodule`` directive.  Thanks to
  Krys Lawrence for the patch.


0.6.2 (2011-02-13)
------------------

- Fix ``TypeError: 'NoneType' object is not iterable`` error when generating
  a rendering of an interface under Python 2.7.


0.6.1 (2011-01-28)
------------------

- Fix ':member-order: bysource' handling.


0.6 (2011-01-28)
----------------

- Correctly handle ':members:' values explicitly set in the directive.


0.5 (2011-01-18)
----------------

- Added support for the ':member-order:' flag, which can take one of the
  three stock values, "alphabetical", "groupwise", or "bysource".  By
  default, members are documented in "hash" order.


0.4 (2010-07-26)
----------------

- Fixed compatibility with Sphinx 1.0

- Un-break PyPI ReST/HTML-rendering again.


0.3 (2009-10-25)
----------------

- Refactor sphinx integration. There are now separate ``autointerface``
  and ``interface`` directives.


0.2.1 (2009-08-20)
------------------

- Fix add_directive arguments to work with Sphinx 0.6.1, now required.


0.1.3 (2009-01-14)
------------------

- Coerce unicode path elements to str in ``_resolve_dotted_name``.
  Note that non-ASCII path elements won't work:  this fix just deals
  with the case where the path was of type unicode.

- Fixed spelling of directive in README.txt.

- Added dependency on ``zope.interface``.


0.1.2 (2008-10-03)
------------------

- Packaging change:  improved description in README.txt.


0.1.1 (2008-10-03)
------------------

- Packaging bug:  the ``long_description`` was not rendering properly to
  HTML on PyPI.


0.1 (2008-10-02)
----------------

- Initial release.
