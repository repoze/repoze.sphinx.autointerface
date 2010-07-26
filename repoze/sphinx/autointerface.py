import types
from sphinx.util.docstrings import prepare_docstring
from sphinx.util import force_decode
try:
    # Sphinx < 1.0
    from sphinx.directives.desc import ClasslikeDesc as PyClasslike
except ImportError:
    from sphinx.domains.python import PyClasslike
from sphinx.ext import autodoc
from zope.interface import Interface

class InterfaceDesc(PyClasslike):
    def get_index_text(self, modname, name_cls):
        return '%s (interface in %s)' % (name_cls[0], modname)


class InterfaceDocumenter(autodoc.ClassDocumenter):
    """
    Specialized Documenter directive for zope interfaces.
    """
    objtype = "interface"
    # Must be a higher priority than ClassDocumenter
    member_order = 10

    def __init__(self, *args, **kwargs):
        super(InterfaceDocumenter, self).__init__(*args, **kwargs)
        self.options.members=autodoc.ALL
        self.options.show_inheritance=True

    @classmethod
    def can_document_member(cls, member, membername, isattr, parent):
        return isinstance(member, types.ClassType) and \
                issubclass(member, Interface)

    def add_directive_header(self, sig):
        if self.doc_as_attr:
            self.directivetype = 'attribute'
        autodoc.Documenter.add_directive_header(self, sig)

        # add inheritance info, if wanted
        bases=[base for base in self.object.__bases__ if base is not Interface]
        if not self.doc_as_attr and self.options.show_inheritance and bases:
            self.add_line(u'', '<autodoc>')
            bases = [u':class:`%s.%s`' % (b.__module__, b.getName())
                     for b in bases]
            self.add_line(u'   Extends: %s' % ', '.join(bases),
                          '<autodoc>')

    def format_args(self):
        return ""


    def document_members(self, all_members=True):
        oldindent = self.indent
        for name, desc in self.object.namesAndDescriptions():
            self.add_line(u'', '<autointerface>')
            sig = getattr(desc, 'getSignatureString', None)
            if sig is None:
                self.add_line(u'.. attribute:: %s' % name, '<autointerface>')
            else:
                self.add_line(u'.. method:: %s%s' % (name, sig()),
                              '<autointerface>')
            doc = desc.getDoc()
            if doc:
                self.add_line(u'', '<autointerface>')
                self.indent += self.content_indent
                sourcename = u'docstring of %s.%s' % (self.fullname, name)
                docstrings=[prepare_docstring(force_decode(doc, None))]
                for i, line in enumerate(self.process_doc(docstrings)):
                    self.add_line(line, sourcename, i)
                self.add_line(u'', '<autointerface>')
                self.indent = oldindent



def setup(app):
    try:
        app.add_directive_to_domain('py', 'interface', InterfaceDesc)
    except AttributeError:
        # Sphinx < 1.0
        app.add_directive('interface', InterfaceDesc)
    app.add_autodocumenter(InterfaceDocumenter)

