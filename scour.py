#!/usr/local/bin/python
#  Scour
#  Version 0.01
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
#  along with Carve.  If not, see http://www.gnu.org/licenses/ .
#

# TODOs:
#
# 10) Remove all inkscape/sodipodi namespaced elements
# 11) Remove all inkscape/sodipodi namespaced attributes
# 12) Command-line switches to enable/disable each option
# 13) Look into automating the testing (how to do reftest?)

import sys
import string
import xml.dom.minidom

APP = 'scour'
VER = '0.02'
COPYRIGHT = 'Copyright Jeff Schiller, 2009'

SVGNS = 'http://www.w3.org/2000/svg'
XLINKNS = 'http://www.w3.org/1999/xlink'

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
if( len(args) == 2):
	if( args[0] == '-i' ):
		input = open(args[1], 'r')
	elif( args[0] == '-o' ):
		output = open(args[1], 'w')
	else:
		printSyntaxAndQuit()

# if both -o and -o are supplied, switch streams to the files
elif( len(args) == 4 ):
	if( args[0] == '-i' and args[2] == '-o' ):
		input = open(args[1], 'r')
		output = open(args[3], 'w')
	elif( args[0] == '-o' and args[2] == 'i' ):
		output = open(args[1], 'w')
		input = open(args[3], 'r')
	else:
		printSyntaxAndQuit()

# else invalid syntax
elif( len(args) != 0 ):
	printSyntaxAndQuit()

# if we are not sending to stdout, then print out app information
bOutputReport = False
if( output != sys.stdout ):
	bOutputReport = True
	printHeader()

# build DOM in memory
doc = xml.dom.minidom.parse(input)

# returns all elements with id attributes
def findElementsWithId(node,elems={}):
	id = node.getAttribute('id')
	if( id != '' ):
		elems[id] = node
	if( node.hasChildNodes() ):
		for child in node.childNodes:
			# from http://www.w3.org/TR/DOM-Level-2-Core/idl-definitions.html
			# we are only really interested in nodes of type Element (1)
			if( child.nodeType == 1 ):
				findElementsWithId(child, elems)
	return elems

# returns the number of times an id is referenced
# currently looks at fill, stroke and xlink:href attributes
def findReferencedElements(node,ids={}):
	href = node.getAttributeNS(XLINKNS,'href')
	
	# if xlink:href is set, then grab the id
	if( href != '' and len(href) > 1 and href[0] == '#'):
		# we remove the hash mark from the beginning of the id
		id = href[1:]
		if( ids.has_key(id) ):
			ids[id] += 1
		else:
			ids[id] = 1

	# now get all style properties and the fill, stroke, filter attributes
	styles = string.split(node.getAttribute('style'),';')
	# TODO: can i reuse this list below in the if/or check?
	for attr in ['fill', 'stroke', 'filter', 'clip-path', 'mask', 
				 'marker-start', 'marker-end', 'marker-mid']:
		styles.append( string.join([attr,node.getAttribute(attr)],':') )
			
	for style in styles:
		propval = string.split(style,':')
		if(len(propval) == 2):
			prop = propval[0].strip()
			val = propval[1].strip()
			if( (prop=='fill' or prop=='stroke' or prop=='filter' or prop=='clip-path' 
				 or prop=='mask' or prop=='marker-start' or prop=='marker-end' or prop=='marker-mid') 
				 and val != '' and val[0:5] == 'url(#' ):
				id = val[5:val.find(')')]
				if( ids.has_key(id) ):
					ids[id] += 1
				else:
					ids[id] = 1
					
	if( node.hasChildNodes() ):
		for child in node.childNodes:
			if( child.nodeType == 1 ):
				findReferencedElements(child, ids)
	return ids

numIDsRemoved = 0
numElemsRemoved = 0

# removes the unreferenced ID attributes
# returns the number of ID attributes removed
def removeUnreferencedIDs(referencedIDs, identifiedElements):
	global numIDsRemoved
	num = 0;
	for id in identifiedElements.keys():
		node = identifiedElements[id]
		if( referencedIDs.has_key(id) == False ):
			node.removeAttribute('id')
			# now remove the element from our list of elements with ids
			del identifiedElements[id]
			numIDsRemoved += 1
			num += 1
	return num

def vacuumDefs(doc):
	global numElemsRemoved
	num = 0
	defs = doc.documentElement.getElementsByTagNameNS(SVGNS, 'defs')
	for aDef in defs:
		for elem in aDef.childNodes:
			if( elem.nodeType == 1 and elem.getAttribute('id') == '' ):
				aDef.removeChild(elem)
				numElemsRemoved += 
				num += 1
	return num

bContinueLooping = True
while bContinueLooping:
	identifiedElements = findElementsWithId(doc.documentElement)
	referencedIDs = findReferencedElements(doc.documentElement)
	bContinueLooping = ((removeUnreferencedIDs(referencedIDs, identifiedElements) + vacuumDefs(doc)) > 0)

# output the document
doc.documentElement.writexml(output)

# Close input and output files
input.close()
output.close()

# output some statistics if we are not using stdout
if( bOutputReport):
	print "Number of unreferenced id attributes removed:", numIDsRemoved 
	print "Number of unreferenced elements removed:", numElemsRemoved
