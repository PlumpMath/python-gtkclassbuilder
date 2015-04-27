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
      which will inherit from the former. The ``class`` attribute must begin
      with "Gtk", and therefore must be from the Gtk package. This has the
      consequence that accessibility is not supported, though adding support
      is considered a priority.
    * Each ``<property>`` element must have a ``name`` attribute, and a
      single child, which must be text (not an element).
    * Each ``<child>`` element's first child must be an ``<object>`` element.
    * If a ``<child>`` has more than one child, the second child must be
      ``<packing>`` element.
    * ``<packing>`` elements may only contain ``<property>`` elements

Note that some of these may be true of all ``.glade`` files; indeed many of
them probably are. The author of this package has not investigated exactly
what a valid ``.glade`` file may contain.

Unless otherwise specified, any additional elements and/or attributes will
be ignored, and a warning will be logged.
"""
from gtkclassbuilder._build import from_string, from_filename
from gtkclassbuilder._check import BadInput
