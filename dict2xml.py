import collections

class Node(object):
    def __init__(self, wrap, tag, data=None):
        self.tag = tag
        self.wrap = wrap
        self.data = data
        self.type = self.determine_type()
        
    def serialize(self, indenter):
        wrap = self.wrap
        content = ""
        start, end = "", ""
        value, children = self.convert()
        
        if wrap:
            start, end = "<%s>" % wrap, "</%s>" % wrap
        
        if children:
            if self.type != "iterable":
                content = indenter((c.serialize(indenter) for c in children), wrap)
            else:
                result = []
                for c in children:
                    content = c.serialize(indenter)
                    if c.type == 'unicode':
                        result.append(content)
                    else:
                        content = indenter([content], True)
                        result.append(''.join((start, content, end)))
                        
                return indenter(result, False)
                
        return ''.join((start, value, content, end))
    
    def determine_type(self):
        data = self.data
        if type(data) in (str, unicode):
            return 'unicode'
        elif isinstance(data, collections.Mapping):
            return 'mapping'
        elif isinstance(data, collections.Iterable):
            return 'iterable'
        else:
            return 'unicode'
        
    def convert(self):
        val = ""
        typ = self.type
        data = self.data
        children = []
        
        if typ == 'mapping':
            for key in sorted(data):
                item = data[key]
                children.append(Node(key, "", item))
                
        elif typ == 'iterable':
            for item in data:
                children.append(Node("", self.wrap, item))
                
        else:
            val = unicode(data)
            if self.tag:
                val = "<%s>%s</%s>" % (self.tag, val, self.tag)
        
        return val, children
        
class Converter(object):
    def __init__(self, wrap=None, indent='  ', newlines=True):
        self.wrap = wrap
        self.indenter = self.make_indenter(indent, newlines)
    
    def eachline(self, nodes):
        for node in nodes:
            for line in node.split('\n'):
                yield line
    
    def make_indenter(self, indent, newlines):
        if not newlines:
            ret = lambda nodes, wrapped: "".join(nodes)
        else:
            if not indent:
                indent = ""
                
            def ret(nodes, wrapped):
                if wrapped:
                    seperator = "\n%s" % indent
                    surrounding = "\n%s%%s\n" % indent
                else:
                    seperator = "\n"
                    surrounding = "%s"
                return surrounding % seperator.join(self.eachline(nodes))
        
        return ret
            
    def build(self, data):
        return Node(self.wrap, "", data).serialize(self.indenter)

def dict2xml(data, **kwargs)
    """ Return an XML string of a Python dict object """
    converter = Converter(wrap='all', **kwargs)
    return converter.build(data)
