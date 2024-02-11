# coding: spec

from textwrap import dedent
from unittest import mock

import pytest

from dict2xml import Converter

describe "Converter":
    describe "Building":

        it "creates an indenter, a node, and then calls serialize on the node with the indenter":
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

        it "doesn't repeat the wrap if iterables_repeat_wrap is False":
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

        it "can produce self closing tags":
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

    describe "Making indentation function":

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

        describe "No newlines":
            it "joins nodes with empty string", V:
                indenter = V.without_newlines._make_indenter()
                assert indenter(["a", "b", "c"], True) == "abc"
                assert indenter(["d", "e", "f"], False) == "def"

        describe "With newlines":
            describe "No indentation":
                it "joins with newlines and never indents", V:
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

            describe "With indentation":
                it "joins with newlines and indents if there is a wrapping tag", V:
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

                it "joins with newlines but doesn't indent if no wrapping tag", V:
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

                it "reindents each new line", V:
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
