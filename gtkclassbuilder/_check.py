"""This module check the validity of an element read from a ``.glade`` file.

passing the root element to `interface` will verify that the xml tree
beneath it conforms to the requirements of this library. It is so named since
the root element must be an ``<interface>`` element. If the xml tree is
invalid, an exception of type `BadInput` will be raised.
"""
import logging

logger = logging.getLogger(__name__)


class BadInput(Exception):
    """An error indicating failure to validate the input."""
    pass


def _or_raise(test, exn):
    """Raise exn if test is False."""
    if not test:
        raise exn


def _check_attrs(elt, required=(), recognized=()):
    """Verify that elt has each of the elements in `required`.

    :param elt: is the element to check.
    :param required: must be a tuple or list of strings, each of which is the
        name of a required attribute.
    :param recognized: is a list of additional attributes that `elt` may also
        have.

    If `elt` has an attribute that is not in either required or recognized,
    a warning will be logged. If it is missing any elements in required, a
    `BadInput` exception will be raised.
    """
    required = set(required)
    recognized = set(recognized)
    for attr in elt.attrib:
        if attr in required:
            required.remove(attr)
        elif attr not in recognized:
            logger.warn("Unrecognized attribute %r for %r element" %
                        (attr, elt.tag))
    _or_raise(len(required) == 0,
              BadInput("element %r is missing required elements: %r" %
                       (elt.tag, list(required))))


def interface(elt):
    """Validate the ``<interface>`` element `elt`.

    The root element in a glade file must be an interface element, therefore
    this function may be used to validate the entire document.

    If the element does not validate, a `BadInput` exception will be raised.
    """
    _or_raise(elt.tag == 'interface',
              BadInput("Expected 'interface' element but got %r" % elt.tag))
    _check_attrs(elt)
    children = list(filter(lambda e: e.tag == 'object', elt))
    children = list(elt)
    _or_raise(len(children) > 0,
              BadInput('Interface with no children'))
    have_object = False
    for child in children:
        if child.tag == 'object':
            have_object = True
            _object(child)
        else:
            logger.warn('Unrecognized element %r' % child.tag)
    _or_raise(have_object, BadInput('Interface has no object child'))


# The remainder of these functions are like `interface` but for differnet
# elements corresponding to their names; _object for <object>, _property for
# <property>, and so on.


def _object(elt):
    _check_attrs(elt, ['id', 'class'], ['signal'])
    _or_raise(elt.attrib['class'].startswith('Gtk'),
              BadInput("Object has non Gtk class: %r" % elt.attrib['class']))
    for child in elt:
        if child.tag == 'property':
            _property(child)
        elif child.tag == 'child':
            _child(child)
        elif child.tag == 'signal':
            _signal(child)


def _property(elt):
    _check_attrs(elt, ['name'])
    _or_raise('name' in elt.attrib, BadInput("Property with no name"))
    _or_raise(len(list(elt)) == 0, BadInput("Property with non-text child"))
    _or_raise(len(list(elt.itertext())) == 1,
              BadInput("Property with more than one child"))


def _signal(elt):
    _check_attrs(elt, ['name', 'handler'])


def _child(elt):
    _check_attrs(elt)
    children = list(elt)
    _or_raise(len(children) > 0, BadInput("Child with no child elements"))
    _or_raise(children[0].tag == 'object',
              BadInput("First child of child element is not an object"))
    if len(children) > 1:
        _or_raise(children[1].tag == 'packing',
                  BadInput("Second child of child element is not packing"))
        _packing(children[1])
    _object(children[0])


def _packing(elt):
    _check_attrs(elt)
    for child in elt:
        _or_raise(child.tag == 'property',
                  BadInput('Child of packing is not a property'))
        _property(child)
