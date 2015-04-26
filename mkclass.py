from gi.repository import Gtk

class BadInput(Exception):
    pass

def _or_raise(test, exn):
    if not test:
        raise exn

def check(elt):
    _or_raise(elt.tag == 'interface',
              BadInput("Expected 'interface' element but got %r" % elt.tag))
    children = filter(lambda e: e.tag == 'object', elt)
    for child in children:
        _check_object(child)

def _check_object(elt):
    _or_raise('id' in elt.attrib, BadInput("Object with no id"))
    _or_raise('class' in elt.attrib, BadInput("Object with no class"))
    for child in elt:
        if child.tag == 'property':
            _check_property(child)
        elif child.tag == 'child':
            _check_child(child)

def _check_property(elt):
    _or_raise('name' in elt.attrib, BadInput("Property with no name"))
    _or_raise(len(list(elt)) == 0, BadInput("Property with non-text child"))
    _or_raise(len(list(elt.itertext())) == 1,
              BadInput("Property with more than one child"))


def _check_child(elt):
    children = list(elt)
    _or_raise(len(children) > 0, BadInput("Child with no child elements"))
    _or_raise(children[0].tag == 'object',
              BadInput("First child of child element is not an object"))
    if len(children) > 1:
        _or_raise(children[1].tag == 'packing',
                  BadInput("Second child of child element is not packing"))
        _check_packing(children[1])
    _check_object(children[0])


def _check_packing(elt):
    for child in elt:
        _or_raise(child.tag == 'property',
                  BadInput('Child of packing is not a property'))
        _check_property(child)


def make_class(elt):
    assert elt.tag == 'object'

    props = {}
    children = []

    for child in elt:
        if child.tag == 'property':
            props[_prop_key(child)] = _prop_val(child)
        elif child.tag == 'child':
            obj = child[0]
            if len(child) > 1:
                pack_elts = child[1]
            else:
                pack_elts = []
            ChildClass = make_class(obj)
            pack_props = {}
            for prop in pack_elts:
                pack_props[_prop_key(prop)] = _prop_val(prop)
            children.append((ChildClass, pack_props))

    ParentClass = getattr(Gtk, elt.attrib['class'][3:])

    class ResultClass(ParentClass):

        def __init__(self):
            ParentClass.__init__(self, **props)
            for ChildClass, pack_props in children:
                child = ChildClass()
                self.add(child)
                for propname in pack_props.keys():
                    self.child_set_property(child, propname, pack_props[propname])

    ResultClass.__name__ = elt.attrib['id']
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
