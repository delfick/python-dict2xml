#!/usr/bin/env python
#coding: utf-8

from distutils.core import setup

setup(
      name = "dict2xml"
    , author = "Stephen Moore"
    , author_email = "stephen@delfick.com"
    , version = "1.0"
    , license = "WTFPL"
    , description = "small script to output xml as a string from a python dictionary"
    , py_modules = ["dict2xml"]
    , extras_require = {
          'tests' : [
              'https://bitbucket.org/delfick/nose-of-yeti/src'
            , 'https://delfick@github.com/delfick/pinocchio.git'
            , 'should-dsl'
            ]
        }
    )
