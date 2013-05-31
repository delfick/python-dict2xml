dict2xml
========

Super Simple utility to convert a python dictionary into an xml string

Installation
============

Make youself a virtualenv (you're using those right?) and do the following::

  $ pip install .

Or if you want to develop on dict2xml, recommended commands are::

  $ pip install -e .
  $ pip install dict2xml[test]
 
Or if you don't want to install from source::

  $ pip install dict2xml

example
=======

    from dict2xml import dict2xml as xmlify
    data = {
        'a' : 1
      , 'b' : [2, 3]
      , 'c' : {
          'd' : [
              {'p' : 9}
            , {'o' : 10}
            ]
          , 'e': 7
          }
      }
      
    print xmlify(data, wrap="all", indent="  ")

Output
------

    <all>
      <a>1</a>
      <b>2</b>
      <b>3</b>
      <c>
        <d>
          <p>9</p>
        </d>
        <d>
          <o>10</o>
        </d>
        <e>7</e>
      </c>
    </all>

methods
=======

dict2xml.dict2xml(data, *args, **kwargs)
----------------------------------------

Equivalent to
  
    dict2xml.Converter(*args, **kwargs).build(data)

dict2xml.Converter(wrap="", indent="  ", newlines=True)
-------------------------------------------------------

Knows how to convert a dictionary into an xml string

 * wrap: Wraps the entire tree in this tag
 * indent: Amount to prefix each line for each level of nesting
 * newlines: Whether or not to use newlines

dict2xml.Converter.build(data)
------------------------------

Instance method on Converter that takes in the data and creates the xml string

Limitations
===========

 * No attributes on elements
 * Currently no explicit way to hook into how to cope with your custom data
 * Currently no way to insert an xml declaration line

license
=======

WTFPL
