from dict2xml.logic import Converter, DataSorter, Node

from .version import VERSION


def dict2xml(
    data,
    wrap=None,
    indent="  ",
    newlines=True,
    iterables_repeat_wrap=True,
    closed_tags_for=None,
    data_sorter=None,
):
    """Return an XML string of a Python dict object."""
    return Converter(wrap=wrap, indent=indent, newlines=newlines).build(
        data,
        iterables_repeat_wrap=iterables_repeat_wrap,
        closed_tags_for=closed_tags_for,
        data_sorter=data_sorter,
    )


__all__ = ["dict2xml", "Converter", "Node", "VERSION", "DataSorter"]
