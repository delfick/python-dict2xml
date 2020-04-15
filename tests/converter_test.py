# coding: spec

from dict2xml import Converter

from fudge import patched_context
from nose.tools import nottest
from unittest import TestCase
from textwrap import dedent
import fudge

describe TestCase, "Converter":
    describe "Building":

        @fudge.patch("dict2xml.logic.Node")
        it "creates an indenter, a node, and then calls serialize on the node with the indenter", fakeNode:
            wrap = fudge.Fake("wrap")
            data = fudge.Fake("data")
            indent = fudge.Fake("indent")
            newlines = fudge.Fake("newlines")
            indenter = fudge.Fake("indenter")
            serialized = fudge.Fake("serialized")

            converter = Converter(wrap, indent, newlines)

            # Model movement of data through a Node
            (
                fakeNode.expects_call()
                .with_args(wrap=wrap, data=data, iterables_repeat_wrap=True)
                .returns_fake()
                .expects("serialize")
                .with_args(indenter)
                .returns(serialized)
            )

            # patch converter to return a dummy indenter function
            fakeMakeIndenter = fudge.Fake("_make_indenter").expects_call().returns(indenter)
            with patched_context(converter, "_make_indenter", fakeMakeIndenter):
                # Test the data flow
                self.assertEqual(converter.build(data), serialized)

        it "doesn't repeat the wrap if iterables_repeat_wrap is False":
            example = {
                "array": [
                    {"item": {"string1": "string", "string2": "string"}},
                    {"item": {"string1": "other string", "string2": "other string"}},
                ]
            }

            result = Converter("").build(example, iterables_repeat_wrap=False)
            self.assertEqual(
                result,
                dedent(
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
                ).strip(),
            )

    describe "Making indentation function":

        @nottest
        def test_indenter(self, indenter, nodes, wrap, expected):
            self.assertEqual(
                "{0}{1}{2}".format(wrap, indenter(nodes, wrap), wrap), expected.strip()
            )

        before_each:
            self.withIndent = Converter(indent="    ", newlines=True)
            self.withoutIndent = Converter(indent="", newlines=True)
            self.withoutNewlines = Converter(newlines=False)

        describe "No newlines":
            it "joins nodes with empty string":
                indenter = self.withoutNewlines._make_indenter()
                self.assertEqual(indenter(["a", "b", "c"], True), "abc")
                self.assertEqual(indenter(["d", "e", "f"], False), "def")

        describe "With newlines":
            describe "No indentation":
                it "joins with newlines and never indents":
                    # Wrap is added to expected output via test_indenter
                    indenter = self.withoutIndent._make_indenter()
                    self.test_indenter(
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
                it "joins with newlines and indents if there is a wrapping tag":
                    # Wrap is added to expected output via test_indenter
                    indenter = self.withIndent._make_indenter()
                    self.test_indenter(
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

                it "joins with newlines but doesn't indent if no wrapping tag":
                    indenter = self.withIndent._make_indenter()
                    self.test_indenter(
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

                it "reindents each new line":
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
                    indenter = self.withIndent._make_indenter()
                    self.test_indenter(
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
