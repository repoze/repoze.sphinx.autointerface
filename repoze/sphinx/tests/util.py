import sys
import os
import tempfile
import shutil

from io import StringIO

from sphinx import application
from sphinx.builders.latex import LaTeXBuilder
from sphinx.pycode import ModuleAnalyzer

from docutils import nodes
from docutils.parsers.rst import directives, roles

rootdir = os.path.abspath(os.path.dirname(__file__) or '.')

class ListOutput(object):
    """
    File-like object that collects written text in a list.
    """
    def __init__(self, name):
        self.name = name
        self.content = []

    def reset(self):
        del self.content[:]

    def write(self, text):
        self.content.append(text)

class TestApp(application.Sphinx):
    """
    A subclass of :class:`Sphinx` that runs on the test root, with some
    better default values for the initialization parameters.
    """

    def __init__(self, buildername='html', testroot=None, srcdir=None,
                 freshenv=False, confoverrides=None, status=None, warning=None,
                 tags=None, docutilsconf=None):
        if testroot is None:
            defaultsrcdir = 'root'
            testroot = os.path.join(rootdir, 'root')
        else:
            defaultsrcdir = 'test-' + testroot
            testroot = os.path.join(rootdir, 'roots', ('test-' + testroot))

        self.__tempdir = os.path.abspath(tempfile.mkdtemp())


        if srcdir is None:
            srcdir = os.path.join(self.__tempdir, defaultsrcdir)
        else:
            srcdir = os.path.join(self.__tempdir, srcdir)

        if not os.path.exists(srcdir):
            shutil.copytree(testroot, srcdir, symlinks=False)

        if docutilsconf is not None:
            with open(os.path.join(srcdir, 'docutils.conf')) as f:
                f.write(docutilsconf)

        builddir = os.path.join(srcdir, '_build')
#        if confdir is None:
        confdir = srcdir
#        if outdir is None:
        outdir = os.path.join(builddir, buildername)
        if not os.path.exists(outdir):
            os.makedirs(outdir)

        doctreedir = os.path.join(builddir, 'doctrees')
        if not os.path.exists(doctreedir):
            os.makedirs(doctreedir)
        if confoverrides is None:
            confoverrides = {}
        if status is None:
            status = StringIO()
        if warning is None:
            warning = ListOutput('stderr')
#        if warningiserror is None:
        warningiserror = False

        self._saved_path = sys.path[:]
        self._saved_directives = directives._directives.copy()
        self._saved_roles = roles._roles.copy()

        self._saved_nodeclasses = set(v for v in dir(nodes.GenericNodeVisitor)
                                      if v.startswith('visit_'))

        try:
            application.Sphinx.__init__(self, srcdir, confdir, outdir, doctreedir,
                                        buildername, confoverrides, status, warning,
                                        freshenv, warningiserror, tags)
        except:
            self.cleanup()
            raise

    def cleanup(self, doctrees=False):
        shutil.rmtree(self.__tempdir)
        ModuleAnalyzer.cache.clear()
        LaTeXBuilder.usepackages = []
        sys.path[:] = self._saved_path
        sys.modules.pop('autodoc_fodder', None)
        directives._directives = self._saved_directives
        roles._roles = self._saved_roles
        for method in dir(nodes.GenericNodeVisitor):
            if method.startswith('visit_') and \
               method not in self._saved_nodeclasses:
                delattr(nodes.GenericNodeVisitor, 'visit_' + method[6:])
                delattr(nodes.GenericNodeVisitor, 'depart_' + method[6:])

    def __repr__(self):
        return '<%s buildername=%r>' % (self.__class__.__name__, self.builder.name)
