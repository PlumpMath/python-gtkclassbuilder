
from . import _check
from ._utils import has_handler, get_handler, namespace_split

from gi.repository import Gtk
import importlib
import logging


logger = logging.getLogger(__name__)


class BuiltObject(object):

    def __init__(self, _builder, _objects):
        for prop in self._properties:
            prop.set(self, _builder, _objects)
        for child_class_name in self._children:
            child = _builder._classes[child_class_name](_builder, _objects)
            self.add(child)
            for prop in child._child_properties:
                prop.set_child(self, child, _builder, _objects)
        self._objects = _objects
        _objects[self.__class__.__name__] = self

    def get_object(self, name):
        return self._objects[name]

    def connect_signals(self, handlers):
        for k, v in self._signals.items():
            if has_handler(handlers, v):
                self.connect(k, get_handler(handlers, v))
        if len(self._children) != 0:
            for child in self.get_children():
                if isinstance(child, BuiltObject):
                    child.connect_signals(handlers)


class Property(object):

    _enums = {
        "item_orientation": Gtk.Orientation,
        "orientation": Gtk.Orientation,
        "justify": Gtk.Justification,
        "relief": Gtk.ReliefStyle,
        "wrap_mode": Gtk.WrapMode,
    }

    def __init__(self, elt):
        self.key = elt.attrib['name']
        # TODO: We should check for a "translateable" attribute, and
        # internationalize the value as appropriate.
        self._value = elt.text

    def set(self, object, _builder, _objects):
        object.set_property(self.key, self._get_value(_builder, _objects))

    def set_child(self, parent, child, _builder, _objects):
        parent.child_set_property(child,
                                  self.key,
                                  self._get_value(_builder, _objects))

    def _get_value(self, _builder, _objects):
        if self.key == "model":
            # model refers to another object in the glade file by it's id.
            # We want to fetch that object out of _objects, but it's possible
            # that it hasn't been created yet. If so, we need to make it
            # first.
            if self._value not in _objects:
                _builder.make_object(self._value, _objects)
            return _objects[self._value]

        if self.key in self._enums:
            return getattr(self._enums[self.key], self._value.upper())

        return self._guess_value()

    def _guess_value(self):
        """Try to guess the correct type based on the text.

        Return the corresponding value.
        """
        if self._value == 'True':
            return True
        if self._value == 'False':
            return False
        try:
            return int(self._value)
        except ValueError:
            return self._value


class Builder(object):

    def __init__(self):
        self._classes = {}

    def make_object(self, class_name, _objects=None):
        if _objects is None:
            _objects = {}
        return self._classes[class_name](_builder=self, _objects=_objects)

    def _from_root(self, elt):
        _check.interface(elt)
        self._do_interface(elt)

    def _do_interface(self, elt):
        for xml_child in elt.findall('./object'):
            self._do_object(xml_child)

    def _do_object(self, elt):
        module_name, class_name = namespace_split(elt.attrib['class'])
        module = importlib.import_module('gi.repository.' + module_name)
        parent_class = getattr(module, class_name)
        ident = elt.attrib['id']

        properties = []
        signals = {}
        children = []

        for xml_child in elt.findall('./property'):
            properties.append(Property(xml_child))
        for xml_child in elt.findall('./signal'):
            signals[xml_child.attrib['name']] = xml_child.attrib['handler']
        for xml_child in elt.findall('./child'):
            self._do_child(elt=xml_child,
                           children=children)

        def _result_init(_obj_self, _builder, _objects):
            parent_class.__init__(_obj_self)
            BuiltObject.__init__(_obj_self, _builder, _objects)

        self._classes[ident] = type(ident, (parent_class, BuiltObject), {
            '__init__': _result_init,
            '_properties': properties,
            '_signals': signals,
            '_children': children,
            '_child_properties': [],
        })

    def _do_child(self, elt, children):
        obj_elt = elt.find('./object')
        packing_elt = elt.find('./packing')

        self._do_object(obj_elt)

        child_properties = []
        if packing_elt is not None:
            for xml_child in packing_elt.findall('./property'):
                child_properties.append(Property(xml_child))

        child_class_name = obj_elt.attrib["id"]
        child = self._classes[child_class_name]
        child._child_properties = child_properties
        children.append(child_class_name)
