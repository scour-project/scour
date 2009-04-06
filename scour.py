#!/usr/local/bin/python
#  Scour
#  Version 0.03
#
#  Copyright 2009 Jeff Schiller
#
#  This file is part of Scour, http://www.codedread.com/scour/
#
#  Scour is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Scour is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with Scour.  If not, see http://www.gnu.org/licenses/ .
#

# Path-crunching ideas here: http://intertwingly.net/code/svgtidy/spec.rb
# (and implemented here: http://intertwingly.net/code/svgtidy/svgtidy.rb )

# Yet more ideas here: http://wiki.inkscape.org/wiki/index.php/Save_Cleaned_SVG

# Next Up:
# - Remove empty defs/elements elements (no children and no attributes)
# - Remove Adobe namespace elements, attributes
# _ Remove inkscape/sodipodi/adobe namespace declarations
# - Convert style to attributes

import sys
import string
import xml.dom.minidom

APP = 'scour'
VER = '0.03'
COPYRIGHT = 'Copyright Jeff Schiller, 2009'

NS = { 	'SVG': 		'http://www.w3.org/2000/svg', 
		'XLINK': 	'http://www.w3.org/1999/xlink', 
		'SODIPODI': 'http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd',
		'INKSCAPE': 'http://www.inkscape.org/namespaces/inkscape'
		}

def printHeader():
	print APP , VER
	print COPYRIGHT

def printSyntaxAndQuit():
	printHeader()
	print 'usage: scour.py [-i input.svg] [-o output.svg]\n'
	print 'If the input file is not specified, stdin is used.'
	print 'If the output file is not specified, stdout is used.'
	quit()	

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
		for attrNum in range(attrList.length):
			attr = attrList.item(attrNum)
			if attr != None and attr.namespaceURI in namespaces:
				num += 1
				numAttrsRemoved += 1
				node.removeAttribute(attr.nodeName)
		
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
		for child in childList:
			if child != None and child.namespaceURI in namespaces:
				num += 1
				numElemsRemoved += 1
				node.removeChild(child)
		
		# now recurse for children
		for child in node.childNodes:
			removeNamespacedElements(child, namespaces)
	return num
	
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
		if styleMap.has_key('opacity') and string.atof(styleMap['opacity']) == 1.0 :
			del styleMap['opacity']
			
		#  if stroke:none, then remove all stroke properties (stroke-width, etc)
		if styleMap.has_key('stroke') and styleMap['stroke'] == 'none' :
			for strokestyle in [ 'stroke-width', 'stroke-linejoin', 'stroke-miterlimit', 
					'stroke-linecap', 'stroke-dasharray', 'stroke-dashoffset', 'stroke-opacity'] :
				if styleMap.has_key(strokestyle) :
					del styleMap[strokestyle]
					num += 1

		#  stop-opacity: 1
		if styleMap.has_key('stop-opacity') and string.atof(styleMap['stop-opacity']) == 1.0 :
			del styleMap['stop-opacity']
		
		#  fill-opacity: 1
		if styleMap.has_key('fill-opacity') and string.atof(styleMap['fill-opacity']) == 1.0 :
			del styleMap['fill-opacity']
		
		#  stroke-opacity: 1
		if styleMap.has_key('stroke-opacity') and string.atof(styleMap['stroke-opacity']) == 1.0 :
			del styleMap['stroke-opacity']
		
		#  TODO: what else?
					
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

# for whatever reason this does not always remove all inkscape/sodipodi attributes/elements
# on the first pass, so we do it multiple times
# does it have to do with removal of children affecting the childlist?
while removeNamespacedElements( doc.documentElement, [ NS['SODIPODI'], NS['INKSCAPE'] ] ) > 0 :
	pass
	
while removeNamespacedAttributes( doc.documentElement, [ NS['SODIPODI'], NS['INKSCAPE'] ] ) > 0 :
	pass

bContinueLooping = True
while bContinueLooping:
	identifiedElements = findElementsWithId(doc.documentElement, {})
	referencedIDs = findReferencedElements(doc.documentElement, {})
	bContinueLooping = ((removeUnreferencedIDs(referencedIDs, identifiedElements) + vacuumDefs(doc)) > 0)

numStylePropsFixed = repairStyle(doc.documentElement)

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
