import re
import importlib
import logging
from ._check import interface as check_interface

logger = logging.getLogger(__name__)


class _BuiltClass(object):
    """Mixin for dynamically generated widget classes.

    Most functionality is defined here; dynamically generated classes are
    creating by sublclassing this and a widget, and calling the constructors
    with the appropriate arguments. Typical use::

        class MyCustomWindow(Gtk.Window, _BuiltClass):

            def __init__(self, objects=None):
                Gtk.Window.__init__(self)
                _BuiltClass.__init__(self,
                                     objects=objects,
                                     object_id=object_id,
                                     properties=properties,
                                     children=children)

    The extra arguments to `__init__` will typically be defined above.
    """

    def __init__(self, objects, object_id, properties, children):
        """Construct a new instance of the class.

        The constructor for the widget class must have already been invoked.

        :param objects: A dictionary mapping names to objects. The newly
           created instance will be added to the dictionary under the name
           specified by :param object_id:.
        :param object_id: The name with which to register the object (see
           :param objects:).
        :param properties: A dictionary mapping gobject property names to
           values. Each of these will be set on the newly created instance.
        :param children: A list of ``(child_class, child_properies)`` pairs,
            where ``child_class`` is a class satisfying the following
            constraints:
                * It must be a gtk widget.
                * Its ``__init__`` must accept a single parameter ``objects``,
                  which has the same semantics as :param objects:
            and ``child_properties`` is a dictionary of child properties, of
            the same form as :param properties:.
        """
        if objects is None:
            objects = {}
        for k, v in properties.items():
            self.set_property(k, v)
        objects[object_id] = self
        self.objects = objects
        for child_class, props in children:
            child = child_class(objects=objects)
            self.add(child)
            for k, v in props.items():
                self.child_set_property(child, k, v)


def build_classes(elt):
    """Build classes from `elt`.

    :param elt: is an instance of :class:`xml.etree.ElementTree.Element`,
       which must be an ``<interface>`` element.

    Returns a dictionary mapping names (ids in the glade file) to classes.
    """
    idents = {}
    check_interface(elt)
    do_interface(elt, idents)
    return idents


def _namespace_split(identifier):
    """Split a gobject namespace from an identifer.

    For example::

        >>> _namespace_split("MylibFancyObject")
        ("Mylib", "FancyObject")
    """
    def replacement(match):
        return ':'.join(match.groups())
    repl = re.sub(r'([a-z])([A-Z])', replacement, identifier, count=1)
    return repl.split(':')


def property_key(elt):
    """Extract the name of the property from `elt`.

    :param elt: A ``<property>`` element representing the property.
    """
    return elt.attrib["name"]


def property_value(elt):
    """Extract the value of the property from `elt`.

    :param elt: A ``<property>`` element representing the property.

    This will try to guess the type of the value, and cast it appropriately.
    """
    # TODO: We should check for a "translateable" attribute, and
    # internationalize the value as appropriate.

    # TODO: We're not actually doing any guessing here, just returning the
    # value as itself (a string). Try harder.
    return elt.text


# Each of the do_* functions takes two arguments:
#
# * ``elt``, an instance of :class:`xml.etree.ElementTree.Element`
# * ``idents``, a dictionary mapping class names to classes.
#
# ``elt`` must be an element of the type specified by the name.
#
# It processes the element, registering each found class with ``idents``.
# Some functions take additional arguments (and do additional things).
# Those are documented in the docstrings for the individual functions.
#
# `build_classes` is the entry-point for all of these.

def do_interface(elt, idents):
    for xml_child in elt:
        if xml_child.tag == 'requires':
            # TODO: maybe we should check for the version here?
            pass
        elif xml_child.tag == 'object':
            do_object(xml_child, idents)
        else:
            logger.warn("Unrecognized element %r in <interface>.",
                        xml_child.tag)


def do_object(elt, idents):
    module_name, class_name = _namespace_split(elt.attrib['class'])
    module = importlib.import_module('gi.repository.' + module_name)
    parent_class = getattr(module, class_name)
    object_id = elt.attrib['id']

    properties = {}
    children = []

    for xml_child in elt:
        if xml_child.tag == 'property':
            properties[property_key(xml_child)] = property_value(xml_child)
        elif xml_child.tag == 'signal':
            logger.warn('Unimplemented element <signal> in <object>')
        elif xml_child.tag == 'child':
            do_child(elt=xml_child,
                     children=children,
                     idents=idents)
        else:
            logger.warn('Unrecognized element %r in <object>', xml_child.tag)

    class result(parent_class, _BuiltClass):

        def __init__(self, objects=None):
            parent_class.__init__(self)
            _BuiltClass.__init__(self,
                                 objects=objects,
                                 object_id=object_id,
                                 properties=properties,
                                 children=children)

    result.__name__ = object_id
    idents[object_id] = result


def do_child(elt, children, idents):
    """Process a ``<child>`` element.

    :param children: should be a list of (child_class, child_properties) pairs.
       The resulting class and properties will be appended to it.
    """
    obj_elt = None
    packing_elt = None
    for xml_child in elt:
        if xml_child.tag == 'object':
            if obj_elt is not None:
                logger.warn('More than one <object> in <child> element.')
            obj_elt = xml_child
        elif xml_child.tag == 'packing':
            packing_elt = xml_child
    obj_class = do_object(obj_elt)

    child_properties = {}
    if packing_elt is not None:
        for xml_child in packing_elt:
            if xml_child.tag == 'property':
                child_properties[property_key(xml_child)] = \
                    property_value(xml_child)
            else:
                logger.warn("Unrecognized element %r in <packing>",
                            xml_child.tag)

    children.append((obj_class, child_properties))
