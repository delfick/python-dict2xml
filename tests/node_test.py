# coding: spec

from dict2xml import Node, Converter

from noseOfYeti.tokeniser.support import noy_sup_setUp
from fudge import patched_context
from nose.tools import nottest
from unittest import TestCase
import collections
import unittest
import fudge

describe TestCase, "Node":
    it "determines type at instantiation":
        self.assertEqual(Node(data={}).type, "mapping")
        self.assertEqual(Node(data=[]).type, "iterable")
        for d in ["", "asdf", u'', u'asdf', 0, 1, False, True]:
            self.assertEqual(Node(data=d).type, "flat")

    describe "Handling entities":
        it "will change string data to take entities into account":
            node = Node(data="<2&a>")
            self.assertEqual(node.data, "&lt;2&amp;a&gt;")

    describe "Determining type":

        @nottest
        def compare_type(self, *datas, **kwargs):
            expected = kwargs.get("expected", None)
            for d in datas:
                self.assertEqual(Node(data=d).determine_type(), expected)

        it "says strings are flat":
            self.compare_type("", "asdf", u'', u'asdf'
                , expected = "flat"
                )

        it "says numbers and booleans are flat":
            self.compare_type(0, 1, False, True
                , expected = "flat"
                )

        it "says anything that implements __iter__  is an iterable":
            class IterableObject(object):
                def __iter__(self): return []

            self.compare_type((), [], set(), IterableObject()
                , expected = "iterable"
                )

        it "says anything that is a dict or subclass of collections.Mapping is a mapping":
            class MappingObject(collections.Mapping):
                def __len__(self): return 0
                def __iter__(self): return []
                def __getitem__(self, key): return key

            self.compare_type({}, MappingObject()
                , expected = "mapping"
                )

        it "can't determine if an object is a mapping if it isn't sublass of collections.Mapping":
            # Would be great if possible, but doesn't seem to be :(
            class WantsToBeMappingObject(object):
                def __iter__(self): return []
                def __getitem__(self, key): return key

            self.compare_type(WantsToBeMappingObject()
                , expected = "iterable"
                )

    describe "Conversion":
        @fudge.patch("dict2xml.logic.Node")
        it "returns list of Nodes with key as wrap and item as data if type is mapping", fakeNode:
            n1 = fudge.Fake("n1")
            n2 = fudge.Fake("n2")
            n3 = fudge.Fake("n3")
            irw = fudge.Fake("irw")
            data = dict(a=1, b=2, c=3)
            (fakeNode.expects_call()
                .with_args('a', "", 1, iterables_repeat_wrap=irw).returns(n1)
                .next_call().with_args("b", "", 2, iterables_repeat_wrap=irw).returns(n2)
                .next_call().with_args("c", "", 3, iterables_repeat_wrap=irw).returns(n3)
                )

            self.assertEqual(Node(data=data, iterables_repeat_wrap=irw).convert(), ("", [n1, n2, n3]))

        @fudge.patch("dict2xml.logic.Node")
        it "returns list of Nodes with wrap as tag and item as data if type is iterable", fakeNode:
            n1 = fudge.Fake("n1")
            n2 = fudge.Fake("n2")
            n3 = fudge.Fake("n3")
            irw = fudge.Fake("irw")
            wrap = fudge.Fake("wrap")
            data = [1, 2, 3]
            (fakeNode.expects_call()
                .with_args('', wrap, 1, iterables_repeat_wrap=irw).returns(n1)
                .next_call().with_args('', wrap, 2, iterables_repeat_wrap=irw).returns(n2)
                .next_call().with_args('', wrap, 3, iterables_repeat_wrap=irw).returns(n3)
                )

            self.assertEqual(Node(wrap=wrap, data=data, iterables_repeat_wrap=irw).convert(), ("", [n1, n2, n3]))

        it "returns data enclosed in tags made from self.tag if not iterable or mapping":
            tag = "thing"
            results = []
            for d in [0, 1, '', u'', 'asdf', u'qwer', False, True]:
                val, children = Node(tag=tag, data=d).convert()
                self.assertEqual(len(children), 0)
                results.append(val)

            self.assertEqual(results,
                [ "<thing>0</thing>"
                , "<thing>1</thing>"
                , "<thing></thing>"
                , "<thing></thing>"
                , "<thing>asdf</thing>"
                , "<thing>qwer</thing>"
                , "<thing>False</thing>"
                , "<thing>True</thing>"
                ])

        it "returns data as is if not iterable or mapping and no self.tag":
            tag = ""
            results = []
            for d in [0, 1, '', u'', 'asdf', u'qwer', False, True]:
                val, children = Node(tag=tag, data=d).convert()
                self.assertEqual(len(children), 0)
                results.append(val)

            self.assertEqual(results,
                [ "0"
                , "1"
                , ""
                , ""
                , "asdf"
                , "qwer"
                , "False"
                , "True"
                ])

