from gi.repository import Gtk
import xml.etree.ElementTree as ET

from gtkclassbuilder._check import interface as check_interface


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


def _from_tree(tree):
    """Build classes from an element tree.

    Returns a dict mapping the id attributes of elements to the corresponding
    generated classes.
    """
    if isinstance(tree, ET.Element):
        root = tree
    else:
        root = tree.getroot()
    idents = {}
    check_interface(root)
    for child in root:
        if child.tag == 'object':
            _build_class(child, idents)
    return idents


def _build_class(elt, cls_idents):
    props = {}
    signals = {}
    children = []

    for child in elt:
        if child.tag == 'property':
            props[_prop_key(child)] = _prop_val(child)
        elif child.tag == 'signal':
            signals[child.attrib['handler']] = child.attrib['name']
        elif child.tag == 'child':
            obj = child[0]
            if len(child) > 1:
                pack_elts = child[1]
            else:
                pack_elts = []
            ChildClass = _build_class(obj, cls_idents)
            pack_props = {}
            for prop in pack_elts:
                pack_props[_prop_key(prop)] = _prop_val(prop)
            children.append((ChildClass, pack_props))

    ParentClass = getattr(Gtk, elt.attrib['class'][len("Gtk"):])

    class ResultClass(ParentClass):

        def __init__(self, obj_idents=None):
            if obj_idents is None:
                obj_idents = {}
            self.obj_idents = obj_idents
            self.obj_idents[type(self).__name__] = self
            ParentClass.__init__(self, **props)
            self._children = []
            for ChildClass, pack_props in children:
                child = ChildClass(obj_idents=self.obj_idents)
                self._children.append(child)
                self.add(child)
                for propname in pack_props.keys():
                    self.child_set_property(child, propname, pack_props[propname])

        def get_object(self, ident):
            return self.obj_idents[ident]

        def connect_signals(self, handlers):
            for handler_name in signals.keys():
                if hasattr(handlers, handler_name):
                    self.connect(signals[handler_name],
                                 getattr(handlers, handler_name))
            for child in self._children:
                child.connect_signals(handlers)

    ResultClass.__name__ = elt.attrib['id']
    cls_idents[ResultClass.__name__] = ResultClass
    return ResultClass


def _prop_key(elt):
    """Return the name of the property represented by ``elt``."""
    return elt.attrib['name']


def _prop_val(elt):
    """Return the value of the property represented by ``elt``."""
    text = list(elt.itertext())[0]
    if text == 'True':
        return True
    if text == 'False':
        return False
    try:
        return int(text)
    except ValueError:
        return text
