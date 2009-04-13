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

# I couldn't figure out how to get ElementTree to work with the following XPath 
# "//*[namespace-uri()='http://example.com']"
# so I decided to use minidom and this helper function that performs a test on a given node 
# and all its children
# func must return either True (if pass) or False (if fail)
def walkTree(elem, func):
	if func(elem) == False:  return False
	for child in elem.childNodes:
		if walkTree(child, func) == False: return False
	return True

class NoInkscapeElements(unittest.TestCase):
	def runTest(self):
		self.assertNotEquals(walkTree(scour.scourXmlFile('unittests/sodipodi.svg').documentElement, 
			lambda e: e.namespaceURI != 'http://www.inkscape.org/namespaces/inkscape'), False,
			'Found Inkscape elements' )

class NoSodipodiElements(unittest.TestCase):
	def runTest(self):
		self.assertNotEquals(walkTree(scour.scourXmlFile('unittests/sodipodi.svg').documentElement, 
			lambda e: e.namespaceURI != 'http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd'), False,
			'Found Sodipodi elements' )

class NoAdobeElements(unittest.TestCase):
	def runTest(self):
		self.assertNotEquals(walkTree(scour.scourXmlFile('unittests/adobe.svg').documentElement, 
			lambda e: e.namespaceURI != 'http://ns.adobe.com/AdobeIllustrator/10.0/'), False,
			'Found Adobe Illustrator elements' )
		self.assertNotEquals(walkTree(scour.scourXmlFile('unittests/adobe.svg').documentElement, 
			lambda e: e.namespaceURI != 'http://ns.adobe.com/Graphs/1.0/'), False,
			'Found Adobe Graphs elements' )
		self.assertNotEquals(walkTree(scour.scourXmlFile('unittests/adobe.svg').documentElement, 
			lambda e: e.namespaceURI != 'http://ns.adobe.com/AdobeSVGViewerExtensions/3.0/'), False,
			'Found Adobe SVG Viewer elements' )
		self.assertNotEquals(walkTree(scour.scourXmlFile('unittests/adobe.svg').documentElement, 
			lambda e: e.namespaceURI != 'http://ns.adobe.com/Variables/1.0/'), False,
			'Found Adobe Variables elements' )
		self.assertNotEquals(walkTree(scour.scourXmlFile('unittests/adobe.svg').documentElement, 
			lambda e: e.namespaceURI != 'http://ns.adobe.com/SaveForWeb/1.0/'), False,
			'Found Adobe Save For Web elements' )
		self.assertNotEquals(walkTree(scour.scourXmlFile('unittests/adobe.svg').documentElement, 
			lambda e: e.namespaceURI != 'http://ns.adobe.com/Extensibility/1.0/'), False,
			'Found Adobe Extensibility elements' )
		
if __name__ == '__main__':
    unittest.main()
