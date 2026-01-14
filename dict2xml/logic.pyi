import re
from collections.abc import Iterable, Iterator, Mapping, Sequence
from typing import Literal, Protocol

start_ranges: str
NameStartChar: re.Pattern[str]
NameChar: re.Pattern[str]

########################
###   NODE
########################

class DataSorter:
    """
    Used to sort a map of data depending on it's type
    """

    def keys_from(self, data: Mapping[str, object]) -> Mapping[str, object]: ...

    class always:
        def keys_from(self, data: Mapping[str, object]) -> Mapping[str, object]: ...

    class never:
        def keys_from(self, data: Mapping[str, object]) -> Mapping[str, object]: ...

class _Indentor(Protocol):
    def __call__(self, items: Iterator[str], wrap: str, /) -> str: ...

class Node:
    # A mapping of characters to treat as escapable entities and their replacements
    entities: Sequence[tuple[str, str]]

    wrap: str
    tag: str
    type: Literal["flat", "mapping", "iterable"]
    data: object | None
    iterables_repeat_wrap: bool
    closed_tags_for: Iterable[object] | None
    data_sorter: DataSorter

    def __init__(
        self,
        wrap: str = "",
        tag: str = "",
        data: object | None = None,
        iterables_repeat_wrap: bool = True,
        closed_tags_for: Iterable[object] | None = None,
        data_sorter: DataSorter | None = None,
    ) -> None: ...
    def serialize(self, indenter: _Indentor) -> str: ...
    def determine_type(self) -> Literal["flat", "mapping", "iterable"]: ...
    def convert(self) -> tuple[str, Sequence[Node]]: ...
    @staticmethod
    def sanitize_element(wrap: str) -> str: ...

########################
###   CONVERTER
########################

class Converter:
    wrap: str | None
    indent: str
    newlines: bool

    def __init__(
        self, wrap: str | None = None, indent: str = "  ", newlines: bool = True
    ): ...
    def _make_indenter(self) -> _Indentor: ...
    def build(
        self,
        data: object,
        iterables_repeat_wrap: bool = True,
        closed_tags_for: Iterable[object] | None = None,
        data_sorter: DataSorter | None = None,
    ) -> str: ...
