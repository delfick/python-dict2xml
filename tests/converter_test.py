from textwrap import dedent
from unittest import mock

import pytest

from dict2xml import Converter


class TestConverter:
    class TestBuilding:
        def test_creates_an_indenter_a_node_and_then_calls_serialize_on_the_node_with_the_indenter(
            self,
        ):
            wrap = mock.Mock("wrap")
            indent = mock.Mock("indent")
            newlines = mock.Mock("newlines")
            converter = Converter(wrap, indent, newlines)

            node = mock.Mock(name="node")
            FakeNode = mock.Mock(name="Node", return_value=node)

            serialized = mock.Mock(name="serialized")
            node.serialize.return_value = serialized

            indenter = mock.Mock(name="indenter")
            make_indenter = mock.Mock(name="make_indenter", return_value=indenter)

            mip = mock.patch.object(converter, "_make_indenter", make_indenter)
            fnp = mock.patch("dict2xml.logic.Node", FakeNode)

            data = mock.Mock(name="data")

            with mip, fnp:
                assert converter.build(data) is serialized

            FakeNode.assert_called_once_with(
                wrap=wrap,
                data=data,
                iterables_repeat_wrap=True,
                closed_tags_for=None,
                data_sorter=None,
            )
            node.serialize.assert_called_once_with(indenter)

        def tes_does_not_repeat_the_wrap_of_iterables_repeat_wrap_is_false(self):
            example = {
                "array": [
                    {"item": {"string1": "string", "string2": "string"}},
                    {"item": {"string1": "other string", "string2": "other string"}},
                ]
            }

            result = Converter("").build(example, iterables_repeat_wrap=False)
            assert (
                result
                == dedent(
                    """
                <array>
                  <item>
                    <string1>string</string1>
                    <string2>string</string2>
                  </item>
                  <item>
                    <string1>other string</string1>
                    <string2>other string</string2>
                  </item>
                </array>
            """
                ).strip()
            )

        def test_can_produce_self_closing_tags(self):
            example = {
                "item1": None,
                "item2": {"string1": "", "string2": None},
                "item3": "special",
            }

            result = Converter("").build(example, closed_tags_for=[None])
            assert (
                result
                == dedent(
                    """
                <item1/>
                <item2>
                  <string1></string1>
                  <string2/>
                </item2>
                <item3>special</item3>
            """
                ).strip()
            )

            result = Converter("").build(example, closed_tags_for=[None, ""])
            assert (
                result
                == dedent(
                    """
                <item1/>
                <item2>
                  <string1/>
                  <string2/>
                </item2>
                <item3>special</item3>
            """
                ).strip()
            )

            result = Converter("").build(example, closed_tags_for=["special"])
            print(result)
            assert (
                result
                == dedent(
                    """
                <item1>None</item1>
                <item2>
                  <string1></string1>
                  <string2>None</string2>
                </item2>
                <item3/>
            """
                ).strip()
            )

    class TestMakingIndentationFunction:
        @pytest.fixture()
        def V(self):
            class V:
                with_indent = Converter(indent="    ", newlines=True)
                without_indent = Converter(indent="", newlines=True)
                without_newlines = Converter(newlines=False)

                def assertIndenter(self, indenter, nodes, wrap, expected):
                    result = "".join([wrap, indenter(nodes, wrap), wrap])
                    assert result == expected.strip()

            return V()

        class TestNoNewlines:
            def test_joins_nodes_with_empty_string(self, V):
                indenter = V.without_newlines._make_indenter()
                assert indenter(["a", "b", "c"], True) == "abc"
                assert indenter(["d", "e", "f"], False) == "def"

        class TestWithNewlines:
            class TestNoIndentation:
                def test_joins_with_newlines_and_never_indents(self, V):
                    # Wrap is added to expected output via test_indenter
                    indenter = V.without_indent._make_indenter()
                    V.assertIndenter(
                        indenter,
                        ["a", "b", "c"],
                        "<>",
                        dedent(
                            """
                            <>
                            a
                            b
                            c
                            <>"""
                        ),
                    )

            class TestWithIndentation:
                def test_joins_with_newlines_and_indents_if_there_is_a_wrapping_tag(self, V):
                    # Wrap is added to expected output via test_indenter
                    indenter = V.with_indent._make_indenter()
                    V.assertIndenter(
                        indenter,
                        ["a", "b", "c"],
                        "<>",
                        dedent(
                            """
                            <>
                                a
                                b
                                c
                            <>"""
                        ),
                    )

                def test_joins_with_newlines_but_does_not_indent_if_no_wrapping_tag(self, V):
                    indenter = V.with_indent._make_indenter()
                    V.assertIndenter(
                        indenter,
                        ["a", "b", "c"],
                        "",
                        dedent(
                            """
                          a
                          b
                          c"""
                        ),
                    )

                def test_it_reindents_each_new_line(self, V):
                    node1 = dedent(
                        """
                        a
                            b
                        c
                            d
                            e
                        """
                    ).strip()

                    node2 = "f"
                    node3 = dedent(
                        """
                        f
                            g
                                h
                        """
                    ).strip()

                    # Wrap is added to expected output via test_indenter
                    indenter = V.with_indent._make_indenter()
                    V.assertIndenter(
                        indenter,
                        [node1, node2, node3],
                        "<>",
                        dedent(
                            """
                            <>
                                a
                                    b
                                c
                                    d
                                    e
                                f
                                f
                                    g
                                        h
                            <>
                            """
                        ),
                    )
