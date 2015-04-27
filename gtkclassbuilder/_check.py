import logging

logger = logging.getLogger(__name__)

class BadInput(Exception):
    pass


def _or_raise(test, exn):
    if not test:
        raise exn


def _check_attrs(elt, required=(), recognized=()):
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


def _object(elt):
    _check_attrs(elt, ['id', 'class'])
    for child in elt:
        if child.tag == 'property':
            _property(child)
        elif child.tag == 'child':
            _child(child)
        else:
            logger.warn('Unrecognized child element of object: %r' %
                         child.tag)


def _property(elt):
    _check_attrs(elt, ['name'])
    _or_raise('name' in elt.attrib, BadInput("Property with no name"))
    _or_raise(len(list(elt)) == 0, BadInput("Property with non-text child"))
    _or_raise(len(list(elt.itertext())) == 1,
              BadInput("Property with more than one child"))


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
