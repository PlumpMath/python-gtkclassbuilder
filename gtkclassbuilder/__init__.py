"""``gtkclassbuilder`` converts Gtk Builder files to python classes.

This is in contrast to what Gtk Builder does, i.e. creating an instance
of the class. Gtk Builder's behavior is problematic since it makes it
difficult to create multiple instances of a widget from the same
``.glade`` file.

===========
Limitations
===========

``gtkclassbuilder`` only supports a small (but growing) subset of the
Gtk Builder file format. To date, ``gtkclassbuilder`` requires that
glade files conform to the following restrictions:

    * Each ``<object>`` element must have a ``class`` attribute and an
      ``id`` attribute. The latter will be the name of the generated class,
      which will inherit from the former. The ``class`` attribute is expected
      to be CapitalizedCamelCase, and its first word will be treated as the
      module name.
    * Each ``<property>`` element must have a ``name`` attribute, and a
      single child, which must be text (not an element).
    * Each ``<child>`` element must contain a exactly one ``<object>`` element,
      and one or zero ``<packing>`` elements.
    * Each ``signal`` element must have both a ``name`` and a ``handler``
      attribute. Signals are only interpreted when they are the children
      ``<object>`` elements.

Note that some of these may be true of all ``.glade`` files; indeed many of
them probably are. The author of this package has not investigated exactly
what a valid ``.glade`` file may contain.

Unless otherwise specified, any additional elements and/or attributes will
be ignored, and a warning will be logged.
"""

from .builder import Builder
import xml.etree.ElementTree as ET
import sys


def _from_tree(tree):
    """Build classes from an element tree.

    Returns a dict mapping the id attributes of elements to the corresponding
    generated classes.
    """
    if isinstance(tree, ET.Element):
        root = tree
    else:
        root = tree.getroot()
    result = Builder()
    result._from_root(root)
    return result


def from_string(input):
    """Generate classes from the string ``input``

    Returns a dict mapping the id attributes of elements to the corresponding
    generated classes.
    """
    return _from_tree(ET.fromstring(input))


def from_filename(filename):
    """Generate classes from the glade file named ``filename``

    Returns a dict mapping the id attributes of elements to the corresponding
    generated classes.
    """
    return _from_tree(ET.parse(filename))


class _ModuleProxy(object):
    """Helper class for the implementation of "replace_module".

    replace module replaces the underlying module in `sys.modules` with an
    instance of this class.
    """

    def __init__(self, module):
        gladefile = module.__file__.replace('.py', '.glade')
        self.builder = from_filename(gladefile)

    def __getattr__(self, name):
        try:
            return self.builder[name]
        except KeyError:
            raise AttributeError


def replace_module(name):
    """Replace the module `name` with the result of parsing a glade file.

    Example usage:

        >>> # foo.py
        >>> from gtkbuilder import replace_module
        >>> replace_module(__name__)

    The above will read ``foo.glade``, and swap out the module foo with an
    object whose attributes are the classes read by gtkclassbuilder:

        >>> # bar.py
        >>> from foo import MainWindow, MyWidget
        >>> # ...
    """
    module = sys.modules[name]
    proxy = _ModuleProxy(module)
    sys.modules[name] = proxy
