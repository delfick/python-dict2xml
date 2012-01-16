# coding: spec

from dict2xml import Node, Converter

from fudge import patched_context
from nose.tools import nottest
import collections
import fudge

describe "Node":
    it "determines type at instantiation":
        Node(data={}).type |should| equal_to("mapping")
        Node(data=[]).type |should| equal_to("iterable")
        for d in ["", "asdf", u'', u'asdf', 0, 1, False, True]:
            Node(data=d).type |should| equal_to("flat")
    
    describe "Determining type":
        
        @nottest
        def compare_type(self, *datas, **kwargs):
            expected = kwargs.get("expected", None)
            for d in datas:
                Node(data=d).determine_type() |should| equal_to(expected)
            
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
        @fudge.patch("dict2xml.Node")
        it "returns list of Nodes with key as wrap and item as data if type is mapping", fakeNode:
            n1 = fudge.Fake("n1")
            n2 = fudge.Fake("n2")
            n3 = fudge.Fake("n3")
            data = dict(a=1, b=2, c=3)
            (fakeNode.expects_call()
                .with_args('a', "", 1).returns(n1)
                .next_call().with_args("b", "", 2).returns(n2)
                .next_call().with_args("c", "", 3).returns(n3)
                )
            
            Node(data=data).convert() |should| equal_to(("", [n1, n2, n3]))
        
        @fudge.patch("dict2xml.Node")
        it "returns list of Nodes with wrap as tag and item as data if type is iterable", fakeNode:
            n1 = fudge.Fake("n1")
            n2 = fudge.Fake("n2")
            n3 = fudge.Fake("n3")
            wrap = fudge.Fake("wrap")
            data = [1, 2, 3]
            (fakeNode.expects_call()
                .with_args('', wrap, 1).returns(n1)
                .next_call().with_args('', wrap, 2).returns(n2)
                .next_call().with_args('', wrap, 3).returns(n3)
                )
            
            Node(wrap=wrap, data=data).convert() |should| equal_to(("", [n1, n2, n3]))
        
        it "returns data enclosed in tags made from self.tag if not iterable or mapping":
            tag = "thing"
            results = []
            for d in [0, 1, '', u'', 'asdf', u'qwer', False, True]:
                val, children = Node(tag=tag, data=d).convert()
                len(children) |should| be(0)
                results.append(val)
            
            results |should| equal_to(
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
                len(children) |should| be(0)
                results.append(val)
            
            results |should| equal_to(
                [ "0"
                , "1"
                , ""
                , ""
                , "asdf"
                , "qwer"
                , "False"
                , "True"
                ])
