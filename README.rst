dict2xml
========

Super Simple utility to convert a python dictionary into an xml string

Installation
------------

Install using pip::

  > python -m pip install dict2xml

example
-------

.. code-block:: python

  from dict2xml import dict2xml

  data = {
    'a': 1,
    'b': [2, 3],
    'c': {
      'd': [
        {'p': 9},
        {'o': 10}
      ],
      'e': 7
    }
  }

  print dict2xml(data, wrap="all", indent="  ")

Output
------

.. code-block:: xml

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
-------

``dict2xml.dict2xml(data, *args, **kwargs)``
    Equivalent to:

    .. code-block:: python

        dict2xml.Converter(*args, **kwargs).build(data)

``dict2xml.Converter(wrap="", indent="  ", newlines=True)``
    Knows how to convert a dictionary into an xml string

    * wrap: Wraps the entire tree in this tag
    * indent: Amount to prefix each line for each level of nesting
    * newlines: Whether or not to use newlines

``dict2xml.Converter.build(data, iterables_repeat_wrap=True, closed_tags_for=None, data_sorter=None)``
    Instance method on Converter that takes in the data and creates the xml string

    * iterables_repeat_wrap - when false the key the array is in will be repeated
    * closed_tags_for - an array of values that will produce self closing tags
    * data_sorter - an object as explained below for sorting keys in maps

``dict2xml.DataSorter``
    An object used to determine the sorting of keys for a map of data.

    By default an ``OrderedDict`` object will not have it's keys sorted, but any
    other type of mapping will.

    It can be made so even ``OrderedDict`` will get sorted by passing in
    ``data_sorter=DataSorter.always()``.

    Or it can be made so that keys are produced from the sorting determined by
    the mapping with ``data_sorter=DataSorter.never()``.

    .. note:: When this library was first created python did not have deterministic
       sorting for normal dictionaries which is why default everything gets sorted but
       ``OrderedDict`` do not.

    To create custom sorting logic requires an object that has a single ``keys_from``
    method on it that accepts a map of data and returns a list of strings, where only
    the keys that appear in the list will go into the output and those keys must exist
    in the original mapping.

Self closing tags
-----------------

To produce self closing tags (like ``<item/>``) then the ``build`` method must
be given a list of values under ``closed_tags_for``. For example, if you want
``None`` to produce a closing tag then:

.. code-block:: python

    example = {
        "item1": None,
        "item2": {"string1": "", "string2": None},
        "item3": "special",
    }

    result = Converter("").build(example, closed_tags_for=[None])
    assert result == dedent("""
        <item1/>
        <item2>
            <string1></string1>
            <string2/>
        </item2>
        <item3>special</item3>
    """).strip())

Here only ``string2`` gets a self closing tag because it has data of ``None``,
which has been designated as special.

If you want to dynamically work out which tags should be self closing then you
may provide an object that implements ``__eq__`` and do your logic there.

Limitations
-----------

* No attributes on elements
* Currently no explicit way to hook into how to cope with your custom data
* Currently no way to insert an xml declaration line

Changelog
---------

1.7.5 - 13 February 2024
    * Introduced the ``data_sorter`` option

1.7.4 - 16 January 2024
    * Make the tests compatible with pytest8

1.7.3 - 25 Feb 2023
    * This version has no changes to the installed code.
    * This release converts to hatch for packaging and adds a wheel to the
      package on pypi.
    * CI will now run against python 3.11 as well

1.7.2 - 18 Oct 2022
    * This version has no changes to the installed code.
    * This release adds the tests to the source distribution put onto pypi.

1.7.1 - 16 Feb 2022
    * Adding an option to have self closing tags when the value for that
      tag equals certain values

1.7.0 - 16 April, 2020
    * Use collections.abc to avoid deprecation warning. Thanks @mangin.
    * This library no longer supports Python2 and is only supported for
      Python3.6+. Note that the library should still work in Python3.5 as I
      have not used f-strings, but the framework I use for the tests is only 3.6+.

1.6.1 - August 27, 2019
    * Include readme and LICENSE in the package

1.6 - April 27, 2018
    * No code changes
    * changed the licence to MIT
    * Added more metadata to pypi
    * Enabled travis ci
    * Updated the tests slightly

1.5
    * No changelog was kept before this point.

Development
-----------

To enter a virtualenv with dict2xml and dev requirements installed run::

    > source run.sh activate

Tests may be run with::

    > ./test.sh 

Or::

    > ./run.sh tox

Linting and formatting is via::

    > ./format
    > ./lint

Python Black will work on the tests as long as ``NOSE_OF_YETI_BLACK_COMPAT=true``
and the correct version of black is available. This is true if your editor
is opened in the same terminal session after sourcing run.sh or if
you make sure that environment variable is set and the editor is using the
virtualenv made by running or sourcing ``run.sh`` (``tools/venv/.python``)
