#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  Test Harness for Scour
#
#  Copyright 2010 Jeff Schiller
#
#  This file is part of Scour, http://www.codedread.com/scour/
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

from __future__ import absolute_import

import unittest

from scour.yocto_css import parseCssString


class Blank(unittest.TestCase):

    def runTest(self):
        r = parseCssString('')
        self.assertEqual(len(r), 0, 'Blank string returned non-empty list')
        self.assertEqual(type(r), type([]), 'Blank string returned non list')


class ElementSelector(unittest.TestCase):

    def runTest(self):
        r = parseCssString('foo {}')
        self.assertEqual(len(r), 1, 'Element selector not returned')
        self.assertEqual(r[0]['selector'], 'foo', 'Selector for foo not returned')
        self.assertEqual(len(r[0]['properties']), 0, 'Property list for foo not empty')


class ElementSelectorWithProperty(unittest.TestCase):

    def runTest(self):
        r = parseCssString('foo { bar: baz}')
        self.assertEqual(len(r), 1, 'Element selector not returned')
        self.assertEqual(r[0]['selector'], 'foo', 'Selector for foo not returned')
        self.assertEqual(len(r[0]['properties']), 1, 'Property list for foo did not have 1')
        self.assertEqual(r[0]['properties']['bar'], 'baz', 'Property bar did not have baz value')


if __name__ == '__main__':
    unittest.main()
