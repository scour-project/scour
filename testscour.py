#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
from svg_regex import svg_parser

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
	simple_colors = True
	style_to_xml = True
	group_collapse = True
	strip_ids = False
	digits = 5
	embed_rasters = True
	keep_editor_data = False
	strip_xml_prolog = False
	indent_type = "space"

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

class NoAdobeIllustratorElements(unittest.TestCase):
	def runTest(self):
		self.assertNotEquals(walkTree(scour.scourXmlFile('unittests/adobe.svg').documentElement, 
			lambda e: e.namespaceURI != 'http://ns.adobe.com/AdobeIllustrator/10.0/'), False,
			'Found Adobe Illustrator elements' )
class NoAdobeGraphsElements(unittest.TestCase):
	def runTest(self):
		self.assertNotEquals(walkTree(scour.scourXmlFile('unittests/adobe.svg').documentElement, 
			lambda e: e.namespaceURI != 'http://ns.adobe.com/Graphs/1.0/'), False,
			'Found Adobe Graphs elements' )
class NoAdobeSVGViewerElements(unittest.TestCase):
	def runTest(self):
		self.assertNotEquals(walkTree(scour.scourXmlFile('unittests/adobe.svg').documentElement, 
			lambda e: e.namespaceURI != 'http://ns.adobe.com/AdobeSVGViewerExtensions/3.0/'), False,
			'Found Adobe SVG Viewer elements' )
class NoAdobeVariablesElements(unittest.TestCase):
	def runTest(self):
		self.assertNotEquals(walkTree(scour.scourXmlFile('unittests/adobe.svg').documentElement, 
			lambda e: e.namespaceURI != 'http://ns.adobe.com/Variables/1.0/'), False,
			'Found Adobe Variables elements' )
class NoAdobeSaveForWebElements(unittest.TestCase):
	def runTest(self):
		self.assertNotEquals(walkTree(scour.scourXmlFile('unittests/adobe.svg').documentElement, 
			lambda e: e.namespaceURI != 'http://ns.adobe.com/SaveForWeb/1.0/'), False,
			'Found Adobe Save For Web elements' )
class NoAdobeExtensibilityElements(unittest.TestCase):
	def runTest(self):
		self.assertNotEquals(walkTree(scour.scourXmlFile('unittests/adobe.svg').documentElement, 
			lambda e: e.namespaceURI != 'http://ns.adobe.com/Extensibility/1.0/'), False,
			'Found Adobe Extensibility elements' )
class NoAdobeFlowsElements(unittest.TestCase):
	def runTest(self):
		self.assertNotEquals(walkTree(scour.scourXmlFile('unittests/adobe.svg').documentElement, 
			lambda e: e.namespaceURI != 'http://ns.adobe.com/Flows/1.0/'), False,
			'Found Adobe Flows elements' )
class NoAdobeImageReplacementElements(unittest.TestCase):
	def runTest(self):
		self.assertNotEquals(walkTree(scour.scourXmlFile('unittests/adobe.svg').documentElement, 
			lambda e: e.namespaceURI != 'http://ns.adobe.com/ImageReplacement/1.0/'), False,
			'Found Adobe Image Replacement elements' )
class NoAdobeCustomElements(unittest.TestCase):
	def runTest(self):
		self.assertNotEquals(walkTree(scour.scourXmlFile('unittests/adobe.svg').documentElement, 
			lambda e: e.namespaceURI != 'http://ns.adobe.com/GenericCustomNamespace/1.0/'), False,
			'Found Adobe Custom elements' )
class NoAdobeXPathElements(unittest.TestCase):
	def runTest(self):
		self.assertNotEquals(walkTree(scour.scourXmlFile('unittests/adobe.svg').documentElement, 
			lambda e: e.namespaceURI != 'http://ns.adobe.com/XPath/1.0/'), False,
			'Found Adobe XPath elements' )

class DoNotRemoveMetadataWithOnlyText(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/metadata-with-text.svg')
		self.assertEquals(len(doc.getElementsByTagNameNS(SVGNS, 'metadata')), 1,
			'Removed metadata element with only text child' )

class RemoveEmptyMetadataElement(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/empty-metadata.svg')
		self.assertEquals(len(doc.getElementsByTagNameNS(SVGNS, 'metadata')), 0,
			'Did not remove empty metadata element' )

class RemoveEmptyGElements(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/empty-g.svg')
		self.assertEquals(len(doc.getElementsByTagNameNS(SVGNS, 'g')), 1,
			'Did not remove empty g element' )

class RemoveUnreferencedPattern(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/unreferenced-pattern.svg')
		self.assertEquals(len(doc.getElementsByTagNameNS(SVGNS, 'pattern')), 0,
			'Unreferenced pattern not removed' )

class RemoveUnreferencedLinearGradient(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/unreferenced-linearGradient.svg')
		self.assertEquals(len(doc.getElementsByTagNameNS(SVGNS, 'linearGradient')), 0,
			'Unreferenced linearGradient not removed' )

class RemoveUnreferencedRadialGradient(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/unreferenced-radialGradient.svg')
		self.assertEquals(len(doc.getElementsByTagNameNS(SVGNS, 'radialradient')), 0,
			'Unreferenced radialGradient not removed' )

class RemoveUnreferencedElementInDefs(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/referenced-elements-1.svg')
		self.assertEquals(len(doc.getElementsByTagNameNS(SVGNS, 'rect')), 1,
			'Unreferenced rect left in defs' )

class KeepTitleInDefs(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/referenced-elements-1.svg')
		self.assertEquals(len(doc.getElementsByTagNameNS(SVGNS, 'title')), 1,
			'Title removed from in defs' )

class KeepUnreferencedIDsWhenEnabled(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/ids-to-strip.svg')
		self.assertEquals(doc.getElementsByTagNameNS(SVGNS, 'svg')[0].getAttribute('id'), 'boo',
			'<svg> ID stripped when it should be disabled' )
			
class RemoveUnreferencedIDsWhenEnabled(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/ids-to-strip.svg',
			scour.parse_args(['--enable-id-stripping'])[0])
		self.assertEquals(doc.getElementsByTagNameNS(SVGNS, 'svg')[0].getAttribute('id'), '',
			'<svg> ID not stripped' )

class RemoveUselessNestedGroups(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/nested-useless-groups.svg')
		self.assertEquals(len(doc.getElementsByTagNameNS(SVGNS, 'g')), 1,
			'Useless nested groups not removed' )

class DoNotRemoveUselessNestedGroups(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/nested-useless-groups.svg',
			scour.parse_args(['--disable-group-collapsing'])[0])
		self.assertEquals(len(doc.getElementsByTagNameNS(SVGNS, 'g')), 2,
			'Useless nested groups were removed despite --disable-group-collapsing' )

class DoNotRemoveNestedGroupsWithTitle(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/groups-with-title-desc.svg')
		self.assertEquals(len(doc.getElementsByTagNameNS(SVGNS, 'g')), 2,
			'Nested groups with title was removed' )

class DoNotRemoveNestedGroupsWithDesc(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/groups-with-title-desc.svg')
		self.assertEquals(len(doc.getElementsByTagNameNS(SVGNS, 'g')), 2,
			'Nested groups with desc was removed' )

class RemoveDuplicateLinearGradientStops(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/duplicate-gradient-stops.svg')
		grad = doc.getElementsByTagNameNS(SVGNS, 'linearGradient')
		self.assertEquals(len(grad[0].getElementsByTagNameNS(SVGNS, 'stop')), 3,
			'Duplicate linear gradient stops not removed' )

class RemoveDuplicateLinearGradientStopsPct(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/duplicate-gradient-stops-pct.svg')
		grad = doc.getElementsByTagNameNS(SVGNS, 'linearGradient')
		self.assertEquals(len(grad[0].getElementsByTagNameNS(SVGNS, 'stop')), 3,
			'Duplicate linear gradient stops with percentages not removed' )

class RemoveDuplicateRadialGradientStops(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/duplicate-gradient-stops.svg')
		grad = doc.getElementsByTagNameNS(SVGNS, 'radialGradient')
		self.assertEquals(len(grad[0].getElementsByTagNameNS(SVGNS, 'stop')), 3,
			'Duplicate radial gradient stops not removed' )

class NoSodipodiNamespaceDecl(unittest.TestCase):
	def runTest(self):
		attrs = scour.scourXmlFile('unittests/sodipodi.svg').documentElement.attributes
		for i in range(len(attrs)):
			self.assertNotEquals(attrs.item(i).nodeValue,
				'http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd',
				'Sodipodi namespace declaration found' )

class NoInkscapeNamespaceDecl(unittest.TestCase):
	def runTest(self):
		attrs = scour.scourXmlFile('unittests/inkscape.svg').documentElement.attributes
		for i in range(len(attrs)):
			self.assertNotEquals(attrs.item(i).nodeValue,
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
		self.assertNotEquals(walkTree(scour.scourXmlFile('unittests/sodipodi.svg').documentElement, 
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
		self.assertNotEquals(walkTree(scour.scourXmlFile('unittests/inkscape.svg').documentElement, 
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
		self.assertEquals(True, FoundNamespace,
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
		self.assertEquals(True, FoundNamespace,
			"Did not find Sodipodi namespace declaration when using --keep-editor-data")
		return False

class KeepReferencedFonts(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/referenced-font.svg')
		fonts = doc.documentElement.getElementsByTagNameNS(SVGNS,'font')
		self.assertEquals(len(fonts), 1,
			'Font wrongly removed from <defs>' )
			
class ConvertStyleToAttrs(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/stroke-transparent.svg')
		self.assertEquals(doc.getElementsByTagNameNS(SVGNS, 'path')[0].getAttribute('style'), '',
			'style attribute not emptied' )
			
class RemoveStrokeWhenStrokeTransparent(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/stroke-transparent.svg')
		self.assertEquals(doc.getElementsByTagNameNS(SVGNS, 'path')[0].getAttribute('stroke'), '',
			'stroke attribute not emptied when stroke opacity zero' )

class RemoveStrokeWidthWhenStrokeTransparent(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/stroke-transparent.svg')
		self.assertEquals(doc.getElementsByTagNameNS(SVGNS, 'path')[0].getAttribute('stroke-width'), '',
			'stroke-width attribute not emptied when stroke opacity zero' )

class RemoveStrokeLinecapWhenStrokeTransparent(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/stroke-transparent.svg')
		self.assertEquals(doc.getElementsByTagNameNS(SVGNS, 'path')[0].getAttribute('stroke-linecap'), '',
			'stroke-linecap attribute not emptied when stroke opacity zero' )

class RemoveStrokeLinejoinWhenStrokeTransparent(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/stroke-transparent.svg')
		self.assertEquals(doc.getElementsByTagNameNS(SVGNS, 'path')[0].getAttribute('stroke-linejoin'), '',
			'stroke-linejoin attribute not emptied when stroke opacity zero' )

class RemoveStrokeDasharrayWhenStrokeTransparent(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/stroke-transparent.svg')
		self.assertEquals(doc.getElementsByTagNameNS(SVGNS, 'path')[0].getAttribute('stroke-dasharray'), '',
			'stroke-dasharray attribute not emptied when stroke opacity zero' )

class RemoveStrokeDashoffsetWhenStrokeTransparent(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/stroke-transparent.svg')
		self.assertEquals(doc.getElementsByTagNameNS(SVGNS, 'path')[0].getAttribute('stroke-dashoffset'), '',
			'stroke-dashoffset attribute not emptied when stroke opacity zero' )

class RemoveStrokeWhenStrokeWidthZero(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/stroke-nowidth.svg')
		self.assertEquals(doc.getElementsByTagNameNS(SVGNS, 'path')[0].getAttribute('stroke'), '',
			'stroke attribute not emptied when width zero' )

class RemoveStrokeOpacityWhenStrokeWidthZero(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/stroke-nowidth.svg')
		self.assertEquals(doc.getElementsByTagNameNS(SVGNS, 'path')[0].getAttribute('stroke-opacity'), '',
			'stroke-opacity attribute not emptied when width zero' )

class RemoveStrokeLinecapWhenStrokeWidthZero(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/stroke-nowidth.svg')
		self.assertEquals(doc.getElementsByTagNameNS(SVGNS, 'path')[0].getAttribute('stroke-linecap'), '',
			'stroke-linecap attribute not emptied when width zero' )

class RemoveStrokeLinejoinWhenStrokeWidthZero(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/stroke-nowidth.svg')
		self.assertEquals(doc.getElementsByTagNameNS(SVGNS, 'path')[0].getAttribute('stroke-linejoin'), '',
			'stroke-linejoin attribute not emptied when width zero' )

class RemoveStrokeDasharrayWhenStrokeWidthZero(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/stroke-nowidth.svg')
		self.assertEquals(doc.getElementsByTagNameNS(SVGNS, 'path')[0].getAttribute('stroke-dasharray'), '',
			'stroke-dasharray attribute not emptied when width zero' )

class RemoveStrokeDashoffsetWhenStrokeWidthZero(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/stroke-nowidth.svg')
		self.assertEquals(doc.getElementsByTagNameNS(SVGNS, 'path')[0].getAttribute('stroke-dashoffset'), '',
			'stroke-dashoffset attribute not emptied when width zero' )

class RemoveStrokeWhenStrokeNone(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/stroke-none.svg')
		self.assertEquals(doc.getElementsByTagNameNS(SVGNS, 'path')[0].getAttribute('stroke'), '',
			'stroke attribute not emptied when no stroke' )
			
class RemoveStrokeWidthWhenStrokeNone(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/stroke-none.svg')
		self.assertEquals(doc.getElementsByTagNameNS(SVGNS, 'path')[0].getAttribute('stroke-width'), '',
			'stroke-width attribute not emptied when no stroke' )

class RemoveStrokeOpacityWhenStrokeNone(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/stroke-none.svg')
		self.assertEquals(doc.getElementsByTagNameNS(SVGNS, 'path')[0].getAttribute('stroke-opacity'), '',
			'stroke-opacity attribute not emptied when no stroke' )

class RemoveStrokeLinecapWhenStrokeNone(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/stroke-none.svg')
		self.assertEquals(doc.getElementsByTagNameNS(SVGNS, 'path')[0].getAttribute('stroke-linecap'), '',
			'stroke-linecap attribute not emptied when no stroke' )

class RemoveStrokeLinejoinWhenStrokeNone(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/stroke-none.svg')
		self.assertEquals(doc.getElementsByTagNameNS(SVGNS, 'path')[0].getAttribute('stroke-linejoin'), '',
			'stroke-linejoin attribute not emptied when no stroke' )

class RemoveStrokeDasharrayWhenStrokeNone(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/stroke-none.svg')
		self.assertEquals(doc.getElementsByTagNameNS(SVGNS, 'path')[0].getAttribute('stroke-dasharray'), '',
			'stroke-dasharray attribute not emptied when no stroke' )

class RemoveStrokeDashoffsetWhenStrokeNone(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/stroke-none.svg')
		self.assertEquals(doc.getElementsByTagNameNS(SVGNS, 'path')[0].getAttribute('stroke-dashoffset'), '',
			'stroke-dashoffset attribute not emptied when no stroke' )

class RemoveFillRuleWhenFillNone(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/fill-none.svg')
		self.assertEquals(doc.getElementsByTagNameNS(SVGNS, 'path')[0].getAttribute('fill-rule'), '',
			'fill-rule attribute not emptied when no fill' )
			
class RemoveFillOpacityWhenFillNone(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/fill-none.svg')
		self.assertEquals(doc.getElementsByTagNameNS(SVGNS, 'path')[0].getAttribute('fill-opacity'), '',
			'fill-opacity attribute not emptied when no fill' )

class ConvertFillPropertyToAttr(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/fill-none.svg',
			scour.parse_args(['--disable-simplify-colors'])[0])
		self.assertEquals(doc.getElementsByTagNameNS(SVGNS, 'path')[1].getAttribute('fill'), 'black',
			'fill property not converted to XML attribute' )

class ConvertFillOpacityPropertyToAttr(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/fill-none.svg')
		self.assertEquals(doc.getElementsByTagNameNS(SVGNS, 'path')[1].getAttribute('fill-opacity'), '0.5',
			'fill-opacity property not converted to XML attribute' )

class ConvertFillRuleOpacityPropertyToAttr(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/fill-none.svg')
		self.assertEquals(doc.getElementsByTagNameNS(SVGNS, 'path')[1].getAttribute('fill-rule'), 'nonzero',
			'fill-rule property not converted to XML attribute' )
			
class CollapseSinglyReferencedGradients(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/collapse-gradients.svg')
		self.assertEquals(len(doc.getElementsByTagNameNS(SVGNS, 'linearGradient')), 0,
			'Singly-referenced linear gradient not collapsed' )

class InheritGradientUnitsUponCollapsing(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/collapse-gradients.svg')
		self.assertEquals(doc.getElementsByTagNameNS(SVGNS, 'radialGradient')[0].getAttribute('gradientUnits'), 
			'userSpaceOnUse',
			'gradientUnits not properly inherited when collapsing gradients' )

class OverrideGradientUnitsUponCollapsing(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/collapse-gradients-gradientUnits.svg')
		self.assertEquals(doc.getElementsByTagNameNS(SVGNS, 'radialGradient')[0].getAttribute('gradientUnits'), '',
			'gradientUnits not properly overrode when collapsing gradients' )

class DoNotCollapseMultiplyReferencedGradients(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/dont-collapse-gradients.svg')
		self.assertNotEquals(len(doc.getElementsByTagNameNS(SVGNS, 'linearGradient')), 0,
			'Multiply-referenced linear gradient collapsed' )

class RemoveTrailingZerosFromPath(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/path-truncate-zeros.svg')
		path = doc.getElementsByTagNameNS(SVGNS, 'path')[0].getAttribute('d')
		self.assertEquals(path[:4] == 'M300' and path[4] != '.', True,
			'Trailing zeros not removed from path data' )

class RemoveTrailingZerosFromPathAfterCalculation(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/path-truncate-zeros-calc.svg')
		path = doc.getElementsByTagNameNS(SVGNS, 'path')[0].getAttribute('d')
		self.assertEquals(path, 'M5.81,0h0.1',
			'Trailing zeros not removed from path data after calculation' )

class RemoveDelimiterBeforeNegativeCoordsInPath(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/path-truncate-zeros.svg')
		path = doc.getElementsByTagNameNS(SVGNS, 'path')[0].getAttribute('d')
		self.assertEquals(path[4], '-', 
			'Delimiters not removed before negative coordinates in path data' )
			
class UseScientificNotationToShortenCoordsInPath(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/path-use-scientific-notation.svg')
		path = doc.getElementsByTagNameNS(SVGNS, 'path')[0].getAttribute('d')
		self.assertEquals(path, 'M1E+4,0',
			'Not using scientific notation for path coord when representation is shorter')

class ConvertAbsoluteToRelativePathCommands(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/path-abs-to-rel.svg')
		path = svg_parser.parse(doc.getElementsByTagNameNS(SVGNS, 'path')[0].getAttribute('d'))
		self.assertEquals(path[1][0], 'v',
			'Absolute V command not converted to relative v command')
		self.assertEquals(path[1][1][0], -20.0,
			'Absolute V value not converted to relative v value')

class RoundPathData(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/path-precision.svg')
		path = svg_parser.parse(doc.getElementsByTagNameNS(SVGNS, 'path')[0].getAttribute('d'))
		self.assertEquals(path[0][1][0][0], 100.0,
			'Not rounding down' )
		self.assertEquals(path[0][1][0][1], 100.0,
			'Not rounding up' )
			
class LimitPrecisionInPathData(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/path-precision.svg')
		path = svg_parser.parse(doc.getElementsByTagNameNS(SVGNS, 'path')[0].getAttribute('d'))
		self.assertEquals(path[1][1][0], 100.01,
			'Not correctly limiting precision on path data' )

class RemoveEmptyLineSegmentsFromPath(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/path-line-optimize.svg')
		path = svg_parser.parse(doc.getElementsByTagNameNS(SVGNS, 'path')[0].getAttribute('d'))
		self.assertEquals(path[4][0], 'z',
			'Did not remove an empty line segment from path' )

class ChangeLineToHorizontalLineSegmentInPath(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/path-line-optimize.svg')
		path = svg_parser.parse(doc.getElementsByTagNameNS(SVGNS, 'path')[0].getAttribute('d'))
		self.assertEquals(path[1][0], 'h',
			'Did not change line to horizontal line segment in path' )
		self.assertEquals(path[1][1][0], 200.0,
			'Did not calculate horizontal line segment in path correctly' )

class ChangeLineToVerticalLineSegmentInPath(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/path-line-optimize.svg')
		path = svg_parser.parse(doc.getElementsByTagNameNS(SVGNS, 'path')[0].getAttribute('d'))
		self.assertEquals(path[2][0], 'v',
			'Did not change line to vertical line segment in path' )
		self.assertEquals(path[2][1][0], 100.0,
			'Did not calculate vertical line segment in path correctly' )

class ChangeBezierToShorthandInPath(unittest.TestCase):
	def runTest(self):
		path = scour.scourXmlFile('unittests/path-bez-optimize.svg').getElementsByTagNameNS(SVGNS, 'path')[0]
		self.assertEquals(path.getAttribute('d'), 'm10,100c50-50,50,50,100,0s50,50,100,0',
			'Did not change bezier curves into shorthand curve segments in path')

class ChangeQuadToShorthandInPath(unittest.TestCase):
	def runTest(self):
		path = scour.scourXmlFile('unittests/path-quad-optimize.svg').getElementsByTagNameNS(SVGNS, 'path')[0]
		self.assertEquals(path.getAttribute('d'), 'm10,100q50-50,100,0t100,0',
			'Did not change quadratic curves into shorthand curve segments in path')

class HandleNonAsciiUtf8(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/utf8.svg')
		desc = unicode(doc.getElementsByTagNameNS(SVGNS, 'desc')[0].firstChild.wholeText).strip()
		self.assertEquals( desc, u'ú',
			'Did not handle non-ASCII characters' )

class HandleSciNoInPathData(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/path-sn.svg')
		self.assertEquals( len(doc.getElementsByTagNameNS(SVGNS, 'path')), 1,
			'Did not handle scientific notation in path data' )
			
class TranslateRGBIntoHex(unittest.TestCase):
	def runTest(self):
		elem = scour.scourXmlFile('unittests/color-formats.svg').getElementsByTagNameNS(SVGNS, 'rect')[0]
		self.assertEquals( elem.getAttribute('fill'), '#0F1011',
			'Not converting rgb into hex')

class TranslateRGBPctIntoHex(unittest.TestCase):
	def runTest(self):
		elem = scour.scourXmlFile('unittests/color-formats.svg').getElementsByTagNameNS(SVGNS, 'stop')[0]
		self.assertEquals( elem.getAttribute('stop-color'), '#7F0000',
			'Not converting rgb pct into hex')

class TranslateColorNamesIntoHex(unittest.TestCase):
	def runTest(self):
		elem = scour.scourXmlFile('unittests/color-formats.svg').getElementsByTagNameNS(SVGNS, 'rect')[0]
		self.assertEquals( elem.getAttribute('stroke'), '#A9A9A9',
			'Not converting standard color names into hex')

class TranslateExtendedColorNamesIntoHex(unittest.TestCase):
	def runTest(self):
		elem = scour.scourXmlFile('unittests/color-formats.svg').getElementsByTagNameNS(SVGNS, 'solidColor')[0]
		self.assertEquals( elem.getAttribute('solid-color'), '#FAFAD2',
			'Not converting extended color names into hex')

class TranslateLongHexColorIntoShortHex(unittest.TestCase):
	def runTest(self):
		elem = scour.scourXmlFile('unittests/color-formats.svg').getElementsByTagNameNS(SVGNS, 'ellipse')[0]
		self.assertEquals( elem.getAttribute('fill'), '#FFF',
			'Not converting long hex color into short hex')

class DoNotConvertShortColorNames(unittest.TestCase):
	def runTest(self):
		elem = scour.scourXmlFile('unittests/dont-convert-short-color-names.svg').getElementsByTagNameNS(SVGNS, 'rect')[0]
		self.assertEquals( 'red', elem.getAttribute('fill'),
			'Converted short color name to longer hex string')

class AllowQuotEntitiesInUrl(unittest.TestCase):
	def runTest(self):
		grads = scour.scourXmlFile('unittests/quot-in-url.svg').getElementsByTagNameNS(SVGNS, 'linearGradient')
		self.assertEquals( len(grads), 1,
			'Removed referenced gradient when &quot; was in the url')
		
class RemoveFontStylesFromNonTextShapes(unittest.TestCase):
	def runTest(self):
		r = scour.scourXmlFile('unittests/font-styles.svg').getElementsByTagNameNS(SVGNS, 'rect')[0]
		self.assertEquals( r.getAttribute('font-size'), '',
			'font-size not removed from rect' )
			
class CollapseConsecutiveHLinesSegments(unittest.TestCase):
	def runTest(self):
		p = scour.scourXmlFile('unittests/consecutive-hlines.svg').getElementsByTagNameNS(SVGNS, 'path')[0]
		self.assertEquals( p.getAttribute('d'), 'M100,100h200v100h-200z',
			'Did not collapse consecutive hlines segments')

class CollapseConsecutiveHLinesCoords(unittest.TestCase):
	def runTest(self):
		p = scour.scourXmlFile('unittests/consecutive-hlines.svg').getElementsByTagNameNS(SVGNS, 'path')[1]
		self.assertEquals( p.getAttribute('d'), 'M100,300h200v100h-200z',
			'Did not collapse consecutive hlines coordinates')
			
class DoNotCollapseConsecutiveHLinesSegsWithDifferingSigns(unittest.TestCase):
	def runTest(self):
		p = scour.scourXmlFile('unittests/consecutive-hlines.svg').getElementsByTagNameNS(SVGNS, 'path')[2]
		self.assertEquals( p.getAttribute('d'), 'M100,500h300-100v100h-200z',
			'Collapsed consecutive hlines segments with differing signs')

class ConvertStraightCurvesToLines(unittest.TestCase):
	def runTest(self):
		p = scour.scourXmlFile('unittests/straight-curve.svg').getElementsByTagNameNS(SVGNS, 'path')[0]
		self.assertEquals(p.getAttribute('d'), 'M10,10l40,40,40-40z', 
			'Did not convert straight curves into lines')
			
class RemoveUnnecessaryPolgonEndPoint(unittest.TestCase):
	def runTest(self):
		p = scour.scourXmlFile('unittests/polygon.svg').getElementsByTagNameNS(SVGNS, 'polygon')[0]
		self.assertEquals(p.getAttribute('points'), '50,50,150,50,150,150,50,150',
			'Unnecessary polygon end point not removed' )

class DoNotRemovePolgonLastPoint(unittest.TestCase):
	def runTest(self):
		p = scour.scourXmlFile('unittests/polygon.svg').getElementsByTagNameNS(SVGNS, 'polygon')[1]
		self.assertEquals(p.getAttribute('points'), '200,50,300,50,300,150,200,150',
			'Last point of polygon removed' )
			
class ScourPolygonCoordinates(unittest.TestCase):
	def runTest(self):
		p = scour.scourXmlFile('unittests/polygon-coord.svg').getElementsByTagNameNS(SVGNS, 'polygon')[0]
		self.assertEquals(p.getAttribute('points'), '1E+4-50',
			'Polygon coordinates not scoured')

class ScourPolylineCoordinates(unittest.TestCase):
	def runTest(self):
		p = scour.scourXmlFile('unittests/polyline-coord.svg').getElementsByTagNameNS(SVGNS, 'polyline')[0]
		self.assertEquals(p.getAttribute('points'), '1E+4-50',
			'Polyline coordinates not scoured')

class DoNotRemoveGroupsWithIDsInDefs(unittest.TestCase):
	def runTest(self):
		f = scour.scourXmlFile('unittests/important-groups-in-defs.svg')
		self.assertEquals(len(f.getElementsByTagNameNS(SVGNS, 'linearGradient')), 1,
			'Group in defs with id\'ed element removed')

class AlwaysKeepClosePathSegments(unittest.TestCase):
	def runTest(self):
		p = scour.scourXmlFile('unittests/path-with-closepath.svg').getElementsByTagNameNS(SVGNS, 'path')[0]
		self.assertEquals(p.getAttribute('d'), 'M10,10h100v100h-100z',
			'Path with closepath not preserved')

class RemoveDuplicateLinearGradients(unittest.TestCase):
	def runTest(self):
		svgdoc = scour.scourXmlFile('unittests/remove-duplicate-gradients.svg')
		lingrads = svgdoc.getElementsByTagNameNS(SVGNS, 'linearGradient')
		self.assertEquals(1, lingrads.length,
			'Duplicate linear gradient not removed')
		
class RereferenceForLinearGradient(unittest.TestCase):
	def runTest(self):
		svgdoc = scour.scourXmlFile('unittests/remove-duplicate-gradients.svg')
		rects = svgdoc.getElementsByTagNameNS(SVGNS, 'rect')
		self.assertEquals(rects[0].getAttribute('fill'), rects[1].getAttribute('stroke'),
			'Rect not changed after removing duplicate linear gradient')
		self.assertEquals(rects[0].getAttribute('fill'), rects[4].getAttribute('fill'),
			'Rect not changed after removing duplicate linear gradient')
			
class RemoveDuplicateRadialGradients(unittest.TestCase):
	def runTest(self):
		svgdoc = scour.scourXmlFile('unittests/remove-duplicate-gradients.svg')
		radgrads = svgdoc.getElementsByTagNameNS(SVGNS, 'radialGradient')
		self.assertEquals(1, radgrads.length,
			'Duplicate radial gradient not removed')
			
class RereferenceForRadialGradient(unittest.TestCase):
	def runTest(self):
		svgdoc = scour.scourXmlFile('unittests/remove-duplicate-gradients.svg')
		rects = svgdoc.getElementsByTagNameNS(SVGNS, 'rect')
		self.assertEquals(rects[2].getAttribute('stroke'), rects[3].getAttribute('fill'),
			'Rect not changed after removing duplicate radial gradient')

class CollapseSamePathPoints(unittest.TestCase):
	def runTest(self):
		p = scour.scourXmlFile('unittests/collapse-same-path-points.svg').getElementsByTagNameNS(SVGNS, 'path')[0];
		self.assertEquals(p.getAttribute('d'), "M100,100l100.12,100.12z",
			'Did not collapse same path points')

class ScourUnitlessLengths(unittest.TestCase):
	def runTest(self):
		r = scour.scourXmlFile('unittests/scour-lengths.svg').getElementsByTagNameNS(SVGNS, 'rect')[0];
		self.assertEquals(r.getAttribute('x'), '123.46',
			'Did not scour x attribute unitless number')
		self.assertEquals(r.getAttribute('y'), '123',
			'Did not scour y attribute unitless number')
		self.assertEquals(r.getAttribute('width'), '300',
			'Did not scour width attribute unitless number')
		self.assertEquals(r.getAttribute('height'), '100',
			'Did not scour height attribute unitless number')

class ScourLengthsWithUnits(unittest.TestCase):
	def runTest(self):
		r = scour.scourXmlFile('unittests/scour-lengths.svg').getElementsByTagNameNS(SVGNS, 'rect')[1];
		self.assertEquals(r.getAttribute('x'), '123.46px',
			'Did not scour x attribute with unit')
		self.assertEquals(r.getAttribute('y'), '35ex',
			'Did not scour y attribute with unit')
		self.assertEquals(r.getAttribute('width'), '300pt',
			'Did not scour width attribute with unit')
		self.assertEquals(r.getAttribute('height'), '50%',
			'Did not scour height attribute with unit')

class RemoveRedundantSvgNamespaceDeclaration(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/redundant-svg-namespace.svg').documentElement
		self.assertNotEquals( doc.getAttribute('xmlns:svg'), 'http://www.w3.org/2000/svg',
			'Redundant svg namespace declaration not removed')

class RemoveRedundantSvgNamespacePrefix(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/redundant-svg-namespace.svg').documentElement
		r = doc.getElementsByTagNameNS(SVGNS, 'rect')[1]
		self.assertEquals( r.tagName, 'rect',
			'Redundant svg: prefix not removed')


class RemoveDefaultGradX1Value(unittest.TestCase):
	def runTest(self):
		g = scour.scourXmlFile('unittests/gradient-default-attrs.svg').getElementsByTagNameNS(SVGNS, 'linearGradient')[0]
		self.assertEquals( g.getAttribute('x1'), '',
			'x1="0" not removed')

class RemoveDefaultGradY1Value(unittest.TestCase):
	def runTest(self):
		g = scour.scourXmlFile('unittests/gradient-default-attrs.svg').getElementsByTagNameNS(SVGNS, 'linearGradient')[0]
		self.assertEquals( g.getAttribute('y1'), '',
			'y1="0" not removed')

class RemoveDefaultGradX2Value(unittest.TestCase):
	def runTest(self):
		g = scour.scourXmlFile('unittests/gradient-default-attrs.svg').getElementsByTagNameNS(SVGNS, 'linearGradient')[0]
		self.assertEquals( g.getAttribute('x2'), '',
			'x2="100%" not removed')

class RemoveDefaultGradY2Value(unittest.TestCase):
	def runTest(self):
		g = scour.scourXmlFile('unittests/gradient-default-attrs.svg').getElementsByTagNameNS(SVGNS, 'linearGradient')[0]
		self.assertEquals( g.getAttribute('y2'), '',
			'y2="0" not removed')

class RemoveDefaultGradGradientUnitsValue(unittest.TestCase):
	def runTest(self):
		g = scour.scourXmlFile('unittests/gradient-default-attrs.svg').getElementsByTagNameNS(SVGNS, 'linearGradient')[0]
		self.assertEquals( g.getAttribute('gradientUnits'), '',
			'gradientUnits="objectBoundingBox" not removed')

class RemoveDefaultGradSpreadMethodValue(unittest.TestCase):
	def runTest(self):
		g = scour.scourXmlFile('unittests/gradient-default-attrs.svg').getElementsByTagNameNS(SVGNS, 'linearGradient')[0]
		self.assertEquals( g.getAttribute('spreadMethod'), '',
			'spreadMethod="pad" not removed')

class RemoveDefaultGradCXValue(unittest.TestCase):
	def runTest(self):
		g = scour.scourXmlFile('unittests/gradient-default-attrs.svg').getElementsByTagNameNS(SVGNS, 'radialGradient')[0]
		self.assertEquals( g.getAttribute('cx'), '',
			'cx="50%" not removed')

class RemoveDefaultGradCYValue(unittest.TestCase):
	def runTest(self):
		g = scour.scourXmlFile('unittests/gradient-default-attrs.svg').getElementsByTagNameNS(SVGNS, 'radialGradient')[0]
		self.assertEquals( g.getAttribute('cy'), '',
			'cy="50%" not removed')

class RemoveDefaultGradRValue(unittest.TestCase):
	def runTest(self):
		g = scour.scourXmlFile('unittests/gradient-default-attrs.svg').getElementsByTagNameNS(SVGNS, 'radialGradient')[0]
		self.assertEquals( g.getAttribute('r'), '',
			'r="50%" not removed')

class RemoveDefaultGradFXValue(unittest.TestCase):
	def runTest(self):
		g = scour.scourXmlFile('unittests/gradient-default-attrs.svg').getElementsByTagNameNS(SVGNS, 'radialGradient')[0]
		self.assertEquals( g.getAttribute('fx'), '',
			'fx matching cx not removed')

class RemoveDefaultGradFYValue(unittest.TestCase):
	def runTest(self):
		g = scour.scourXmlFile('unittests/gradient-default-attrs.svg').getElementsByTagNameNS(SVGNS, 'radialGradient')[0]
		self.assertEquals( g.getAttribute('fy'), '',
			'fy matching cy not removed')

class CDATAInXml(unittest.TestCase):
	def runTest(self):
		self.assertEquals( scour.scourString(open('unittests/cdata.svg').read()), 
			'''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg xmlns="http://www.w3.org/2000/svg">
 <script type="application/ecmascript"><![CDATA[
  	alert('pb&j');
 ]]></script>
</svg>''',
			'Improperly serialized the cdata unit tests')

class WellFormedXMLLesserThanInAttrValue(unittest.TestCase):
	def runTest(self):
		wellformed = scour.scourString(open('unittests/xml-well-formed.svg').read())
		self.assert_( wellformed.find('unicode="&lt;"') != -1,
			"Improperly serialized &lt; in attribute value")

class WellFormedXMLAmpersandInAttrValue(unittest.TestCase):
	def runTest(self):
		wellformed = scour.scourString(open('unittests/xml-well-formed.svg').read())
		self.assert_( wellformed.find('unicode="&amp;"') != -1,
			'Improperly serialized &amp; in attribute value' )

class WellFormedXMLLesserThanInTextContent(unittest.TestCase):
	def runTest(self):
		wellformed = scour.scourString(open('unittests/xml-well-formed.svg').read())
		self.assert_( wellformed.find('<title>2 &lt; 5</title>') != -1,
			'Improperly serialized &lt; in text content')

class WellFormedXMLAmpersandInTextContent(unittest.TestCase):
	def runTest(self):
		wellformed = scour.scourString(open('unittests/xml-well-formed.svg').read())
		self.assert_( wellformed.find('<desc>Peanut Butter &amp; Jelly</desc>') != -1,
			'Improperly serialized &amp; in text content')

class NamespaceDeclPrefixesInXML(unittest.TestCase):
	def runTest(self):
		xmlstring = scour.scourString(open('unittests/xml-ns-decl.svg').read())
		self.assert_( xmlstring.find('xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"') != -1,
			'Improperly serialized namespace prefix declarations')
# TODO; write a test for embedding rasters
# TODO: write a test for --disable-embed-rasters
# TODO: write tests for --keep-editor-data
# TODO: write tests for --strip-xml-prolog

if __name__ == '__main__':
    unittest.main()
