import unittest

from docutils.statemachine import ViewList
from sphinx.ext.autodoc import ALL
from zope import interface

from repoze.sphinx import autointerface
from .util import SphinxTestApp

class IPlumbusMaker(interface.Interface):

    grumbo = interface.Attribute("The dinglebop is fed through here")
    fleeb = interface.Attribute("The dinglebop is polished with this")

    def smoothTheDinglebop(schleem):
        """Smooth it out

        The schleem is then repurposed.
        """

class Options(dict):
    inherited_members = False
    undoc_members = False
    private_members = False
    special_members = False
    imported_members = False
    show_inheritance = False
    noindex = False
    no_index = False  # FBO Sphinx 8.x
    no_index_entry = False  # FBO Sphinx 9.x
    annotation = None
    synopsis = ''
    platform = ''
    deprecated = False
    members = ()
    member_order = 'alphabetic'
    exclude_members = ()

    def __init__(self):
        super(Options, self).__init__()
        self.exclude_members = set()
        self.members = []
        self.__dict__ = self

class Settings(object):

    tab_width = 4


class Document(object):

    def __init__(self, settings):
        self.settings = settings


class State(object):

    def __init__(self, document):
        self.document = document


class Directive(object):
    env = None
    genopt = None
    result = None
    record_dependencies = None

    def __init__(self):
        self._warnings = []
        self.filename_set = set()
        self.result = ViewList()
        self.record_dependencies = set()
        self.state = State(Document(Settings()))

    def warn(self, msg):
        self._warnings.append(msg)

class AutoInterfaceTests(unittest.TestCase):

    def setUp(self):
        app = self.app = SphinxTestApp()
        app.builder.env.temp_data['docname'] = 'dummy'

        autointerface.setup(app)

        opt = self.options = Options()
        d = self.directive = Directive()
        d.env = app.builder.env
        d.genopt = opt

    def tearDown(self):
        self.app.cleanup()
        self.app = None

    def assertResultContains(
        self,
        item,
        objtype='interface',
        name='tests.unit.test_autointerface.IPlumbusMaker',
        **kw,
    ):
        directive = self.directive
        inst = self.app.registry.documenters['interface'](directive, name)
        inst.generate(**kw)
        # print '\n'.join(directive.result)
        self.assertEqual([], directive._warnings)
        self.assertIn(item, directive.result)
        results = directive.result[:]
        del directive.result[:]
        return '\n'.join(results)

    def test_restricted_members(self):
        self.options.members = ['smoothTheDinglebop']
        all_results = self.assertResultContains(
            '   .. method:: smoothTheDinglebop(schleem)'
        )
        self.assertNotIn('grumbo', all_results)

    def test_all_members(self):
        self.options.members = ALL
        all_results = self.assertResultContains(
            '   .. method:: smoothTheDinglebop(schleem)'
        )
        self.assertIn('grumbo', all_results)
        self.assertIn('fleeb', all_results)
