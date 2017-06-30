
from sphinx.util.docstrings import prepare_docstring
from sphinx.util import force_decode
from sphinx.domains import ObjType
from sphinx.domains.python import (
    PyClasslike,
    PyXRefRole,
)
from sphinx.ext import autodoc
from zope.interface import Interface
from zope.interface.interface import InterfaceClass

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
        self.options.show_inheritance = True

    @classmethod
    def can_document_member(cls, member, membername, isattr, parent):
        return isinstance(member, InterfaceClass)

    def add_directive_header(self, sig):
        if self.doc_as_attr:
            self.directivetype = 'attribute'
        autodoc.Documenter.add_directive_header(self, sig)

        # add inheritance info, if wanted
        bases = [base for base in self.object.__bases__
                       if base is not Interface]
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
        members = list(self.object.namesAndDescriptions())

        if self.options.members is not autodoc.ALL:
            specified = []
            for line in (self.options.members or []):
                specified.extend(line.split())
            mapping = dict(members)
            members = [(x, mapping[x]) for x in specified]
        member_order = (self.options.member_order or
                        self.env.config.autodoc_member_order)
        if member_order == 'alphabetical':
            members.sort()
        if member_order == 'groupwise':
            # sort by group; relies on stable sort to keep items in the
            # same group sorted alphabetically
            members.sort(key=lambda e:
                                getattr(e[1], 'getSignatureString',
                                        None) is not None)
        elif member_order == 'bysource' and self.analyzer:
            # sort by source order, by virtue of the module analyzer
            tagorder = self.analyzer.tagorder
            name = self.object.__name__
            def keyfunc(entry):
                return tagorder.get('%s.%s' % (name, entry[0]), len(tagorder))
            members.sort(key=keyfunc)

        for name, desc in members:
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
                docstrings = [prepare_docstring(force_decode(doc, None))]
                for i, line in enumerate(self.process_doc(docstrings)):
                    self.add_line(line, sourcename, i)
                self.add_line(u'', '<autointerface>')
                self.indent = oldindent


def setup(app):
    # We have to add a new ``object type`` for ``:interface:`` references 
    # to work properly. However, Sphinx does not have an 
    # ``add_object_type_to_domain()`` method, so we have to carefully 
    # override the whole domain. We are using the currently configured 
    # domain class instead of importing it, because it could be already 
    # overriden.
    try:
        # New API
        current_domain = app.registry.domains['py']
    except AttributeError:
        # Old API
        current_domain = app.domains['py']

    new_types = current_domain.object_types.copy()
    new_types['interface'] = ObjType('interface', 'interface', 'obj', 'class')
    
    class InterfacePythonDomain(current_domain):
        object_types = new_types

    app.override_domain(InterfacePythonDomain)
    app.add_directive_to_domain('py', 'interface', InterfaceDesc)
    app.add_role_to_domain('py', 'interface', PyXRefRole())
    app.add_autodocumenter(InterfaceDocumenter)
    
