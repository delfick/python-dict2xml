from setuptools import setup

# Setup the project
setup(
      name = "dict2xml"
    , version = '1.5'
    , packages = ['dict2xml']

    , extras_require =
      { 'tests' :
        [ 'fudge'
        , 'noseOfYeti>=1.5.0'
        , 'nose'
        ]
      }

    , install_requires =
      [ "six"
      ]

    # metadata
    , author = "Stephen Moore"
    , author_email = "stephen@delfick.com"
    , description = "small script to output xml as a string from a python dictionary"
    , license = "WTFPL"
    )

