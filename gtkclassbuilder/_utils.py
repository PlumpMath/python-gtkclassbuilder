import re

# _has_handler and _get_handler implement the dict vs non dict logic needed by
# .builder.BuiltObject.connect_signals.


def has_handler(handlers, name):
    if type(handlers) is dict:
        return name in handlers
    else:
        return hasattr(handlers, name)


def get_handler(handlers, name):
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
