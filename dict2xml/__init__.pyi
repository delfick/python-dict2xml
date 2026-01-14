from collections.abc import Iterable

from dict2xml.logic import Converter, DataSorter, Node

from .version import VERSION

def dict2xml(
    data: object,
    wrap: str | None = None,
    indent: str = "  ",
    newlines: bool = True,
    iterables_repeat_wrap: bool = True,
    closed_tags_for: Iterable[object] | None = None,
    data_sorter: DataSorter | None = None,
) -> str: ...

__all__ = ["dict2xml", "Converter", "Node", "VERSION", "DataSorter"]
