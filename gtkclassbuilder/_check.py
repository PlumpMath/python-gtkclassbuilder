

class BadInput(Exception):
    pass


def _or_raise(test, exn):
    if not test:
        raise exn


def interface(elt):
    _or_raise(elt.tag == 'interface',
              BadInput("Expected 'interface' element but got %r" % elt.tag))
    children = list(filter(lambda e: e.tag == 'object', elt))
    _or_raise(len(children) > 0, BadInput('No object children'))
    for child in children:
        _object(child)


def _object(elt):
    _or_raise('id' in elt.attrib, BadInput("Object with no id"))
    _or_raise('class' in elt.attrib, BadInput("Object with no class"))
    for child in elt:
        if child.tag == 'property':
            _property(child)
        elif child.tag == 'child':
            _child(child)


def _property(elt):
    _or_raise('name' in elt.attrib, BadInput("Property with no name"))
    _or_raise(len(list(elt)) == 0, BadInput("Property with non-text child"))
    _or_raise(len(list(elt.itertext())) == 1,
              BadInput("Property with more than one child"))


def _child(elt):
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
    for child in elt:
        _or_raise(child.tag == 'property',
                  BadInput('Child of packing is not a property'))
        _property(child)
