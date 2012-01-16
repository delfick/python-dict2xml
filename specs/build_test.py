# coding: spec

from dict2xml import Converter
from textwrap import dedent

describe "Build":

    def compare(self, data, result, **kwargs):
        converter = Converter(wrap='all', **kwargs)
        made = converter.build(data)
        result.strip() |should| equal_to(made)
        
    describe "Just Working":
        before_each:
            self.data = {'a' : [1, 2, 3], 'b' : {'c' : 'd', 'e' : {'f':'g'}}, 'd' : 1}
            
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
                </all>""")
            self.compare(self.data, expected, indent="  ", newlines=True)
        
        it "with just newlines":
            expected = dedent("""
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
                </all>""")
            self.compare(self.data, expected, indent=None, newlines=True)
            
        it "with just indentation":
            # Indentation requires newlines to work... so meh
            expected = "<all><a>1</a><a>2</a><a>3</a><b><c>d</c><e><f>g</f></e></b><d>1</d></all>"
            self.compare(self.data, expected, indent='  ', newlines=False)
            
        it "with no whitespace":
            expected = "<all><a>1</a><a>2</a><a>3</a><b><c>d</c><e><f>g</f></e></b><d>1</d></all>"
            self.compare(self.data, expected, indent=None, newlines=False)
        
        it "works on a massive, complex dictionary":
            from examples.python_dict import data
            from examples.xml_result import result
            self.compare(data, result, indent='  ', newlines=True)
