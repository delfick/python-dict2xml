from setuptools import setup

# fmt: off

# Setup the project
setup(
      name = "dict2xml"
    , version = '1.7.0'
    , packages = ['dict2xml']

    , extras_require =
      { 'tests' :
        [ "noseOfYeti==2.0.1"
        , "pytest==5.3.1"
        ]
      }

    , classifiers =
      [ "Development Status :: 5 - Production/Stable"
      , "License :: OSI Approved :: MIT License"
      , "Operating System :: OS Independent"
      , "Programming Language :: Python"
      , "Programming Language :: Python :: 2.7"
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
