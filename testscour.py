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
		doc = scour.scourXmlFile('unittests/ids-to-strip.svg', ['--enable-id-stripping'])
		self.assertEquals(doc.getElementsByTagNameNS(SVGNS, 'svg')[0].getAttribute('id'), '',
			'<svg> ID not stripped' )

class RemoveUselessNestedGroups(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/nested-useless-groups.svg')
		self.assertEquals(len(doc.getElementsByTagNameNS(SVGNS, 'g')), 1,
			'Useless nested groups not removed' )

class DoNotRemoveUselessNestedGroups(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/nested-useless-groups.svg', ['--disable-group-collapsing'])
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
		doc = scour.scourXmlFile('unittests/fill-none.svg')
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
		self.assertEquals(doc.getElementsByTagNameNS(SVGNS, 'radialGradient')[0].getAttribute('gradientUnits'), 
			'objectBoundingBox',
			'gradientUnits not properly overrode when collapsing gradients' )

class DoNotCollapseMultiplyReferencedGradients(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/dont-collapse-gradients.svg')
		self.assertNotEquals(len(doc.getElementsByTagNameNS(SVGNS, 'linearGradient')), 0,
			'Multiply-referenced linear gradient collapsed' )

class RemoveTrailingZeroesFromPath(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/path-truncate-zeroes.svg')
		path = doc.getElementsByTagNameNS(SVGNS, 'path')[0].getAttribute('d')
		self.assertEquals(path[:4] == 'M300' and path[4] != '.', True,
			'Trailing zeros not removed from path data' )

class RemoveDelimiterBeforeNegativeCoordsInPath(unittest.TestCase):
	def runTest(self):
		doc = scour.scourXmlFile('unittests/path-truncate-zeroes.svg')
		path = doc.getElementsByTagNameNS(SVGNS, 'path')[0].getAttribute('d')
		self.assertEquals(path[4], '-', 
			'Delimiters not removed before negative coordinates in path data' )

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
		self.assertEquals(path[1][1][0], 100.001,
			'Not correctly limiting precision on path data' )
			
if __name__ == '__main__':
    unittest.main()
