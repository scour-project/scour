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

import unittest
import xml.dom.minidom
from svg_regex import svg_parser
from scour import scourXmlFile, scourString, parse_args, makeWellFormed

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
	enable_viewboxing = False
	shorten_ids = False
	strip_comments = False
	remove_metadata = False
	group_create = False

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

class DoNotRemoveChainedRefsInDefs(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/refs-in-defs.svg')
		g = doc.getElementsByTagNameNS(SVGNS, 'g')[0]
		self.assertEquals( g.childNodes.length >= 2, True,
			'Chained references not honored in defs' )

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
		self.assertEquals(doc.getElementsByTagNameNS(SVGNS, 'path')[1].getAttribute('fill-opacity'), '.5',
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
		self.assertEquals(path[:4] == 'm300' and path[4] != '.', True,
			'Trailing zeros not removed from path data' )

class RemoveTrailingZerosFromPathAfterCalculation(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/path-truncate-zeros-calc.svg')
		path = doc.getElementsByTagNameNS(SVGNS, 'path')[0].getAttribute('d')
		self.assertEquals(path, 'm5.81 0h0.1',
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
		self.assertEquals(path, 'm1e4 0',
			'Not using scientific notation for path coord when representation is shorter')

class ConvertAbsoluteToRelativePathCommands(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/path-abs-to-rel.svg')
		path = svg_parser.parse(doc.getElementsByTagNameNS(SVGNS, 'path')[0].getAttribute('d'))
		self.assertEquals(path[1][0], 'v',
			'Absolute V command not converted to relative v command')
		self.assertEquals(float(path[1][1][0]), -20.0,
			'Absolute V value not converted to relative v value')

class RoundPathData(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/path-precision.svg')
		path = svg_parser.parse(doc.getElementsByTagNameNS(SVGNS, 'path')[0].getAttribute('d'))
		self.assertEquals(float(path[0][1][0]), 100.0,
			'Not rounding down' )
		self.assertEquals(float(path[0][1][1]), 100.0,
			'Not rounding up' )
			
class LimitPrecisionInPathData(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/path-precision.svg')
		path = svg_parser.parse(doc.getElementsByTagNameNS(SVGNS, 'path')[0].getAttribute('d'))
		self.assertEquals(float(path[1][1][0]), 100.01,
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
		self.assertEquals(float(path[1][1][0]), 200.0,
			'Did not calculate horizontal line segment in path correctly' )

class ChangeLineToVerticalLineSegmentInPath(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/path-line-optimize.svg')
		path = svg_parser.parse(doc.getElementsByTagNameNS(SVGNS, 'path')[0].getAttribute('d'))
		self.assertEquals(path[2][0], 'v',
			'Did not change line to vertical line segment in path' )
		self.assertEquals(float(path[2][1][0]), 100.0,
			'Did not calculate vertical line segment in path correctly' )

class ChangeBezierToShorthandInPath(unittest.TestCase):
	def runTest(self):
		path = scour.scourXmlFile('unittests/path-bez-optimize.svg').getElementsByTagNameNS(SVGNS, 'path')[0]
		self.assertEquals(path.getAttribute('d'), 'm10 100c50-50 50 50 100 0s50 50 100 0',
			'Did not change bezier curves into shorthand curve segments in path')

class ChangeQuadToShorthandInPath(unittest.TestCase):
	def runTest(self):
		path = scour.scourXmlFile('unittests/path-quad-optimize.svg').getElementsByTagNameNS(SVGNS, 'path')[0]
		self.assertEquals(path.getAttribute('d'), 'm10 100q50-50 100 0t100 0',
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
		self.assertEquals( elem.getAttribute('fill'), '#0f1011',
			'Not converting rgb into hex')

class TranslateRGBPctIntoHex(unittest.TestCase):
	def runTest(self):
		elem = scour.scourXmlFile('unittests/color-formats.svg').getElementsByTagNameNS(SVGNS, 'stop')[0]
		self.assertEquals( elem.getAttribute('stop-color'), '#7f0000',
			'Not converting rgb pct into hex')

class TranslateColorNamesIntoHex(unittest.TestCase):
	def runTest(self):
		elem = scour.scourXmlFile('unittests/color-formats.svg').getElementsByTagNameNS(SVGNS, 'rect')[0]
		self.assertEquals( elem.getAttribute('stroke'), '#a9a9a9',
			'Not converting standard color names into hex')

class TranslateExtendedColorNamesIntoHex(unittest.TestCase):
	def runTest(self):
		elem = scour.scourXmlFile('unittests/color-formats.svg').getElementsByTagNameNS(SVGNS, 'solidColor')[0]
		self.assertEquals( elem.getAttribute('solid-color'), '#fafad2',
			'Not converting extended color names into hex')

class TranslateLongHexColorIntoShortHex(unittest.TestCase):
	def runTest(self):
		elem = scour.scourXmlFile('unittests/color-formats.svg').getElementsByTagNameNS(SVGNS, 'ellipse')[0]
		self.assertEquals( elem.getAttribute('fill'), '#fff',
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
		self.assertEquals( p.getAttribute('d'), 'm100 100h200v100h-200z',
			'Did not collapse consecutive hlines segments')

class CollapseConsecutiveHLinesCoords(unittest.TestCase):
	def runTest(self):
		p = scour.scourXmlFile('unittests/consecutive-hlines.svg').getElementsByTagNameNS(SVGNS, 'path')[1]
		self.assertEquals( p.getAttribute('d'), 'm100 300h200v100h-200z',
			'Did not collapse consecutive hlines coordinates')
			
class DoNotCollapseConsecutiveHLinesSegsWithDifferingSigns(unittest.TestCase):
	def runTest(self):
		p = scour.scourXmlFile('unittests/consecutive-hlines.svg').getElementsByTagNameNS(SVGNS, 'path')[2]
		self.assertEquals( p.getAttribute('d'), 'm100 500h300-100v100h-200z',
			'Collapsed consecutive hlines segments with differing signs')

class ConvertStraightCurvesToLines(unittest.TestCase):
	def runTest(self):
		p = scour.scourXmlFile('unittests/straight-curve.svg').getElementsByTagNameNS(SVGNS, 'path')[0]
		self.assertEquals(p.getAttribute('d'), 'm10 10l40 40 40-40z', 
			'Did not convert straight curves into lines')
			
class RemoveUnnecessaryPolygonEndPoint(unittest.TestCase):
	def runTest(self):
		p = scour.scourXmlFile('unittests/polygon.svg').getElementsByTagNameNS(SVGNS, 'polygon')[0]
		self.assertEquals(p.getAttribute('points'), '50 50 150 50 150 150 50 150',
			'Unnecessary polygon end point not removed' )

class DoNotRemovePolgonLastPoint(unittest.TestCase):
	def runTest(self):
		p = scour.scourXmlFile('unittests/polygon.svg').getElementsByTagNameNS(SVGNS, 'polygon')[1]
		self.assertEquals(p.getAttribute('points'), '200 50 300 50 300 150 200 150',
			'Last point of polygon removed' )
			
class ScourPolygonCoordsSciNo(unittest.TestCase):
	def runTest(self):
		p = scour.scourXmlFile('unittests/polygon-coord.svg').getElementsByTagNameNS(SVGNS, 'polygon')[0]
		self.assertEquals(p.getAttribute('points'), '1e4 50',
			'Polygon coordinates not scoured')

class ScourPolylineCoordsSciNo(unittest.TestCase):
	def runTest(self):
		p = scour.scourXmlFile('unittests/polyline-coord.svg').getElementsByTagNameNS(SVGNS, 'polyline')[0]
		self.assertEquals(p.getAttribute('points'), '1e4 50',
			'Polyline coordinates not scoured')

class ScourPolygonNegativeCoords(unittest.TestCase):
	def runTest(self):
		p = scour.scourXmlFile('unittests/polygon-coord-neg.svg').getElementsByTagNameNS(SVGNS, 'polygon')[0]
		#  points="100,-100,100-100,100-100-100,-100-100,200" />
		self.assertEquals(p.getAttribute('points'), '100 -100 100 -100 100 -100 -100 -100 -100 200',
			'Negative polygon coordinates not properly parsed')

class ScourPolylineNegativeCoords(unittest.TestCase):
	def runTest(self):
		p = scour.scourXmlFile('unittests/polyline-coord-neg.svg').getElementsByTagNameNS(SVGNS, 'polyline')[0]
		self.assertEquals(p.getAttribute('points'), '100 -100 100 -100 100 -100 -100 -100 -100 200',
			'Negative polyline coordinates not properly parsed')

class DoNotRemoveGroupsWithIDsInDefs(unittest.TestCase):
	def runTest(self):
		f = scour.scourXmlFile('unittests/important-groups-in-defs.svg')
		self.assertEquals(len(f.getElementsByTagNameNS(SVGNS, 'linearGradient')), 1,
			'Group in defs with id\'ed element removed')

class AlwaysKeepClosePathSegments(unittest.TestCase):
	def runTest(self):
		p = scour.scourXmlFile('unittests/path-with-closepath.svg').getElementsByTagNameNS(SVGNS, 'path')[0]
		self.assertEquals(p.getAttribute('d'), 'm10 10h100v100h-100z',
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
		self.assertEquals(p.getAttribute('d'), "m100 100l100.12 100.12z",
			'Did not collapse same path points')

class ScourUnitlessLengths(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/scour-lengths.svg')
		r = doc.getElementsByTagNameNS(SVGNS, 'rect')[0];
		svg = doc.documentElement
		self.assertEquals(svg.getAttribute('x'), '1',
			'Did not scour x attribute of svg element with unitless number')
		self.assertEquals(r.getAttribute('x'), '123.46',
			'Did not scour x attribute of rect with unitless number')
		self.assertEquals(r.getAttribute('y'), '123',
			'Did not scour y attribute of rect unitless number')
		self.assertEquals(r.getAttribute('width'), '300',
			'Did not scour width attribute of rect with unitless number')
		self.assertEquals(r.getAttribute('height'), '100',
			'Did not scour height attribute of rect with unitless number')

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
		lines = scour.scourString(open('unittests/cdata.svg').read()).splitlines()
		self.assertEquals( lines[3], 
			"  	alert('pb&j');",
			'CDATA did not come out correctly')

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

class WellFormedXMLNamespacePrefix(unittest.TestCase):
	def runTest(self):
		wellformed = scour.scourString(open('unittests/xml-well-formed.svg').read())
		self.assert_( wellformed.find('xmlns:foo=') != -1,
			'Improperly serialized namespace prefix declarations')

class NamespaceDeclPrefixesInXMLWhenNotInDefaultNamespace(unittest.TestCase):
	def runTest(self):
		xmlstring = scour.scourString(open('unittests/xml-ns-decl.svg').read())
		self.assert_( xmlstring.find('xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"') != -1,
			'Improperly serialized namespace prefix declarations when not in default namespace')

class MoveSVGElementsToDefaultNamespace(unittest.TestCase):
	def runTest(self):
		xmlstring = scour.scourString(open('unittests/xml-ns-decl.svg').read())
		self.assert_( xmlstring.find('<rect ') != -1,
			'Did not bring SVG elements into the default namespace')

class MoveCommonAttributesToParent(unittest.TestCase):
	def runTest(self):
		g = scour.scourXmlFile('unittests/move-common-attributes-to-parent.svg').getElementsByTagNameNS(SVGNS, 'g')[0]
		self.assertEquals( g.getAttribute('fill'), '#0F0',
			'Did not move common fill attribute to parent group')

class RemoveCommonAttributesFromChild(unittest.TestCase):
	def runTest(self):
		r = scour.scourXmlFile('unittests/move-common-attributes-to-parent.svg').getElementsByTagNameNS(SVGNS, 'rect')[0]
		self.assertNotEquals( r.getAttribute('fill'), '#0F0',
			'Did not remove common fill attribute from child')
			
class DontRemoveCommonAttributesIfParentHasTextNodes(unittest.TestCase):
	def runTest(self):
		text = scour.scourXmlFile('unittests/move-common-attributes-to-parent.svg').getElementsByTagNameNS(SVGNS, 'text')[0]
		self.assertNotEquals( text.getAttribute('font-style'), 'italic',
			'Removed common attributes when parent contained text elements')

class PropagateCommonAttributesUp(unittest.TestCase):
	def runTest(self):
		g = scour.scourXmlFile('unittests/move-common-attributes-to-grandparent.svg').getElementsByTagNameNS(SVGNS, 'g')[0]
		self.assertEquals( g.getAttribute('fill'), '#0F0',
			'Did not move common fill attribute to grandparent')
			
class PathEllipticalArcParsingCommaWsp(unittest.TestCase):
	def runTest(self):
		p = scour.scourXmlFile('unittests/path-elliptical-arc-parsing.svg').getElementsByTagNameNS(SVGNS, 'path')[0]
		self.assertEquals( p.getAttribute('d'), 'm100 100a100 100 0 1 1 -50 100z',
			'Did not parse elliptical arc command properly')

class RemoveUnusedAttributesOnParent(unittest.TestCase):
	def runTest(self):
		g = scour.scourXmlFile('unittests/remove-unused-attributes-on-parent.svg').getElementsByTagNameNS(SVGNS, 'g')[0]
		self.assertNotEquals( g.getAttribute('stroke'), '#000',
			'Unused attributes on group not removed')

class DoNotRemoveCommonAttributesOnParentIfAtLeastOneUsed(unittest.TestCase):
	def runTest(self):
		g = scour.scourXmlFile('unittests/remove-unused-attributes-on-parent.svg').getElementsByTagNameNS(SVGNS, 'g')[0]
		self.assertEquals( g.getAttribute('fill'), '#0F0',
			'Used attributes on group were removed')

class DoNotRemoveGradientsWhenReferencedInStyleCss(unittest.TestCase):
	def runTest(self):
		grads = scour.scourXmlFile('unittests/css-reference.svg').getElementsByTagNameNS(SVGNS, 'linearGradient')
		self.assertEquals( grads.length, 2,
			'Gradients removed when referenced in CSS')

class DoNotPrettyPrintWhenWhitespacePreserved(unittest.TestCase):
	def runTest(self):
		s = scour.scourString(open('unittests/whitespace-important.svg').read()).splitlines()
		c = '''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg xmlns="http://www.w3.org/2000/svg">
 <text xml:space="preserve">This is some <tspan font-style="italic">messed-up</tspan> markup</text>
</svg>
'''.splitlines()
		for i in range(4):
			self.assertEquals( s[i], c[i],
			'Whitespace not preserved for line ' + str(i))

class DoNotPrettyPrintWhenNestedWhitespacePreserved(unittest.TestCase):
	def runTest(self):
		s = scour.scourString(open('unittests/whitespace-nested.svg').read()).splitlines()
		c = '''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg xmlns="http://www.w3.org/2000/svg">
 <text xml:space="preserve"><tspan font-style="italic">Use <tspan font-style="bold">bold</tspan> text</tspan></text>
</svg>
'''.splitlines()
		for i in range(4):
			self.assertEquals( s[i], c[i], 
				'Whitespace not preserved when nested for line ' + str(i))
	
class GetAttrPrefixRight(unittest.TestCase):
	def runTest(self):
		grad = scour.scourXmlFile('unittests/xml-namespace-attrs.svg').getElementsByTagNameNS(SVGNS, 'linearGradient')[1]
		self.assertEquals( grad.getAttributeNS('http://www.w3.org/1999/xlink', 'href'), '#linearGradient841',
			'Did not get xlink:href prefix right')

class EnsurePreserveWhitespaceOnNonTextElements(unittest.TestCase):
	def runTest(self):
		s = scour.scourString(open('unittests/no-collapse-lines.svg').read())
		self.assertEquals( len(s.splitlines()), 6,
			'Did not properly preserve whitespace on elements even if they were not textual')

class HandleEmptyStyleElement(unittest.TestCase):
	def runTest(self):
		try:
			styles = scour.scourXmlFile('unittests/empty-style.svg').getElementsByTagNameNS(SVGNS, 'style')
			fail = len(styles) != 1
		except AttributeError:
			fail = True
		self.assertEquals( fail, False,
			'Could not handle an empty style element')

class EnsureLineEndings(unittest.TestCase):
	def runTest(self):
		s = scour.scourString(open('unittests/whitespace-important.svg').read())
		self.assertEquals( len(s.splitlines()), 4, 
			'Did not output line ending character correctly')

class XmlEntities(unittest.TestCase):
	def runTest(self):
		self.assertEquals( scour.makeWellFormed('<>&"\''), '&lt;&gt;&amp;&quot;&apos;',
			'Incorrectly translated XML entities')

class DoNotStripCommentsOutsideOfRoot(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/comments.svg')
		self.assertEquals( doc.childNodes.length, 4, 
			'Did not include all comment children outside of root')
		self.assertEquals( doc.childNodes[0].nodeType, 8, 'First node not a comment')
		self.assertEquals( doc.childNodes[1].nodeType, 8, 'Second node not a comment')
		self.assertEquals( doc.childNodes[3].nodeType, 8, 'Fourth node not a comment')

class DoNotStripDoctype(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/doctype.svg')
		self.assertEquals( doc.childNodes.length, 3, 
			'Did not include the DOCROOT')
		self.assertEquals( doc.childNodes[0].nodeType, 8, 'First node not a comment')
		self.assertEquals( doc.childNodes[1].nodeType, 10, 'Second node not a doctype')
		self.assertEquals( doc.childNodes[2].nodeType, 1, 'Third node not the root node')

class PathImplicitLineWithMoveCommands(unittest.TestCase):
	def runTest(self):
		path = scour.scourXmlFile('unittests/path-implicit-line.svg').getElementsByTagNameNS(SVGNS, 'path')[0]
		self.assertEquals( path.getAttribute('d'), "m100 100v100m200-100h-200m200 100v-100",
			"Implicit line segments after move not preserved")

class RemoveMetadataOption(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/full-metadata.svg',
			scour.parse_args(['--remove-metadata'])[0])
		self.assertEquals(doc.childNodes.length, 1,
			'Did not remove <metadata> tag with --remove-metadata')

class EnableCommentStrippingOption(unittest.TestCase):
	def runTest(self):
		docStr = file('unittests/comment-beside-xml-decl.svg').read()
		docStr = scour.scourString(docStr,
			scour.parse_args(['--enable-comment-stripping'])[0])
		self.assertEquals(docStr.find('<!--'), -1,
			'Did not remove document-level comment with --enable-comment-stripping')

class StripXmlPrologOption(unittest.TestCase):
	def runTest(self):
		docStr = file('unittests/comment-beside-xml-decl.svg').read()
		docStr = scour.scourString(docStr,
			scour.parse_args(['--strip-xml-prolog'])[0])
		self.assertEquals(docStr.find('<?xml'), -1,
			'Did not remove <?xml?> with --strip-xml-prolog')

class ShortenIDsOption(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/shorten-ids.svg',
			scour.parse_args(['--shorten-ids'])[0])
		gradientTag = doc.getElementsByTagName('linearGradient')[0]
		self.assertEquals(gradientTag.getAttribute('id'), 'a',
			"Did not shorten a linear gradient's ID with --shorten-ids")
		rectTag = doc.getElementsByTagName('rect')[0]
		self.assertEquals(rectTag.getAttribute('fill'), 'url(#a)',
			'Did not update reference to shortened ID')

class MustKeepGInSwitch(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/groups-in-switch.svg')
		self.assertEquals(doc.getElementsByTagName('g').length, 1,
			'Erroneously removed a <g> in a <switch>')

class MustKeepGInSwitch2(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/groups-in-switch-with-id.svg',
			scour.parse_args(['--enable-id-stripping'])[0])
		self.assertEquals(doc.getElementsByTagName('g').length, 1,
			'Erroneously removed a <g> in a <switch>')

class GroupCreation(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/group-creation.svg',
			scour.parse_args(['--create-groups'])[0])
		self.assertEquals(doc.getElementsByTagName('g').length, 1,
			'Did not create a <g> for a run of elements having similar attributes')

class GroupCreationForInheritableAttributesOnly(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/group-creation.svg',
			scour.parse_args(['--create-groups'])[0])
		self.assertEquals(doc.getElementsByTagName('g').item(0).getAttribute('y'), '',
			'Promoted the uninheritable attribute y to a <g>')

class GroupNoCreation(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/group-no-creation.svg',
			scour.parse_args(['--create-groups'])[0])
		self.assertEquals(doc.getElementsByTagName('g').length, 0,
			'Created a <g> for a run of elements having dissimilar attributes')

class DoNotCommonizeAttributesOnReferencedElements(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/commonized-referenced-elements.svg')
		self.assertEquals(doc.getElementsByTagName('circle')[0].getAttribute('fill'), '#0f0',
			'Grouped an element referenced elsewhere into a <g>')

class DoNotRemoveOverflowVisibleOnMarker(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/overflow-marker.svg')
		self.assertEquals(doc.getElementsByTagName('marker')[0].getAttribute('overflow'), 'visible',
			'Removed the overflow attribute when it was not using the default value')
		self.assertEquals(doc.getElementsByTagName('marker')[1].getAttribute('overflow'), '',
			'Did not remove the overflow attribute when it was using the default value')

class MarkerOnSvgElements(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/overflow-svg.svg')
		self.assertEquals(doc.getElementsByTagName('svg')[0].getAttribute('overflow'), '',
			'Did not remove the overflow attribute when it was using the default value')
		self.assertEquals(doc.getElementsByTagName('svg')[1].getAttribute('overflow'), '',
			'Did not remove the overflow attribute when it was using the default value')
		self.assertEquals(doc.getElementsByTagName('svg')[2].getAttribute('overflow'), 'visible',
			'Removed the overflow attribute when it was not using the default value')

class GradientReferencedByStyleCDATA(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/style-cdata.svg')
		self.assertEquals(len(doc.getElementsByTagName('linearGradient')), 1,
			'Removed a gradient referenced by an internal stylesheet')

class ShortenIDsInStyleCDATA(unittest.TestCase):
	def runTest(self):
		docStr = file('unittests/style-cdata.svg').read()
		docStr = scour.scourString(docStr,
			scour.parse_args(['--shorten-ids'])[0])
		self.assertEquals(docStr.find('somethingreallylong'), -1,
			'Did not shorten IDs in the internal stylesheet')

# TODO: write tests for --enable-viewboxing
# TODO; write a test for embedding rasters
# TODO: write a test for --disable-embed-rasters
# TODO: write tests for --keep-editor-data
# TODO: write tests for scouring transformations

if __name__ == '__main__':
	testcss = __import__('testcss')
	scour = __import__('__main__')
	suite = unittest.TestSuite( map(unittest.defaultTestLoader.loadTestsFromModule, [testcss, scour]) )
	unittest.main(defaultTest="suite")
