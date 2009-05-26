import sys
from docutils.nodes import paragraph
from docutils.parsers.rst import Directive
from docutils.statemachine import ViewList
from zope.interface import Interface

class AutoInterfaceDirective(Directive):
    required_arguments = 1
    optional_arguments = 0
    final_argument_whiltepace = False
    option_spec = {}
    has_content = False
    def __init__(self,
                 directive,
                 arguments,
                 options,           # ignored
                 content,           # ignored
                 lineno,
                 content_offset,    # ignored
                 block_text,        # ignored
                 state,
                 state_machine,     # ignored
                ):
        assert directive == 'autointerface'
        self.name = arguments[0]
        self.state = state
        self.lineno = lineno

    def _buildLines(self):
        try:
            iface = _resolve_dotted_name(self.name)
        except (ImportError, AttributeError):
            return [self.state.document.reporter.warning(
                'autointerface can\'t import/find %r: \n'
                'please check your spelling and sys.path' %
                str(self.name), line=self.lineno)]
        bases = [x for x in iface.__bases__ if x is not Interface]

        module_file = sys.modules.get(iface.__module__)
        if module_file is not None:
            self.state.document.settings.env.note_dependency(
                    module_file.__file__)

        result = ViewList()
        result.append(u'', '')

        result.append(u'Interface: ``%s``' % self.name, '<autointerface>')
 
        if bases:
            result.append(u'', '')
            for b in bases:
                result.append(u'- Extends: %s' % b.getName(), '<autointerface>')
            result.append(u'', '')

        docstring = iface.getDoc()
        if docstring:
            for line in _indent_and_wrap(docstring, 1):
                result.append(line, '<autointerface>')

        for name, desc in iface.namesAndDescriptions():
            result.append(u'', '<autointerface>')
            sig = getattr(desc, 'getSignatureString', None)
            if sig is None:
                result.append(u'  Attribute: ``%s``' % name, '<autointerface>')
            else:
                result.append(u'  Method: ``%s%s``' % (name, sig()),
                              '<autointerface>')
            doc = desc.getDoc()
            if doc:
                for line in _indent_and_wrap(doc, 2):
                    result.append(line, '<autointerface>')

        return result

    def run(self):
        result = self._buildLines()

        node = paragraph()
        self.state.nested_parse(result, 0, node)
        return node.children

def _resolve_dotted_name(dotted):
    #return EntryPoint.parse('x=%s' % dotted).load(False)
    tokens = [str(x) for x in dotted.split('.')]
    path, name = tokens[:-1], tokens[-1]
    thing = __import__('.'.join(path), {}, {}, [name])
    return getattr(thing, name)

def _indent_and_wrap(text, level, width=72):
    indent = u' ' * level
    lines = []
    current = indent

    for line in text.splitlines():
        if not line.strip():
            lines.append(current)
            lines.append(indent)
            current = indent
            continue

        for token in line.split():
            current = u' '.join([current, token])
            if len(current) > width:
                lines.append(current)
                current = indent
    else:
        lines.append(current)
    return lines


def setup(app):
    app.add_directive('autointerface', AutoInterfaceDirective)


if __name__ == '__main__':
    from zope.interface import Attribute
    from zope.interface import Interface

    class IFoo(Interface):
        """ Foo API.
        """
        bar = Attribute(u'Explain bar')

        def bam(baz, qux):
            """ -> frobnatz.
            """

    class IBar(IFoo):
        """ Extending IFoo for fun and profit.
        """
        spam = Attribute(u'Great with eggs.')

    class DummyReporter:
        def warning(self, msg, line):
            return '%s [%s]' % (msg, line)

    class DummyDocument:
        reporter = DummyReporter()

    class DummyState:
        document = DummyDocument()

    directive = AutoInterfaceDirective(
        'autointerface', 
        ['__main__.ISpaz'],
        {},
        content=None,
        lineno=42,
        content_offset=127,
        block_text='XYZZY',
        state=DummyState(),
        state_machine=None,
       )
    for x in directive._buildLines():
        print x

    directive = AutoInterfaceDirective(
        'autointerface', 
        ['__main__.IFoo'],
        {},
        content=None,
        lineno=42,
        content_offset=127,
        block_text='XYZZY',
        state=DummyState(),
        state_machine=None,
       )

    for x in directive._buildLines():
        print x

    directive = AutoInterfaceDirective(
        'autointerface', 
        ['__main__.IBar'],
        {},
        content=None,
        lineno=42,
        content_offset=127,
        block_text='XYZZY',
        state=DummyState(),
        state_machine=None,
       )

    for x in directive._buildLines():
        print x
