import re

# has_handler and get_handler implement the dict vs non dict logic needed by
# .builder.BuiltObject.connect_signals. If the user passes a dictionary, want
# to use the contents of the dictonary as our handlers, and otherwise we want
# to use the object's attributes.


def has_handler(handlers, name):
    """Return a boolean indicating whether `handlers` has the named handler."""
    if type(handlers) is dict:
        return name in handlers
    else:
        return hasattr(handlers, name)


def get_handler(handlers, name):
    """Get the handler with the given name from `handlers`."""
    if type(handlers) is dict:
        return handlers[name]
    else:
        return getattr(handlers, name)


def namespace_split(identifier):
    """Split a gobject namespace from an identifer.

    For example::

        >>> namespace_split("MylibFancyObject")
        ("Mylib", "FancyObject")
    """
    def replacement(match):
        return ':'.join(match.groups())
    repl = re.sub(r'([a-z])([A-Z])', replacement, identifier, count=1)
    return repl.split(':')
