#!/usr/local/bin/python
#  Scour
#  Version 0.05
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

# Notes:

# rubys path-crunching ideas here: http://intertwingly.net/code/svgtidy/spec.rb
# (and implemented here: http://intertwingly.net/code/svgtidy/svgtidy.rb )

# Yet more ideas here: http://wiki.inkscape.org/wiki/index.php/Save_Cleaned_SVG
# TODO: Adapt this script into an Inkscape python plugin
#
# * Specify a limit to the precision of all positional elements.
# * Clean up XML Elements
#  * Collapse multiple redundent groups
# * Clean up Definitions
#  * Remove duplicate gradient stops
#  * Collapse duplicate gradient definitions
#  * Remove gradients that are only referenced by one other gradient
# * Clean up CSS
#  * Convert RGB colours from RGB(r,g,b) to #RRGGBB format
#  * Convert RGB colours from #RRGGBB to #RGB if possible
# * Clean up paths
#  * Detect vertical/horizontal lines and replace.
#  * Eliminate empty path segments
#  * Eliminate last segment in a polygon
#  * Collapse straight curves.
#  * Convert absolute path segments to relative ones.
# * Process Transformations
#  * Process quadratic Bezier curves
#  * Collapse all group based transformations
# * Output Standard SVG
#  * Use viewPort instead of document width/height

# Next Up:
# + Prevent error when stroke-width property value has a unit
# - Removed duplicate gradient stops
# - Convert all colors to #RRGGBB format
# - Convert all referenced rasters into base64 encoded URLs if the files can be found

import sys
import string
import xml.dom.minidom
import re
import math

APP = 'scour'
VER = '0.06'
COPYRIGHT = 'Copyright Jeff Schiller, 2009'

NS = { 	'SVG': 		'http://www.w3.org/2000/svg', 
		'XLINK': 	'http://www.w3.org/1999/xlink', 
		'SODIPODI': 'http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd',
		'INKSCAPE': 'http://www.inkscape.org/namespaces/inkscape',
		'ADOBE_ILLUSTRATOR': 'http://ns.adobe.com/AdobeIllustrator/10.0/',
		'ADOBE_GRAPHS': 'http://ns.adobe.com/Graphs/1.0/',
		'ADOBE_SVG_VIEWER': 'http://ns.adobe.com/AdobeSVGViewerExtensions/3.0/',
		'ADOBE_VARIABLES': 'http://ns.adobe.com/Variables/1.0/',
		'ADOBE_SFW': 'http://ns.adobe.com/SaveForWeb/1.0/',
		'ADOBE_EXTENSIBILITY': 'http://ns.adobe.com/Extensibility/1.0/'
		}

unwanted_ns = [ NS['SODIPODI'], NS['INKSCAPE'], NS['ADOBE_ILLUSTRATOR'],
				NS['ADOBE_GRAPHS'], NS['ADOBE_SVG_VIEWER'], NS['ADOBE_VARIABLES'],
				NS['ADOBE_SFW'], NS['ADOBE_EXTENSIBILITY'] ] 

svgAttributes = [
				'clip-rule',
				'fill',
				'fill-opacity',
				'fill-rule',
				'filter',
				'font-family',
				'font-size',
				'font-stretch',
				'font-style',
				'font-variant',
				'font-weight',
				'line-height',
				'opacity',
				'stop-color',
				'stop-opacity',
				'stroke',
				'stroke-dashoffset',
				'stroke-linecap',
				'stroke-linejoin',
				'stroke-miterlimit',
				'stroke-opacity',
				'stroke-width',
				]

def printHeader():
	print APP , VER
	print COPYRIGHT

def printSyntaxAndQuit():
	printHeader()
	print 'usage: scour.py [-i input.svg] [-o output.svg]\n'
	print 'If the input file is not specified, stdin is used.'
	print 'If the output file is not specified, stdout is used.'
	quit()	

# returns all elements with id attributes
def findElementsWithId(node,elems={}):
	id = node.getAttribute('id')
	if id != '' :
		elems[id] = node
	if node.hasChildNodes() :
		for child in node.childNodes:
			# from http://www.w3.org/TR/DOM-Level-2-Core/idl-definitions.html
			# we are only really interested in nodes of type Element (1)
			if child.nodeType == 1 :
				findElementsWithId(child, elems)
	return elems

# returns the number of times an id is referenced
# currently looks at fill, stroke and xlink:href attributes
def findReferencedElements(node,ids={}):
	# TODO: error here (ids is not cleared upon next invocation), the
	# input argument ids is clunky here (see below how it is called)
	href = node.getAttributeNS(NS['XLINK'],'href')
	
	# if xlink:href is set, then grab the id
	if href != '' and len(href) > 1 and href[0] == '#':
		# we remove the hash mark from the beginning of the id
		id = href[1:]
		if ids.has_key(id) :
			ids[id] += 1
		else:
			ids[id] = 1

	# now get all style properties and the fill, stroke, filter attributes
	styles = string.split(node.getAttribute('style'),';')
	referencingProps = ['fill', 'stroke', 'filter', 'clip-path', 'mask',  'marker-start', 
						'marker-end', 'marker-mid']
	for attr in referencingProps:
		styles.append( string.join([attr,node.getAttribute(attr)],':') )
			
	for style in styles:
		propval = string.split(style,':')
		if len(propval) == 2 :
			prop = propval[0].strip()
			val = propval[1].strip()
			if prop in referencingProps and val != '' and val[0:5] == 'url(#' :
				id = val[5:val.find(')')]
				if ids.has_key(id) :
					ids[id] += 1
				else:
					ids[id] = 1
					
	if node.hasChildNodes() :
		for child in node.childNodes:
			if child.nodeType == 1 :
				findReferencedElements(child, ids)
	return ids

numIDsRemoved = 0
numElemsRemoved = 0
numAttrsRemoved = 0

# removes the unreferenced ID attributes
# returns the number of ID attributes removed
def removeUnreferencedIDs(referencedIDs, identifiedElements):
	global numIDsRemoved
	num = 0;
	for id in identifiedElements.keys():
		node = identifiedElements[id]
		if referencedIDs.has_key(id) == False :
			node.removeAttribute('id')
			# now remove the element from our list of elements with ids
			# not necessary if we're calculating the array again every time
#			del identifiedElements[id]
			numIDsRemoved += 1
			num += 1
	return num

def vacuumDefs(doc):
	global numElemsRemoved
	num = 0
	defs = doc.documentElement.getElementsByTagNameNS(NS['SVG'], 'defs')
	for aDef in defs:
		for elem in aDef.childNodes:
			if elem.nodeType == 1 and elem.getAttribute('id') == '' :
				aDef.removeChild(elem)
				numElemsRemoved += 1
				num += 1
	return num

def removeNamespacedAttributes(node, namespaces):
	global numAttrsRemoved
	num = 0
	if node.nodeType == 1 :
		# remove all namespace'd attributes from this element
		attrList = node.attributes
		attrsToRemove = []
		for attrNum in range(attrList.length):
			attr = attrList.item(attrNum)
			if attr != None and attr.namespaceURI in namespaces:
				attrsToRemove.append(attr.nodeName)
		for attrName in attrsToRemove :
			num += 1
			numAttrsRemoved += 1
			node.removeAttribute(attrName)
		
		# now recurse for children
		for child in node.childNodes:
			removeNamespacedAttributes(child, namespaces)
	return num
	
def removeNamespacedElements(node, namespaces):
	global numElemsRemoved
	num = 0
	if node.nodeType == 1 :
		# remove all namespace'd child nodes from this element
		childList = node.childNodes
		childrenToRemove = []
		for child in childList:
			if child != None and child.namespaceURI in namespaces:
				childrenToRemove.append(child)
		for child in childrenToRemove :
			num += 1
			numElemsRemoved += 1
			node.removeChild(child)
		
		# now recurse for children
		for child in node.childNodes:
			removeNamespacedElements(child, namespaces)
	return num

# TODO: create a class for a SVGLength type (including value and unit)

coord = re.compile("\\-?\\d+\\.?\\d*")
scinumber = re.compile("[\\-\\+]?(\\d*\\.?)?\\d+[eE][\\-\\+]?\\d+")
number = re.compile("[\\-\\+]?(\\d*\\.?)?\\d+")
sciExponent = re.compile("[eE]([\\-\\+]?\\d+)")
unit = re.compile("(em|ex|px|pt|pc|cm|mm|in|\\%){1,1}$")

class Unit:
	INVALID = -1
	NONE = 0
	PCT = 1
	PX = 2
	PT = 3
	PC = 4
	EM = 5
	EX = 6
	CM = 7
	MM = 8
	IN = 9
	
	@staticmethod
	def get(str):
		if str == None or str == '': return Unit.NONE
		elif str == '%': return Unit.PCT
		elif str == 'px': return Unit.PX
		elif str == 'pt': return Unit.PT
		elif str == 'pc': return Unit.PC
		elif str == 'em': return Unit.EM
		elif str == 'ex': return Unit.EX
		elif str == 'cm': return Unit.CM
		elif str == 'mm': return Unit.MM
		elif str == 'in': return Unit.IN
		return Unit.INVALID
	
class SVGLength:
	def __init__(self, str):
#		print "Parsing '%s'" % str
		try: # simple unitless and no scientific notation
			self.value = string.atof(str)
			self.units = Unit.NONE
#			print "  Value =", self.value
		except ValueError:
			# we know that the length string has an exponent, a unit, both or is invalid

			# TODO: parse out number, exponent and unit
			unitBegin = 0
			scinum = scinumber.match(str)
			if scinum != None:
				# this will always match, no need to check it
				numMatch = number.match(str)
				expMatch = sciExponent.search(str, numMatch.start(0))
				self.value = string.atof(numMatch.group(0)) * math.pow(10, string.atof(expMatch.group(1)))
				unitBegin = expMatch.end(1)
			else:
				# unit or invalid
				numMatch = number.match(str)
				if numMatch != None:
					self.value = numMatch.group(0)
					unitBegin = numMatch.end(0)

			if unitBegin != 0 :
#				print "  Value =", self.value
				unitMatch = unit.search(str, unitBegin)
				if unitMatch != None :
					self.units = Unit.get(unitMatch.group(0))
#					print "  Units =", self.units
				
			# invalid
			else:
				# TODO: this needs to set the default for the given attribute (how?)
#				print "  Invalid: ", str
				self.value = 0 
				self.units = Unit.INVALID

# returns the length of a property
# TODO: eventually use the above class once it is complete
def getSVGLength(value):
	try:
		v = string.atof(value)
	except ValueError:
		coordMatch = coord.match(value)
		if coordMatch != None:
			unitMatch = unit.search(value, coordMatch.start(0))
		v = value
	return v
	
def repairStyle(node):
	num = 0
	if node.nodeType == 1 and len(node.getAttribute('style')) > 0 :	
		# get all style properties and stuff them into a dictionary
		styleMap = { }
		rawStyles = string.split(node.getAttribute('style'),';')
		for style in rawStyles:
			propval = string.split(style,':')
			if len(propval) == 2 :
				styleMap[propval[0].strip()] = propval[1].strip()

		# I've seen this enough to know that I need to correct it:
		# fill: url(#linearGradient4918) rgb(0, 0, 0);
		for prop in ['fill', 'stroke'] :
			if styleMap.has_key(prop) :
				chunk = styleMap[prop].split(') ')
				if len(chunk) == 2 and chunk[0][:5] == 'url(#' and chunk[1] == 'rgb(0, 0, 0)' :
					styleMap[prop] = chunk[0] + ')'
					num += 1

		# Here is where we can weed out unnecessary styles like:
		#  opacity:1
		if styleMap.has_key('opacity') :
			opacity = string.atof(styleMap['opacity'])
			# opacity='1.0' is useless, remove it
			if opacity == 1.0 :
				del styleMap['opacity']
				
			# if opacity='0' then all fill and stroke properties are useless, remove them
			elif opacity == 0.0 :
				for uselessStyle in ['fill', 'fill-opacity', 'fill-rule', 'stroke', 'stroke-linejoin',
					'stroke-opacity', 'stroke-miterlimit', 'stroke-linecap', 'stroke-dasharray',
					'stroke-dashoffset', 'stroke-opacity'] :
					del styleMap[uselessStyle]
					num += 1

		#  if stroke:none, then remove all stroke-related properties (stroke-width, etc)
		#  TODO: should also detect if the computed value of this element is fill="none"
		if styleMap.has_key('stroke') and styleMap['stroke'] == 'none' :
			for strokestyle in [ 'stroke-width', 'stroke-linejoin', 'stroke-miterlimit', 
					'stroke-linecap', 'stroke-dasharray', 'stroke-dashoffset', 'stroke-opacity'] :
				if styleMap.has_key(strokestyle) :
					del styleMap[strokestyle]
					num += 1

		#  if fill:none, then remove all fill-related properties (fill-rule, etc)
		#  TODO: should also detect if fill-opacity=0
		if styleMap.has_key('fill') and styleMap['fill'] == 'none' :
			for fillstyle in [ 'fill-rule', 'fill-opacity' ] :
				if styleMap.has_key(fillstyle) :
					del styleMap[fillstyle]
					num += 1
					
		#  stop-opacity: 1
		if styleMap.has_key('stop-opacity') :
			if string.atof(styleMap['stop-opacity']) == 1.0 :
				del styleMap['stop-opacity']
				num += 1
		
		#  fill-opacity: 1 or 0
		if styleMap.has_key('fill-opacity') :
			fillOpacity = string.atof(styleMap['fill-opacity'])
			#  TODO: This is actually a problem is the parent element does not have fill-opacity = 1
			if fillOpacity == 1.0 :
				del styleMap['fill-opacity']
				num += 1
			elif fillOpacity == 0.0 :
				for uselessFillStyle in [ 'fill', 'fill-rule' ] :
					del styleMap[uselessFillStyle]
					num += 1
		
		#  stroke-opacity: 1 or 0
		if styleMap.has_key('stroke-opacity') :
			strokeOpacity = string.atof(styleMap['stroke-opacity']) 
			#  TODO: This is actually a problem is the parent element does not have stroke-opacity = 1
			if strokeOpacity == 1.0 :
				del styleMap['stroke-opacity']
				num += 1
			elif strokeOpacity == 0.0 :
				for uselessStrokeStyle in [ 'stroke', 'stroke-width', 'stroke-linejoin', 'stroke-linecap', 
							'stroke-dasharray', 'stroke-dashoffset' ] :
					del styleMap[uselessStrokeStyle]
					num += 1

		# stroke-width: 0
		if styleMap.has_key('stroke-width') :
			strokeWidth = getSVGLength(styleMap['stroke-width']) 
			if strokeWidth == 0.0 :
				for uselessStrokeStyle in [ 'stroke', 'stroke-linejoin', 'stroke-linecap', 
							'stroke-dasharray', 'stroke-dashoffset', 'stroke-opacity' ] :
					del styleMap[uselessStrokeStyle]
					num += 1
		
		#  TODO: what else?
		
		# now if any of the properties match known SVG attributes we prefer attributes 
		# over style so emit them and remove them from the style map
		for propName in styleMap.keys() :
			if propName in svgAttributes :
				node.setAttribute(propName, styleMap[propName])
				del styleMap[propName]

		# sew our style back together
		fixedStyle = ''
		for prop in styleMap.keys() :
			fixedStyle += prop + ':' + styleMap[prop] + ';'
			
		if fixedStyle != '' :
			node.setAttribute('style', fixedStyle)
		else:
			node.removeAttribute('style')
		
	for child in node.childNodes :
		num += repairStyle(child)
			
	return num

# does nothing at the moment but waste time
def cleanPath(element) :
	path = element.getAttribute('d')

def properlySizeDoc(docElement):
	# get doc width and height
	w = SVGLength(docElement.getAttribute('width'))
	h = SVGLength(docElement.getAttribute('height'))
	
	if ((w.units == Unit.PCT or w.units == Unit.INVALID) and
	    (h.units == Unit.PCT or h.units == Unit.INVALID)):
	    return

	# else we have a statically sized image and we should try to remedy that	

	# parse viewBox attribute
	vbSep = re.split("\\s*\\,?\\s*", docElement.getAttribute('viewBox'), 3)
	# if we have a valid viewBox we probably shouldn't change anything unless
	# the viewbox width/height matches the doc width/height
#	if len(vbSep) == 4:
#		vbWidth = 
	
	

# parse command-line arguments
args = sys.argv[1:]

# by default the input and output are the standard streams
input = sys.stdin
output = sys.stdout

# if -i or -o is supplied, switch the stream to the file
if len(args) == 2:
	if args[0] == '-i' :
		input = open(args[1], 'r')
	elif args[0] == '-o' :
		output = open(args[1], 'w')
	else:
		printSyntaxAndQuit()

# if both -o and -o are supplied, switch streams to the files
elif len(args) == 4 :
	if args[0] == '-i' and args[2] == '-o' :
		input = open(args[1], 'r')
		output = open(args[3], 'w')
	elif args[0] == '-o' and args[2] == 'i' :
		output = open(args[1], 'w')
		input = open(args[3], 'r')
	else:
		printSyntaxAndQuit()

# else invalid syntax
elif len(args) != 0 :
	printSyntaxAndQuit()

# if we are not sending to stdout, then print out app information
bOutputReport = False
if output != sys.stdout :
	bOutputReport = True
	printHeader()

# build DOM in memory
doc = xml.dom.minidom.parse(input)

# for whatever reason this does not always remove all inkscape/sodipodi attributes/elements
# on the first pass, so we do it multiple times
# does it have to do with removal of children affecting the childlist?
while removeNamespacedElements( doc.documentElement, unwanted_ns ) > 0 :
	pass	
while removeNamespacedAttributes( doc.documentElement, unwanted_ns ) > 0 :
	pass
	
# remove the xmlns: declarations now
xmlnsDeclsToRemove = []
attrList = doc.documentElement.attributes
for num in range(attrList.length) :
	if attrList.item(num).nodeValue in unwanted_ns :
		xmlnsDeclsToRemove.append(attrList.item(num).nodeName)

for attr in xmlnsDeclsToRemove :
	doc.documentElement.removeAttribute(attr)
	numAttrsRemoved += 1

bContinueLooping = True
while bContinueLooping:
	identifiedElements = findElementsWithId(doc.documentElement, {})
	referencedIDs = findReferencedElements(doc.documentElement, {})
	bContinueLooping = ((removeUnreferencedIDs(referencedIDs, identifiedElements) + vacuumDefs(doc)) > 0)

# repair style (remove unnecessary style properties and change them into XML attributes)
numStylePropsFixed = repairStyle(doc.documentElement)

# remove empty defs, metadata, g
# NOTE: these elements will be removed even if they have (invalid) text nodes
elemsToRemove = []
for tag in ['defs', 'metadata', 'g'] :
	for elem in doc.documentElement.getElementsByTagNameNS(NS['SVG'], tag) :
		removeElem = not elem.hasChildNodes()
		if removeElem == False :
			for child in elem.childNodes :
				if child.nodeType in [1, 4, 8] :
					break
			else:
				removeElem = True
		if removeElem :
			elem.parentNode.removeChild(elem)
			numElemsRemoved += 1

# properly size the SVG document (width/height should be 100% with a viewBox)
properlySizeDoc(doc.documentElement)

# clean path data
for elem in doc.documentElement.getElementsByTagNameNS(NS['SVG'], 'path') :
	cleanPath(elem)

# output the document
doc.documentElement.writexml(output)

# Close input and output files
input.close()
output.close()

# output some statistics if we are not using stdout
if bOutputReport :
	print "Number of unreferenced id attributes removed:", numIDsRemoved 
	print "Number of elements removed:", numElemsRemoved
	print "Number of attributes removed:", numAttrsRemoved
	print "Number of style properties fixed:", numStylePropsFixed
