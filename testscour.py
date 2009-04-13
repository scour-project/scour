#!/usr/local/bin/python
#  Test Harness for Scour
#
#  Copyright 2009 Jeff Schiller
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

import unittest
import scour
import xml.dom.minidom

# performs a test on a given node
# func must return either True or False
def walkTree(elem, func):
	if func(elem) == False:  return False
	for child in elem.childNodes:
		if walkTree(child, func) == False: return False
	return True

class NoInkscapeElements(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/inkscape.svg')
		self.assertNotEquals( walkTree( doc.documentElement, 
			lambda e: e.namespaceURI != "http://www.inkscape.org/namespaces/inkscape" ), False,
			'Found Inkscape elements' )

if __name__ == '__main__':
    unittest.main()

print "done"