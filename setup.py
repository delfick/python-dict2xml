from setuptools import setup

# Setup the project
setup(
      name = "dict2xml"
    , version = '1.6'
    , packages = ['dict2xml']

    , extras_require =
      { 'tests' :
        [ 'fudge'
        , 'noseOfYeti>=1.7.0'
        , 'nose'
        ]
      }

    , install_requires =
      [ "six"
      ]

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
    , author = "Stephen Moore"
    , author_email = "stephen@delfick.com"
    , description = "small script to output xml as a string from a python dictionary"
    , license = "MIT"
    )

