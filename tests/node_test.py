# coding: spec

import collections
import collections.abc
from unittest import mock

from dict2xml import DataSorter, Node

describe "Node":
    it "determines type at instantiation":
        assert Node(data={}).type == "mapping"
        assert Node(data=[]).type == "iterable"
        for d in ["", "asdf", "", "asdf", 0, 1, False, True]:
            assert Node(data=d).type == "flat"

    describe "Handling entities":
        it "will change string data to take entities into account":
            node = Node(data="<2&a>")
            assert node.data == "&lt;2&amp;a&gt;"

    describe "Determining type":

        def assertType(self, *datas, **kwargs):
            expected = kwargs.get("expected", None)
            for d in datas:
                assert Node(data=d).determine_type() == expected

        it "says strings are flat":
            self.assertType("", "asdf", "", "asdf", expected="flat")

        it "says numbers and booleans are flat":
            self.assertType(0, 1, False, True, expected="flat")

        it "says anything that implements __iter__  is an iterable":

            class IterableObject(object):
                def __iter__(s):
                    return []

            self.assertType((), [], set(), IterableObject(), expected="iterable")

        it "says anything that is a dict or subclass of collections.Mapping is a mapping":

            class MappingObject(collections.abc.Mapping):
                def __len__(s):
                    return 0

                def __iter__(s):
                    return []

                def __getitem__(s, key):
                    return key

            self.assertType({}, MappingObject(), expected="mapping")

        it "can't determine if an object is a mapping if it isn't sublass of collections.Mapping":
            # Would be great if possible, but doesn't seem to be :(
            class WantsToBeMappingObject(object):
                def __iter__(s):
                    return []

                def __getitem__(s, key):
                    return key

            self.assertType(WantsToBeMappingObject(), expected="iterable")

    describe "Conversion":

        it "returns list of Nodes with key as wrap and item as data if type is mapping":

            called = []

            nodes = [mock.Mock(name="n{0}".format(i)) for i in range(3)]

            def N(*args, **kwargs):
                called.append(1)
                return nodes[len(called) - 1]

            ds = DataSorter()
            irw = mock.Mock("irw")
            ctf = mock.Mock("ctf")
            FakeNode = mock.Mock(name="Node", side_effect=N)

            with mock.patch("dict2xml.logic.Node", FakeNode):
                data = dict(a=1, b=2, c=3)
                result = Node(
                    data=data, iterables_repeat_wrap=irw, closed_tags_for=ctf, data_sorter=ds
                ).convert()
                assert result == ("", nodes)

            assert FakeNode.mock_calls == [
                mock.call(
                    "a", "", 1, iterables_repeat_wrap=irw, closed_tags_for=ctf, data_sorter=ds
                ),
                mock.call(
                    "b", "", 2, iterables_repeat_wrap=irw, closed_tags_for=ctf, data_sorter=ds
                ),
                mock.call(
                    "c", "", 3, iterables_repeat_wrap=irw, closed_tags_for=ctf, data_sorter=ds
                ),
            ]

        it "respects the order of an OrderedDict":
            called = []

            nodes = [mock.Mock(name="n{0}".format(i)) for i in range(3)]

            def N(*args, **kwargs):
                called.append(1)
                return nodes[len(called) - 1]

            ds = DataSorter()
            irw = mock.Mock("irw")
            ctf = mock.Mock("ctf")
            FakeNode = mock.Mock(name="Node", side_effect=N)

            with mock.patch("dict2xml.logic.Node", FakeNode):
                data = collections.OrderedDict([("b", 2), ("c", 3), ("a", 1)])
                result = Node(
                    data=data, iterables_repeat_wrap=irw, closed_tags_for=ctf, data_sorter=ds
                ).convert()
                assert result == ("", nodes)

            assert FakeNode.mock_calls == [
                mock.call(
                    "b", "", 2, iterables_repeat_wrap=irw, closed_tags_for=ctf, data_sorter=ds
                ),
                mock.call(
                    "c", "", 3, iterables_repeat_wrap=irw, closed_tags_for=ctf, data_sorter=ds
                ),
                mock.call(
                    "a", "", 1, iterables_repeat_wrap=irw, closed_tags_for=ctf, data_sorter=ds
                ),
            ]

        it "can be told to also sort OrderedDict":
            called = []

            nodes = [mock.Mock(name="n{0}".format(i)) for i in range(3)]

            def N(*args, **kwargs):
                called.append(1)
                return nodes[len(called) - 1]

            ds = DataSorter.always()
            irw = mock.Mock("irw")
            ctf = mock.Mock("ctf")
            FakeNode = mock.Mock(name="Node", side_effect=N)

            with mock.patch("dict2xml.logic.Node", FakeNode):
                data = collections.OrderedDict([("b", 2), ("c", 3), ("a", 1)])
                result = Node(
                    data=data, iterables_repeat_wrap=irw, closed_tags_for=ctf, data_sorter=ds
                ).convert()
                assert result == ("", nodes)

            assert FakeNode.mock_calls == [
                mock.call(
                    "a", "", 1, iterables_repeat_wrap=irw, closed_tags_for=ctf, data_sorter=ds
                ),
                mock.call(
                    "b", "", 2, iterables_repeat_wrap=irw, closed_tags_for=ctf, data_sorter=ds
                ),
                mock.call(
                    "c", "", 3, iterables_repeat_wrap=irw, closed_tags_for=ctf, data_sorter=ds
                ),
            ]

        it "can be told to never sort":
            called = []

            nodes = [mock.Mock(name="n{0}".format(i)) for i in range(3)]

            def N(*args, **kwargs):
                called.append(1)
                return nodes[len(called) - 1]

            ds = DataSorter.never()
            irw = mock.Mock("irw")
            ctf = mock.Mock("ctf")
            FakeNode = mock.Mock(name="Node", side_effect=N)

            with mock.patch("dict2xml.logic.Node", FakeNode):
                data = {"c": 3, "a": 1, "b": 2}
                result = Node(
                    data=data, iterables_repeat_wrap=irw, closed_tags_for=ctf, data_sorter=ds
                ).convert()
                assert result == ("", nodes)

            assert FakeNode.mock_calls == [
                mock.call(
                    "c", "", 3, iterables_repeat_wrap=irw, closed_tags_for=ctf, data_sorter=ds
                ),
                mock.call(
                    "a", "", 1, iterables_repeat_wrap=irw, closed_tags_for=ctf, data_sorter=ds
                ),
                mock.call(
                    "b", "", 2, iterables_repeat_wrap=irw, closed_tags_for=ctf, data_sorter=ds
                ),
            ]

        it "returns list of Nodes with wrap as tag and item as data if type is iterable":
            called = []

            nodes = [mock.Mock(name="n{0}".format(i)) for i in range(3)]

            def N(*args, **kwargs):
                called.append(1)
                return nodes[len(called) - 1]

            ds = DataSorter()
            irw = mock.Mock("irw")
            ctf = mock.Mock("ctf")
            FakeNode = mock.Mock(name="Node", side_effect=N)

            with mock.patch("dict2xml.logic.Node", FakeNode):
                data = [1, 2, 3]
                result = Node(
                    data=data, iterables_repeat_wrap=irw, closed_tags_for=ctf, data_sorter=ds
                ).convert()
                assert result == ("", nodes)

            assert FakeNode.mock_calls == [
                mock.call(
                    "", "", 1, iterables_repeat_wrap=irw, closed_tags_for=ctf, data_sorter=ds
                ),
                mock.call(
                    "", "", 2, iterables_repeat_wrap=irw, closed_tags_for=ctf, data_sorter=ds
                ),
                mock.call(
                    "", "", 3, iterables_repeat_wrap=irw, closed_tags_for=ctf, data_sorter=ds
                ),
            ]

        it "returns data enclosed in tags made from self.tag if not iterable or mapping":
            tag = "thing"
            results = []
            for d in [0, 1, "", "", "asdf", "qwer", False, True]:
                val, children = Node(tag=tag, data=d).convert()
                assert len(children) == 0
                results.append(val)

            assert results == [
                "<thing>0</thing>",
                "<thing>1</thing>",
                "<thing></thing>",
                "<thing></thing>",
                "<thing>asdf</thing>",
                "<thing>qwer</thing>",
                "<thing>False</thing>",
                "<thing>True</thing>",
            ]

        it "returns data as is if not iterable or mapping and no self.tag":
            tag = ""
            results = []
            for d in [0, 1, "", "", "asdf", "qwer", False, True]:
                val, children = Node(tag=tag, data=d).convert()
                assert len(children) == 0
                results.append(val)

            assert results == ["0", "1", "", "", "asdf", "qwer", "False", "True"]
