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

from __future__ import print_function   # use print() as a function in Python 2 (see PEP 3105)
from __future__ import absolute_import  # use absolute imports by default in Python 2 (see PEP 328)

import os
import sys
import unittest

import six
from six.moves import map, range

from scour.scour import (make_well_formed, parse_args, scourString, scourXmlFile, start, run,
                         XML_ENTS_ESCAPE_APOS, XML_ENTS_ESCAPE_QUOT)
from scour.svg_regex import svg_parser
from scour import __version__


SVGNS = 'http://www.w3.org/2000/svg'


# I couldn't figure out how to get ElementTree to work with the following XPath
# "//*[namespace-uri()='http://example.com']"
# so I decided to use minidom and this helper function that performs a test on a given node
# and all its children
# func must return either True (if pass) or False (if fail)
def walkTree(elem, func):
    if func(elem) is False:
        return False
    for child in elem.childNodes:
        if walkTree(child, func) is False:
            return False
    return True


class ScourOptions:
    pass


class EmptyOptions(unittest.TestCase):

    MINIMAL_SVG = '<?xml version="1.0" encoding="UTF-8"?>\n' \
                  '<svg xmlns="http://www.w3.org/2000/svg"/>\n'

    def test_scourString(self):
        options = ScourOptions
        try:
            scourString(self.MINIMAL_SVG, options)
            fail = False
        except Exception:
            fail = True
        self.assertEqual(fail, False,
                         'Exception when calling "scourString" with empty options object')

    def test_scourXmlFile(self):
        options = ScourOptions
        try:
            scourXmlFile('unittests/minimal.svg', options)
            fail = False
        except Exception:
            fail = True
        self.assertEqual(fail, False,
                         'Exception when calling "scourXmlFile" with empty options object')

    def test_start(self):
        options = ScourOptions
        input = open('unittests/minimal.svg', 'rb')
        output = open('testscour_temp.svg', 'wb')

        stdout_temp = sys.stdout
        sys.stdout = None
        try:
            start(options, input, output)
            fail = False
        except Exception:
            fail = True
        sys.stdout = stdout_temp

        os.remove('testscour_temp.svg')

        self.assertEqual(fail, False,
                         'Exception when calling "start" with empty options object')


class InvalidOptions(unittest.TestCase):

    def runTest(self):
        options = ScourOptions
        options.invalidOption = "invalid value"
        try:
            scourXmlFile('unittests/ids-to-strip.svg', options)
            fail = False
        except Exception:
            fail = True
        self.assertEqual(fail, False,
                         'Exception when calling Scour with invalid options')


class GetElementById(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/ids.svg')
        self.assertIsNotNone(doc.getElementById('svg1'), 'Root SVG element not found by ID')
        self.assertIsNotNone(doc.getElementById('linearGradient1'), 'linearGradient not found by ID')
        self.assertIsNotNone(doc.getElementById('layer1'), 'g not found by ID')
        self.assertIsNotNone(doc.getElementById('rect1'), 'rect not found by ID')
        self.assertIsNone(doc.getElementById('rect2'), 'Non-existing element found by ID')


class NoInkscapeElements(unittest.TestCase):

    def runTest(self):
        self.assertNotEqual(walkTree(scourXmlFile('unittests/sodipodi.svg').documentElement,
                            lambda e: e.namespaceURI != 'http://www.inkscape.org/namespaces/inkscape'),
                            False,
                            'Found Inkscape elements')


class NoSodipodiElements(unittest.TestCase):

    def runTest(self):
        self.assertNotEqual(walkTree(scourXmlFile('unittests/sodipodi.svg').documentElement,
                            lambda e: e.namespaceURI != 'http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd'),
                            False,
                            'Found Sodipodi elements')


class NoAdobeIllustratorElements(unittest.TestCase):

    def runTest(self):
        self.assertNotEqual(walkTree(scourXmlFile('unittests/adobe.svg').documentElement,
                            lambda e: e.namespaceURI != 'http://ns.adobe.com/AdobeIllustrator/10.0/'),
                            False,
                            'Found Adobe Illustrator elements')


class NoAdobeGraphsElements(unittest.TestCase):

    def runTest(self):
        self.assertNotEqual(walkTree(scourXmlFile('unittests/adobe.svg').documentElement,
                            lambda e: e.namespaceURI != 'http://ns.adobe.com/Graphs/1.0/'),
                            False,
                            'Found Adobe Graphs elements')


class NoAdobeSVGViewerElements(unittest.TestCase):

    def runTest(self):
        self.assertNotEqual(walkTree(scourXmlFile('unittests/adobe.svg').documentElement,
                            lambda e: e.namespaceURI != 'http://ns.adobe.com/AdobeSVGViewerExtensions/3.0/'),
                            False,
                            'Found Adobe SVG Viewer elements')


class NoAdobeVariablesElements(unittest.TestCase):

    def runTest(self):
        self.assertNotEqual(walkTree(scourXmlFile('unittests/adobe.svg').documentElement,
                            lambda e: e.namespaceURI != 'http://ns.adobe.com/Variables/1.0/'),
                            False,
                            'Found Adobe Variables elements')


class NoAdobeSaveForWebElements(unittest.TestCase):

    def runTest(self):
        self.assertNotEqual(walkTree(scourXmlFile('unittests/adobe.svg').documentElement,
                            lambda e: e.namespaceURI != 'http://ns.adobe.com/SaveForWeb/1.0/'),
                            False,
                            'Found Adobe Save For Web elements')


class NoAdobeExtensibilityElements(unittest.TestCase):

    def runTest(self):
        self.assertNotEqual(walkTree(scourXmlFile('unittests/adobe.svg').documentElement,
                            lambda e: e.namespaceURI != 'http://ns.adobe.com/Extensibility/1.0/'),
                            False,
                            'Found Adobe Extensibility elements')


class NoAdobeFlowsElements(unittest.TestCase):

    def runTest(self):
        self.assertNotEqual(walkTree(scourXmlFile('unittests/adobe.svg').documentElement,
                            lambda e: e.namespaceURI != 'http://ns.adobe.com/Flows/1.0/'),
                            False,
                            'Found Adobe Flows elements')


class NoAdobeImageReplacementElements(unittest.TestCase):

    def runTest(self):
        self.assertNotEqual(walkTree(scourXmlFile('unittests/adobe.svg').documentElement,
                            lambda e: e.namespaceURI != 'http://ns.adobe.com/ImageReplacement/1.0/'),
                            False,
                            'Found Adobe Image Replacement elements')


class NoAdobeCustomElements(unittest.TestCase):

    def runTest(self):
        self.assertNotEqual(walkTree(scourXmlFile('unittests/adobe.svg').documentElement,
                            lambda e: e.namespaceURI != 'http://ns.adobe.com/GenericCustomNamespace/1.0/'),
                            False,
                            'Found Adobe Custom elements')


class NoAdobeXPathElements(unittest.TestCase):

    def runTest(self):
        self.assertNotEqual(walkTree(scourXmlFile('unittests/adobe.svg').documentElement,
                            lambda e: e.namespaceURI != 'http://ns.adobe.com/XPath/1.0/'),
                            False,
                            'Found Adobe XPath elements')


class DoNotRemoveTitleWithOnlyText(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/descriptive-elements-with-text.svg')
        self.assertEqual(len(doc.getElementsByTagNameNS(SVGNS, 'title')), 1,
                         'Removed title element with only text child')


class RemoveEmptyTitleElement(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/empty-descriptive-elements.svg')
        self.assertEqual(len(doc.getElementsByTagNameNS(SVGNS, 'title')), 0,
                         'Did not remove empty title element')


class DoNotRemoveDescriptionWithOnlyText(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/descriptive-elements-with-text.svg')
        self.assertEqual(len(doc.getElementsByTagNameNS(SVGNS, 'desc')), 1,
                         'Removed description element with only text child')


class RemoveEmptyDescriptionElement(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/empty-descriptive-elements.svg')
        self.assertEqual(len(doc.getElementsByTagNameNS(SVGNS, 'desc')), 0,
                         'Did not remove empty description element')


class DoNotRemoveMetadataWithOnlyText(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/descriptive-elements-with-text.svg')
        self.assertEqual(len(doc.getElementsByTagNameNS(SVGNS, 'metadata')), 1,
                         'Removed metadata element with only text child')


class RemoveEmptyMetadataElement(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/empty-descriptive-elements.svg')
        self.assertEqual(len(doc.getElementsByTagNameNS(SVGNS, 'metadata')), 0,
                         'Did not remove empty metadata element')


class DoNotRemoveDescriptiveElementsWithOnlyText(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/descriptive-elements-with-text.svg')
        self.assertEqual(len(doc.getElementsByTagNameNS(SVGNS, 'title')), 1,
                         'Removed title element with only text child')
        self.assertEqual(len(doc.getElementsByTagNameNS(SVGNS, 'desc')), 1,
                         'Removed description element with only text child')
        self.assertEqual(len(doc.getElementsByTagNameNS(SVGNS, 'metadata')), 1,
                         'Removed metadata element with only text child')


class RemoveEmptyDescriptiveElements(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/empty-descriptive-elements.svg')
        self.assertEqual(len(doc.getElementsByTagNameNS(SVGNS, 'title')), 0,
                         'Did not remove empty title element')
        self.assertEqual(len(doc.getElementsByTagNameNS(SVGNS, 'desc')), 0,
                         'Did not remove empty description element')
        self.assertEqual(len(doc.getElementsByTagNameNS(SVGNS, 'metadata')), 0,
                         'Did not remove empty metadata element')


class RemoveEmptyGElements(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/empty-g.svg')
        self.assertEqual(len(doc.getElementsByTagNameNS(SVGNS, 'g')), 1,
                         'Did not remove empty g element')


class RemoveUnreferencedPattern(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/unreferenced-pattern.svg')
        self.assertEqual(len(doc.getElementsByTagNameNS(SVGNS, 'pattern')), 0,
                         'Unreferenced pattern not removed')


class RemoveUnreferencedLinearGradient(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/unreferenced-linearGradient.svg')
        self.assertEqual(len(doc.getElementsByTagNameNS(SVGNS, 'linearGradient')), 0,
                         'Unreferenced linearGradient not removed')


class RemoveUnreferencedRadialGradient(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/unreferenced-radialGradient.svg')
        self.assertEqual(len(doc.getElementsByTagNameNS(SVGNS, 'radialradient')), 0,
                         'Unreferenced radialGradient not removed')


class RemoveUnreferencedElementInDefs(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/referenced-elements-1.svg')
        self.assertEqual(len(doc.getElementsByTagNameNS(SVGNS, 'rect')), 1,
                         'Unreferenced rect left in defs')


class RemoveUnreferencedDefs(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/unreferenced-defs.svg')
        self.assertEqual(len(doc.getElementsByTagNameNS(SVGNS, 'linearGradient')), 1,
                         'Referenced linearGradient removed from defs')
        self.assertEqual(len(doc.getElementsByTagNameNS(SVGNS, 'radialGradient')), 0,
                         'Unreferenced radialGradient left in defs')
        self.assertEqual(len(doc.getElementsByTagNameNS(SVGNS, 'pattern')), 0,
                         'Unreferenced pattern left in defs')
        self.assertEqual(len(doc.getElementsByTagNameNS(SVGNS, 'rect')), 1,
                         'Referenced rect removed from defs')
        self.assertEqual(len(doc.getElementsByTagNameNS(SVGNS, 'circle')), 0,
                         'Unreferenced circle left in defs')


class KeepUnreferencedDefs(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/unreferenced-defs.svg',
                           parse_args(['--keep-unreferenced-defs']))
        self.assertEqual(len(doc.getElementsByTagNameNS(SVGNS, 'linearGradient')), 1,
                         'Referenced linearGradient removed from defs with `--keep-unreferenced-defs`')
        self.assertEqual(len(doc.getElementsByTagNameNS(SVGNS, 'radialGradient')), 1,
                         'Unreferenced radialGradient removed from defs with `--keep-unreferenced-defs`')
        self.assertEqual(len(doc.getElementsByTagNameNS(SVGNS, 'pattern')), 1,
                         'Unreferenced pattern removed from defs with `--keep-unreferenced-defs`')
        self.assertEqual(len(doc.getElementsByTagNameNS(SVGNS, 'rect')), 1,
                         'Referenced rect removed from defs with `--keep-unreferenced-defs`')
        self.assertEqual(len(doc.getElementsByTagNameNS(SVGNS, 'circle')), 1,
                         'Unreferenced circle removed from defs with `--keep-unreferenced-defs`')


class DoNotRemoveChainedRefsInDefs(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/refs-in-defs.svg')
        g = doc.getElementsByTagNameNS(SVGNS, 'g')[0]
        self.assertEqual(g.childNodes.length >= 2, True,
                         'Chained references not honored in defs')


class KeepTitleInDefs(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/referenced-elements-1.svg')
        self.assertEqual(len(doc.getElementsByTagNameNS(SVGNS, 'title')), 1,
                         'Title removed from in defs')


class RemoveNestedDefs(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/nested-defs.svg')
        allDefs = doc.getElementsByTagNameNS(SVGNS, 'defs')
        self.assertEqual(len(allDefs), 1, 'More than one defs left in doc')


class KeepUnreferencedIDsWhenEnabled(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/ids-to-strip.svg')
        self.assertEqual(doc.getElementsByTagNameNS(SVGNS, 'svg')[0].getAttribute('id'), 'boo',
                         '<svg> ID stripped when it should be disabled')


class RemoveUnreferencedIDsWhenEnabled(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/ids-to-strip.svg',
                           parse_args(['--enable-id-stripping']))
        self.assertEqual(doc.getElementsByTagNameNS(SVGNS, 'svg')[0].getAttribute('id'), '',
                         '<svg> ID not stripped')


class ProtectIDs(unittest.TestCase):

    def test_protect_none(self):
        doc = scourXmlFile('unittests/ids-protect.svg',
                           parse_args(['--enable-id-stripping']))
        self.assertEqual(doc.getElementsByTagNameNS(SVGNS, 'text')[0].getAttribute('id'), '',
                         "ID 'text1' not stripped when none of the '--protect-ids-_' options was specified")
        self.assertEqual(doc.getElementsByTagNameNS(SVGNS, 'text')[1].getAttribute('id'), '',
                         "ID 'text2' not stripped when none of the '--protect-ids-_' options was specified")
        self.assertEqual(doc.getElementsByTagNameNS(SVGNS, 'text')[2].getAttribute('id'), '',
                         "ID 'text3' not stripped when none of the '--protect-ids-_' options was specified")
        self.assertEqual(doc.getElementsByTagNameNS(SVGNS, 'text')[3].getAttribute('id'), '',
                         "ID 'text_custom' not stripped when none of the '--protect-ids-_' options was specified")
        self.assertEqual(doc.getElementsByTagNameNS(SVGNS, 'text')[4].getAttribute('id'), '',
                         "ID 'my_text1' not stripped when none of the '--protect-ids-_' options was specified")

    def test_protect_ids_noninkscape(self):
        doc = scourXmlFile('unittests/ids-protect.svg',
                           parse_args(['--enable-id-stripping', '--protect-ids-noninkscape']))
        self.assertEqual(doc.getElementsByTagNameNS(SVGNS, 'text')[0].getAttribute('id'), '',
                         "ID 'text1' should have been stripped despite '--protect-ids-noninkscape' being specified")
        self.assertEqual(doc.getElementsByTagNameNS(SVGNS, 'text')[1].getAttribute('id'), '',
                         "ID 'text2' should have been stripped despite '--protect-ids-noninkscape' being specified")
        self.assertEqual(doc.getElementsByTagNameNS(SVGNS, 'text')[2].getAttribute('id'), '',
                         "ID 'text3' should have been stripped despite '--protect-ids-noninkscape' being specified")
        self.assertEqual(doc.getElementsByTagNameNS(SVGNS, 'text')[3].getAttribute('id'), 'text_custom',
                         "ID 'text_custom' should NOT have been stripped because of '--protect-ids-noninkscape'")
        self.assertEqual(doc.getElementsByTagNameNS(SVGNS, 'text')[4].getAttribute('id'), '',
                         "ID 'my_text1' should have been stripped despite '--protect-ids-noninkscape' being specified")

    def test_protect_ids_list(self):
        doc = scourXmlFile('unittests/ids-protect.svg',
                           parse_args(['--enable-id-stripping', '--protect-ids-list=text2,text3']))
        self.assertEqual(doc.getElementsByTagNameNS(SVGNS, 'text')[0].getAttribute('id'), '',
                         "ID 'text1' should have been stripped despite '--protect-ids-list' being specified")
        self.assertEqual(doc.getElementsByTagNameNS(SVGNS, 'text')[1].getAttribute('id'), 'text2',
                         "ID 'text2' should NOT have been stripped because of '--protect-ids-list'")
        self.assertEqual(doc.getElementsByTagNameNS(SVGNS, 'text')[2].getAttribute('id'), 'text3',
                         "ID 'text3' should NOT have been stripped because of '--protect-ids-list'")
        self.assertEqual(doc.getElementsByTagNameNS(SVGNS, 'text')[3].getAttribute('id'), '',
                         "ID 'text_custom' should have been stripped despite '--protect-ids-list' being specified")
        self.assertEqual(doc.getElementsByTagNameNS(SVGNS, 'text')[4].getAttribute('id'), '',
                         "ID 'my_text1' should have been stripped despite '--protect-ids-list' being specified")

    def test_protect_ids_prefix(self):
        doc = scourXmlFile('unittests/ids-protect.svg',
                           parse_args(['--enable-id-stripping', '--protect-ids-prefix=my']))
        self.assertEqual(doc.getElementsByTagNameNS(SVGNS, 'text')[0].getAttribute('id'), '',
                         "ID 'text1' should have been stripped despite '--protect-ids-prefix' being specified")
        self.assertEqual(doc.getElementsByTagNameNS(SVGNS, 'text')[1].getAttribute('id'), '',
                         "ID 'text2' should have been stripped despite '--protect-ids-prefix' being specified")
        self.assertEqual(doc.getElementsByTagNameNS(SVGNS, 'text')[2].getAttribute('id'), '',
                         "ID 'text3' should have been stripped despite '--protect-ids-prefix' being specified")
        self.assertEqual(doc.getElementsByTagNameNS(SVGNS, 'text')[3].getAttribute('id'), '',
                         "ID 'text_custom' should have been stripped despite '--protect-ids-prefix' being specified")
        self.assertEqual(doc.getElementsByTagNameNS(SVGNS, 'text')[4].getAttribute('id'), 'my_text1',
                         "ID 'my_text1' should NOT have been stripped because of '--protect-ids-prefix'")


class RemoveUselessNestedGroups(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/nested-useless-groups.svg')
        self.assertEqual(len(doc.getElementsByTagNameNS(SVGNS, 'g')), 1,
                         'Useless nested groups not removed')


class DoNotRemoveUselessNestedGroups(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/nested-useless-groups.svg',
                           parse_args(['--disable-group-collapsing']))
        self.assertEqual(len(doc.getElementsByTagNameNS(SVGNS, 'g')), 2,
                         'Useless nested groups were removed despite --disable-group-collapsing')


class DoNotRemoveNestedGroupsWithTitle(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/groups-with-title-desc.svg')
        self.assertEqual(len(doc.getElementsByTagNameNS(SVGNS, 'g')), 2,
                         'Nested groups with title was removed')


class DoNotRemoveNestedGroupsWithDesc(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/groups-with-title-desc.svg')
        self.assertEqual(len(doc.getElementsByTagNameNS(SVGNS, 'g')), 2,
                         'Nested groups with desc was removed')


class RemoveDuplicateLinearGradientStops(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/duplicate-gradient-stops.svg')
        grad = doc.getElementsByTagNameNS(SVGNS, 'linearGradient')
        self.assertEqual(len(grad[0].getElementsByTagNameNS(SVGNS, 'stop')), 3,
                         'Duplicate linear gradient stops not removed')


class RemoveDuplicateLinearGradientStopsPct(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/duplicate-gradient-stops-pct.svg')
        grad = doc.getElementsByTagNameNS(SVGNS, 'linearGradient')
        self.assertEqual(len(grad[0].getElementsByTagNameNS(SVGNS, 'stop')), 3,
                         'Duplicate linear gradient stops with percentages not removed')


class RemoveDuplicateRadialGradientStops(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/duplicate-gradient-stops.svg')
        grad = doc.getElementsByTagNameNS(SVGNS, 'radialGradient')
        self.assertEqual(len(grad[0].getElementsByTagNameNS(SVGNS, 'stop')), 3,
                         'Duplicate radial gradient stops not removed')


class NoSodipodiNamespaceDecl(unittest.TestCase):

    def runTest(self):
        attrs = scourXmlFile('unittests/sodipodi.svg').documentElement.attributes
        for i in range(len(attrs)):
            self.assertNotEqual(attrs.item(i).nodeValue,
                                'http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd',
                                'Sodipodi namespace declaration found')


class NoInkscapeNamespaceDecl(unittest.TestCase):

    def runTest(self):
        attrs = scourXmlFile('unittests/inkscape.svg').documentElement.attributes
        for i in range(len(attrs)):
            self.assertNotEqual(attrs.item(i).nodeValue,
                                'http://www.inkscape.org/namespaces/inkscape',
                                'Inkscape namespace declaration found')


class NoSodipodiAttributes(unittest.TestCase):

    def runTest(self):
        def findSodipodiAttr(elem):
            attrs = elem.attributes
            if attrs is None:
                return True
            for i in range(len(attrs)):
                if attrs.item(i).namespaceURI == 'http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd':
                    return False
            return True
        self.assertNotEqual(walkTree(scourXmlFile('unittests/sodipodi.svg').documentElement, findSodipodiAttr),
                            False,
                            'Found Sodipodi attributes')


class NoInkscapeAttributes(unittest.TestCase):

    def runTest(self):
        def findInkscapeAttr(elem):
            attrs = elem.attributes
            if attrs is None:
                return True
            for i in range(len(attrs)):
                if attrs.item(i).namespaceURI == 'http://www.inkscape.org/namespaces/inkscape':
                    return False
            return True
        self.assertNotEqual(walkTree(scourXmlFile('unittests/inkscape.svg').documentElement, findInkscapeAttr),
                            False,
                            'Found Inkscape attributes')


class KeepInkscapeNamespaceDeclarationsWhenKeepEditorData(unittest.TestCase):

    def runTest(self):
        options = ScourOptions
        options.keep_editor_data = True
        attrs = scourXmlFile('unittests/inkscape.svg', options).documentElement.attributes
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
        attrs = scourXmlFile('unittests/sodipodi.svg', options).documentElement.attributes
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
        doc = scourXmlFile('unittests/referenced-font.svg')
        fonts = doc.documentElement.getElementsByTagNameNS(SVGNS, 'font')
        self.assertEqual(len(fonts), 1,
                         'Font wrongly removed from <defs>')


class ConvertStyleToAttrs(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/stroke-transparent.svg')
        self.assertEqual(doc.getElementsByTagNameNS(SVGNS, 'path')[0].getAttribute('style'), '',
                         'style attribute not emptied')


class RemoveStrokeWhenStrokeTransparent(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/stroke-transparent.svg')
        self.assertEqual(doc.getElementsByTagNameNS(SVGNS, 'path')[0].getAttribute('stroke'), '',
                         'stroke attribute not emptied when stroke opacity zero')


class RemoveStrokeWidthWhenStrokeTransparent(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/stroke-transparent.svg')
        self.assertEqual(doc.getElementsByTagNameNS(SVGNS, 'path')[0].getAttribute('stroke-width'), '',
                         'stroke-width attribute not emptied when stroke opacity zero')


class RemoveStrokeLinecapWhenStrokeTransparent(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/stroke-transparent.svg')
        self.assertEqual(doc.getElementsByTagNameNS(SVGNS, 'path')[0].getAttribute('stroke-linecap'), '',
                         'stroke-linecap attribute not emptied when stroke opacity zero')


class RemoveStrokeLinejoinWhenStrokeTransparent(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/stroke-transparent.svg')
        self.assertEqual(doc.getElementsByTagNameNS(SVGNS, 'path')[0].getAttribute('stroke-linejoin'), '',
                         'stroke-linejoin attribute not emptied when stroke opacity zero')


class RemoveStrokeDasharrayWhenStrokeTransparent(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/stroke-transparent.svg')
        self.assertEqual(doc.getElementsByTagNameNS(SVGNS, 'path')[0].getAttribute('stroke-dasharray'), '',
                         'stroke-dasharray attribute not emptied when stroke opacity zero')


class RemoveStrokeDashoffsetWhenStrokeTransparent(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/stroke-transparent.svg')
        self.assertEqual(doc.getElementsByTagNameNS(SVGNS, 'path')[0].getAttribute('stroke-dashoffset'), '',
                         'stroke-dashoffset attribute not emptied when stroke opacity zero')


class RemoveStrokeWhenStrokeWidthZero(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/stroke-nowidth.svg')
        self.assertEqual(doc.getElementsByTagNameNS(SVGNS, 'path')[0].getAttribute('stroke'), '',
                         'stroke attribute not emptied when width zero')


class RemoveStrokeOpacityWhenStrokeWidthZero(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/stroke-nowidth.svg')
        self.assertEqual(doc.getElementsByTagNameNS(SVGNS, 'path')[0].getAttribute('stroke-opacity'), '',
                         'stroke-opacity attribute not emptied when width zero')


class RemoveStrokeLinecapWhenStrokeWidthZero(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/stroke-nowidth.svg')
        self.assertEqual(doc.getElementsByTagNameNS(SVGNS, 'path')[0].getAttribute('stroke-linecap'), '',
                         'stroke-linecap attribute not emptied when width zero')


class RemoveStrokeLinejoinWhenStrokeWidthZero(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/stroke-nowidth.svg')
        self.assertEqual(doc.getElementsByTagNameNS(SVGNS, 'path')[0].getAttribute('stroke-linejoin'), '',
                         'stroke-linejoin attribute not emptied when width zero')


class RemoveStrokeDasharrayWhenStrokeWidthZero(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/stroke-nowidth.svg')
        self.assertEqual(doc.getElementsByTagNameNS(SVGNS, 'path')[0].getAttribute('stroke-dasharray'), '',
                         'stroke-dasharray attribute not emptied when width zero')


class RemoveStrokeDashoffsetWhenStrokeWidthZero(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/stroke-nowidth.svg')
        self.assertEqual(doc.getElementsByTagNameNS(SVGNS, 'path')[0].getAttribute('stroke-dashoffset'), '',
                         'stroke-dashoffset attribute not emptied when width zero')


class RemoveStrokeWhenStrokeNone(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/stroke-none.svg')
        self.assertEqual(doc.getElementsByTagNameNS(SVGNS, 'path')[0].getAttribute('stroke'), '',
                         'stroke attribute not emptied when no stroke')


class KeepStrokeWhenInheritedFromParent(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/stroke-none.svg')
        self.assertEqual(doc.getElementById('p1').getAttribute('stroke'), 'none',
                         'stroke attribute removed despite a different value being inherited from a parent')


class KeepStrokeWhenInheritedByChild(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/stroke-none.svg')
        self.assertEqual(doc.getElementById('g2').getAttribute('stroke'), 'none',
                         'stroke attribute removed despite it being inherited by a child')


class RemoveStrokeWidthWhenStrokeNone(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/stroke-none.svg')
        self.assertEqual(doc.getElementsByTagNameNS(SVGNS, 'path')[0].getAttribute('stroke-width'), '',
                         'stroke-width attribute not emptied when no stroke')


class KeepStrokeWidthWhenInheritedByChild(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/stroke-none.svg')
        self.assertEqual(doc.getElementById('g3').getAttribute('stroke-width'), '1px',
                         'stroke-width attribute removed despite it being inherited by a child')


class RemoveStrokeOpacityWhenStrokeNone(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/stroke-none.svg')
        self.assertEqual(doc.getElementsByTagNameNS(SVGNS, 'path')[0].getAttribute('stroke-opacity'), '',
                         'stroke-opacity attribute not emptied when no stroke')


class RemoveStrokeLinecapWhenStrokeNone(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/stroke-none.svg')
        self.assertEqual(doc.getElementsByTagNameNS(SVGNS, 'path')[0].getAttribute('stroke-linecap'), '',
                         'stroke-linecap attribute not emptied when no stroke')


class RemoveStrokeLinejoinWhenStrokeNone(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/stroke-none.svg')
        self.assertEqual(doc.getElementsByTagNameNS(SVGNS, 'path')[0].getAttribute('stroke-linejoin'), '',
                         'stroke-linejoin attribute not emptied when no stroke')


class RemoveStrokeDasharrayWhenStrokeNone(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/stroke-none.svg')
        self.assertEqual(doc.getElementsByTagNameNS(SVGNS, 'path')[0].getAttribute('stroke-dasharray'), '',
                         'stroke-dasharray attribute not emptied when no stroke')


class RemoveStrokeDashoffsetWhenStrokeNone(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/stroke-none.svg')
        self.assertEqual(doc.getElementsByTagNameNS(SVGNS, 'path')[0].getAttribute('stroke-dashoffset'), '',
                         'stroke-dashoffset attribute not emptied when no stroke')


class RemoveFillRuleWhenFillNone(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/fill-none.svg')
        self.assertEqual(doc.getElementsByTagNameNS(SVGNS, 'path')[0].getAttribute('fill-rule'), '',
                         'fill-rule attribute not emptied when no fill')


class RemoveFillOpacityWhenFillNone(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/fill-none.svg')
        self.assertEqual(doc.getElementsByTagNameNS(SVGNS, 'path')[0].getAttribute('fill-opacity'), '',
                         'fill-opacity attribute not emptied when no fill')


class ConvertFillPropertyToAttr(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/fill-none.svg',
                           parse_args(['--disable-simplify-colors']))
        self.assertEqual(doc.getElementsByTagNameNS(SVGNS, 'path')[1].getAttribute('fill'), 'black',
                         'fill property not converted to XML attribute')


class ConvertFillOpacityPropertyToAttr(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/fill-none.svg')
        self.assertEqual(doc.getElementsByTagNameNS(SVGNS, 'path')[1].getAttribute('fill-opacity'), '.5',
                         'fill-opacity property not converted to XML attribute')


class ConvertFillRuleOpacityPropertyToAttr(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/fill-none.svg')
        self.assertEqual(doc.getElementsByTagNameNS(SVGNS, 'path')[1].getAttribute('fill-rule'), 'evenodd',
                         'fill-rule property not converted to XML attribute')


class CollapseSinglyReferencedGradients(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/collapse-gradients.svg')
        self.assertEqual(len(doc.getElementsByTagNameNS(SVGNS, 'linearGradient')), 0,
                         'Singly-referenced linear gradient not collapsed')


class InheritGradientUnitsUponCollapsing(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/collapse-gradients.svg')
        self.assertEqual(doc.getElementsByTagNameNS(SVGNS, 'radialGradient')[0].getAttribute('gradientUnits'),
                         'userSpaceOnUse',
                         'gradientUnits not properly inherited when collapsing gradients')


class OverrideGradientUnitsUponCollapsing(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/collapse-gradients-gradientUnits.svg')
        self.assertEqual(doc.getElementsByTagNameNS(SVGNS, 'radialGradient')[0].getAttribute('gradientUnits'), '',
                         'gradientUnits not properly overrode when collapsing gradients')


class DoNotCollapseMultiplyReferencedGradients(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/dont-collapse-gradients.svg')
        self.assertNotEqual(len(doc.getElementsByTagNameNS(SVGNS, 'linearGradient')), 0,
                            'Multiply-referenced linear gradient collapsed')


class PreserveXLinkHrefWhenCollapsingReferencedGradients(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/collapse-gradients-preserve-xlink-href.svg')
        g1 = doc.getElementById("g1")
        g2 = doc.getElementById("g2")
        g3 = doc.getElementById("g3")
        self.assertTrue(g1, 'g1 is still present')
        self.assertTrue(g2 is None, 'g2 was removed')
        self.assertTrue(g3, 'g3 is still present')
        self.assertEqual(g3.getAttributeNS('http://www.w3.org/1999/xlink', 'href'), '#g1',
                         'g3 has a xlink:href to g1')


class RemoveTrailingZerosFromPath(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/path-truncate-zeros.svg')
        path = doc.getElementsByTagNameNS(SVGNS, 'path')[0].getAttribute('d')
        self.assertEqual(path[:4] == 'm300' and path[4] != '.', True,
                         'Trailing zeros not removed from path data')


class RemoveTrailingZerosFromPathAfterCalculation(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/path-truncate-zeros-calc.svg')
        path = doc.getElementsByTagNameNS(SVGNS, 'path')[0].getAttribute('d')
        self.assertEqual(path, 'm5.81 0h0.1',
                         'Trailing zeros not removed from path data after calculation')


class RemoveDelimiterBeforeNegativeCoordsInPath(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/path-truncate-zeros.svg')
        path = doc.getElementsByTagNameNS(SVGNS, 'path')[0].getAttribute('d')
        self.assertEqual(path[4], '-',
                         'Delimiters not removed before negative coordinates in path data')


class UseScientificNotationToShortenCoordsInPath(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/path-use-scientific-notation.svg')
        path = doc.getElementsByTagNameNS(SVGNS, 'path')[0].getAttribute('d')
        self.assertEqual(path, 'm1e4 0',
                         'Not using scientific notation for path coord when representation is shorter')


class ConvertAbsoluteToRelativePathCommands(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/path-abs-to-rel.svg')
        path = svg_parser.parse(doc.getElementsByTagNameNS(SVGNS, 'path')[0].getAttribute('d'))
        self.assertEqual(path[1][0], 'v',
                         'Absolute V command not converted to relative v command')
        self.assertEqual(float(path[1][1][0]), -20.0,
                         'Absolute V value not converted to relative v value')


class RoundPathData(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/path-precision.svg')
        path = svg_parser.parse(doc.getElementsByTagNameNS(SVGNS, 'path')[0].getAttribute('d'))
        self.assertEqual(float(path[0][1][0]), 100.0,
                         'Not rounding down')
        self.assertEqual(float(path[0][1][1]), 100.0,
                         'Not rounding up')


class LimitPrecisionInPathData(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/path-precision.svg')
        path = svg_parser.parse(doc.getElementsByTagNameNS(SVGNS, 'path')[0].getAttribute('d'))
        self.assertEqual(float(path[1][1][0]), 100.01,
                         'Not correctly limiting precision on path data')


class KeepPrecisionInPathDataIfSameLength(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/path-precision.svg', parse_args(['--set-precision=1']))
        paths = doc.getElementsByTagNameNS(SVGNS, 'path')
        for path in paths[1:3]:
            self.assertEqual(path.getAttribute('d'), "m1 21 321 4e3 5e4 7e5",
                             'Precision not correctly reduced with "--set-precision=1" '
                             'for path with ID ' + path.getAttribute('id'))
        self.assertEqual(paths[4].getAttribute('d'), "m-1-21-321-4e3 -5e4 -7e5",
                         'Precision not correctly reduced with "--set-precision=1" '
                         'for path with ID ' + paths[4].getAttribute('id'))
        self.assertEqual(paths[5].getAttribute('d'), "m123 101-123-101",
                         'Precision not correctly reduced with "--set-precision=1" '
                         'for path with ID ' + paths[5].getAttribute('id'))

        doc = scourXmlFile('unittests/path-precision.svg', parse_args(['--set-precision=2']))
        paths = doc.getElementsByTagNameNS(SVGNS, 'path')
        for path in paths[1:3]:
            self.assertEqual(path.getAttribute('d'), "m1 21 321 4321 54321 6.5e5",
                             'Precision not correctly reduced with "--set-precision=2" '
                             'for path with ID ' + path.getAttribute('id'))
        self.assertEqual(paths[4].getAttribute('d'), "m-1-21-321-4321-54321-6.5e5",
                         'Precision not correctly reduced with "--set-precision=2" '
                         'for path with ID ' + paths[4].getAttribute('id'))
        self.assertEqual(paths[5].getAttribute('d'), "m123 101-123-101",
                         'Precision not correctly reduced with "--set-precision=2" '
                         'for path with ID ' + paths[5].getAttribute('id'))

        doc = scourXmlFile('unittests/path-precision.svg', parse_args(['--set-precision=3']))
        paths = doc.getElementsByTagNameNS(SVGNS, 'path')
        for path in paths[1:3]:
            self.assertEqual(path.getAttribute('d'), "m1 21 321 4321 54321 654321",
                             'Precision not correctly reduced with "--set-precision=3" '
                             'for path with ID ' + path.getAttribute('id'))
        self.assertEqual(paths[4].getAttribute('d'), "m-1-21-321-4321-54321-654321",
                         'Precision not correctly reduced with "--set-precision=3" '
                         'for path with ID ' + paths[4].getAttribute('id'))
        self.assertEqual(paths[5].getAttribute('d'), "m123 101-123-101",
                         'Precision not correctly reduced with "--set-precision=3" '
                         'for path with ID ' + paths[5].getAttribute('id'))

        doc = scourXmlFile('unittests/path-precision.svg', parse_args(['--set-precision=4']))
        paths = doc.getElementsByTagNameNS(SVGNS, 'path')
        for path in paths[1:3]:
            self.assertEqual(path.getAttribute('d'), "m1 21 321 4321 54321 654321",
                             'Precision not correctly reduced with "--set-precision=4" '
                             'for path with ID ' + path.getAttribute('id'))
        self.assertEqual(paths[4].getAttribute('d'), "m-1-21-321-4321-54321-654321",
                         'Precision not correctly reduced with "--set-precision=4" '
                         'for path with ID ' + paths[4].getAttribute('id'))
        self.assertEqual(paths[5].getAttribute('d'), "m123.5 101-123.5-101",
                         'Precision not correctly reduced with "--set-precision=4" '
                         'for path with ID ' + paths[5].getAttribute('id'))


class LimitPrecisionInControlPointPathData(unittest.TestCase):

    def runTest(self):
        path_data = ("m1.1 2.2 3.3 4.4m-4.4-6.7"
                     "c1 2 3 4 5.6 6.7 1 2 3 4 5.6 6.7 1 2 3 4 5.6 6.7m-17-20"
                     "s1 2 3.3 4.4 1 2 3.3 4.4 1 2 3.3 4.4m-10-13"
                     "q1 2 3.3 4.4 1 2 3.3 4.4 1 2 3.3 4.4")
        doc = scourXmlFile('unittests/path-precision-control-points.svg',
                           parse_args(['--set-precision=2', '--set-c-precision=1']))
        path_data2 = doc.getElementsByTagNameNS(SVGNS, 'path')[0].getAttribute('d')
        self.assertEqual(path_data2, path_data,
                         'Not correctly limiting precision on path data with --set-c-precision')


class RemoveEmptyLineSegmentsFromPath(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/path-line-optimize.svg')
        path = svg_parser.parse(doc.getElementsByTagNameNS(SVGNS, 'path')[0].getAttribute('d'))
        self.assertEqual(path[4][0], 'z',
                         'Did not remove an empty line segment from path')


class RemoveEmptySegmentsFromPathWithButtLineCaps(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/path-with-caps.svg', parse_args(['--disable-style-to-xml']))
        for id in ['none', 'attr_butt', 'style_butt']:
            path = svg_parser.parse(doc.getElementById(id).getAttribute('d'))
            self.assertEqual(len(path), 1,
                             'Did not remove empty segments when path had butt linecaps')


class DoNotRemoveEmptySegmentsFromPathWithRoundSquareLineCaps(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/path-with-caps.svg', parse_args(['--disable-style-to-xml']))
        for id in ['attr_round', 'attr_square', 'style_round', 'style_square']:
            path = svg_parser.parse(doc.getElementById(id).getAttribute('d'))
            self.assertEqual(len(path), 2,
                             'Did remove empty segments when path had round or square linecaps')


class ChangeLineToHorizontalLineSegmentInPath(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/path-line-optimize.svg')
        path = svg_parser.parse(doc.getElementsByTagNameNS(SVGNS, 'path')[0].getAttribute('d'))
        self.assertEqual(path[1][0], 'h',
                         'Did not change line to horizontal line segment in path')
        self.assertEqual(float(path[1][1][0]), 200.0,
                         'Did not calculate horizontal line segment in path correctly')


class ChangeLineToVerticalLineSegmentInPath(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/path-line-optimize.svg')
        path = svg_parser.parse(doc.getElementsByTagNameNS(SVGNS, 'path')[0].getAttribute('d'))
        self.assertEqual(path[2][0], 'v',
                         'Did not change line to vertical line segment in path')
        self.assertEqual(float(path[2][1][0]), 100.0,
                         'Did not calculate vertical line segment in path correctly')


class ChangeBezierToShorthandInPath(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/path-bez-optimize.svg')
        self.assertEqual(doc.getElementById('path1').getAttribute('d'), 'm10 100c50-50 50 50 100 0s50 50 100 0',
                         'Did not change bezier curves into shorthand curve segments in path')
        self.assertEqual(doc.getElementById('path2a').getAttribute('d'), 'm200 200s200 100 200 0',
                         'Did not change bezier curve into shorthand curve segment when first control point '
                         'is the current point and previous command was not a bezier curve')
        self.assertEqual(doc.getElementById('path2b').getAttribute('d'), 'm0 300s200-100 200 0c0 0 200 100 200 0',
                         'Did change bezier curve into shorthand curve segment when first control point '
                         'is the current point but previous command was a bezier curve with a different control point')


class ChangeQuadToShorthandInPath(unittest.TestCase):

    def runTest(self):
        path = scourXmlFile('unittests/path-quad-optimize.svg').getElementsByTagNameNS(SVGNS, 'path')[0]
        self.assertEqual(path.getAttribute('d'), 'm10 100q50-50 100 0t100 0',
                         'Did not change quadratic curves into shorthand curve segments in path')


class BooleanFlagsInEllipticalPath(unittest.TestCase):

    def test_omit_spaces(self):
        doc = scourXmlFile('unittests/path-elliptical-flags.svg', parse_args(['--no-renderer-workaround']))
        paths = doc.getElementsByTagNameNS(SVGNS, 'path')
        for path in paths:
            self.assertEqual(path.getAttribute('d'), 'm0 0a100 50 0 00100 50',
                             'Did not ommit spaces after boolean flags in elliptical arg path command')

    def test_output_spaces_with_renderer_workaround(self):
        doc = scourXmlFile('unittests/path-elliptical-flags.svg', parse_args(['--renderer-workaround']))
        paths = doc.getElementsByTagNameNS(SVGNS, 'path')
        for path in paths:
            self.assertEqual(path.getAttribute('d'), 'm0 0a100 50 0 0 0 100 50',
                             'Did not output spaces after boolean flags in elliptical arg path command '
                             'with renderer workaround')


class DoNotOptimzePathIfLarger(unittest.TestCase):

    def runTest(self):
        p = scourXmlFile('unittests/path-no-optimize.svg').getElementsByTagNameNS(SVGNS, 'path')[0]
        self.assertTrue(len(p.getAttribute('d')) <=
                        # this was the scoured path data as of 2016-08-31 without the length check in cleanPath():
                        #    d="m100 100l100.12 100.12c14.877 4.8766-15.123-5.1234-0.00345-0.00345z"
                        len("M100,100 L200.12345,200.12345 C215,205 185,195 200.12,200.12 Z"),
                        'Made path data longer during optimization')


class HandleEncodingUTF8(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/encoding-utf8.svg')
        text = u'Hello in many languages:\n' \
               u'ar: أهلا\n' \
               u'bn: হ্যালো\n' \
               u'el: Χαίρετε\n' \
               u'en: Hello\n' \
               u'hi: नमस्ते\n' \
               u'iw: שלום\n' \
               u'ja: こんにちは\n' \
               u'km: ជំរាបសួរ\n' \
               u'ml: ഹലോ\n' \
               u'ru: Здравствуйте\n' \
               u'ur: ہیلو\n' \
               u'zh: 您好'
        desc = six.text_type(doc.getElementsByTagNameNS(SVGNS, 'desc')[0].firstChild.wholeText).strip()
        self.assertEqual(desc, text,
                         'Did not handle international UTF8 characters')
        desc = six.text_type(doc.getElementsByTagNameNS(SVGNS, 'desc')[1].firstChild.wholeText).strip()
        self.assertEqual(desc, u'“”‘’–—…‐‒°©®™•½¼¾⅓⅔†‡µ¢£€«»♠♣♥♦¿�',
                         'Did not handle common UTF8 characters')
        desc = six.text_type(doc.getElementsByTagNameNS(SVGNS, 'desc')[2].firstChild.wholeText).strip()
        self.assertEqual(desc, u':-×÷±∞π∅≤≥≠≈∧∨∩∪∈∀∃∄∑∏←↑→↓↔↕↖↗↘↙↺↻⇒⇔',
                         'Did not handle mathematical UTF8 characters')
        desc = six.text_type(doc.getElementsByTagNameNS(SVGNS, 'desc')[3].firstChild.wholeText).strip()
        self.assertEqual(desc, u'⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁽⁾ⁿⁱ₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎',
                         'Did not handle superscript/subscript UTF8 characters')


class HandleEncodingISO_8859_15(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/encoding-iso-8859-15.svg')
        desc = six.text_type(doc.getElementsByTagNameNS(SVGNS, 'desc')[0].firstChild.wholeText).strip()
        self.assertEqual(desc, u'áèîäöüß€ŠšŽžŒœŸ', 'Did not handle ISO 8859-15 encoded characters')


class HandleSciNoInPathData(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/path-sn.svg')
        self.assertEqual(len(doc.getElementsByTagNameNS(SVGNS, 'path')), 1,
                         'Did not handle scientific notation in path data')


class TranslateRGBIntoHex(unittest.TestCase):

    def runTest(self):
        elem = scourXmlFile('unittests/color-formats.svg').getElementsByTagNameNS(SVGNS, 'rect')[0]
        self.assertEqual(elem.getAttribute('fill'), '#0f1011',
                         'Not converting rgb into hex')


class TranslateRGBPctIntoHex(unittest.TestCase):

    def runTest(self):
        elem = scourXmlFile('unittests/color-formats.svg').getElementsByTagNameNS(SVGNS, 'stop')[0]
        self.assertEqual(elem.getAttribute('stop-color'), '#7f0000',
                         'Not converting rgb pct into hex')


class TranslateColorNamesIntoHex(unittest.TestCase):

    def runTest(self):
        elem = scourXmlFile('unittests/color-formats.svg').getElementsByTagNameNS(SVGNS, 'rect')[0]
        self.assertEqual(elem.getAttribute('stroke'), '#a9a9a9',
                         'Not converting standard color names into hex')


class TranslateExtendedColorNamesIntoHex(unittest.TestCase):

    def runTest(self):
        elem = scourXmlFile('unittests/color-formats.svg').getElementsByTagNameNS(SVGNS, 'solidColor')[0]
        self.assertEqual(elem.getAttribute('solid-color'), '#fafad2',
                         'Not converting extended color names into hex')


class TranslateLongHexColorIntoShortHex(unittest.TestCase):

    def runTest(self):
        elem = scourXmlFile('unittests/color-formats.svg').getElementsByTagNameNS(SVGNS, 'ellipse')[0]
        self.assertEqual(elem.getAttribute('fill'), '#fff',
                         'Not converting long hex color into short hex')


class DoNotConvertShortColorNames(unittest.TestCase):

    def runTest(self):
        elem = scourXmlFile('unittests/dont-convert-short-color-names.svg') \
                    .getElementsByTagNameNS(SVGNS, 'rect')[0]
        self.assertEqual('red', elem.getAttribute('fill'),
                         'Converted short color name to longer hex string')


class AllowQuotEntitiesInUrl(unittest.TestCase):

    def runTest(self):
        grads = scourXmlFile('unittests/quot-in-url.svg').getElementsByTagNameNS(SVGNS, 'linearGradient')
        self.assertEqual(len(grads), 1,
                         'Removed referenced gradient when &quot; was in the url')


class RemoveFontStylesFromNonTextShapes(unittest.TestCase):

    def runTest(self):
        r = scourXmlFile('unittests/font-styles.svg').getElementsByTagNameNS(SVGNS, 'rect')[0]
        self.assertEqual(r.getAttribute('font-size'), '',
                         'font-size not removed from rect')


class CollapseStraightPathSegments(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/collapse-straight-path-segments.svg', parse_args(['--disable-style-to-xml']))
        paths = doc.getElementsByTagNameNS(SVGNS, 'path')
        path_data = [path.getAttribute('d') for path in paths]
        path_data_expected = ['m0 0h30',
                              'm0 0v30',
                              'm0 0h10.5v10.5',
                              'm0 0h10-1v10-1',
                              'm0 0h30',
                              'm0 0h30',
                              'm0 0h10 20',
                              'm0 0h10 20',
                              'm0 0h10 20',
                              'm0 0h10 20',
                              'm0 0 20 40v1l10 20',
                              'm0 0 10 10-20-20 10 10-20-20',
                              'm0 0 1 2m1 2 2 4m1 2 2 4',
                              'm6.3228 7.1547 81.198 45.258']

        self.assertEqual(path_data[0:3], path_data_expected[0:3],
                         'Did not collapse h/v commands into a single h/v commands')
        self.assertEqual(path_data[3], path_data_expected[3],
                         'Collapsed h/v commands with different direction')
        self.assertEqual(path_data[4:6], path_data_expected[4:6],
                         'Did not collapse h/v commands with only start/end markers present')
        self.assertEqual(path_data[6:10], path_data_expected[6:10],
                         'Did not preserve h/v commands with intermediate markers present')

        self.assertEqual(path_data[10], path_data_expected[10],
                         'Did not collapse lineto commands into a single (implicit) lineto command')
        self.assertEqual(path_data[11], path_data_expected[11],
                         'Collapsed lineto commands with different direction')
        self.assertEqual(path_data[12], path_data_expected[12],
                         'Collapsed first parameter pair of a moveto subpath')
        self.assertEqual(path_data[13], path_data_expected[13],
                         'Did not collapse the nodes of a straight real world path')


class ConvertStraightCurvesToLines(unittest.TestCase):

    def runTest(self):
        p = scourXmlFile('unittests/straight-curve.svg').getElementsByTagNameNS(SVGNS, 'path')[0]
        self.assertEqual(p.getAttribute('d'), 'm10 10 40 40 40-40z',
                         'Did not convert straight curves into lines')


class RemoveUnnecessaryPolygonEndPoint(unittest.TestCase):

    def runTest(self):
        p = scourXmlFile('unittests/polygon.svg').getElementsByTagNameNS(SVGNS, 'polygon')[0]
        self.assertEqual(p.getAttribute('points'), '50 50 150 50 150 150 50 150',
                         'Unnecessary polygon end point not removed')


class DoNotRemovePolgonLastPoint(unittest.TestCase):

    def runTest(self):
        p = scourXmlFile('unittests/polygon.svg').getElementsByTagNameNS(SVGNS, 'polygon')[1]
        self.assertEqual(p.getAttribute('points'), '200 50 300 50 300 150 200 150',
                         'Last point of polygon removed')


class ScourPolygonCoordsSciNo(unittest.TestCase):

    def runTest(self):
        p = scourXmlFile('unittests/polygon-coord.svg').getElementsByTagNameNS(SVGNS, 'polygon')[0]
        self.assertEqual(p.getAttribute('points'), '1e4 50',
                         'Polygon coordinates not scoured')


class ScourPolylineCoordsSciNo(unittest.TestCase):

    def runTest(self):
        p = scourXmlFile('unittests/polyline-coord.svg').getElementsByTagNameNS(SVGNS, 'polyline')[0]
        self.assertEqual(p.getAttribute('points'), '1e4 50',
                         'Polyline coordinates not scoured')


class ScourPolygonNegativeCoords(unittest.TestCase):

    def runTest(self):
        p = scourXmlFile('unittests/polygon-coord-neg.svg').getElementsByTagNameNS(SVGNS, 'polygon')[0]
        #  points="100,-100,100-100,100-100-100,-100-100,200" />
        self.assertEqual(p.getAttribute('points'), '100 -100 100 -100 100 -100 -100 -100 -100 200',
                         'Negative polygon coordinates not properly parsed')


class ScourPolylineNegativeCoords(unittest.TestCase):

    def runTest(self):
        p = scourXmlFile('unittests/polyline-coord-neg.svg').getElementsByTagNameNS(SVGNS, 'polyline')[0]
        self.assertEqual(p.getAttribute('points'), '100 -100 100 -100 100 -100 -100 -100 -100 200',
                         'Negative polyline coordinates not properly parsed')


class ScourPolygonNegativeCoordFirst(unittest.TestCase):

    def runTest(self):
        p = scourXmlFile('unittests/polygon-coord-neg-first.svg').getElementsByTagNameNS(SVGNS, 'polygon')[0]
        #  points="-100,-100,100-100,100-100-100,-100-100,200" />
        self.assertEqual(p.getAttribute('points'), '-100 -100 100 -100 100 -100 -100 -100 -100 200',
                         'Negative polygon coordinates not properly parsed')


class ScourPolylineNegativeCoordFirst(unittest.TestCase):

    def runTest(self):
        p = scourXmlFile('unittests/polyline-coord-neg-first.svg').getElementsByTagNameNS(SVGNS, 'polyline')[0]
        self.assertEqual(p.getAttribute('points'), '-100 -100 100 -100 100 -100 -100 -100 -100 200',
                         'Negative polyline coordinates not properly parsed')


class DoNotRemoveGroupsWithIDsInDefs(unittest.TestCase):

    def runTest(self):
        f = scourXmlFile('unittests/important-groups-in-defs.svg')
        self.assertEqual(len(f.getElementsByTagNameNS(SVGNS, 'linearGradient')), 1,
                         'Group in defs with id\'ed element removed')


class AlwaysKeepClosePathSegments(unittest.TestCase):

    def runTest(self):
        p = scourXmlFile('unittests/path-with-closepath.svg').getElementsByTagNameNS(SVGNS, 'path')[0]
        self.assertEqual(p.getAttribute('d'), 'm10 10h100v100h-100z',
                         'Path with closepath not preserved')


class RemoveDuplicateLinearGradients(unittest.TestCase):

    def runTest(self):
        svgdoc = scourXmlFile('unittests/remove-duplicate-gradients.svg')
        lingrads = svgdoc.getElementsByTagNameNS(SVGNS, 'linearGradient')
        self.assertEqual(1, lingrads.length,
                         'Duplicate linear gradient not removed')


class RereferenceForLinearGradient(unittest.TestCase):

    def runTest(self):
        svgdoc = scourXmlFile('unittests/remove-duplicate-gradients.svg')
        rects = svgdoc.getElementsByTagNameNS(SVGNS, 'rect')
        self.assertEqual(rects[0].getAttribute('fill'), rects[1].getAttribute('stroke'),
                         'Reference not updated after removing duplicate linear gradient')
        self.assertEqual(rects[0].getAttribute('fill'), rects[4].getAttribute('fill'),
                         'Reference not updated after removing duplicate linear gradient')


class RemoveDuplicateRadialGradients(unittest.TestCase):

    def runTest(self):
        svgdoc = scourXmlFile('unittests/remove-duplicate-gradients.svg')
        radgrads = svgdoc.getElementsByTagNameNS(SVGNS, 'radialGradient')
        self.assertEqual(1, radgrads.length,
                         'Duplicate radial gradient not removed')


class RemoveDuplicateRadialGradientsEnsureMasterHasID(unittest.TestCase):

    def runTest(self):
        svgdoc = scourXmlFile('unittests/remove-duplicate-gradients-master-without-id.svg')
        lingrads = svgdoc.getElementsByTagNameNS(SVGNS, 'linearGradient')
        rect = svgdoc.getElementById('r1')
        self.assertEqual(1, lingrads.length,
                         'Duplicate linearGradient not removed')
        self.assertEqual(lingrads[0].getAttribute("id"), "g1",
                         "linearGradient has a proper ID")
        self.assertNotEqual(rect.getAttribute("fill"), "url(#)",
                            "linearGradient has a proper ID")


class RereferenceForRadialGradient(unittest.TestCase):

    def runTest(self):
        svgdoc = scourXmlFile('unittests/remove-duplicate-gradients.svg')
        rects = svgdoc.getElementsByTagNameNS(SVGNS, 'rect')
        self.assertEqual(rects[2].getAttribute('stroke'), rects[3].getAttribute('fill'),
                         'Reference not updated after removing duplicate radial gradient')


class RereferenceForGradientWithFallback(unittest.TestCase):

    def runTest(self):
        svgdoc = scourXmlFile('unittests/remove-duplicate-gradients.svg')
        rects = svgdoc.getElementsByTagNameNS(SVGNS, 'rect')
        self.assertEqual(rects[0].getAttribute('fill') + ' #fff', rects[5].getAttribute('fill'),
                         'Reference (with fallback) not updated after removing duplicate linear gradient')


class CollapseSamePathPoints(unittest.TestCase):

    def runTest(self):
        p = scourXmlFile('unittests/collapse-same-path-points.svg').getElementsByTagNameNS(SVGNS, 'path')[0]
        self.assertEqual(p.getAttribute('d'), "m100 100 100.12 100.12c14.877 4.8766-15.123-5.1234 0 0z",
                         'Did not collapse same path points')


class ScourUnitlessLengths(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/scour-lengths.svg')
        r = doc.getElementsByTagNameNS(SVGNS, 'rect')[0]
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
        r = scourXmlFile('unittests/scour-lengths.svg').getElementsByTagNameNS(SVGNS, 'rect')[1]
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
        doc = scourXmlFile('unittests/redundant-svg-namespace.svg').documentElement
        self.assertNotEqual(doc.getAttribute('xmlns:svg'), 'http://www.w3.org/2000/svg',
                            'Redundant svg namespace declaration not removed')


class RemoveRedundantSvgNamespacePrefix(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/redundant-svg-namespace.svg').documentElement
        r = doc.getElementsByTagNameNS(SVGNS, 'rect')[1]
        self.assertEqual(r.tagName, 'rect',
                         'Redundant svg: prefix not removed from rect')
        t = doc.getElementsByTagNameNS(SVGNS, 'text')[0]
        self.assertEqual(t.tagName, 'text',
                         'Redundant svg: prefix not removed from text')

        # Regression test for #239
        self.assertEqual(t.getAttribute('xml:space'), 'preserve',
                         'Required xml: prefix removed in error')
        self.assertEqual(t.getAttribute("space"), '',
                         'Required xml: prefix removed in error')


class RemoveDefaultGradX1Value(unittest.TestCase):

    def runTest(self):
        g = scourXmlFile('unittests/gradient-default-attrs.svg').getElementById('grad1')
        self.assertEqual(g.getAttribute('x1'), '',
                         'x1="0" not removed')


class RemoveDefaultGradY1Value(unittest.TestCase):

    def runTest(self):
        g = scourXmlFile('unittests/gradient-default-attrs.svg').getElementById('grad1')
        self.assertEqual(g.getAttribute('y1'), '',
                         'y1="0" not removed')


class RemoveDefaultGradX2Value(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/gradient-default-attrs.svg')
        self.assertEqual(doc.getElementById('grad1').getAttribute('x2'), '',
                         'x2="100%" not removed')
        self.assertEqual(doc.getElementById('grad1b').getAttribute('x2'), '',
                         'x2="1" not removed, '
                         'which is equal to the default x2="100%" when gradientUnits="objectBoundingBox"')
        self.assertNotEqual(doc.getElementById('grad1c').getAttribute('x2'), '',
                            'x2="1" removed, '
                            'which is NOT equal to the default x2="100%" when gradientUnits="userSpaceOnUse"')


class RemoveDefaultGradY2Value(unittest.TestCase):

    def runTest(self):
        g = scourXmlFile('unittests/gradient-default-attrs.svg').getElementById('grad1')
        self.assertEqual(g.getAttribute('y2'), '',
                         'y2="0" not removed')


class RemoveDefaultGradGradientUnitsValue(unittest.TestCase):

    def runTest(self):
        g = scourXmlFile('unittests/gradient-default-attrs.svg').getElementById('grad1')
        self.assertEqual(g.getAttribute('gradientUnits'), '',
                         'gradientUnits="objectBoundingBox" not removed')


class RemoveDefaultGradSpreadMethodValue(unittest.TestCase):

    def runTest(self):
        g = scourXmlFile('unittests/gradient-default-attrs.svg').getElementById('grad1')
        self.assertEqual(g.getAttribute('spreadMethod'), '',
                         'spreadMethod="pad" not removed')


class RemoveDefaultGradCXValue(unittest.TestCase):

    def runTest(self):
        g = scourXmlFile('unittests/gradient-default-attrs.svg').getElementById('grad2')
        self.assertEqual(g.getAttribute('cx'), '',
                         'cx="50%" not removed')


class RemoveDefaultGradCYValue(unittest.TestCase):

    def runTest(self):
        g = scourXmlFile('unittests/gradient-default-attrs.svg').getElementById('grad2')
        self.assertEqual(g.getAttribute('cy'), '',
                         'cy="50%" not removed')


class RemoveDefaultGradRValue(unittest.TestCase):

    def runTest(self):
        g = scourXmlFile('unittests/gradient-default-attrs.svg').getElementById('grad2')
        self.assertEqual(g.getAttribute('r'), '',
                         'r="50%" not removed')


class RemoveDefaultGradFXValue(unittest.TestCase):

    def runTest(self):
        g = scourXmlFile('unittests/gradient-default-attrs.svg').getElementById('grad2')
        self.assertEqual(g.getAttribute('fx'), '',
                         'fx matching cx not removed')


class RemoveDefaultGradFYValue(unittest.TestCase):

    def runTest(self):
        g = scourXmlFile('unittests/gradient-default-attrs.svg').getElementById('grad2')
        self.assertEqual(g.getAttribute('fy'), '',
                         'fy matching cy not removed')


class RemoveDefaultAttributeOrderSVGLengthCrash(unittest.TestCase):

    # Triggered a crash in v0.36
    def runTest(self):
        try:
            scourXmlFile('unittests/remove-default-attr-order.svg')
        except AttributeError:
            self.fail("Processing the order attribute triggered an AttributeError")


class RemoveDefaultAttributeStdDeviationSVGLengthCrash(unittest.TestCase):

    # Triggered a crash in v0.36
    def runTest(self):
        try:
            scourXmlFile('unittests/remove-default-attr-std-deviation.svg')
        except AttributeError:
            self.fail("Processing the order attribute triggered an AttributeError")


class CDATAInXml(unittest.TestCase):

    def runTest(self):
        with open('unittests/cdata.svg') as f:
            lines = scourString(f.read()).splitlines()
        self.assertEqual(lines[3],
                         "  	alert('pb&j');",
                         'CDATA did not come out correctly')


class WellFormedXMLLesserThanInAttrValue(unittest.TestCase):

    def runTest(self):
        with open('unittests/xml-well-formed.svg') as f:
            wellformed = scourString(f.read())
        self.assertTrue(wellformed.find('unicode="&lt;"') != -1,
                        "Improperly serialized &lt; in attribute value")


class WellFormedXMLAmpersandInAttrValue(unittest.TestCase):

    def runTest(self):
        with open('unittests/xml-well-formed.svg') as f:
            wellformed = scourString(f.read())
        self.assertTrue(wellformed.find('unicode="&amp;"') != -1,
                        'Improperly serialized &amp; in attribute value')


class WellFormedXMLLesserThanInTextContent(unittest.TestCase):

    def runTest(self):
        with open('unittests/xml-well-formed.svg') as f:
            wellformed = scourString(f.read())
        self.assertTrue(wellformed.find('<title>2 &lt; 5</title>') != -1,
                        'Improperly serialized &lt; in text content')


class WellFormedXMLAmpersandInTextContent(unittest.TestCase):

    def runTest(self):
        with open('unittests/xml-well-formed.svg') as f:
            wellformed = scourString(f.read())
        self.assertTrue(wellformed.find('<desc>Peanut Butter &amp; Jelly</desc>') != -1,
                        'Improperly serialized &amp; in text content')


class WellFormedXMLNamespacePrefixRemoveUnused(unittest.TestCase):

    def runTest(self):
        with open('unittests/xml-well-formed.svg') as f:
            wellformed = scourString(f.read())
        self.assertTrue(wellformed.find('xmlns:foo=') == -1,
                        'Improperly serialized namespace prefix declarations: Unused namespace decaration not removed')


class WellFormedXMLNamespacePrefixKeepUsedElementPrefix(unittest.TestCase):

    def runTest(self):
        with open('unittests/xml-well-formed.svg') as f:
            wellformed = scourString(f.read())
        self.assertTrue(wellformed.find('xmlns:bar=') != -1,
                        'Improperly serialized namespace prefix declarations: Used element prefix removed')


class WellFormedXMLNamespacePrefixKeepUsedAttributePrefix(unittest.TestCase):

    def runTest(self):
        with open('unittests/xml-well-formed.svg') as f:
            wellformed = scourString(f.read())
        self.assertTrue(wellformed.find('xmlns:baz=') != -1,
                        'Improperly serialized namespace prefix declarations: Used attribute prefix removed')


class NamespaceDeclPrefixesInXMLWhenNotInDefaultNamespace(unittest.TestCase):

    def runTest(self):
        with open('unittests/xml-ns-decl.svg') as f:
            xmlstring = scourString(f.read())
        self.assertTrue(xmlstring.find('xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"') != -1,
                        'Improperly serialized namespace prefix declarations when not in default namespace')


class MoveSVGElementsToDefaultNamespace(unittest.TestCase):

    def runTest(self):
        with open('unittests/xml-ns-decl.svg') as f:
            xmlstring = scourString(f.read())
        self.assertTrue(xmlstring.find('<rect ') != -1,
                        'Did not bring SVG elements into the default namespace')


class MoveCommonAttributesToParent(unittest.TestCase):

    def runTest(self):
        g = scourXmlFile('unittests/move-common-attributes-to-parent.svg') \
                 .getElementsByTagNameNS(SVGNS, 'g')[0]
        self.assertEqual(g.getAttribute('fill'), '#0F0',
                         'Did not move common fill attribute to parent group')


class RemoveCommonAttributesFromChild(unittest.TestCase):

    def runTest(self):
        r = scourXmlFile('unittests/move-common-attributes-to-parent.svg') \
                 .getElementsByTagNameNS(SVGNS, 'rect')[0]
        self.assertNotEqual(r.getAttribute('fill'), '#0F0',
                            'Did not remove common fill attribute from child')


class DontRemoveCommonAttributesIfParentHasTextNodes(unittest.TestCase):

    def runTest(self):
        text = scourXmlFile('unittests/move-common-attributes-to-parent.svg') \
                    .getElementsByTagNameNS(SVGNS, 'text')[0]
        self.assertNotEqual(text.getAttribute('font-style'), 'italic',
                            'Removed common attributes when parent contained text elements')


class PropagateCommonAttributesUp(unittest.TestCase):

    def runTest(self):
        g = scourXmlFile('unittests/move-common-attributes-to-grandparent.svg') \
                 .getElementsByTagNameNS(SVGNS, 'g')[0]
        self.assertEqual(g.getAttribute('fill'), '#0F0',
                         'Did not move common fill attribute to grandparent')


class RemoveUnusedAttributesOnParent(unittest.TestCase):

    def runTest(self):
        g = scourXmlFile('unittests/remove-unused-attributes-on-parent.svg') \
                 .getElementsByTagNameNS(SVGNS, 'g')[0]
        self.assertNotEqual(g.getAttribute('stroke'), '#000',
                            'Unused attributes on group not removed')


class DoNotRemoveCommonAttributesOnParentIfAtLeastOneUsed(unittest.TestCase):

    def runTest(self):
        g = scourXmlFile('unittests/remove-unused-attributes-on-parent.svg') \
                 .getElementsByTagNameNS(SVGNS, 'g')[0]
        self.assertEqual(g.getAttribute('fill'), '#0F0',
                         'Used attributes on group were removed')


class DoNotRemoveGradientsWhenReferencedInStyleCss(unittest.TestCase):

    def runTest(self):
        grads = scourXmlFile('unittests/css-reference.svg') \
                     .getElementsByTagNameNS(SVGNS, 'linearGradient')
        self.assertEqual(grads.length, 2,
                         'Gradients removed when referenced in CSS')


class Whitespace(unittest.TestCase):

    def setUp(self):
        self.doc = scourXmlFile('unittests/whitespace.svg')

    def test_basic(self):
        text = self.doc.getElementById('txt_a1')
        self.assertIn('text1 text2', text.toxml(),
                      'Multiple spaces not stripped from text element')
        text = self.doc.getElementById('txt_a2')
        self.assertIn('text1 text2', text.toxml(),
                      'Tab not replaced with space in text element')
        text = self.doc.getElementById('txt_a3')
        self.assertIn('text1 text2', text.toxml(),
                      'Multiple spaces not stripped from text element with xml:space="default"')
        text = self.doc.getElementById('txt_a4')
        self.assertIn('text1 text2', text.toxml(),
                      'Tab not replaced with space in text element with xml:space="default"')
        text = self.doc.getElementById('txt_a5')
        self.assertIn('text1    text2', text.toxml(),
                      'Multiple spaces not preserved in text element with xml:space="preserve"')
        text = self.doc.getElementById('txt_a6')
        self.assertIn('text1\ttext2', text.toxml(),
                      'Tab not preserved in text element with xml:space="preserve"')

    def test_newlines(self):
        text = self.doc.getElementById('txt_b1')
        self.assertIn('text1 text2', text.toxml(),
                      'Newline not replaced with space in text element')
        text = self.doc.getElementById('txt_b2')
        self.assertIn('text1 text2', text.toxml(),
                      'Newline not replaced with space in text element with xml:space="default"')
        text = self.doc.getElementById('txt_b3')
        self.assertIn('text1\n       text2', text.toxml(),
                      'Newline not preserved in text element with xml:space="preserve"')

    def test_inheritance(self):
        text = self.doc.getElementById('txt_c1')
        self.assertIn('text1    text2', text.toxml(),
                      '<tspan> does not inherit xml:space="preserve" of parent text element')
        text = self.doc.getElementById('txt_c2')
        self.assertIn('text1 text2', text.toxml(),
                      'xml:space="default" of <tspan> does not overwrite xml:space="preserve" of parent text element')
        text = self.doc.getElementById('txt_c3')
        self.assertIn('text1    text2', text.toxml(),
                      'xml:space="preserve" of <tspan> does not overwrite xml:space="default" of parent text element')
        text = self.doc.getElementById('txt_c4')
        self.assertIn('text1    text2', text.toxml(),
                      '<text> does not inherit xml:space="preserve" of parent group')
        text = self.doc.getElementById('txt_c5')
        self.assertIn('text1 text2', text.toxml(),
                      'xml:space="default" of text element does not overwrite xml:space="preserve" of parent group')
        text = self.doc.getElementById('txt_c6')
        self.assertIn('text1    text2', text.toxml(),
                      'xml:space="preserve" of text element does not overwrite xml:space="default" of parent group')

    def test_important_whitespace(self):
        text = self.doc.getElementById('txt_d1')
        self.assertIn('text1 text2', text.toxml(),
                      'Newline with whitespace collapsed in text element')
        text = self.doc.getElementById('txt_d2')
        self.assertIn('text1 <tspan>tspan1</tspan> text2', text.toxml(),
                      'Whitespace stripped from the middle of a text element')
        text = self.doc.getElementById('txt_d3')
        self.assertIn('text1 <tspan>tspan1 <tspan>tspan2</tspan> text2</tspan>', text.toxml(),
                      'Whitespace stripped from the middle of a text element')

    def test_incorrect_whitespace(self):
        text = self.doc.getElementById('txt_e1')
        self.assertIn('text1text2', text.toxml(),
                      'Whitespace introduced in text element with newline')
        text = self.doc.getElementById('txt_e2')
        self.assertIn('text1<tspan>tspan</tspan>text2', text.toxml(),
                      'Whitespace introduced in text element with <tspan>')
        text = self.doc.getElementById('txt_e3')
        self.assertIn('text1<tspan>tspan</tspan>text2', text.toxml(),
                      'Whitespace introduced in text element with <tspan> and newlines')


class GetAttrPrefixRight(unittest.TestCase):

    def runTest(self):
        grad = scourXmlFile('unittests/xml-namespace-attrs.svg') \
                    .getElementsByTagNameNS(SVGNS, 'linearGradient')[1]
        self.assertEqual(grad.getAttributeNS('http://www.w3.org/1999/xlink', 'href'), '#linearGradient841',
                         'Did not get xlink:href prefix right')


class EnsurePreserveWhitespaceOnNonTextElements(unittest.TestCase):

    def runTest(self):
        with open('unittests/no-collapse-lines.svg') as f:
            s = scourString(f.read())
        self.assertEqual(len(s.splitlines()), 6,
                         'Did not properly preserve whitespace on elements even if they were not textual')


class HandleEmptyStyleElement(unittest.TestCase):

    def runTest(self):
        try:
            styles = scourXmlFile('unittests/empty-style.svg').getElementsByTagNameNS(SVGNS, 'style')
            fail = len(styles) != 1
        except AttributeError:
            fail = True
        self.assertEqual(fail, False,
                         'Could not handle an empty style element')


class EnsureLineEndings(unittest.TestCase):

    def runTest(self):
        with open('unittests/newlines.svg') as f:
            s = scourString(f.read())
        self.assertEqual(len(s.splitlines()), 24,
                         'Did handle reading or outputting line ending characters correctly')


class XmlEntities(unittest.TestCase):

    def runTest(self):
        self.assertEqual(make_well_formed('<>&'), '&lt;&gt;&amp;',
                         'Incorrectly translated unquoted XML entities')
        self.assertEqual(make_well_formed('<>&', XML_ENTS_ESCAPE_APOS), '&lt;&gt;&amp;',
                         'Incorrectly translated single-quoted XML entities')
        self.assertEqual(make_well_formed('<>&', XML_ENTS_ESCAPE_QUOT), '&lt;&gt;&amp;',
                         'Incorrectly translated double-quoted XML entities')

        self.assertEqual(make_well_formed("'"), "'",
                         'Incorrectly translated unquoted single quote')
        self.assertEqual(make_well_formed('"'), '"',
                         'Incorrectly translated unquoted double quote')

        self.assertEqual(make_well_formed("'", XML_ENTS_ESCAPE_QUOT), "'",
                         'Incorrectly translated double-quoted single quote')
        self.assertEqual(make_well_formed('"', XML_ENTS_ESCAPE_APOS), '"',
                         'Incorrectly translated single-quoted double quote')

        self.assertEqual(make_well_formed("'", XML_ENTS_ESCAPE_APOS), '&apos;',
                         'Incorrectly translated single-quoted single quote')
        self.assertEqual(make_well_formed('"', XML_ENTS_ESCAPE_QUOT), '&quot;',
                         'Incorrectly translated double-quoted double quote')


class HandleQuotesInAttributes(unittest.TestCase):

    def runTest(self):
        with open('unittests/entities.svg', "rb") as f:
            output = scourString(f.read())
        self.assertTrue('a="\'"' in output,
                        'Failed on attribute value with non-double quote')
        self.assertTrue("b='\"'" in output,
                        'Failed on attribute value with non-single quote')
        self.assertTrue("c=\"''&quot;\"" in output,
                        'Failed on attribute value with more single quotes than double quotes')
        self.assertTrue('d=\'""&apos;\'' in output,
                        'Failed on attribute value with more double quotes than single quotes')
        self.assertTrue("e=\"''&quot;&quot;\"" in output,
                        'Failed on attribute value with the same number of double quotes as single quotes')


class PreserveQuotesInStyles(unittest.TestCase):

    def runTest(self):
        with open('unittests/quotes-in-styles.svg', "rb") as f:
            output = scourString(f.read())
        self.assertTrue('use[id="t"]' in output,
                        'Failed to preserve quote characters in a style element')
        self.assertTrue("'Times New Roman'" in output,
                        'Failed to preserve quote characters in a style attribute')


class DoNotStripCommentsOutsideOfRoot(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/comments.svg')
        self.assertEqual(doc.childNodes.length, 4,
                         'Did not include all comment children outside of root')
        self.assertEqual(doc.childNodes[0].nodeType, 8, 'First node not a comment')
        self.assertEqual(doc.childNodes[1].nodeType, 8, 'Second node not a comment')
        self.assertEqual(doc.childNodes[3].nodeType, 8, 'Fourth node not a comment')


class DoNotStripDoctype(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/doctype.svg')
        self.assertEqual(doc.childNodes.length, 3,
                         'Did not include the DOCROOT')
        self.assertEqual(doc.childNodes[0].nodeType, 8, 'First node not a comment')
        self.assertEqual(doc.childNodes[1].nodeType, 10, 'Second node not a doctype')
        self.assertEqual(doc.childNodes[2].nodeType, 1, 'Third node not the root node')


class PathImplicitLineWithMoveCommands(unittest.TestCase):

    def runTest(self):
        path = scourXmlFile('unittests/path-implicit-line.svg').getElementsByTagNameNS(SVGNS, 'path')[0]
        self.assertEqual(path.getAttribute('d'), "m100 100v100m200-100h-200m200 100v-100",
                         "Implicit line segments after move not preserved")


class RemoveTitlesOption(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/full-descriptive-elements.svg',
                           parse_args(['--remove-titles']))
        self.assertEqual(doc.childNodes.length, 1,
                         'Did not remove <title> tag with --remove-titles')


class RemoveDescriptionsOption(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/full-descriptive-elements.svg',
                           parse_args(['--remove-descriptions']))
        self.assertEqual(doc.childNodes.length, 1,
                         'Did not remove <desc> tag with --remove-descriptions')


class RemoveMetadataOption(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/full-descriptive-elements.svg',
                           parse_args(['--remove-metadata']))
        self.assertEqual(doc.childNodes.length, 1,
                         'Did not remove <metadata> tag with --remove-metadata')


class RemoveDescriptiveElementsOption(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/full-descriptive-elements.svg',
                           parse_args(['--remove-descriptive-elements']))
        self.assertEqual(doc.childNodes.length, 1,
                         'Did not remove <title>, <desc> and <metadata> tags with --remove-descriptive-elements')


class EnableCommentStrippingOption(unittest.TestCase):

    def runTest(self):
        with open('unittests/comment-beside-xml-decl.svg') as f:
            docStr = f.read()
        docStr = scourString(docStr,
                             parse_args(['--enable-comment-stripping']))
        self.assertEqual(docStr.find('<!--'), -1,
                         'Did not remove document-level comment with --enable-comment-stripping')


class StripXmlPrologOption(unittest.TestCase):

    def runTest(self):
        with open('unittests/comment-beside-xml-decl.svg') as f:
            docStr = f.read()
        docStr = scourString(docStr,
                             parse_args(['--strip-xml-prolog']))
        self.assertEqual(docStr.find('<?xml'), -1,
                         'Did not remove <?xml?> with --strip-xml-prolog')


class ShortenIDsOption(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/shorten-ids.svg',
                           parse_args(['--shorten-ids']))
        gradientTag = doc.getElementsByTagName('linearGradient')[0]
        self.assertEqual(gradientTag.getAttribute('id'), 'a',
                         "Did not shorten a linear gradient's ID with --shorten-ids")
        rectTag = doc.getElementsByTagName('rect')[0]
        self.assertEqual(rectTag.getAttribute('fill'), 'url(#a)',
                         'Did not update reference to shortened ID')


class ShortenIDsStableOutput(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/shorten-ids-stable-output.svg',
                           parse_args(['--shorten-ids']))
        use_tags = doc.getElementsByTagName('use')
        hrefs_ordered = [x.getAttributeNS('http://www.w3.org/1999/xlink', 'href')
                         for x in use_tags]
        expected = ['#a', '#b', '#b']
        self.assertEqual(hrefs_ordered, expected,
                         '--shorten-ids pointlessly reassigned ids')


class MustKeepGInSwitch(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/groups-in-switch.svg')
        self.assertEqual(doc.getElementsByTagName('g').length, 1,
                         'Erroneously removed a <g> in a <switch>')


class MustKeepGInSwitch2(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/groups-in-switch-with-id.svg',
                           parse_args(['--enable-id-stripping']))
        self.assertEqual(doc.getElementsByTagName('g').length, 1,
                         'Erroneously removed a <g> in a <switch>')


class GroupSiblingMerge(unittest.TestCase):

    def test_sibling_merge(self):
        doc = scourXmlFile('unittests/group-sibling-merge.svg',
                           parse_args([]))
        self.assertEqual(doc.getElementsByTagName('g').length, 5,
                         'Merged sibling <g> tags with similar values')

    def test_sibling_merge_disabled(self):
        doc = scourXmlFile('unittests/group-sibling-merge.svg',
                           parse_args(['--disable-group-collapsing']))
        self.assertEqual(doc.getElementsByTagName('g').length, 8,
                         'Sibling merging is disabled by --disable-group-collapsing')

    def test_sibling_merge_crash(self):
        doc = scourXmlFile('unittests/group-sibling-merge-crash.svg',
                           parse_args(['']))
        self.assertEqual(doc.getElementsByTagName('g').length, 1,
                         'Sibling merge should work without causing crashes')


class GroupCreation(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/group-creation.svg',
                           parse_args(['--create-groups']))
        self.assertEqual(doc.getElementsByTagName('g').length, 1,
                         'Did not create a <g> for a run of elements having similar attributes')


class GroupCreationForInheritableAttributesOnly(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/group-creation.svg',
                           parse_args(['--create-groups']))
        self.assertEqual(doc.getElementsByTagName('g').item(0).getAttribute('y'), '',
                         'Promoted the uninheritable attribute y to a <g>')


class GroupNoCreation(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/group-no-creation.svg',
                           parse_args(['--create-groups']))
        self.assertEqual(doc.getElementsByTagName('g').length, 0,
                         'Created a <g> for a run of elements having dissimilar attributes')


class GroupNoCreationForTspan(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/group-no-creation-tspan.svg',
                           parse_args(['--create-groups']))
        self.assertEqual(doc.getElementsByTagName('g').length, 0,
                         'Created a <g> for a run of <tspan>s '
                         'that are not allowed as children according to content model')


class DoNotCommonizeAttributesOnReferencedElements(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/commonized-referenced-elements.svg')
        self.assertEqual(doc.getElementsByTagName('circle')[0].getAttribute('fill'), '#0f0',
                         'Grouped an element referenced elsewhere into a <g>')


class DoNotRemoveOverflowVisibleOnMarker(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/overflow-marker.svg')
        self.assertEqual(doc.getElementById('m1').getAttribute('overflow'), 'visible',
                         'Removed the overflow attribute when it was not using the default value')
        self.assertEqual(doc.getElementById('m2').getAttribute('overflow'), '',
                         'Did not remove the overflow attribute when it was using the default value')


class DoNotRemoveOrientAutoOnMarker(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/orient-marker.svg')
        self.assertEqual(doc.getElementById('m1').getAttribute('orient'), 'auto',
                         'Removed the orient attribute when it was not using the default value')
        self.assertEqual(doc.getElementById('m2').getAttribute('orient'), '',
                         'Did not remove the orient attribute when it was using the default value')


class MarkerOnSvgElements(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/overflow-svg.svg')
        self.assertEqual(doc.getElementsByTagName('svg')[0].getAttribute('overflow'), '',
                         'Did not remove the overflow attribute when it was using the default value')
        self.assertEqual(doc.getElementsByTagName('svg')[1].getAttribute('overflow'), '',
                         'Did not remove the overflow attribute when it was using the default value')
        self.assertEqual(doc.getElementsByTagName('svg')[2].getAttribute('overflow'), 'visible',
                         'Removed the overflow attribute when it was not using the default value')


class GradientReferencedByStyleCDATA(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/style-cdata.svg')
        self.assertEqual(len(doc.getElementsByTagName('linearGradient')), 1,
                         'Removed a gradient referenced by an internal stylesheet')


class ShortenIDsInStyleCDATA(unittest.TestCase):

    def runTest(self):
        with open('unittests/style-cdata.svg') as f:
            docStr = f.read()
        docStr = scourString(docStr,
                             parse_args(['--shorten-ids']))
        self.assertEqual(docStr.find('somethingreallylong'), -1,
                         'Did not shorten IDs in the internal stylesheet')


class StyleToAttr(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/style-to-attr.svg')
        line = doc.getElementsByTagName('line')[0]
        self.assertEqual(line.getAttribute('stroke'), '#000')
        self.assertEqual(line.getAttribute('marker-start'), 'url(#m)')
        self.assertEqual(line.getAttribute('marker-mid'), 'url(#m)')
        self.assertEqual(line.getAttribute('marker-end'), 'url(#m)')


class PathCommandRewrites(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/path-command-rewrites.svg')
        paths = doc.getElementsByTagName('path')
        expected_paths = [
            ('m100 100 200 100', "Trailing m0 0z not removed"),
            ('m100 100v200m0 0 100 100z', "Mangled m0 0 100 100"),
            ("m100 100v200m0 0 2-1-2 1z", "Should have removed empty m0 0"),
            ("m100 100v200l3-5-5 3m0 0 2-1-2 1z", "Rewrite m0 0 3-5-5 3 ... -> l3-5-5 3 ..."),
            ("m100 100v200m0 0 3-5-5 3zm0 0 2-1-2 1z", "No rewrite of m0 0 3-5-5 3z"),
        ]
        self.assertEqual(len(paths), len(expected_paths), "len(actual_paths) != len(expected_paths)")
        for i in range(len(paths)):
            actual_path = paths[i].getAttribute('d')
            expected_path, message = expected_paths[i]
            self.assertEqual(actual_path,
                             expected_path,
                             '%s: "%s" != "%s"' % (message, actual_path, expected_path))


class DefaultsRemovalToplevel(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/cascading-default-attribute-removal.svg')
        self.assertEqual(doc.getElementsByTagName('path')[1].getAttribute('fill-rule'), '',
                         'Default attribute fill-rule:nonzero not removed')


class DefaultsRemovalToplevelInverse(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/cascading-default-attribute-removal.svg')
        self.assertEqual(doc.getElementsByTagName('path')[0].getAttribute('fill-rule'), 'evenodd',
                         'Non-Default attribute fill-rule:evenodd removed')


class DefaultsRemovalToplevelFormat(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/cascading-default-attribute-removal.svg')
        self.assertEqual(doc.getElementsByTagName('path')[0].getAttribute('stroke-width'), '',
                         'Default attribute stroke-width:1.00 not removed')


class DefaultsRemovalInherited(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/cascading-default-attribute-removal.svg')
        self.assertEqual(doc.getElementsByTagName('path')[3].getAttribute('fill-rule'), '',
                         'Default attribute fill-rule:nonzero not removed in child')


class DefaultsRemovalInheritedInverse(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/cascading-default-attribute-removal.svg')
        self.assertEqual(doc.getElementsByTagName('path')[2].getAttribute('fill-rule'), 'evenodd',
                         'Non-Default attribute fill-rule:evenodd removed in child')


class DefaultsRemovalInheritedFormat(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/cascading-default-attribute-removal.svg')
        self.assertEqual(doc.getElementsByTagName('path')[2].getAttribute('stroke-width'), '',
                         'Default attribute stroke-width:1.00 not removed in child')


class DefaultsRemovalOverwrite(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/cascading-default-attribute-removal.svg')
        self.assertEqual(doc.getElementsByTagName('path')[5].getAttribute('fill-rule'), 'nonzero',
                         'Default attribute removed, although it overwrites parent element')


class DefaultsRemovalOverwriteMarker(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/cascading-default-attribute-removal.svg')
        self.assertEqual(doc.getElementsByTagName('path')[4].getAttribute('marker-start'), 'none',
                         'Default marker attribute removed, although it overwrites parent element')


class DefaultsRemovalNonOverwrite(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/cascading-default-attribute-removal.svg')
        self.assertEqual(doc.getElementsByTagName('path')[10].getAttribute('fill-rule'), '',
                         'Default attribute not removed, although its parent used default')


class RemoveDefsWithUnreferencedElements(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/useless-defs.svg')
        self.assertEqual(doc.getElementsByTagName('defs').length, 0,
                         'Kept defs, although it contains only unreferenced elements')


class RemoveDefsWithWhitespace(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/whitespace-defs.svg')
        self.assertEqual(doc.getElementsByTagName('defs').length, 0,
                         'Kept defs, although it contains only whitespace or is <defs/>')


class TransformIdentityMatrix(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/transform-matrix-is-identity.svg')
        self.assertEqual(doc.getElementsByTagName('line')[0].getAttribute('transform'), '',
                         'Transform containing identity matrix not removed')


class TransformRotate135(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/transform-matrix-is-rotate-135.svg')
        self.assertEqual(doc.getElementsByTagName('line')[0].getAttribute('transform'), 'rotate(135)',
                         'Rotation matrix not converted to rotate(135)')


class TransformRotate45(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/transform-matrix-is-rotate-45.svg')
        self.assertEqual(doc.getElementsByTagName('line')[0].getAttribute('transform'), 'rotate(45)',
                         'Rotation matrix not converted to rotate(45)')


class TransformRotate90(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/transform-matrix-is-rotate-90.svg')
        self.assertEqual(doc.getElementsByTagName('line')[0].getAttribute('transform'), 'rotate(90)',
                         'Rotation matrix not converted to rotate(90)')


class TransformRotateCCW135(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/transform-matrix-is-rotate-225.svg')
        self.assertEqual(doc.getElementsByTagName('line')[0].getAttribute('transform'), 'rotate(225)',
                         'Counter-clockwise rotation matrix not converted to rotate(225)')


class TransformRotateCCW45(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/transform-matrix-is-rotate-neg-45.svg')
        self.assertEqual(doc.getElementsByTagName('line')[0].getAttribute('transform'), 'rotate(-45)',
                         'Counter-clockwise rotation matrix not converted to rotate(-45)')


class TransformRotateCCW90(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/transform-matrix-is-rotate-neg-90.svg')
        self.assertEqual(doc.getElementsByTagName('line')[0].getAttribute('transform'), 'rotate(-90)',
                         'Counter-clockwise rotation matrix not converted to rotate(-90)')


class TransformScale2by3(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/transform-matrix-is-scale-2-3.svg')
        self.assertEqual(doc.getElementsByTagName('line')[0].getAttribute('transform'), 'scale(2 3)',
                         'Scaling matrix not converted to scale(2 3)')


class TransformScaleMinus1(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/transform-matrix-is-scale-neg-1.svg')
        self.assertEqual(doc.getElementsByTagName('line')[0].getAttribute('transform'), 'scale(-1)',
                         'Scaling matrix not converted to scale(-1)')


class TransformTranslate(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/transform-matrix-is-translate.svg')
        self.assertEqual(doc.getElementsByTagName('line')[0].getAttribute('transform'), 'translate(2 3)',
                         'Translation matrix not converted to translate(2 3)')


class TransformRotationRange719_5(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/transform-rotate-trim-range-719.5.svg')
        self.assertEqual(doc.getElementsByTagName('line')[0].getAttribute('transform'), 'rotate(-.5)',
                         'Transform containing rotate(719.5) not shortened to rotate(-.5)')


class TransformRotationRangeCCW540_0(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/transform-rotate-trim-range-neg-540.0.svg')
        self.assertEqual(doc.getElementsByTagName('line')[0].getAttribute('transform'), 'rotate(180)',
                         'Transform containing rotate(-540.0) not shortened to rotate(180)')


class TransformRotation3Args(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/transform-rotate-fold-3args.svg')
        self.assertEqual(doc.getElementsByTagName('line')[0].getAttribute('transform'), 'rotate(90)',
                         'Optional zeroes in rotate(angle 0 0) not removed')


class TransformIdentityRotation(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/transform-rotate-is-identity.svg')
        self.assertEqual(doc.getElementsByTagName('line')[0].getAttribute('transform'), '',
                         'Transform containing identity rotation not removed')


class TransformIdentitySkewX(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/transform-skewX-is-identity.svg')
        self.assertEqual(doc.getElementsByTagName('line')[0].getAttribute('transform'), '',
                         'Transform containing identity X-axis skew not removed')


class TransformIdentitySkewY(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/transform-skewY-is-identity.svg')
        self.assertEqual(doc.getElementsByTagName('line')[0].getAttribute('transform'), '',
                         'Transform containing identity Y-axis skew not removed')


class TransformIdentityTranslate(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/transform-translate-is-identity.svg')
        self.assertEqual(doc.getElementsByTagName('line')[0].getAttribute('transform'), '',
                         'Transform containing identity translation not removed')


class TransformIdentityScale(unittest.TestCase):

    def runTest(self):
        try:
            doc = scourXmlFile('unittests/transform-scale-is-identity.svg')
        except IndexError:
            self.fail("scour failed to handled scale(1) [See GH#190]")
        self.assertEqual(doc.getElementsByTagName('line')[0].getAttribute('scale'), '',
                         'Transform containing identity translation not removed')


class DuplicateGradientsUpdateStyle(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/duplicate-gradients-update-style.svg',
                           parse_args(['--disable-style-to-xml']))
        gradient = doc.getElementsByTagName('linearGradient')[0]
        rects = doc.getElementsByTagName('rect')
        self.assertEqual('fill:url(#' + gradient.getAttribute('id') + ')', rects[0].getAttribute('style'),
                         'Either of #duplicate-one or #duplicate-two was removed, '
                         'but style="fill:" was not updated to reflect this')
        self.assertEqual('fill:url(#' + gradient.getAttribute('id') + ')', rects[1].getAttribute('style'),
                         'Either of #duplicate-one or #duplicate-two was removed, '
                         'but style="fill:" was not updated to reflect this')
        self.assertEqual('fill:url(#' + gradient.getAttribute('id') + ') #fff', rects[2].getAttribute('style'),
                         'Either of #duplicate-one or #duplicate-two was removed, '
                         'but style="fill:" (with fallback) was not updated to reflect this')


class DocWithFlowtext(unittest.TestCase):

    def runTest(self):
        with self.assertRaises(Exception):
            scourXmlFile('unittests/flowtext.svg',
                         parse_args(['--error-on-flowtext']))


class DocWithNoFlowtext(unittest.TestCase):

    def runTest(self):
        try:
            scourXmlFile('unittests/flowtext-less.svg',
                         parse_args(['--error-on-flowtext']))
        except Exception as e:
            self.fail("exception '{}' was raised, and we didn't expect that!".format(e))


class ParseStyleAttribute(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/style.svg')
        self.assertEqual(doc.documentElement.getAttribute('style'),
                         'property1:value1;property2:value2;property3:value3',
                         "Style attribute not properly parsed and/or serialized")


class StripXmlSpaceAttribute(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/xml-space.svg',
                           parse_args(['--strip-xml-space']))
        self.assertEqual(doc.documentElement.getAttribute('xml:space'), '',
                         "'xml:space' attribute not removed from root SVG element"
                         "when '--strip-xml-space' was specified")
        self.assertNotEqual(doc.getElementById('text1').getAttribute('xml:space'), '',
                            "'xml:space' attribute removed from a child element "
                            "when '--strip-xml-space' was specified (should only operate on root SVG element)")


class DoNotStripXmlSpaceAttribute(unittest.TestCase):

    def runTest(self):
        doc = scourXmlFile('unittests/xml-space.svg')
        self.assertNotEqual(doc.documentElement.getAttribute('xml:space'), '',
                            "'xml:space' attribute removed from root SVG element"
                            "when '--strip-xml-space' was NOT specified")
        self.assertNotEqual(doc.getElementById('text1').getAttribute('xml:space'), '',
                            "'xml:space' attribute removed from a child element "
                            "when '--strip-xml-space' was NOT specified (should never be removed!)")


class CommandLineUsage(unittest.TestCase):

    USAGE_STRING = "Usage: scour [INPUT.SVG [OUTPUT.SVG]] [OPTIONS]"
    MINIMAL_SVG = '<?xml version="1.0" encoding="UTF-8"?>\n' \
                  '<svg xmlns="http://www.w3.org/2000/svg"/>\n'
    TEMP_SVG_FILE = 'testscour_temp.svg'

    # wrapper function for scour.run() to emulate command line usage
    #
    # returns an object with the following attributes:
    #     status: the exit status
    #     stdout: a string representing the combined output to 'stdout'
    #     stderr: a string representing the combined output to 'stderr'
    def _run_scour(self):
        class Result(object):
            pass

        result = Result()
        try:
            run()
            result.status = 0
        except SystemExit as exception:  # catch any calls to sys.exit()
            result.status = exception.code
        result.stdout = self.temp_stdout.getvalue()
        result.stderr = self.temp_stderr.getvalue()

        return result

    def setUp(self):
        # store current values of 'argv', 'stdin', 'stdout' and 'stderr'
        self.argv = sys.argv
        self.stdin = sys.stdin
        self.stdout = sys.stdout
        self.stderr = sys.stderr

        # start with a fresh 'argv'
        sys.argv = ['scour']  # TODO: Do we need a (more) valid 'argv[0]' for anything?

        # create 'stdin', 'stdout' and 'stderr' with behavior close to the original
        # TODO: can we create file objects that behave *exactly* like the original?
        #       this is a mess since we have to ensure compatibility across Python 2 and 3 and it seems impossible
        #       to replicate all the details of 'stdin', 'stdout' and 'stderr'
        class InOutBuffer(six.StringIO, object):
            def write(self, string):
                try:
                    return super(InOutBuffer, self).write(string)
                except TypeError:
                    return super(InOutBuffer, self).write(string.decode())

        sys.stdin = self.temp_stdin = InOutBuffer()
        sys.stdout = self.temp_stdout = InOutBuffer()
        sys.stderr = self.temp_stderr = InOutBuffer()

        self.temp_stdin.name = '<stdin>'  # Scour wants to print the name of the input file...

    def tearDown(self):
        # restore previous values of 'argv', 'stdin', 'stdout' and 'stderr'
        sys.argv = self.argv
        sys.stdin = self.stdin
        sys.stdout = self.stdout
        sys.stderr = self.stderr

        # clean up
        self.temp_stdin.close()
        self.temp_stdout.close()
        self.temp_stderr.close()

    def test_no_arguments(self):
        # we have to pretend that our input stream is a TTY, otherwise Scour waits for input from stdin
        self.temp_stdin.isatty = lambda: True

        result = self._run_scour()

        self.assertEqual(result.status, 2, "Execution of 'scour' without any arguments should exit with status '2'")
        self.assertTrue(self.USAGE_STRING in result.stderr,
                        "Usage information not displayed when calling 'scour' without any arguments")

    def test_version(self):
        sys.argv.append('--version')

        result = self._run_scour()

        self.assertEqual(result.status, 0, "Execution of 'scour --version' erorred'")
        self.assertEqual(__version__ + "\n", result.stdout,  "Unexpected output of 'scour --version'")

    def test_help(self):
        sys.argv.append('--help')

        result = self._run_scour()

        self.assertEqual(result.status, 0, "Execution of 'scour --help' erorred'")
        self.assertTrue(self.USAGE_STRING in result.stdout and 'Options:' in result.stdout,
                        "Unexpected output of 'scour --help'")

    def test_stdin_stdout(self):
        sys.stdin.write(self.MINIMAL_SVG)
        sys.stdin.seek(0)

        result = self._run_scour()

        self.assertEqual(result.status, 0, "Usage of Scour via 'stdin' / 'stdout' erorred'")
        self.assertEqual(result.stdout, self.MINIMAL_SVG, "Unexpected SVG output via 'stdout'")

    def test_filein_fileout_named(self):
        sys.argv.extend(['-i', 'unittests/minimal.svg', '-o', self.TEMP_SVG_FILE])

        result = self._run_scour()

        self.assertEqual(result.status, 0, "Usage of Scour with filenames specified as named parameters errored'")
        with open(self.TEMP_SVG_FILE) as file:
            file_content = file.read()
            self.assertEqual(file_content, self.MINIMAL_SVG, "Unexpected SVG output in generated file")
        os.remove(self.TEMP_SVG_FILE)

    def test_filein_fileout_positional(self):
        sys.argv.extend(['unittests/minimal.svg', self.TEMP_SVG_FILE])

        result = self._run_scour()

        self.assertEqual(result.status, 0, "Usage of Scour with filenames specified as positional parameters errored'")
        with open(self.TEMP_SVG_FILE) as file:
            file_content = file.read()
            self.assertEqual(file_content, self.MINIMAL_SVG, "Unexpected SVG output in generated file")
        os.remove(self.TEMP_SVG_FILE)

    def test_quiet(self):
        sys.argv.append('-q')
        sys.argv.extend(['-i', 'unittests/minimal.svg', '-o', self.TEMP_SVG_FILE])

        result = self._run_scour()
        os.remove(self.TEMP_SVG_FILE)

        self.assertEqual(result.status, 0, "Execution of 'scour -q ...' erorred'")
        self.assertEqual(result.stdout, '', "Output writtent to 'stdout' when '--quiet' options was used")
        self.assertEqual(result.stderr, '', "Output writtent to 'stderr' when '--quiet' options was used")

    def test_verbose(self):
        sys.argv.append('-v')
        sys.argv.extend(['-i', 'unittests/minimal.svg', '-o', self.TEMP_SVG_FILE])

        result = self._run_scour()
        os.remove(self.TEMP_SVG_FILE)

        self.assertEqual(result.status, 0, "Execution of 'scour -v ...' erorred'")
        self.assertEqual(result.stdout.count('Number'), 14,
                         "Statistics output not as expected when '--verbose' option was used")
        self.assertEqual(result.stdout.count(': 0'), 14,
                         "Statistics output not as expected when '--verbose' option was used")


class EmbedRasters(unittest.TestCase):

    # quick way to ping a host using the OS 'ping' command and return the execution result
    def _ping(host):
        import os
        import platform

        # work around https://github.com/travis-ci/travis-ci/issues/3080 as pypy throws if 'ping' can't be executed
        import distutils.spawn
        if not distutils.spawn.find_executable('ping'):
            return -1

        system = platform.system().lower()
        ping_count = '-n' if system == 'windows' else '-c'
        dev_null = 'NUL' if system == 'windows' else '/dev/null'

        return os.system('ping ' + ping_count + ' 1 ' + host + ' > ' + dev_null)

    def test_disable_embed_rasters(self):
        doc = scourXmlFile('unittests/raster-formats.svg',
                           parse_args(['--disable-embed-rasters']))
        self.assertEqual(doc.getElementById('png').getAttribute('xlink:href'), 'raster.png',
                         "Raster image embedded when '--disable-embed-rasters' was specified")

    def test_raster_formats(self):
        doc = scourXmlFile('unittests/raster-formats.svg')
        self.assertEqual(doc.getElementById('png').getAttribute('xlink:href'),
                         'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAMAAAABAgMAAABmjvwnAAAAC'
                         'VBMVEUAAP//AAAA/wBmtfVOAAAACklEQVQI12NIAAAAYgBhGxZhsAAAAABJRU5ErkJggg==',
                         "Raster image (PNG) not correctly embedded.")
        self.assertEqual(doc.getElementById('gif').getAttribute('xlink:href'),
                         'data:image/gif;base64,R0lGODdhAwABAKEDAAAA//8AAAD/AP///ywAAAAAAwABAAACAoxQADs=',
                         "Raster image (GIF) not correctly embedded.")
        self.assertEqual(doc.getElementById('jpg').getAttribute('xlink:href'),
                         'data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEASABIAAD//gATQ3JlYXRlZCB3aXRoIEdJTVD/'
                         '2wBDAAEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQH/'
                         '2wBDAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQH/'
                         'wAARCAABAAMDAREAAhEBAxEB/8QAFAABAAAAAAAAAAAAAAAAAAAACv/EABoQAAEFAQAAAAAAAAAAAAAAAAgABQc3d7j/'
                         'xAAVAQEBAAAAAAAAAAAAAAAAAAAHCv/EABwRAAEDBQAAAAAAAAAAAAAAAAgAB7gJODl2eP/aAAwDAQACEQMRAD8AMeaF'
                         '/u2aj5z1Fqp7oN4rxx2kn5cPuhV6LkzG7qOyYL2r/9k=',
                         "Raster image (JPG) not correctly embedded.")

    def test_raster_paths_local(self):
        doc = scourXmlFile('unittests/raster-paths-local.svg')
        images = doc.getElementsByTagName('image')
        for image in images:
            href = image.getAttribute('xlink:href')
            self.assertTrue(href.startswith('data:image/'),
                            "Raster image from local path '" + href + "' not embedded.")

    def test_raster_paths_local_absolute(self):
        with open('unittests/raster-formats.svg', 'r') as f:
            svg = f.read()

        # create a reference string by scouring the original file with relative links
        options = ScourOptions
        options.infilename = 'unittests/raster-formats.svg'
        reference_svg = scourString(svg, options)

        # this will not always create formally valid paths but it'll check how robust our implementation is
        # (the third path is invalid for sure because file: needs three slashes according to URI spec)
        svg = svg.replace('raster.png',
                          '/' + os.path.abspath(os.path.dirname(__file__)) + '\\unittests\\raster.png')
        svg = svg.replace('raster.gif',
                          'file:///' + os.path.abspath(os.path.dirname(__file__)) + '/unittests/raster.gif')
        svg = svg.replace('raster.jpg',
                          'file:/' + os.path.abspath(os.path.dirname(__file__)) + '/unittests/raster.jpg')

        svg = scourString(svg)

        self.assertEqual(svg, reference_svg,
                         "Raster images from absolute local paths not properly embedded.")

    @unittest.skipIf(_ping('raw.githubusercontent.com') != 0, "Remote server not reachable.")
    def test_raster_paths_remote(self):
        doc = scourXmlFile('unittests/raster-paths-remote.svg')
        images = doc.getElementsByTagName('image')
        for image in images:
            href = image.getAttribute('xlink:href')
            self.assertTrue(href.startswith('data:image/'),
                            "Raster image from remote path '" + href + "' not embedded.")


class ViewBox(unittest.TestCase):

    def test_viewbox_create(self):
        doc = scourXmlFile('unittests/viewbox-create.svg', parse_args(['--enable-viewboxing']))
        viewBox = doc.documentElement.getAttribute('viewBox')
        self.assertEqual(viewBox, '0 0 123.46 654.32', "viewBox not properly created with '--enable-viewboxing'.")

    def test_viewbox_remove_width_and_height(self):
        doc = scourXmlFile('unittests/viewbox-remove.svg', parse_args(['--enable-viewboxing']))
        width = doc.documentElement.getAttribute('width')
        height = doc.documentElement.getAttribute('height')
        self.assertEqual(width, '', "width not removed with '--enable-viewboxing'.")
        self.assertEqual(height, '', "height not removed with '--enable-viewboxing'.")


# TODO: write tests for --keep-editor-data

if __name__ == '__main__':
    testcss = __import__('test_css')
    scour = __import__('__main__')
    suite = unittest.TestSuite(list(map(unittest.defaultTestLoader.loadTestsFromModule, [testcss, scour])))
    unittest.main(defaultTest="suite")
