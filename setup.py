from dict2xml import VERSION
from setuptools import setup

# fmt: off

# Setup the project
setup(
      name = "dict2xml"
    , version = VERSION
    , packages = ['dict2xml']
    
    , python_requires = ">= 3.5"

    , extras_require =
      { 'tests' :
        [ "noseOfYeti==2.1.0"
        , "pytest==6.2.5"
        ]
      }

    , classifiers =
      [ "Development Status :: 5 - Production/Stable"
      , "License :: OSI Approved :: MIT License"
      , "Operating System :: OS Independent"
      , "Programming Language :: Python"
      , "Programming Language :: Python :: 3"
      , "Topic :: Software Development :: Libraries :: Python Modules"
      , "Topic :: Text Processing :: Markup :: XML"
      ]

    # metadata
    , url = "http://github.com/delfick/python-dict2xml"
    , author = "Stephen Moore"
    , author_email = "stephen@delfick.com"
    , description = "Small utility to convert a python dictionary into an XML string"
    , long_description = open("README.rst").read()
    , license = "MIT"
    )

# fmt: on
