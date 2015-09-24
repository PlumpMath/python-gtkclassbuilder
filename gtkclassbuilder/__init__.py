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

    * The root ``<interface>`` element must have at least one ``<object>``
      element child. The first ``<object>`` child will be used to
      generate the class; everything else in the file is ignored.
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

from . import _take2
import xml.etree.ElementTree as ET


def _from_tree(tree):
    """Build classes from an element tree.

    Returns a dict mapping the id attributes of elements to the corresponding
    generated classes.
    """
    if isinstance(tree, ET.Element):
        root = tree
    else:
        root = tree.getroot()
    return _take2.build_classes(root)


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
