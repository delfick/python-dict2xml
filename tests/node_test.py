import collections
import collections.abc
from unittest import mock

from dict2xml import DataSorter, Node


class TestNode:
    def test_determines_type_at_instantiation(self):
        assert Node(data={}).type == "mapping"
        assert Node(data=[]).type == "iterable"
        for d in ["", "asdf", "", "asdf", 0, 1, False, True]:
            assert Node(data=d).type == "flat"

    class TestHandlingEntities:
        def test_will_change_string_data_to_take_entities_into_account(self):
            node = Node(data="<2&a>")
            assert node.data == "&lt;2&amp;a&gt;"

    class TestDetermininType:
        def assertType(self, *datas, **kwargs):
            expected = kwargs.get("expected", None)
            for d in datas:
                assert Node(data=d).determine_type() == expected

        def test_says_strings_are_falt(self):
            self.assertType("", "asdf", "", "asdf", expected="flat")

        def test_says_numbers_and_booleans_are_flat(self):
            self.assertType(0, 1, False, True, expected="flat")

        def test_says_anything_that_implements_dunder_iter_is_an_iterable(self):
            class IterableObject(object):
                def __iter__(s):
                    return []

            self.assertType((), [], set(), IterableObject(), expected="iterable")

        def test_says_anything_that_is_a_dict_or_subclass_of_collections_Mapping_is_a_mapping(
            self,
        ):
            class MappingObject(collections.abc.Mapping):
                def __len__(s):
                    return 0

                def __iter__(s):
                    return []

                def __getitem__(s, key):
                    return key

            self.assertType({}, MappingObject(), expected="mapping")

        def test_can_not_determine_if_an_object_is_a_mapping_if_it_is_not_subclass_of_collections_Mapping(
            self,
        ):
            # Would be great if possible, but doesn't seem to be :(
            class WantsToBeMappingObject(object):
                def __iter__(s):
                    return []

                def __getitem__(s, key):
                    return key

            self.assertType(WantsToBeMappingObject(), expected="iterable")

    class TestConversion:
        def test_it_returns_list_of_Nodes_with_key_as_wrap_and_item_as_data_if_type_is_mapping(
            self,
        ):
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
                    data=data,
                    iterables_repeat_wrap=irw,
                    closed_tags_for=ctf,
                    data_sorter=ds,
                ).convert()
                assert result == ("", nodes)

            assert FakeNode.mock_calls == [
                mock.call(
                    "a",
                    "",
                    1,
                    iterables_repeat_wrap=irw,
                    closed_tags_for=ctf,
                    data_sorter=ds,
                ),
                mock.call(
                    "b",
                    "",
                    2,
                    iterables_repeat_wrap=irw,
                    closed_tags_for=ctf,
                    data_sorter=ds,
                ),
                mock.call(
                    "c",
                    "",
                    3,
                    iterables_repeat_wrap=irw,
                    closed_tags_for=ctf,
                    data_sorter=ds,
                ),
            ]

        def test_it_respects_the_order_of_an_ordered_dict(self):
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
                    data=data,
                    iterables_repeat_wrap=irw,
                    closed_tags_for=ctf,
                    data_sorter=ds,
                ).convert()
                assert result == ("", nodes)

            assert FakeNode.mock_calls == [
                mock.call(
                    "b",
                    "",
                    2,
                    iterables_repeat_wrap=irw,
                    closed_tags_for=ctf,
                    data_sorter=ds,
                ),
                mock.call(
                    "c",
                    "",
                    3,
                    iterables_repeat_wrap=irw,
                    closed_tags_for=ctf,
                    data_sorter=ds,
                ),
                mock.call(
                    "a",
                    "",
                    1,
                    iterables_repeat_wrap=irw,
                    closed_tags_for=ctf,
                    data_sorter=ds,
                ),
            ]

        def test_it_can_be_told_to_also_sort_OrderdDict(self):
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
                    data=data,
                    iterables_repeat_wrap=irw,
                    closed_tags_for=ctf,
                    data_sorter=ds,
                ).convert()
                assert result == ("", nodes)

            assert FakeNode.mock_calls == [
                mock.call(
                    "a",
                    "",
                    1,
                    iterables_repeat_wrap=irw,
                    closed_tags_for=ctf,
                    data_sorter=ds,
                ),
                mock.call(
                    "b",
                    "",
                    2,
                    iterables_repeat_wrap=irw,
                    closed_tags_for=ctf,
                    data_sorter=ds,
                ),
                mock.call(
                    "c",
                    "",
                    3,
                    iterables_repeat_wrap=irw,
                    closed_tags_for=ctf,
                    data_sorter=ds,
                ),
            ]

        def test_it_can_be_told_to_never_sort(self):
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
                    data=data,
                    iterables_repeat_wrap=irw,
                    closed_tags_for=ctf,
                    data_sorter=ds,
                ).convert()
                assert result == ("", nodes)

            assert FakeNode.mock_calls == [
                mock.call(
                    "c",
                    "",
                    3,
                    iterables_repeat_wrap=irw,
                    closed_tags_for=ctf,
                    data_sorter=ds,
                ),
                mock.call(
                    "a",
                    "",
                    1,
                    iterables_repeat_wrap=irw,
                    closed_tags_for=ctf,
                    data_sorter=ds,
                ),
                mock.call(
                    "b",
                    "",
                    2,
                    iterables_repeat_wrap=irw,
                    closed_tags_for=ctf,
                    data_sorter=ds,
                ),
            ]

        def test_it_returns_list_of_Nodes_with_wrap_as_tag_and_item_as_data_if_type_is_iterable(
            self,
        ):
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
                    data=data,
                    iterables_repeat_wrap=irw,
                    closed_tags_for=ctf,
                    data_sorter=ds,
                ).convert()
                assert result == ("", nodes)

            assert FakeNode.mock_calls == [
                mock.call(
                    "",
                    "",
                    1,
                    iterables_repeat_wrap=irw,
                    closed_tags_for=ctf,
                    data_sorter=ds,
                ),
                mock.call(
                    "",
                    "",
                    2,
                    iterables_repeat_wrap=irw,
                    closed_tags_for=ctf,
                    data_sorter=ds,
                ),
                mock.call(
                    "",
                    "",
                    3,
                    iterables_repeat_wrap=irw,
                    closed_tags_for=ctf,
                    data_sorter=ds,
                ),
            ]

        def test_it_returns_data_enclosed_in_tags_made_from_self_tag_if_not_iterable_or_mapping(
            self,
        ):
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

        def test_it_returns_data_as_is_if_not_iterable_or_mapping_and_no_self_tag(self):
            tag = ""
            results = []
            for d in [0, 1, "", "", "asdf", "qwer", False, True]:
                val, children = Node(tag=tag, data=d).convert()
                assert len(children) == 0
                results.append(val)

            assert results == ["0", "1", "", "", "asdf", "qwer", "False", "True"]
