# coding: spec

import json
import os
from textwrap import dedent
from unittest import mock

import pytest

from dict2xml import Converter, DataSorter, dict2xml

examples = os.path.join(os.path.dirname(__file__), "examples")

describe "Build":
    describe "Convenience Function":

        it "Creates a Converter with *args and **kwargs and calls build on it with provided data":
            data = mock.Mock(name="data")
            serialized = mock.Mock(name="serialized")

            converter = mock.Mock(name="converter")
            converter.build.return_value = serialized

            FakeConverter = mock.Mock(name="Converter", return_value=converter)
            data_sorter = DataSorter.never()

            with mock.patch("dict2xml.Converter", FakeConverter):
                assert (
                    dict2xml(
                        data,
                        wrap="wrap",
                        indent="indent",
                        newlines=False,
                        iterables_repeat_wrap=False,
                        closed_tags_for=["one"],
                        data_sorter=data_sorter,
                    )
                    is serialized
                )

            FakeConverter.assert_called_once_with(wrap="wrap", indent="indent", newlines=False)
            converter.build.assert_called_once_with(
                data, iterables_repeat_wrap=False, closed_tags_for=["one"], data_sorter=data_sorter
            )

    describe "Just Working":

        @pytest.fixture()
        def assertResult(self):
            def assertResult(result, **kwargs):
                data = {"a": [1, 2, 3], "b": {"c": "d", "e": {"f": "g"}}, "d": 1}

                converter = Converter(wrap="all", **kwargs)
                print(converter.build(data))
                assert dedent(result).strip() == converter.build(data)

            return assertResult

        it "with both indentation and newlines", assertResult:
            expected = """
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
                </all>
            """
            assertResult(expected, indent="  ", newlines=True)

        it "with just newlines", assertResult:
            expected = """
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
                </all>
            """
            assertResult(expected, indent=None, newlines=True)

        it "with just indentation", assertResult:
            # Indentation requires newlines to work
            expected = "<all><a>1</a><a>2</a><a>3</a><b><c>d</c><e><f>g</f></e></b><d>1</d></all>"
            assertResult(expected, indent="  ", newlines=False)

        it "with no whitespace", assertResult:
            expected = "<all><a>1</a><a>2</a><a>3</a><b><c>d</c><e><f>g</f></e></b><d>1</d></all>"
            assertResult(expected, indent=None, newlines=False)

        it "works on a massive, complex dictionary":
            with open(os.path.join(examples, "python_dict.json"), "r") as fle:
                data = json.load(fle)

            with open(os.path.join(examples, "result.xml"), "r") as fle:
                result = fle.read()

            converter = Converter(wrap="all", indent="  ", newlines=True)
            assert dedent(result).strip() == converter.build(data)
