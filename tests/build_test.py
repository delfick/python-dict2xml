# coding: spec

from dict2xml import Converter, dict2xml

from unittest import TestCase
from textwrap import dedent
import fudge

describe TestCase, "Build":

    def compare(self, data, result, **kwargs):
        self.assertEqual.__self__.maxDiff = None
        converter = Converter(wrap="all", **kwargs)
        made = converter.build(data)
        self.assertEqual(result.strip(), made)

    describe "Convenience Function":

        @fudge.patch("dict2xml.Converter")
        it "Creates a Converter with *args and **kwargs and calls build on it with provided data", fakeConverter:
            data = fudge.Fake("data")
            serialized = fudge.Fake("serialized")
            (
                fakeConverter.expects_call()
                .with_args(1, 2, 3, a=5, b=8)
                .returns_fake()
                .expects("build")
                .with_args(data)
                .returns(serialized)
            )

            self.assertEqual(dict2xml(data, 1, 2, 3, a=5, b=8), serialized)

    describe "Just Working":
        before_each:
            self.data = {"a": [1, 2, 3], "b": {"c": "d", "e": {"f": "g"}}, "d": 1}

        it "with both indentation and newlines":
            expected = dedent(
                """
                <all>
                  <a>1</a>
                  <a>2</a>
                  <a>3</a>
                  <b>
                    <c>d</c>
                    <e>
                      <f>g</f>
                    </e>
                  </b>
                  <d>1</d>
                </all>"""
            )
            self.compare(self.data, expected, indent="  ", newlines=True)

        it "with just newlines":
            expected = dedent(
                """
                <all>
                <a>1</a>
                <a>2</a>
                <a>3</a>
                <b>
                <c>d</c>
                <e>
                <f>g</f>
                </e>
                </b>
                <d>1</d>
                </all>"""
            )
            self.compare(self.data, expected, indent=None, newlines=True)

        it "with just indentation":
            # Indentation requires newlines to work... so meh
            expected = "<all><a>1</a><a>2</a><a>3</a><b><c>d</c><e><f>g</f></e></b><d>1</d></all>"
            self.compare(self.data, expected, indent="  ", newlines=False)

        it "with no whitespace":
            expected = "<all><a>1</a><a>2</a><a>3</a><b><c>d</c><e><f>g</f></e></b><d>1</d></all>"
            self.compare(self.data, expected, indent=None, newlines=False)

        it "works on a massive, complex dictionary":
            from tests.examples.python_dict import data
            from tests.examples.xml_result import result

            self.compare(data, result, indent="  ", newlines=True)
