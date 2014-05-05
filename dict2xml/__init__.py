from dict2xml.logic import Converter, Node

def dict2xml(data, *args, **kwargs):
    """Return an XML string of a Python dict object."""
    return Converter(*args, **kwargs).build(data)

