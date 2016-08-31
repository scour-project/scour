#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  Test Harness for Scour
#
#  Copyright 2010 Jeff Schiller
#  Copyright 2010 Louis Simard
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

import six
from six.moves import map, range

import unittest
import xml.dom.minidom

from scour.svg_regex import svg_parser
from scour.scour import scourXmlFile, scourString, parse_args, makeWellFormed


SVGNS = 'http://www.w3.org/2000/svg'

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


class ScourOptions:
	pass


class EmptyOptions(unittest.TestCase):
	def runTest(self):
		options = ScourOptions
		try:
			scour.scourXmlFile('unittests/ids-to-strip.svg', options)
			fail = False
		except:
			fail = True
		self.assertEqual(fail, False, 'Exception when calling Scour with empty options object')

class InvalidOptions(unittest.TestCase):
	def runTest(self):
		options = ScourOptions
		options.invalidOption = "invalid value"
		try:
			scour.scourXmlFile('unittests/ids-to-strip.svg', options)
			fail = False
		except:
			fail = True
		self.assertEqual(fail, False, 'Exception when calling Scour with invalid options')

class GetElementById(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/ids.svg')
		self.assertIsNotNone(doc.getElementById('svg1'), 'Root SVG element not found by ID')
		self.assertIsNotNone(doc.getElementById('linearGradient1'), 'linearGradient not found by ID')
		self.assertIsNotNone(doc.getElementById('layer1'), 'g not found by ID')
		self.assertIsNotNone(doc.getElementById('rect1'), 'rect not found by ID')
		self.assertIsNone(doc.getElementById('rect2'), 'Non-existing element found by ID')

class NoInkscapeElements(unittest.TestCase):
	def runTest(self):
		self.assertNotEqual(walkTree(scour.scourXmlFile('unittests/sodipodi.svg').documentElement,
			lambda e: e.namespaceURI != 'http://www.inkscape.org/namespaces/inkscape'), False,
			'Found Inkscape elements' )
class NoSodipodiElements(unittest.TestCase):
	def runTest(self):
		self.assertNotEqual(walkTree(scour.scourXmlFile('unittests/sodipodi.svg').documentElement,
			lambda e: e.namespaceURI != 'http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd'), False,
			'Found Sodipodi elements' )
class NoAdobeIllustratorElements(unittest.TestCase):
	def runTest(self):
		self.assertNotEqual(walkTree(scour.scourXmlFile('unittests/adobe.svg').documentElement,
			lambda e: e.namespaceURI != 'http://ns.adobe.com/AdobeIllustrator/10.0/'), False,
			'Found Adobe Illustrator elements' )
class NoAdobeGraphsElements(unittest.TestCase):
	def runTest(self):
		self.assertNotEqual(walkTree(scour.scourXmlFile('unittests/adobe.svg').documentElement,
			lambda e: e.namespaceURI != 'http://ns.adobe.com/Graphs/1.0/'), False,
			'Found Adobe Graphs elements' )
class NoAdobeSVGViewerElements(unittest.TestCase):
	def runTest(self):
		self.assertNotEqual(walkTree(scour.scourXmlFile('unittests/adobe.svg').documentElement,
			lambda e: e.namespaceURI != 'http://ns.adobe.com/AdobeSVGViewerExtensions/3.0/'), False,
			'Found Adobe SVG Viewer elements' )
class NoAdobeVariablesElements(unittest.TestCase):
	def runTest(self):
		self.assertNotEqual(walkTree(scour.scourXmlFile('unittests/adobe.svg').documentElement,
			lambda e: e.namespaceURI != 'http://ns.adobe.com/Variables/1.0/'), False,
			'Found Adobe Variables elements' )
class NoAdobeSaveForWebElements(unittest.TestCase):
	def runTest(self):
		self.assertNotEqual(walkTree(scour.scourXmlFile('unittests/adobe.svg').documentElement,
			lambda e: e.namespaceURI != 'http://ns.adobe.com/SaveForWeb/1.0/'), False,
			'Found Adobe Save For Web elements' )
class NoAdobeExtensibilityElements(unittest.TestCase):
	def runTest(self):
		self.assertNotEqual(walkTree(scour.scourXmlFile('unittests/adobe.svg').documentElement,
			lambda e: e.namespaceURI != 'http://ns.adobe.com/Extensibility/1.0/'), False,
			'Found Adobe Extensibility elements' )
class NoAdobeFlowsElements(unittest.TestCase):
	def runTest(self):
		self.assertNotEqual(walkTree(scour.scourXmlFile('unittests/adobe.svg').documentElement,
			lambda e: e.namespaceURI != 'http://ns.adobe.com/Flows/1.0/'), False,
			'Found Adobe Flows elements' )
class NoAdobeImageReplacementElements(unittest.TestCase):
	def runTest(self):
		self.assertNotEqual(walkTree(scour.scourXmlFile('unittests/adobe.svg').documentElement,
			lambda e: e.namespaceURI != 'http://ns.adobe.com/ImageReplacement/1.0/'), False,
			'Found Adobe Image Replacement elements' )
class NoAdobeCustomElements(unittest.TestCase):
	def runTest(self):
		self.assertNotEqual(walkTree(scour.scourXmlFile('unittests/adobe.svg').documentElement,
			lambda e: e.namespaceURI != 'http://ns.adobe.com/GenericCustomNamespace/1.0/'), False,
			'Found Adobe Custom elements' )
class NoAdobeXPathElements(unittest.TestCase):
	def runTest(self):
		self.assertNotEqual(walkTree(scour.scourXmlFile('unittests/adobe.svg').documentElement,
			lambda e: e.namespaceURI != 'http://ns.adobe.com/XPath/1.0/'), False,
			'Found Adobe XPath elements' )

class DoNotRemoveTitleWithOnlyText(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/descriptive-elements-with-text.svg')
		self.assertEqual(len(doc.getElementsByTagNameNS(SVGNS, 'title')), 1,
			'Removed title element with only text child' )

class RemoveEmptyTitleElement(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/empty-descriptive-elements.svg')
		self.assertEqual(len(doc.getElementsByTagNameNS(SVGNS, 'title')), 0,
			'Did not remove empty title element' )

class DoNotRemoveDescriptionWithOnlyText(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/descriptive-elements-with-text.svg')
		self.assertEqual(len(doc.getElementsByTagNameNS(SVGNS, 'desc')), 1,
			'Removed description element with only text child' )

class RemoveEmptyDescriptionElement(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/empty-descriptive-elements.svg')
		self.assertEqual(len(doc.getElementsByTagNameNS(SVGNS, 'desc')), 0,
			'Did not remove empty description element' )

class DoNotRemoveMetadataWithOnlyText(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/descriptive-elements-with-text.svg')
		self.assertEqual(len(doc.getElementsByTagNameNS(SVGNS, 'metadata')), 1,
			'Removed metadata element with only text child' )

class RemoveEmptyMetadataElement(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/empty-descriptive-elements.svg')
		self.assertEqual(len(doc.getElementsByTagNameNS(SVGNS, 'metadata')), 0,
			'Did not remove empty metadata element' )

class DoNotRemoveDescriptiveElementsWithOnlyText(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/descriptive-elements-with-text.svg')
		self.assertEqual(len(doc.getElementsByTagNameNS(SVGNS, 'title')), 1,
			'Removed title element with only text child' )
		self.assertEqual(len(doc.getElementsByTagNameNS(SVGNS, 'desc')), 1,
			'Removed description element with only text child')
		self.assertEqual(len(doc.getElementsByTagNameNS(SVGNS, 'metadata')), 1,
			'Removed metadata element with only text child' )

class RemoveEmptyDescriptiveElements(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/empty-descriptive-elements.svg')
		self.assertEqual(len(doc.getElementsByTagNameNS(SVGNS, 'title')), 0,
			'Did not remove empty title element' )
		self.assertEqual(len(doc.getElementsByTagNameNS(SVGNS, 'desc')), 0,
			'Did not remove empty description element' )
		self.assertEqual(len(doc.getElementsByTagNameNS(SVGNS, 'metadata')), 0,
			'Did not remove empty metadata element' )

class RemoveEmptyGElements(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/empty-g.svg')
		self.assertEqual(len(doc.getElementsByTagNameNS(SVGNS, 'g')), 1,
			'Did not remove empty g element' )

class RemoveUnreferencedPattern(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/unreferenced-pattern.svg')
		self.assertEqual(len(doc.getElementsByTagNameNS(SVGNS, 'pattern')), 0,
			'Unreferenced pattern not removed' )

class RemoveUnreferencedLinearGradient(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/unreferenced-linearGradient.svg')
		self.assertEqual(len(doc.getElementsByTagNameNS(SVGNS, 'linearGradient')), 0,
			'Unreferenced linearGradient not removed' )

class RemoveUnreferencedRadialGradient(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/unreferenced-radialGradient.svg')
		self.assertEqual(len(doc.getElementsByTagNameNS(SVGNS, 'radialradient')), 0,
			'Unreferenced radialGradient not removed' )

class RemoveUnreferencedElementInDefs(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/referenced-elements-1.svg')
		self.assertEqual(len(doc.getElementsByTagNameNS(SVGNS, 'rect')), 1,
			'Unreferenced rect left in defs' )

class RemoveUnreferencedDefs(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/unreferenced-defs.svg')
		self.assertEqual(len(doc.getElementsByTagNameNS(SVGNS, 'linearGradient')), 1,
			'Referenced linearGradient removed from defs' )
		self.assertEqual(len(doc.getElementsByTagNameNS(SVGNS, 'radialGradient')), 0,
			'Unreferenced radialGradient left in defs' )
		self.assertEqual(len(doc.getElementsByTagNameNS(SVGNS, 'pattern')), 0,
			'Unreferenced pattern left in defs' )
		self.assertEqual(len(doc.getElementsByTagNameNS(SVGNS, 'rect')), 1,
			'Referenced rect removed from defs' )
		self.assertEqual(len(doc.getElementsByTagNameNS(SVGNS, 'circle')), 0,
			'Unreferenced circle left in defs' )

class KeepUnreferencedDefs(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/unreferenced-defs.svg',
			scour.parse_args(['--keep-unreferenced-defs']))
		self.assertEqual(len(doc.getElementsByTagNameNS(SVGNS, 'linearGradient')), 1,
			'Referenced linearGradient removed from defs with `--keep-unreferenced-defs`' )
		self.assertEqual(len(doc.getElementsByTagNameNS(SVGNS, 'radialGradient')), 1,
			'Unreferenced radialGradient removed from defs with `--keep-unreferenced-defs`' )
		self.assertEqual(len(doc.getElementsByTagNameNS(SVGNS, 'pattern')), 1,
			'Unreferenced pattern removed from defs with `--keep-unreferenced-defs`' )
		self.assertEqual(len(doc.getElementsByTagNameNS(SVGNS, 'rect')), 1,
			'Referenced rect removed from defs with `--keep-unreferenced-defs`' )
		self.assertEqual(len(doc.getElementsByTagNameNS(SVGNS, 'circle')), 1,
			'Unreferenced circle removed from defs with `--keep-unreferenced-defs`' )

class DoNotRemoveChainedRefsInDefs(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/refs-in-defs.svg')
		g = doc.getElementsByTagNameNS(SVGNS, 'g')[0]
		self.assertEqual( g.childNodes.length >= 2, True,
			'Chained references not honored in defs' )

class KeepTitleInDefs(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/referenced-elements-1.svg')
		self.assertEqual(len(doc.getElementsByTagNameNS(SVGNS, 'title')), 1,
			'Title removed from in defs' )

class RemoveNestedDefs(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/nested-defs.svg')
		allDefs = doc.getElementsByTagNameNS(SVGNS, 'defs')
		self.assertEqual(len(allDefs), 1, 'More than one defs left in doc')

class KeepUnreferencedIDsWhenEnabled(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/ids-to-strip.svg')
		self.assertEqual(doc.getElementsByTagNameNS(SVGNS, 'svg')[0].getAttribute('id'), 'boo',
			'<svg> ID stripped when it should be disabled' )

class RemoveUnreferencedIDsWhenEnabled(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/ids-to-strip.svg',
			scour.parse_args(['--enable-id-stripping']))
		self.assertEqual(doc.getElementsByTagNameNS(SVGNS, 'svg')[0].getAttribute('id'), '',
			'<svg> ID not stripped' )

class RemoveUselessNestedGroups(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/nested-useless-groups.svg')
		self.assertEqual(len(doc.getElementsByTagNameNS(SVGNS, 'g')), 1,
			'Useless nested groups not removed' )

class DoNotRemoveUselessNestedGroups(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/nested-useless-groups.svg',
			scour.parse_args(['--disable-group-collapsing']))
		self.assertEqual(len(doc.getElementsByTagNameNS(SVGNS, 'g')), 2,
			'Useless nested groups were removed despite --disable-group-collapsing' )

class DoNotRemoveNestedGroupsWithTitle(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/groups-with-title-desc.svg')
		self.assertEqual(len(doc.getElementsByTagNameNS(SVGNS, 'g')), 2,
			'Nested groups with title was removed' )

class DoNotRemoveNestedGroupsWithDesc(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/groups-with-title-desc.svg')
		self.assertEqual(len(doc.getElementsByTagNameNS(SVGNS, 'g')), 2,
			'Nested groups with desc was removed' )

class RemoveDuplicateLinearGradientStops(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/duplicate-gradient-stops.svg')
		grad = doc.getElementsByTagNameNS(SVGNS, 'linearGradient')
		self.assertEqual(len(grad[0].getElementsByTagNameNS(SVGNS, 'stop')), 3,
			'Duplicate linear gradient stops not removed' )

class RemoveDuplicateLinearGradientStopsPct(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/duplicate-gradient-stops-pct.svg')
		grad = doc.getElementsByTagNameNS(SVGNS, 'linearGradient')
		self.assertEqual(len(grad[0].getElementsByTagNameNS(SVGNS, 'stop')), 3,
			'Duplicate linear gradient stops with percentages not removed' )

class RemoveDuplicateRadialGradientStops(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/duplicate-gradient-stops.svg')
		grad = doc.getElementsByTagNameNS(SVGNS, 'radialGradient')
		self.assertEqual(len(grad[0].getElementsByTagNameNS(SVGNS, 'stop')), 3,
			'Duplicate radial gradient stops not removed' )

class NoSodipodiNamespaceDecl(unittest.TestCase):
	def runTest(self):
		attrs = scour.scourXmlFile('unittests/sodipodi.svg').documentElement.attributes
		for i in range(len(attrs)):
			self.assertNotEqual(attrs.item(i).nodeValue,
				'http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd',
				'Sodipodi namespace declaration found' )

class NoInkscapeNamespaceDecl(unittest.TestCase):
	def runTest(self):
		attrs = scour.scourXmlFile('unittests/inkscape.svg').documentElement.attributes
		for i in range(len(attrs)):
			self.assertNotEqual(attrs.item(i).nodeValue,
				'http://www.inkscape.org/namespaces/inkscape',
				'Inkscape namespace declaration found' )

class NoSodipodiAttributes(unittest.TestCase):
	def runTest(self):
		def findSodipodiAttr(elem):
			attrs = elem.attributes
			if attrs == None: return True
			for i in range(len(attrs)):
				if attrs.item(i).namespaceURI == 'http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd':
					return False
			return True
		self.assertNotEqual(walkTree(scour.scourXmlFile('unittests/sodipodi.svg').documentElement,
			findSodipodiAttr), False,
			'Found Sodipodi attributes' )

class NoInkscapeAttributes(unittest.TestCase):
	def runTest(self):
		def findInkscapeAttr(elem):
			attrs = elem.attributes
			if attrs == None: return True
			for i in range(len(attrs)):
				if attrs.item(i).namespaceURI == 'http://www.inkscape.org/namespaces/inkscape':
					return False
			return True
		self.assertNotEqual(walkTree(scour.scourXmlFile('unittests/inkscape.svg').documentElement,
			findInkscapeAttr), False,
			'Found Inkscape attributes' )

class KeepInkscapeNamespaceDeclarationsWhenKeepEditorData(unittest.TestCase):
	def runTest(self):
		options = ScourOptions
		options.keep_editor_data = True
		attrs = scour.scourXmlFile('unittests/inkscape.svg', options).documentElement.attributes
		FoundNamespace = False
		for i in range(len(attrs)):
			if attrs.item(i).nodeValue == 'http://www.inkscape.org/namespaces/inkscape':
				FoundNamespace = True
				break
		self.assertEqual(True, FoundNamespace,
			"Did not find Inkscape namespace declaration when using --keep-editor-data")
		return False

class KeepSodipodiNamespaceDeclarationsWhenKeepEditorData(unittest.TestCase):
	def runTest(self):
		options = ScourOptions
		options.keep_editor_data = True
		attrs = scour.scourXmlFile('unittests/sodipodi.svg', options).documentElement.attributes
		FoundNamespace = False
		for i in range(len(attrs)):
			if attrs.item(i).nodeValue == 'http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd':
				FoundNamespace = True
				break
		self.assertEqual(True, FoundNamespace,
			"Did not find Sodipodi namespace declaration when using --keep-editor-data")
		return False

class KeepReferencedFonts(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/referenced-font.svg')
		fonts = doc.documentElement.getElementsByTagNameNS(SVGNS,'font')
		self.assertEqual(len(fonts), 1,
			'Font wrongly removed from <defs>' )

class ConvertStyleToAttrs(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/stroke-transparent.svg')
		self.assertEqual(doc.getElementsByTagNameNS(SVGNS, 'path')[0].getAttribute('style'), '',
			'style attribute not emptied' )

class RemoveStrokeWhenStrokeTransparent(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/stroke-transparent.svg')
		self.assertEqual(doc.getElementsByTagNameNS(SVGNS, 'path')[0].getAttribute('stroke'), '',
			'stroke attribute not emptied when stroke opacity zero' )

class RemoveStrokeWidthWhenStrokeTransparent(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/stroke-transparent.svg')
		self.assertEqual(doc.getElementsByTagNameNS(SVGNS, 'path')[0].getAttribute('stroke-width'), '',
			'stroke-width attribute not emptied when stroke opacity zero' )

class RemoveStrokeLinecapWhenStrokeTransparent(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/stroke-transparent.svg')
		self.assertEqual(doc.getElementsByTagNameNS(SVGNS, 'path')[0].getAttribute('stroke-linecap'), '',
			'stroke-linecap attribute not emptied when stroke opacity zero' )

class RemoveStrokeLinejoinWhenStrokeTransparent(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/stroke-transparent.svg')
		self.assertEqual(doc.getElementsByTagNameNS(SVGNS, 'path')[0].getAttribute('stroke-linejoin'), '',
			'stroke-linejoin attribute not emptied when stroke opacity zero' )

class RemoveStrokeDasharrayWhenStrokeTransparent(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/stroke-transparent.svg')
		self.assertEqual(doc.getElementsByTagNameNS(SVGNS, 'path')[0].getAttribute('stroke-dasharray'), '',
			'stroke-dasharray attribute not emptied when stroke opacity zero' )

class RemoveStrokeDashoffsetWhenStrokeTransparent(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/stroke-transparent.svg')
		self.assertEqual(doc.getElementsByTagNameNS(SVGNS, 'path')[0].getAttribute('stroke-dashoffset'), '',
			'stroke-dashoffset attribute not emptied when stroke opacity zero' )

class RemoveStrokeWhenStrokeWidthZero(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/stroke-nowidth.svg')
		self.assertEqual(doc.getElementsByTagNameNS(SVGNS, 'path')[0].getAttribute('stroke'), '',
			'stroke attribute not emptied when width zero' )

class RemoveStrokeOpacityWhenStrokeWidthZero(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/stroke-nowidth.svg')
		self.assertEqual(doc.getElementsByTagNameNS(SVGNS, 'path')[0].getAttribute('stroke-opacity'), '',
			'stroke-opacity attribute not emptied when width zero' )

class RemoveStrokeLinecapWhenStrokeWidthZero(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/stroke-nowidth.svg')
		self.assertEqual(doc.getElementsByTagNameNS(SVGNS, 'path')[0].getAttribute('stroke-linecap'), '',
			'stroke-linecap attribute not emptied when width zero' )

class RemoveStrokeLinejoinWhenStrokeWidthZero(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/stroke-nowidth.svg')
		self.assertEqual(doc.getElementsByTagNameNS(SVGNS, 'path')[0].getAttribute('stroke-linejoin'), '',
			'stroke-linejoin attribute not emptied when width zero' )

class RemoveStrokeDasharrayWhenStrokeWidthZero(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/stroke-nowidth.svg')
		self.assertEqual(doc.getElementsByTagNameNS(SVGNS, 'path')[0].getAttribute('stroke-dasharray'), '',
			'stroke-dasharray attribute not emptied when width zero' )

class RemoveStrokeDashoffsetWhenStrokeWidthZero(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/stroke-nowidth.svg')
		self.assertEqual(doc.getElementsByTagNameNS(SVGNS, 'path')[0].getAttribute('stroke-dashoffset'), '',
			'stroke-dashoffset attribute not emptied when width zero' )

class RemoveStrokeWhenStrokeNone(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/stroke-none.svg')
		self.assertEqual(doc.getElementsByTagNameNS(SVGNS, 'path')[0].getAttribute('stroke'), '',
			'stroke attribute not emptied when no stroke' )

class RemoveStrokeWidthWhenStrokeNone(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/stroke-none.svg')
		self.assertEqual(doc.getElementsByTagNameNS(SVGNS, 'path')[0].getAttribute('stroke-width'), '',
			'stroke-width attribute not emptied when no stroke' )

class RemoveStrokeOpacityWhenStrokeNone(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/stroke-none.svg')
		self.assertEqual(doc.getElementsByTagNameNS(SVGNS, 'path')[0].getAttribute('stroke-opacity'), '',
			'stroke-opacity attribute not emptied when no stroke' )

class RemoveStrokeLinecapWhenStrokeNone(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/stroke-none.svg')
		self.assertEqual(doc.getElementsByTagNameNS(SVGNS, 'path')[0].getAttribute('stroke-linecap'), '',
			'stroke-linecap attribute not emptied when no stroke' )

class RemoveStrokeLinejoinWhenStrokeNone(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/stroke-none.svg')
		self.assertEqual(doc.getElementsByTagNameNS(SVGNS, 'path')[0].getAttribute('stroke-linejoin'), '',
			'stroke-linejoin attribute not emptied when no stroke' )

class RemoveStrokeDasharrayWhenStrokeNone(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/stroke-none.svg')
		self.assertEqual(doc.getElementsByTagNameNS(SVGNS, 'path')[0].getAttribute('stroke-dasharray'), '',
			'stroke-dasharray attribute not emptied when no stroke' )

class RemoveStrokeDashoffsetWhenStrokeNone(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/stroke-none.svg')
		self.assertEqual(doc.getElementsByTagNameNS(SVGNS, 'path')[0].getAttribute('stroke-dashoffset'), '',
			'stroke-dashoffset attribute not emptied when no stroke' )

class RemoveFillRuleWhenFillNone(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/fill-none.svg')
		self.assertEqual(doc.getElementsByTagNameNS(SVGNS, 'path')[0].getAttribute('fill-rule'), '',
			'fill-rule attribute not emptied when no fill' )

class RemoveFillOpacityWhenFillNone(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/fill-none.svg')
		self.assertEqual(doc.getElementsByTagNameNS(SVGNS, 'path')[0].getAttribute('fill-opacity'), '',
			'fill-opacity attribute not emptied when no fill' )

class ConvertFillPropertyToAttr(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/fill-none.svg',
			scour.parse_args(['--disable-simplify-colors']))
		self.assertEqual(doc.getElementsByTagNameNS(SVGNS, 'path')[1].getAttribute('fill'), 'black',
			'fill property not converted to XML attribute' )

class ConvertFillOpacityPropertyToAttr(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/fill-none.svg')
		self.assertEqual(doc.getElementsByTagNameNS(SVGNS, 'path')[1].getAttribute('fill-opacity'), '.5',
			'fill-opacity property not converted to XML attribute' )

class ConvertFillRuleOpacityPropertyToAttr(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/fill-none.svg')
		self.assertEqual(doc.getElementsByTagNameNS(SVGNS, 'path')[1].getAttribute('fill-rule'), 'evenodd',
			'fill-rule property not converted to XML attribute' )

class CollapseSinglyReferencedGradients(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/collapse-gradients.svg')
		self.assertEqual(len(doc.getElementsByTagNameNS(SVGNS, 'linearGradient')), 0,
			'Singly-referenced linear gradient not collapsed' )

class InheritGradientUnitsUponCollapsing(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/collapse-gradients.svg')
		self.assertEqual(doc.getElementsByTagNameNS(SVGNS, 'radialGradient')[0].getAttribute('gradientUnits'),
			'userSpaceOnUse',
			'gradientUnits not properly inherited when collapsing gradients' )

class OverrideGradientUnitsUponCollapsing(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/collapse-gradients-gradientUnits.svg')
		self.assertEqual(doc.getElementsByTagNameNS(SVGNS, 'radialGradient')[0].getAttribute('gradientUnits'), '',
			'gradientUnits not properly overrode when collapsing gradients' )

class DoNotCollapseMultiplyReferencedGradients(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/dont-collapse-gradients.svg')
		self.assertNotEqual(len(doc.getElementsByTagNameNS(SVGNS, 'linearGradient')), 0,
			'Multiply-referenced linear gradient collapsed' )

class RemoveTrailingZerosFromPath(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/path-truncate-zeros.svg')
		path = doc.getElementsByTagNameNS(SVGNS, 'path')[0].getAttribute('d')
		self.assertEqual(path[:4] == 'm300' and path[4] != '.', True,
			'Trailing zeros not removed from path data' )

class RemoveTrailingZerosFromPathAfterCalculation(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/path-truncate-zeros-calc.svg')
		path = doc.getElementsByTagNameNS(SVGNS, 'path')[0].getAttribute('d')
		self.assertEqual(path, 'm5.81 0h0.1',
			'Trailing zeros not removed from path data after calculation' )

class RemoveDelimiterBeforeNegativeCoordsInPath(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/path-truncate-zeros.svg')
		path = doc.getElementsByTagNameNS(SVGNS, 'path')[0].getAttribute('d')
		self.assertEqual(path[4], '-',
			'Delimiters not removed before negative coordinates in path data' )

class UseScientificNotationToShortenCoordsInPath(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/path-use-scientific-notation.svg')
		path = doc.getElementsByTagNameNS(SVGNS, 'path')[0].getAttribute('d')
		self.assertEqual(path, 'm1e4 0',
			'Not using scientific notation for path coord when representation is shorter')

class ConvertAbsoluteToRelativePathCommands(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/path-abs-to-rel.svg')
		path = svg_parser.parse(doc.getElementsByTagNameNS(SVGNS, 'path')[0].getAttribute('d'))
		self.assertEqual(path[1][0], 'v',
			'Absolute V command not converted to relative v command')
		self.assertEqual(float(path[1][1][0]), -20.0,
			'Absolute V value not converted to relative v value')

class RoundPathData(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/path-precision.svg')
		path = svg_parser.parse(doc.getElementsByTagNameNS(SVGNS, 'path')[0].getAttribute('d'))
		self.assertEqual(float(path[0][1][0]), 100.0,
			'Not rounding down' )
		self.assertEqual(float(path[0][1][1]), 100.0,
			'Not rounding up' )

class LimitPrecisionInPathData(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/path-precision.svg')
		path = svg_parser.parse(doc.getElementsByTagNameNS(SVGNS, 'path')[0].getAttribute('d'))
		self.assertEqual(float(path[1][1][0]), 100.01,
			'Not correctly limiting precision on path data' )

class RemoveEmptyLineSegmentsFromPath(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/path-line-optimize.svg')
		path = svg_parser.parse(doc.getElementsByTagNameNS(SVGNS, 'path')[0].getAttribute('d'))
		self.assertEqual(path[4][0], 'z',
			'Did not remove an empty line segment from path' )

# Do not remove empty segments if round linecaps.
class DoNotRemoveEmptySegmentsFromPathWithRoundLineCaps(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/path-with-caps.svg')
		path = svg_parser.parse(doc.getElementsByTagNameNS(SVGNS, 'path')[0].getAttribute('d'))
		self.assertEqual(len(path), 2,
			'Did not preserve empty segments when path had round linecaps' )

class ChangeLineToHorizontalLineSegmentInPath(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/path-line-optimize.svg')
		path = svg_parser.parse(doc.getElementsByTagNameNS(SVGNS, 'path')[0].getAttribute('d'))
		self.assertEqual(path[1][0], 'h',
			'Did not change line to horizontal line segment in path' )
		self.assertEqual(float(path[1][1][0]), 200.0,
			'Did not calculate horizontal line segment in path correctly' )

class ChangeLineToVerticalLineSegmentInPath(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/path-line-optimize.svg')
		path = svg_parser.parse(doc.getElementsByTagNameNS(SVGNS, 'path')[0].getAttribute('d'))
		self.assertEqual(path[2][0], 'v',
			'Did not change line to vertical line segment in path' )
		self.assertEqual(float(path[2][1][0]), 100.0,
			'Did not calculate vertical line segment in path correctly' )

class ChangeBezierToShorthandInPath(unittest.TestCase):
	def runTest(self):
		path = scour.scourXmlFile('unittests/path-bez-optimize.svg').getElementsByTagNameNS(SVGNS, 'path')[0]
		self.assertEqual(path.getAttribute('d'), 'm10 100c50-50 50 50 100 0s50 50 100 0',
			'Did not change bezier curves into shorthand curve segments in path')

class ChangeQuadToShorthandInPath(unittest.TestCase):
	def runTest(self):
		path = scour.scourXmlFile('unittests/path-quad-optimize.svg').getElementsByTagNameNS(SVGNS, 'path')[0]
		self.assertEqual(path.getAttribute('d'), 'm10 100q50-50 100 0t100 0',
			'Did not change quadratic curves into shorthand curve segments in path')

class HandleEncodingUTF8(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/encoding-utf8.svg')
		text = u'Hello in many languages:\nar: أهلا\nbn: হ্যালো\nel: Χαίρετε\nen: Hello\nhi: नमस्ते\niw: שלום\nja: こんにちは\nkm: ជំរាបសួរ\nml: ഹലോ\nru: Здравствуйте\nur: ہیلو\nzh: 您好'
		desc = six.text_type(doc.getElementsByTagNameNS(SVGNS, 'desc')[0].firstChild.wholeText).strip()
		self.assertEqual( desc, text, 'Did not handle international UTF8 characters' )
		desc = six.text_type(doc.getElementsByTagNameNS(SVGNS, 'desc')[1].firstChild.wholeText).strip()
		self.assertEqual( desc, u'“”‘’–—…‐‒°©®™•½¼¾⅓⅔†‡µ¢£€«»♠♣♥♦¿�', 'Did not handle common UTF8 characters' )
		desc = six.text_type(doc.getElementsByTagNameNS(SVGNS, 'desc')[2].firstChild.wholeText).strip()
		self.assertEqual( desc, u':-×÷±∞π∅≤≥≠≈∧∨∩∪∈∀∃∄∑∏←↑→↓↔↕↖↗↘↙↺↻⇒⇔', 'Did not handle mathematical UTF8 characters' )
		desc = six.text_type(doc.getElementsByTagNameNS(SVGNS, 'desc')[3].firstChild.wholeText).strip()
		self.assertEqual( desc, u'⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁽⁾ⁿⁱ₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎', 'Did not handle superscript/subscript UTF8 characters' )

class HandleEncodingISO_8859_15(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/encoding-iso-8859-15.svg')
		desc = six.text_type(doc.getElementsByTagNameNS(SVGNS, 'desc')[0].firstChild.wholeText).strip()
		self.assertEqual( desc, u'áèîäöüß€ŠšŽžŒœŸ', 'Did not handle ISO 8859-15 encoded characters' )

class HandleSciNoInPathData(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/path-sn.svg')
		self.assertEqual( len(doc.getElementsByTagNameNS(SVGNS, 'path')), 1,
			'Did not handle scientific notation in path data' )

class TranslateRGBIntoHex(unittest.TestCase):
	def runTest(self):
		elem = scour.scourXmlFile('unittests/color-formats.svg').getElementsByTagNameNS(SVGNS, 'rect')[0]
		self.assertEqual( elem.getAttribute('fill'), '#0f1011',
			'Not converting rgb into hex')

class TranslateRGBPctIntoHex(unittest.TestCase):
	def runTest(self):
		elem = scour.scourXmlFile('unittests/color-formats.svg').getElementsByTagNameNS(SVGNS, 'stop')[0]
		self.assertEqual( elem.getAttribute('stop-color'), '#7f0000',
			'Not converting rgb pct into hex')

class TranslateColorNamesIntoHex(unittest.TestCase):
	def runTest(self):
		elem = scour.scourXmlFile('unittests/color-formats.svg').getElementsByTagNameNS(SVGNS, 'rect')[0]
		self.assertEqual( elem.getAttribute('stroke'), '#a9a9a9',
			'Not converting standard color names into hex')

class TranslateExtendedColorNamesIntoHex(unittest.TestCase):
	def runTest(self):
		elem = scour.scourXmlFile('unittests/color-formats.svg').getElementsByTagNameNS(SVGNS, 'solidColor')[0]
		self.assertEqual( elem.getAttribute('solid-color'), '#fafad2',
			'Not converting extended color names into hex')

class TranslateLongHexColorIntoShortHex(unittest.TestCase):
	def runTest(self):
		elem = scour.scourXmlFile('unittests/color-formats.svg').getElementsByTagNameNS(SVGNS, 'ellipse')[0]
		self.assertEqual( elem.getAttribute('fill'), '#fff',
			'Not converting long hex color into short hex')

class DoNotConvertShortColorNames(unittest.TestCase):
	def runTest(self):
		elem = scour.scourXmlFile('unittests/dont-convert-short-color-names.svg').getElementsByTagNameNS(SVGNS, 'rect')[0]
		self.assertEqual( 'red', elem.getAttribute('fill'),
			'Converted short color name to longer hex string')

class AllowQuotEntitiesInUrl(unittest.TestCase):
	def runTest(self):
		grads = scour.scourXmlFile('unittests/quot-in-url.svg').getElementsByTagNameNS(SVGNS, 'linearGradient')
		self.assertEqual( len(grads), 1,
			'Removed referenced gradient when &quot; was in the url')

class RemoveFontStylesFromNonTextShapes(unittest.TestCase):
	def runTest(self):
		r = scour.scourXmlFile('unittests/font-styles.svg').getElementsByTagNameNS(SVGNS, 'rect')[0]
		self.assertEqual( r.getAttribute('font-size'), '',
			'font-size not removed from rect' )

class CollapseConsecutiveHLinesSegments(unittest.TestCase):
	def runTest(self):
		p = scour.scourXmlFile('unittests/consecutive-hlines.svg').getElementsByTagNameNS(SVGNS, 'path')[0]
		self.assertEqual( p.getAttribute('d'), 'm100 100h200v100h-200z',
			'Did not collapse consecutive hlines segments')

class CollapseConsecutiveHLinesCoords(unittest.TestCase):
	def runTest(self):
		p = scour.scourXmlFile('unittests/consecutive-hlines.svg').getElementsByTagNameNS(SVGNS, 'path')[1]
		self.assertEqual( p.getAttribute('d'), 'm100 300h200v100h-200z',
			'Did not collapse consecutive hlines coordinates')

class DoNotCollapseConsecutiveHLinesSegsWithDifferingSigns(unittest.TestCase):
	def runTest(self):
		p = scour.scourXmlFile('unittests/consecutive-hlines.svg').getElementsByTagNameNS(SVGNS, 'path')[2]
		self.assertEqual( p.getAttribute('d'), 'm100 500h300-100v100h-200z',
			'Collapsed consecutive hlines segments with differing signs')

class ConvertStraightCurvesToLines(unittest.TestCase):
	def runTest(self):
		p = scour.scourXmlFile('unittests/straight-curve.svg').getElementsByTagNameNS(SVGNS, 'path')[0]
		self.assertEqual(p.getAttribute('d'), 'm10 10l40 40 40-40z',
			'Did not convert straight curves into lines')

class RemoveUnnecessaryPolygonEndPoint(unittest.TestCase):
	def runTest(self):
		p = scour.scourXmlFile('unittests/polygon.svg').getElementsByTagNameNS(SVGNS, 'polygon')[0]
		self.assertEqual(p.getAttribute('points'), '50 50 150 50 150 150 50 150',
			'Unnecessary polygon end point not removed' )

class DoNotRemovePolgonLastPoint(unittest.TestCase):
	def runTest(self):
		p = scour.scourXmlFile('unittests/polygon.svg').getElementsByTagNameNS(SVGNS, 'polygon')[1]
		self.assertEqual(p.getAttribute('points'), '200 50 300 50 300 150 200 150',
			'Last point of polygon removed' )

class ScourPolygonCoordsSciNo(unittest.TestCase):
	def runTest(self):
		p = scour.scourXmlFile('unittests/polygon-coord.svg').getElementsByTagNameNS(SVGNS, 'polygon')[0]
		self.assertEqual(p.getAttribute('points'), '1e4 50',
			'Polygon coordinates not scoured')

class ScourPolylineCoordsSciNo(unittest.TestCase):
	def runTest(self):
		p = scour.scourXmlFile('unittests/polyline-coord.svg').getElementsByTagNameNS(SVGNS, 'polyline')[0]
		self.assertEqual(p.getAttribute('points'), '1e4 50',
			'Polyline coordinates not scoured')

class ScourPolygonNegativeCoords(unittest.TestCase):
	def runTest(self):
		p = scour.scourXmlFile('unittests/polygon-coord-neg.svg').getElementsByTagNameNS(SVGNS, 'polygon')[0]
		#  points="100,-100,100-100,100-100-100,-100-100,200" />
		self.assertEqual(p.getAttribute('points'), '100 -100 100 -100 100 -100 -100 -100 -100 200',
			'Negative polygon coordinates not properly parsed')

class ScourPolylineNegativeCoords(unittest.TestCase):
	def runTest(self):
		p = scour.scourXmlFile('unittests/polyline-coord-neg.svg').getElementsByTagNameNS(SVGNS, 'polyline')[0]
		self.assertEqual(p.getAttribute('points'), '100 -100 100 -100 100 -100 -100 -100 -100 200',
			'Negative polyline coordinates not properly parsed')

class ScourPolygonNegativeCoordFirst(unittest.TestCase):
	def runTest(self):
		p = scour.scourXmlFile('unittests/polygon-coord-neg-first.svg').getElementsByTagNameNS(SVGNS, 'polygon')[0]
		#  points="-100,-100,100-100,100-100-100,-100-100,200" />
		self.assertEqual(p.getAttribute('points'), '-100 -100 100 -100 100 -100 -100 -100 -100 200',
			'Negative polygon coordinates not properly parsed')

class ScourPolylineNegativeCoordFirst(unittest.TestCase):
	def runTest(self):
		p = scour.scourXmlFile('unittests/polyline-coord-neg-first.svg').getElementsByTagNameNS(SVGNS, 'polyline')[0]
		self.assertEqual(p.getAttribute('points'), '-100 -100 100 -100 100 -100 -100 -100 -100 200',
			'Negative polyline coordinates not properly parsed')

class DoNotRemoveGroupsWithIDsInDefs(unittest.TestCase):
	def runTest(self):
		f = scour.scourXmlFile('unittests/important-groups-in-defs.svg')
		self.assertEqual(len(f.getElementsByTagNameNS(SVGNS, 'linearGradient')), 1,
			'Group in defs with id\'ed element removed')

class AlwaysKeepClosePathSegments(unittest.TestCase):
	def runTest(self):
		p = scour.scourXmlFile('unittests/path-with-closepath.svg').getElementsByTagNameNS(SVGNS, 'path')[0]
		self.assertEqual(p.getAttribute('d'), 'm10 10h100v100h-100z',
			'Path with closepath not preserved')

class RemoveDuplicateLinearGradients(unittest.TestCase):
	def runTest(self):
		svgdoc = scour.scourXmlFile('unittests/remove-duplicate-gradients.svg')
		lingrads = svgdoc.getElementsByTagNameNS(SVGNS, 'linearGradient')
		self.assertEqual(1, lingrads.length,
			'Duplicate linear gradient not removed')

class RereferenceForLinearGradient(unittest.TestCase):
	def runTest(self):
		svgdoc = scour.scourXmlFile('unittests/remove-duplicate-gradients.svg')
		rects = svgdoc.getElementsByTagNameNS(SVGNS, 'rect')
		self.assertEqual(rects[0].getAttribute('fill'), rects[1].getAttribute('stroke'),
			'Rect not changed after removing duplicate linear gradient')
		self.assertEqual(rects[0].getAttribute('fill'), rects[4].getAttribute('fill'),
			'Rect not changed after removing duplicate linear gradient')

class RemoveDuplicateRadialGradients(unittest.TestCase):
	def runTest(self):
		svgdoc = scour.scourXmlFile('unittests/remove-duplicate-gradients.svg')
		radgrads = svgdoc.getElementsByTagNameNS(SVGNS, 'radialGradient')
		self.assertEqual(1, radgrads.length,
			'Duplicate radial gradient not removed')

class RereferenceForRadialGradient(unittest.TestCase):
	def runTest(self):
		svgdoc = scour.scourXmlFile('unittests/remove-duplicate-gradients.svg')
		rects = svgdoc.getElementsByTagNameNS(SVGNS, 'rect')
		self.assertEqual(rects[2].getAttribute('stroke'), rects[3].getAttribute('fill'),
			'Rect not changed after removing duplicate radial gradient')

class CollapseSamePathPoints(unittest.TestCase):
	def runTest(self):
		p = scour.scourXmlFile('unittests/collapse-same-path-points.svg').getElementsByTagNameNS(SVGNS, 'path')[0];
		self.assertEqual(p.getAttribute('d'), "m100 100l100.12 100.12c14.877 4.8766-15.123-5.1234 0 0z",
			'Did not collapse same path points')

class ScourUnitlessLengths(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/scour-lengths.svg')
		r = doc.getElementsByTagNameNS(SVGNS, 'rect')[0];
		svg = doc.documentElement
		self.assertEqual(svg.getAttribute('x'), '1',
			'Did not scour x attribute of svg element with unitless number')
		self.assertEqual(r.getAttribute('x'), '123.46',
			'Did not scour x attribute of rect with unitless number')
		self.assertEqual(r.getAttribute('y'), '123',
			'Did not scour y attribute of rect unitless number')
		self.assertEqual(r.getAttribute('width'), '300',
			'Did not scour width attribute of rect with unitless number')
		self.assertEqual(r.getAttribute('height'), '100',
			'Did not scour height attribute of rect with unitless number')

class ScourLengthsWithUnits(unittest.TestCase):
	def runTest(self):
		r = scour.scourXmlFile('unittests/scour-lengths.svg').getElementsByTagNameNS(SVGNS, 'rect')[1];
		self.assertEqual(r.getAttribute('x'), '123.46px',
			'Did not scour x attribute with unit')
		self.assertEqual(r.getAttribute('y'), '35ex',
			'Did not scour y attribute with unit')
		self.assertEqual(r.getAttribute('width'), '300pt',
			'Did not scour width attribute with unit')
		self.assertEqual(r.getAttribute('height'), '50%',
			'Did not scour height attribute with unit')

class RemoveRedundantSvgNamespaceDeclaration(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/redundant-svg-namespace.svg').documentElement
		self.assertNotEqual( doc.getAttribute('xmlns:svg'), 'http://www.w3.org/2000/svg',
			'Redundant svg namespace declaration not removed')

class RemoveRedundantSvgNamespacePrefix(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/redundant-svg-namespace.svg').documentElement
		r = doc.getElementsByTagNameNS(SVGNS, 'rect')[1]
		self.assertEqual( r.tagName, 'rect',
			'Redundant svg: prefix not removed')


class RemoveDefaultGradX1Value(unittest.TestCase):
	def runTest(self):
		g = scour.scourXmlFile('unittests/gradient-default-attrs.svg').getElementById('grad1')
		self.assertEqual( g.getAttribute('x1'), '',
			'x1="0" not removed')

class RemoveDefaultGradY1Value(unittest.TestCase):
	def runTest(self):
		g = scour.scourXmlFile('unittests/gradient-default-attrs.svg').getElementById('grad1')
		self.assertEqual( g.getAttribute('y1'), '',
			'y1="0" not removed')

class RemoveDefaultGradX2Value(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/gradient-default-attrs.svg')
		self.assertEqual( doc.getElementById('grad1').getAttribute('x2'), '',
			'x2="100%" not removed')
		self.assertEqual( doc.getElementById('grad1b').getAttribute('x2'), '',
			'x2="1" not removed, which is equal to the default x2="100%" when gradientUnits="objectBoundingBox"')
		self.assertNotEqual( doc.getElementById('grad1c').getAttribute('x2'), '',
			'x2="1" removed, which is NOT equal to the default x2="100%" when gradientUnits="userSpaceOnUse"')

class RemoveDefaultGradY2Value(unittest.TestCase):
	def runTest(self):
		g = scour.scourXmlFile('unittests/gradient-default-attrs.svg').getElementById('grad1')
		self.assertEqual( g.getAttribute('y2'), '',
			'y2="0" not removed')

class RemoveDefaultGradGradientUnitsValue(unittest.TestCase):
	def runTest(self):
		g = scour.scourXmlFile('unittests/gradient-default-attrs.svg').getElementById('grad1')
		self.assertEqual( g.getAttribute('gradientUnits'), '',
			'gradientUnits="objectBoundingBox" not removed')

class RemoveDefaultGradSpreadMethodValue(unittest.TestCase):
	def runTest(self):
		g = scour.scourXmlFile('unittests/gradient-default-attrs.svg').getElementById('grad1')
		self.assertEqual( g.getAttribute('spreadMethod'), '',
			'spreadMethod="pad" not removed')

class RemoveDefaultGradCXValue(unittest.TestCase):
	def runTest(self):
		g = scour.scourXmlFile('unittests/gradient-default-attrs.svg').getElementById('grad2')
		self.assertEqual( g.getAttribute('cx'), '',
			'cx="50%" not removed')

class RemoveDefaultGradCYValue(unittest.TestCase):
	def runTest(self):
		g = scour.scourXmlFile('unittests/gradient-default-attrs.svg').getElementById('grad2')
		self.assertEqual( g.getAttribute('cy'), '',
			'cy="50%" not removed')

class RemoveDefaultGradRValue(unittest.TestCase):
	def runTest(self):
		g = scour.scourXmlFile('unittests/gradient-default-attrs.svg').getElementById('grad2')
		self.assertEqual( g.getAttribute('r'), '',
			'r="50%" not removed')

class RemoveDefaultGradFXValue(unittest.TestCase):
	def runTest(self):
		g = scour.scourXmlFile('unittests/gradient-default-attrs.svg').getElementById('grad2')
		self.assertEqual( g.getAttribute('fx'), '',
			'fx matching cx not removed')

class RemoveDefaultGradFYValue(unittest.TestCase):
	def runTest(self):
		g = scour.scourXmlFile('unittests/gradient-default-attrs.svg').getElementById('grad2')
		self.assertEqual( g.getAttribute('fy'), '',
			'fy matching cy not removed')

class CDATAInXml(unittest.TestCase):
	def runTest(self):
		with open('unittests/cdata.svg') as f:
			lines = scour.scourString(f.read()).splitlines()
		self.assertEqual( lines[3],
			"  	alert('pb&j');",
			'CDATA did not come out correctly')

class WellFormedXMLLesserThanInAttrValue(unittest.TestCase):
	def runTest(self):
		with open('unittests/xml-well-formed.svg') as f:
			wellformed = scour.scourString(f.read())
		self.assertTrue( wellformed.find('unicode="&lt;"') != -1,
			"Improperly serialized &lt; in attribute value")

class WellFormedXMLAmpersandInAttrValue(unittest.TestCase):
	def runTest(self):
		with open('unittests/xml-well-formed.svg') as f:
			wellformed = scour.scourString(f.read())
		self.assertTrue( wellformed.find('unicode="&amp;"') != -1,
			'Improperly serialized &amp; in attribute value' )

class WellFormedXMLLesserThanInTextContent(unittest.TestCase):
	def runTest(self):
		with open('unittests/xml-well-formed.svg') as f:
			wellformed = scour.scourString(f.read())
		self.assertTrue( wellformed.find('<title>2 &lt; 5</title>') != -1,
			'Improperly serialized &lt; in text content')

class WellFormedXMLAmpersandInTextContent(unittest.TestCase):
	def runTest(self):
		with open('unittests/xml-well-formed.svg') as f:
			wellformed = scour.scourString(f.read())
		self.assertTrue( wellformed.find('<desc>Peanut Butter &amp; Jelly</desc>') != -1,
			'Improperly serialized &amp; in text content')

class WellFormedXMLNamespacePrefixRemoveUnused(unittest.TestCase):
	def runTest(self):
		with open('unittests/xml-well-formed.svg') as f:
			wellformed = scour.scourString(f.read())
		self.assertTrue( wellformed.find('xmlns:foo=') == -1,
			'Improperly serialized namespace prefix declarations: Unused namespace decaration not removed')

class WellFormedXMLNamespacePrefixKeepUsedElementPrefix(unittest.TestCase):
	def runTest(self):
		with open('unittests/xml-well-formed.svg') as f:
			wellformed = scour.scourString(f.read())
		self.assertTrue( wellformed.find('xmlns:bar=') != -1,
			'Improperly serialized namespace prefix declarations: Used element prefix removed')

class WellFormedXMLNamespacePrefixKeepUsedAttributePrefix(unittest.TestCase):
	def runTest(self):
		with open('unittests/xml-well-formed.svg') as f:
			wellformed = scour.scourString(f.read())
		self.assertTrue( wellformed.find('xmlns:baz=') != -1,
			'Improperly serialized namespace prefix declarations: Used attribute prefix removed')

class NamespaceDeclPrefixesInXMLWhenNotInDefaultNamespace(unittest.TestCase):
	def runTest(self):
		with open('unittests/xml-ns-decl.svg') as f:
			xmlstring = scour.scourString(f.read())
		self.assertTrue( xmlstring.find('xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"') != -1,
			'Improperly serialized namespace prefix declarations when not in default namespace')

class MoveSVGElementsToDefaultNamespace(unittest.TestCase):
	def runTest(self):
		with open('unittests/xml-ns-decl.svg') as f:
			xmlstring = scour.scourString(f.read())
		self.assertTrue( xmlstring.find('<rect ') != -1,
			'Did not bring SVG elements into the default namespace')

class MoveCommonAttributesToParent(unittest.TestCase):
	def runTest(self):
		g = scour.scourXmlFile('unittests/move-common-attributes-to-parent.svg').getElementsByTagNameNS(SVGNS, 'g')[0]
		self.assertEqual( g.getAttribute('fill'), '#0F0',
			'Did not move common fill attribute to parent group')

class RemoveCommonAttributesFromChild(unittest.TestCase):
	def runTest(self):
		r = scour.scourXmlFile('unittests/move-common-attributes-to-parent.svg').getElementsByTagNameNS(SVGNS, 'rect')[0]
		self.assertNotEqual( r.getAttribute('fill'), '#0F0',
			'Did not remove common fill attribute from child')

class DontRemoveCommonAttributesIfParentHasTextNodes(unittest.TestCase):
	def runTest(self):
		text = scour.scourXmlFile('unittests/move-common-attributes-to-parent.svg').getElementsByTagNameNS(SVGNS, 'text')[0]
		self.assertNotEqual( text.getAttribute('font-style'), 'italic',
			'Removed common attributes when parent contained text elements')

class PropagateCommonAttributesUp(unittest.TestCase):
	def runTest(self):
		g = scour.scourXmlFile('unittests/move-common-attributes-to-grandparent.svg').getElementsByTagNameNS(SVGNS, 'g')[0]
		self.assertEqual( g.getAttribute('fill'), '#0F0',
			'Did not move common fill attribute to grandparent')

class PathEllipticalArcParsingCommaWsp(unittest.TestCase):
	def runTest(self):
		p = scour.scourXmlFile('unittests/path-elliptical-arc-parsing.svg').getElementsByTagNameNS(SVGNS, 'path')[0]
		self.assertEqual( p.getAttribute('d'), 'm100 100a100 100 0 1 1 -50 100z',
			'Did not parse elliptical arc command properly')

class RemoveUnusedAttributesOnParent(unittest.TestCase):
	def runTest(self):
		g = scour.scourXmlFile('unittests/remove-unused-attributes-on-parent.svg').getElementsByTagNameNS(SVGNS, 'g')[0]
		self.assertNotEqual( g.getAttribute('stroke'), '#000',
			'Unused attributes on group not removed')

class DoNotRemoveCommonAttributesOnParentIfAtLeastOneUsed(unittest.TestCase):
	def runTest(self):
		g = scour.scourXmlFile('unittests/remove-unused-attributes-on-parent.svg').getElementsByTagNameNS(SVGNS, 'g')[0]
		self.assertEqual( g.getAttribute('fill'), '#0F0',
			'Used attributes on group were removed')

class DoNotRemoveGradientsWhenReferencedInStyleCss(unittest.TestCase):
	def runTest(self):
		grads = scour.scourXmlFile('unittests/css-reference.svg').getElementsByTagNameNS(SVGNS, 'linearGradient')
		self.assertEqual( grads.length, 2,
			'Gradients removed when referenced in CSS')

class DoNotPrettyPrintWhenWhitespacePreserved(unittest.TestCase):
	def runTest(self):
		with open('unittests/whitespace-important.svg') as f:
			s = scour.scourString(f.read()).splitlines()
		c = '''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg">
 <text xml:space="preserve">This is some <tspan font-style="italic">messed-up</tspan> markup</text>
</svg>
'''.splitlines()
		for i in range(4):
			self.assertEqual( s[i], c[i],
			'Whitespace not preserved for line ' + str(i))

class DoNotPrettyPrintWhenNestedWhitespacePreserved(unittest.TestCase):
	def runTest(self):
		with open('unittests/whitespace-nested.svg') as f:
			s = scour.scourString(f.read()).splitlines()
		c = '''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg">
 <text xml:space="preserve"><tspan font-style="italic">Use <tspan font-style="bold">bold</tspan> text</tspan></text>
</svg>
'''.splitlines()
		for i in range(4):
			self.assertEqual( s[i], c[i],
				'Whitespace not preserved when nested for line ' + str(i))

class GetAttrPrefixRight(unittest.TestCase):
	def runTest(self):
		grad = scour.scourXmlFile('unittests/xml-namespace-attrs.svg').getElementsByTagNameNS(SVGNS, 'linearGradient')[1]
		self.assertEqual( grad.getAttributeNS('http://www.w3.org/1999/xlink', 'href'), '#linearGradient841',
			'Did not get xlink:href prefix right')

class EnsurePreserveWhitespaceOnNonTextElements(unittest.TestCase):
	def runTest(self):
		with open('unittests/no-collapse-lines.svg') as f:
			s = scour.scourString(f.read())
		self.assertEqual( len(s.splitlines()), 6,
			'Did not properly preserve whitespace on elements even if they were not textual')

class HandleEmptyStyleElement(unittest.TestCase):
	def runTest(self):
		try:
			styles = scour.scourXmlFile('unittests/empty-style.svg').getElementsByTagNameNS(SVGNS, 'style')
			fail = len(styles) != 1
		except AttributeError:
			fail = True
		self.assertEqual( fail, False,
			'Could not handle an empty style element')

class EnsureLineEndings(unittest.TestCase):
	def runTest(self):
		with open('unittests/whitespace-important.svg') as f:
			s = scour.scourString(f.read())
		self.assertEqual( len(s.splitlines()), 4,
			'Did not output line ending character correctly')

class XmlEntities(unittest.TestCase):
	def runTest(self):
		self.assertEqual( scour.makeWellFormed('<>&'), '&lt;&gt;&amp;',
			'Incorrectly translated XML entities')

class DoNotStripCommentsOutsideOfRoot(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/comments.svg')
		self.assertEqual( doc.childNodes.length, 4,
			'Did not include all comment children outside of root')
		self.assertEqual( doc.childNodes[0].nodeType, 8, 'First node not a comment')
		self.assertEqual( doc.childNodes[1].nodeType, 8, 'Second node not a comment')
		self.assertEqual( doc.childNodes[3].nodeType, 8, 'Fourth node not a comment')

class DoNotStripDoctype(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/doctype.svg')
		self.assertEqual( doc.childNodes.length, 3,
			'Did not include the DOCROOT')
		self.assertEqual( doc.childNodes[0].nodeType, 8, 'First node not a comment')
		self.assertEqual( doc.childNodes[1].nodeType, 10, 'Second node not a doctype')
		self.assertEqual( doc.childNodes[2].nodeType, 1, 'Third node not the root node')

class PathImplicitLineWithMoveCommands(unittest.TestCase):
	def runTest(self):
		path = scour.scourXmlFile('unittests/path-implicit-line.svg').getElementsByTagNameNS(SVGNS, 'path')[0]
		self.assertEqual( path.getAttribute('d'), "m100 100v100m200-100h-200m200 100v-100",
			"Implicit line segments after move not preserved")

class RemoveTitlesOption(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/full-descriptive-elements.svg',
			scour.parse_args(['--remove-titles']))
		self.assertEqual(doc.childNodes.length, 1,
			'Did not remove <title> tag with --remove-titles')

class RemoveDescriptionsOption(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/full-descriptive-elements.svg',
			scour.parse_args(['--remove-descriptions']))
		self.assertEqual(doc.childNodes.length, 1,
			'Did not remove <desc> tag with --remove-descriptions')

class RemoveMetadataOption(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/full-descriptive-elements.svg',
			scour.parse_args(['--remove-metadata']))
		self.assertEqual(doc.childNodes.length, 1,
			'Did not remove <metadata> tag with --remove-metadata')

class RemoveDescriptiveElementsOption(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/full-descriptive-elements.svg',
			scour.parse_args(['--remove-descriptive-elements']))
		self.assertEqual(doc.childNodes.length, 1,
			'Did not remove <title>, <desc> and <metadata> tags with --remove-descriptive-elements')

class EnableCommentStrippingOption(unittest.TestCase):
	def runTest(self):
		with open('unittests/comment-beside-xml-decl.svg') as f:
			docStr = f.read()
		docStr = scour.scourString(docStr,
			scour.parse_args(['--enable-comment-stripping']))
		self.assertEqual(docStr.find('<!--'), -1,
			'Did not remove document-level comment with --enable-comment-stripping')

class StripXmlPrologOption(unittest.TestCase):
	def runTest(self):
		with open('unittests/comment-beside-xml-decl.svg') as f:
			docStr = f.read()
		docStr = scour.scourString(docStr,
			scour.parse_args(['--strip-xml-prolog']))
		self.assertEqual(docStr.find('<?xml'), -1,
			'Did not remove <?xml?> with --strip-xml-prolog')

class ShortenIDsOption(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/shorten-ids.svg',
			scour.parse_args(['--shorten-ids']))
		gradientTag = doc.getElementsByTagName('linearGradient')[0]
		self.assertEqual(gradientTag.getAttribute('id'), 'a',
			"Did not shorten a linear gradient's ID with --shorten-ids")
		rectTag = doc.getElementsByTagName('rect')[0]
		self.assertEqual(rectTag.getAttribute('fill'), 'url(#a)',
			'Did not update reference to shortened ID')

class MustKeepGInSwitch(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/groups-in-switch.svg')
		self.assertEqual(doc.getElementsByTagName('g').length, 1,
			'Erroneously removed a <g> in a <switch>')

class MustKeepGInSwitch2(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/groups-in-switch-with-id.svg',
			scour.parse_args(['--enable-id-stripping']))
		self.assertEqual(doc.getElementsByTagName('g').length, 1,
			'Erroneously removed a <g> in a <switch>')

class GroupCreation(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/group-creation.svg',
			scour.parse_args(['--create-groups']))
		self.assertEqual(doc.getElementsByTagName('g').length, 1,
			'Did not create a <g> for a run of elements having similar attributes')

class GroupCreationForInheritableAttributesOnly(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/group-creation.svg',
			scour.parse_args(['--create-groups']))
		self.assertEqual(doc.getElementsByTagName('g').item(0).getAttribute('y'), '',
			'Promoted the uninheritable attribute y to a <g>')

class GroupNoCreation(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/group-no-creation.svg',
			scour.parse_args(['--create-groups']))
		self.assertEqual(doc.getElementsByTagName('g').length, 0,
			'Created a <g> for a run of elements having dissimilar attributes')

class GroupNoCreationForTspan(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/group-no-creation-tspan.svg',
			scour.parse_args(['--create-groups']))
		self.assertEqual(doc.getElementsByTagName('g').length, 0,
			'Created a <g> for a run of <tspan>s that are not allowed as children according to content model')

class DoNotCommonizeAttributesOnReferencedElements(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/commonized-referenced-elements.svg')
		self.assertEqual(doc.getElementsByTagName('circle')[0].getAttribute('fill'), '#0f0',
			'Grouped an element referenced elsewhere into a <g>')

class DoNotRemoveOverflowVisibleOnMarker(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/overflow-marker.svg')
		self.assertEqual(doc.getElementById('m1').getAttribute('overflow'), 'visible',
			'Removed the overflow attribute when it was not using the default value')
		self.assertEqual(doc.getElementById('m2').getAttribute('overflow'), '',
			'Did not remove the overflow attribute when it was using the default value')

class DoNotRemoveOrientAutoOnMarker(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/orient-marker.svg')
		self.assertEqual(doc.getElementById('m1').getAttribute('orient'), 'auto',
			'Removed the orient attribute when it was not using the default value')
		self.assertEqual(doc.getElementById('m2').getAttribute('orient'), '',
			'Did not remove the orient attribute when it was using the default value')

class MarkerOnSvgElements(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/overflow-svg.svg')
		self.assertEqual(doc.getElementsByTagName('svg')[0].getAttribute('overflow'), '',
			'Did not remove the overflow attribute when it was using the default value')
		self.assertEqual(doc.getElementsByTagName('svg')[1].getAttribute('overflow'), '',
			'Did not remove the overflow attribute when it was using the default value')
		self.assertEqual(doc.getElementsByTagName('svg')[2].getAttribute('overflow'), 'visible',
			'Removed the overflow attribute when it was not using the default value')

class GradientReferencedByStyleCDATA(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/style-cdata.svg')
		self.assertEqual(len(doc.getElementsByTagName('linearGradient')), 1,
			'Removed a gradient referenced by an internal stylesheet')

class ShortenIDsInStyleCDATA(unittest.TestCase):
	def runTest(self):
		with open('unittests/style-cdata.svg') as f:
			docStr = f.read()
		docStr = scour.scourString(docStr,
			scour.parse_args(['--shorten-ids']))
		self.assertEqual(docStr.find('somethingreallylong'), -1,
			'Did not shorten IDs in the internal stylesheet')

class StyleToAttr(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/style-to-attr.svg')
		line = doc.getElementsByTagName('line')[0]
		self.assertEqual(line.getAttribute('stroke'), '#000')
		self.assertEqual(line.getAttribute('marker-start'), 'url(#m)')
		self.assertEqual(line.getAttribute('marker-mid'), 'url(#m)')
		self.assertEqual(line.getAttribute('marker-end'), 'url(#m)')

class PathEmptyMove(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/path-empty-move.svg')
		self.assertEqual(doc.getElementsByTagName('path')[0].getAttribute('d'), 'm100 100l200 100z')
		self.assertEqual(doc.getElementsByTagName('path')[1].getAttribute('d'), 'm100 100v200l100 100z')

class DefaultsRemovalToplevel(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/cascading-default-attribute-removal.svg')
		self.assertEqual(doc.getElementsByTagName('path')[1].getAttribute('fill-rule'), '',
			'Default attribute fill-rule:nonzero not removed')

class DefaultsRemovalToplevelInverse(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/cascading-default-attribute-removal.svg')
		self.assertEqual(doc.getElementsByTagName('path')[0].getAttribute('fill-rule'), 'evenodd',
			'Non-Default attribute fill-rule:evenodd removed')

class DefaultsRemovalToplevelFormat(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/cascading-default-attribute-removal.svg')
		self.assertEqual(doc.getElementsByTagName('path')[0].getAttribute('stroke-width'), '',
			'Default attribute stroke-width:1.00 not removed');

class DefaultsRemovalInherited(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/cascading-default-attribute-removal.svg')
		self.assertEqual(doc.getElementsByTagName('path')[3].getAttribute('fill-rule'), '',
			'Default attribute fill-rule:nonzero not removed in child')

class DefaultsRemovalInheritedInverse(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/cascading-default-attribute-removal.svg')
		self.assertEqual(doc.getElementsByTagName('path')[2].getAttribute('fill-rule'), 'evenodd',
			'Non-Default attribute fill-rule:evenodd removed in child')

class DefaultsRemovalInheritedFormat(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/cascading-default-attribute-removal.svg')
		self.assertEqual(doc.getElementsByTagName('path')[2].getAttribute('stroke-width'), '',
			'Default attribute stroke-width:1.00 not removed in child')

class DefaultsRemovalOverwrite(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/cascading-default-attribute-removal.svg')
		self.assertEqual(doc.getElementsByTagName('path')[5].getAttribute('fill-rule'), 'nonzero',
			'Default attribute removed, although it overwrites parent element')

class DefaultsRemovalOverwriteMarker(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/cascading-default-attribute-removal.svg')
		self.assertEqual(doc.getElementsByTagName('path')[4].getAttribute('marker-start'), 'none',
			'Default marker attribute removed, although it overwrites parent element')

class DefaultsRemovalNonOverwrite(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/cascading-default-attribute-removal.svg')
		self.assertEqual(doc.getElementsByTagName('path')[10].getAttribute('fill-rule'), '',
			'Default attribute not removed, although its parent used default')

class RemoveDefsWithUnreferencedElements(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/useless-defs.svg')
		self.assertEqual(doc.getElementsByTagName('defs').length, 0,
			'Kept defs, although it contains only unreferenced elements')

class RemoveDefsWithWhitespace(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/whitespace-defs.svg')
		self.assertEqual(doc.getElementsByTagName('defs').length, 0,
			'Kept defs, although it contains only whitespace or is <defs/>')

class TransformIdentityMatrix(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/transform-matrix-is-identity.svg')
		self.assertEqual(doc.getElementsByTagName('line')[0].getAttribute('transform'), '',
			'Transform containing identity matrix not removed')

class TransformRotate135(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/transform-matrix-is-rotate-135.svg')
		self.assertEqual(doc.getElementsByTagName('line')[0].getAttribute('transform'), 'rotate(135)',
			'Rotation matrix not converted to rotate(135)')

class TransformRotate45(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/transform-matrix-is-rotate-45.svg')
		self.assertEqual(doc.getElementsByTagName('line')[0].getAttribute('transform'), 'rotate(45)',
			'Rotation matrix not converted to rotate(45)')

class TransformRotate90(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/transform-matrix-is-rotate-90.svg')
		self.assertEqual(doc.getElementsByTagName('line')[0].getAttribute('transform'), 'rotate(90)',
			'Rotation matrix not converted to rotate(90)')

class TransformRotateCCW135(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/transform-matrix-is-rotate-225.svg')
		self.assertEqual(doc.getElementsByTagName('line')[0].getAttribute('transform'), 'rotate(225)',
			'Counter-clockwise rotation matrix not converted to rotate(225)')

class TransformRotateCCW45(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/transform-matrix-is-rotate-neg-45.svg')
		self.assertEqual(doc.getElementsByTagName('line')[0].getAttribute('transform'), 'rotate(-45)',
			'Counter-clockwise rotation matrix not converted to rotate(-45)')

class TransformRotateCCW90(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/transform-matrix-is-rotate-neg-90.svg')
		self.assertEqual(doc.getElementsByTagName('line')[0].getAttribute('transform'), 'rotate(-90)',
			'Counter-clockwise rotation matrix not converted to rotate(-90)')

class TransformScale2by3(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/transform-matrix-is-scale-2-3.svg')
		self.assertEqual(doc.getElementsByTagName('line')[0].getAttribute('transform'), 'scale(2 3)',
			'Scaling matrix not converted to scale(2 3)')

class TransformScaleMinus1(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/transform-matrix-is-scale-neg-1.svg')
		self.assertEqual(doc.getElementsByTagName('line')[0].getAttribute('transform'), 'scale(-1)',
			'Scaling matrix not converted to scale(-1)')

class TransformTranslate(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/transform-matrix-is-translate.svg')
		self.assertEqual(doc.getElementsByTagName('line')[0].getAttribute('transform'), 'translate(2 3)',
			'Translation matrix not converted to translate(2 3)')

class TransformRotationRange719_5(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/transform-rotate-trim-range-719.5.svg')
		self.assertEqual(doc.getElementsByTagName('line')[0].getAttribute('transform'), 'rotate(-.5)',
			'Transform containing rotate(719.5) not shortened to rotate(-.5)')

class TransformRotationRangeCCW540_0(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/transform-rotate-trim-range-neg-540.0.svg')
		self.assertEqual(doc.getElementsByTagName('line')[0].getAttribute('transform'), 'rotate(180)',
			'Transform containing rotate(-540.0) not shortened to rotate(180)')

class TransformRotation3Args(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/transform-rotate-fold-3args.svg')
		self.assertEqual(doc.getElementsByTagName('line')[0].getAttribute('transform'), 'rotate(90)',
			'Optional zeroes in rotate(angle 0 0) not removed')

class TransformIdentityRotation(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/transform-rotate-is-identity.svg')
		self.assertEqual(doc.getElementsByTagName('line')[0].getAttribute('transform'), '',
			'Transform containing identity rotation not removed')

class TransformIdentitySkewX(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/transform-skewX-is-identity.svg')
		self.assertEqual(doc.getElementsByTagName('line')[0].getAttribute('transform'), '',
			'Transform containing identity X-axis skew not removed')

class TransformIdentitySkewY(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/transform-skewY-is-identity.svg')
		self.assertEqual(doc.getElementsByTagName('line')[0].getAttribute('transform'), '',
			'Transform containing identity Y-axis skew not removed')

class TransformIdentityTranslate(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/transform-translate-is-identity.svg')
		self.assertEqual(doc.getElementsByTagName('line')[0].getAttribute('transform'), '',
			'Transform containing identity translation not removed')

class DuplicateGradientsUpdateStyle(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/duplicate-gradients-update-style.svg',
			scour.parse_args(['--disable-style-to-xml']))
		gradientTag = doc.getElementsByTagName('linearGradient')[0]
		rectTag0 = doc.getElementsByTagName('rect')[0]
		rectTag1 = doc.getElementsByTagName('rect')[1]
		self.assertEqual('fill:url(#' + gradientTag.getAttribute('id') + ')', rectTag0.getAttribute('style'),
			'Either of #duplicate-one or #duplicate-two was removed, but style="fill:" was not updated to reflect this')
		self.assertEqual('fill:url(#' + gradientTag.getAttribute('id') + ')', rectTag1.getAttribute('style'),
			'Either of #duplicate-one or #duplicate-two was removed, but style="fill:" was not updated to reflect this')

class DocWithFlowtext(unittest.TestCase):
    def runTest(self):
        with self.assertRaises(Exception):
            scour.scourXmlFile('unittests/flowtext.svg',
                               scour.parse_args(['--error-on-flowtext']))

class DocWithNoFlowtext(unittest.TestCase):
    def runTest(self):
        try:
            scour.scourXmlFile('unittests/flowtext-less.svg',
                               scour.parse_args(['--error-on-flowtext']))
        except Exception as e:
            self.fail("exception '{}' was raised, and we didn't expect that!".format(e))

# TODO: write tests for --enable-viewboxing
# TODO; write a test for embedding rasters
# TODO: write a test for --disable-embed-rasters
# TODO: write tests for --keep-editor-data

if __name__ == '__main__':
	testcss = __import__('testcss')
	scour = __import__('__main__')
	suite = unittest.TestSuite( list(map(unittest.defaultTestLoader.loadTestsFromModule, [testcss, scour])) )
	unittest.main(defaultTest="suite")
