#!/usr/bin/env python

#  Scour
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

# rubys' path-crunching ideas here: http://intertwingly.net/code/svgtidy/spec.rb
# (and implemented here: http://intertwingly.net/code/svgtidy/svgtidy.rb )

# Yet more ideas here: http://wiki.inkscape.org/wiki/index.php/Save_Cleaned_SVG
# TODO: Adapt this script into an Inkscape python plugin
#
# * Specify a limit to the precision of all positional elements.
# * Clean up Definitions
#  * Collapse duplicate gradient definitions
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

# Suggestion from Richard Hutch:
#  * Put id attributes first in the serialization (or make the d attribute last)

# Next Up:
# - Remove unnecessary units of precision on attributes
# - Remove unnecessary units of precision on path coordinates
# - Convert all colors to #RRGGBB format
# - Reduce #RRGGBB format to #RGB format when possible
# https://bugs.edge.launchpad.net/ubuntu/+source/human-icon-theme/+bug/361667/

# Some notes to not forget:
# - removing empty nested groups also potentially loses some semantic information
#   (i.e. the following button:
#     <g>
#       <rect .../>
#       <text .../>
#     </g>
#   will be flattened)


# necessary to get true division
from __future__ import division

import os
import sys
import string
import xml.dom.minidom
import re
import math
import base64
import os.path
import urllib

APP = 'scour'
VER = '0.10'
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
		'ADOBE_EXTENSIBILITY': 'http://ns.adobe.com/Extensibility/1.0/',
     	'ADOBE_FLOWS': 'http://ns.adobe.com/Flows/1.0/',
     	'ADOBE_IMAGE_REPLACEMENT': 'http://ns.adobe.com/ImageReplacement/1.0/',     
     	'ADOBE_CUSTOM': 'http://ns.adobe.com/GenericCustomNamespace/1.0/',
     	'ADOBE_XPATH': 'http://ns.adobe.com/XPath/1.0/'
		}

unwanted_ns = [ NS['SODIPODI'], NS['INKSCAPE'], NS['ADOBE_ILLUSTRATOR'],
				NS['ADOBE_GRAPHS'], NS['ADOBE_SVG_VIEWER'], NS['ADOBE_VARIABLES'],
				NS['ADOBE_SFW'], NS['ADOBE_EXTENSIBILITY'], NS['ADOBE_FLOWS'],
				NS['ADOBE_IMAGE_REPLACEMENT'], NS['ADOBE_CUSTOM'], NS['ADOBE_XPATH'] ] 

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

def findElementById(node, id):
	if node == None or node.nodeType != 1: return None
	if node.getAttribute('id') == id: return node
	for child in node.childNodes :
		e = findElementById(child,id)
		if e != None: return e
	return None

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

# returns the number of times an id is referenced as well as all elements that reference it
# currently looks at fill, stroke, clip-path, mask, marker and xlink:href attributes
def findReferencedElements(node,ids={}):
	# TODO: error here (ids is not cleared upon next invocation), the
	# input argument ids is clunky here (see below how it is called)
	href = node.getAttributeNS(NS['XLINK'],'href')
	
	# if xlink:href is set, then grab the id
	if href != '' and len(href) > 1 and href[0] == '#':
		# we remove the hash mark from the beginning of the id
		id = href[1:]
		if ids.has_key(id) :
			ids[id][0] += 1
			ids[id][1].append(node)
		else:
			ids[id] = [1,[node]]

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
					ids[id][0] += 1
					ids[id][1].append(node)
				else:
					ids[id] = [1,[node]]
					
	if node.hasChildNodes() :
		for child in node.childNodes:
			if child.nodeType == 1 :
				findReferencedElements(child, ids)
	return ids

numIDsRemoved = 0
numElemsRemoved = 0
numAttrsRemoved = 0
numRastersEmbedded = 0

# removes all unreferenced elements except for <svg>, <font>, <metadata>, <title>, and <desc>
# also vacuums the defs of any non-referenced renderable elements
# returns the number of unreferenced elements removed from the document
def removeUnreferencedElements(doc):
	global numElemsRemoved
	num = 0
	removeTags = ['linearGradient', 'radialGradient', 'pattern']

	identifiedElements = findElementsWithId(doc.documentElement, {})
	referencedIDs = findReferencedElements(doc.documentElement, {})

	for id in identifiedElements:
		if not id in referencedIDs:
			goner = findElementById(doc.documentElement, id)
			if goner != None and goner.parentNode != None and goner.nodeName in removeTags:
				goner.parentNode.removeChild(goner)
				num += 1
				numElemsRemoved += 1

	# TODO: should also go through defs and vacuum it
	identifiedElements = findElementsWithId(doc.documentElement, {})
	referencedIDs = findReferencedElements(doc.documentElement, {})
	
	keepTags = ['font', 'style', 'metadata', 'script', 'title', 'desc']
	num = 0
	defs = doc.documentElement.getElementsByTagNameNS(NS['SVG'], 'defs')
	for aDef in defs:
		elemsToRemove = []
		for elem in aDef.childNodes:
			if elem.nodeType == 1 and (elem.getAttribute('id') == '' or \
					(not elem.getAttribute('id') in referencedIDs)) and \
					not elem.nodeName in keepTags:
				elemsToRemove.append(elem)
		for elem in elemsToRemove:
			aDef.removeChild(elem)
			numElemsRemoved += 1
			num += 1
	return num
	
	return num

# removes the unreferenced ID attributes
# returns the number of ID attributes removed
def removeUnreferencedIDs(referencedIDs, identifiedElements):
	global numIDsRemoved
	keepTags = ['font']
	num = 0;
	for id in identifiedElements.keys():
		node = identifiedElements[id]
		if referencedIDs.has_key(id) == False and not node.nodeName in keepTags:
			node.removeAttribute('id')
			numIDsRemoved += 1
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
			num += removeNamespacedAttributes(child, namespaces)
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
			num += removeNamespacedElements(child, namespaces)
	return num

# this walks further and further down the tree, removing groups
# which do not have any attributes or a title/desc child and 
# promoting their children up one level
def removeNestedGroups(node):
	global numElemsRemoved
	num = 0
	
	groupsToRemove = []
	for child in node.childNodes:
		if child.nodeName == 'g' and child.namespaceURI == NS['SVG'] and len(child.attributes) == 0:
			# only collapse group if it does not have a title or desc as a direct descendant
			for grandchild in child.childNodes:
				if grandchild.nodeType == 1 and grandchild.namespaceURI == NS['SVG'] and \
						grandchild.nodeName in ['title','desc']:
					break
			else:
				groupsToRemove.append(child)

	for g in groupsToRemove:
		while g.childNodes.length > 0:
			g.parentNode.insertBefore(g.firstChild, g)
		g.parentNode.removeChild(g)
		numElemsRemoved += 1
		num += 1

	# now recurse for children
	for child in node.childNodes:
		if child.nodeType == 1:
			num += removeNestedGroups(child)		
	return num

def removeDuplicateGradientStops(doc):
	global numElemsRemoved
	num = 0
	
	for gradType in ['linearGradient', 'radialGradient']:
		for grad in doc.getElementsByTagNameNS(NS['SVG'], gradType):
			stops = {}
			stopsToRemove = []
			for stop in grad.getElementsByTagNameNS(NS['SVG'], 'stop'):
				offset = string.atof(stop.getAttribute('offset'))
				color = stop.getAttribute('stop-color')
				opacity = stop.getAttribute('stop-opacity')
				if stops.has_key(offset) :
					oldStop = stops[offset]
					if oldStop[0] == color and oldStop[1] == opacity:
						stopsToRemove.append(stop)
				stops[offset] = [color, opacity]
				
			for stop in stopsToRemove:
				stop.parentNode.removeChild(stop)
				num += 1
				numElemsRemoved += 1
	
	# linear gradients
	return num

def collapseSinglyReferencedGradients(doc):
	global numElemsRemoved
	num = 0
	
	# make sure to reset the ref'ed ids for when we are running this in testscour
	for rid,nodeCount in findReferencedElements(doc.documentElement, {}).iteritems():
		count = nodeCount[0]
		nodes = nodeCount[1]
		if count == 1:
			elem = findElementById(doc.documentElement,rid)
			if elem != None and elem.nodeType == 1 and elem.nodeName in ['linearGradient', 'radialGradient'] \
					and elem.namespaceURI == NS['SVG']:
				# found a gradient that is referenced by only 1 other element
				refElem = nodes[0]
				if refElem.nodeType == 1 and refElem.nodeName in ['linearGradient', 'radialGradient'] \
						and refElem.namespaceURI == NS['SVG']:
					# elem is a gradient referenced by only one other gradient (refElem)
					# TODO: update elem with properties and stops from refElem
					
					# add the stops to the referencing gradient (this removes them from elem)
					if len(refElem.getElementsByTagNameNS(NS['SVG'], 'stop')) == 0:
						stopsToAdd = elem.getElementsByTagNameNS(NS['SVG'], 'stop')
						for stop in stopsToAdd:
							refElem.appendChild(stop)
							
					# adopt the gradientUnits, spreadMethod,  gradientTransform attributess if
					# they are unspecified on refElem
					for attr in ['gradientUnits','spreadMethod','gradientTransform']:
						if refElem.getAttribute(attr) == '' and not elem.getAttribute(attr) == '':
							refElem.setAttributeNS(None, attr, elem.getAttribute(attr))
							
					# if both are radialGradients, adopt elem's fx,fy,cx,cy,r attributes if
					# they are unspecified on refElem
					if elem.nodeName == 'radialGradient' and refElem.nodeName == 'radialGradient':
						for attr in ['fx','fy','cx','cy','r']:
							if refElem.getAttribute(attr) == '' and not elem.getAttribute(attr) == '':
								refElem.setAttributeNS(None, attr, elem.getAttribute(attr))
					
					# if both are linearGradients, adopt elem's x1,y1,x2,y2 attributes if 
					# they are unspecified on refElem
					if elem.nodeName == 'linearGradient' and refElem.nodeName == 'linearGradient':
						for attr in ['x1','y1','x2','y2']:
							if refElem.getAttribute(attr) == '' and not elem.getAttribute(attr) == '':
								refElem.setAttributeNS(None, attr, elem.getAttribute(attr))
								
					# now remove the xlink:href from refElem
					refElem.removeAttributeNS(NS['XLINK'], 'href')
					
					# now delete elem
					elem.parentNode.removeChild(elem)
					numElemsRemoved += 1
					num += 1
					
	return num

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
					self.value = string.atof(numMatch.group(0))
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
					if styleMap.has_key(uselessStyle):
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
			del styleMap['stroke']

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
					if styleMap.has_key(uselessFillStyle):
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
					if styleMap.has_key(uselessStrokeStyle): 
						del styleMap[uselessStrokeStyle]
						num += 1

		# stroke-width: 0
		if styleMap.has_key('stroke-width') :
			strokeWidth = getSVGLength(styleMap['stroke-width']) 
			if strokeWidth == 0.0 :
				for uselessStrokeStyle in [ 'stroke', 'stroke-linejoin', 'stroke-linecap', 
							'stroke-dasharray', 'stroke-dashoffset', 'stroke-opacity' ] :
					if styleMap.has_key(uselessStrokeStyle): 
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

# converts raster references to inline images
# NOTE: there are size limits to base64-encoding handling in browsers 
def embedRasters(element) :
	global numRastersEmbedded

	href = element.getAttributeNS(NS['XLINK'],'href')
	
	# if xlink:href is set, then grab the id
	if href != '' and len(href) > 1:
		# find if href value has filename ext		
		ext = os.path.splitext(os.path.basename(href))[1].lower()[1:]
				
		# look for 'png', 'jpg', and 'gif' extensions 
		if ext == 'png' or ext == 'jpg' or ext == 'gif':

			# check if href resolves to an existing file
			if os.path.isfile(href) == False :
				if href[:7] != 'http://' and os.path.isfile(href) == False :
						# if this is not an absolute path, set path relative
						# to script file based on input arg 
						href = os.path.join(os.path.dirname(args[1]), href)				
				
			rasterdata = ''
			# test if file exists locally
			if os.path.isfile(href) == True :
				# open raster file as raw binary
				raster = open( href, "rb")
				rasterdata = raster.read()

			elif href[:7] == 'http://':
				# raster = open( href, "rb")
				webFile = urllib.urlopen( href )
				rasterdata = webFile.read()
				webFile.close()
			
			# ... should we remove all images which don't resolve?	
			if rasterdata != '' :
				# base64-encode raster
				b64eRaster = base64.b64encode( rasterdata )

				# set href attribute to base64-encoded equivalent
				if b64eRaster != '':
					# PNG and GIF both have MIME Type 'image/[ext]', but 
					# JPEG has MIME Type 'image/jpeg'
					if ext == 'jpg':
						ext = 'jpeg'

					element.setAttributeNS(NS['XLINK'], 'href', 'data:image/' + ext + ';base64,' + b64eRaster)
					numRastersEmbedded += 1
					del b64eRaster				

def properlySizeDoc(docElement):
	# get doc width and height
	w = SVGLength(docElement.getAttribute('width'))
	h = SVGLength(docElement.getAttribute('height'))

	# if width/height are not unitless or px then it is not ok to rewrite them into a viewBox	
	if ((w.units != Unit.NONE and w.units != Unit.PX) or
		(w.units != Unit.NONE and w.units != Unit.PX)):
	    return

	# else we have a statically sized image and we should try to remedy that	

	# parse viewBox attribute
	vbSep = re.split("\\s*\\,?\\s*", docElement.getAttribute('viewBox'), 3)
	# if we have a valid viewBox we need to check it
	vbWidth,vbHeight = 0,0
	if len(vbSep) == 4:
		try:
			# if x or y are specified and non-zero then it is not ok to overwrite it
			vbX = string.atof(vbSep[0])
			vbY = string.atof(vbSep[1])
			if vbX != 0 or vbY != 0:
				return
				
			# if width or height are not equal to doc width/height then it is not ok to overwrite it
			vbWidth = string.atof(vbSep[2])
			vbHeight = string.atof(vbSep[3])
			if vbWidth != w.value or vbHeight != h.value:
				return
		# if the viewBox did not parse properly it is invalid and ok to overwrite it
		except ValueError:
			pass
	
	# at this point it's safe to set the viewBox and remove width/height
	docElement.setAttribute('viewBox', '0 0 %s %s' % (w.value, h.value))
	docElement.removeAttribute('width')
	docElement.removeAttribute('height')

# this is the main method
# input is a string representation of the input XML
# returns a string representation of the output XML
def scourString(in_string, options=[]):
	global numAttrsRemoved
	global numStylePropsFixed
	global numElemsRemoved
	doc = xml.dom.minidom.parseString(in_string)

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
					if child.nodeType in [1, 3, 4, 8] :
						break
				else:
					removeElem = True
			if removeElem :
				elem.parentNode.removeChild(elem)
				numElemsRemoved += 1

	# remove unreferenced gradients/patterns outside of defs
	while removeUnreferencedElements(doc) > 0:
		pass

	if '--enable-id-stripping' in options:
		bContinueLooping = True
		while bContinueLooping:
			identifiedElements = findElementsWithId(doc.documentElement, {})
			referencedIDs = findReferencedElements(doc.documentElement, {})
			bContinueLooping = (removeUnreferencedIDs(referencedIDs, identifiedElements) > 0)
	
	if not '--disable-group-collapsing' in options:
		while removeNestedGroups(doc.documentElement) > 0:
			pass

	while removeDuplicateGradientStops(doc) > 0:
		pass
	
	# remove gradients that are only referenced by one other gradient
	while collapseSinglyReferencedGradients(doc) > 0:
		pass
	
	# clean path data
	for elem in doc.documentElement.getElementsByTagNameNS(NS['SVG'], 'path') :
		cleanPath(elem)

	# convert rasters references to base64-encoded strings 
	for elem in doc.documentElement.getElementsByTagNameNS(NS['SVG'], 'image') :
		embedRasters(elem)		

	# properly size the SVG document (ideally width/height should be 100% with a viewBox)
	properlySizeDoc(doc.documentElement)

	# output the document as a pretty string with a single space for indent
	out_string = doc.documentElement.toprettyxml(' ')
	
	# now strip out empty lines
	lines = []
	# Get rid of empty lines
	for line in out_string.splitlines(True):
		if line.strip():
			lines.append(line)

	# return the string stripped of empty lines
	return "".join(lines)

# used mostly by unit tests
# input is a filename
# returns the minidom doc representation of the SVG
def scourXmlFile(filename, options=[]):
	in_string = open(filename).read()
#	print 'IN=',in_string
	out_string = scourString(in_string, options)
#	print 'OUT=',out_string
	return xml.dom.minidom.parseString(out_string)

def printHeader():
	print APP , VER
	print COPYRIGHT

def printSyntaxAndQuit():
	printHeader()
	print 'usage: scour.py [-i input.svg] [-o output.svg] [OPTIONS]\n'
	print 'If the input file is not specified, stdin is used.'
	print 'If the output file is not specified, stdout is used.\n'
	print 'If an option is not available below that means it occurs automatically'
	print 'when scour is invoked.  Available OPTIONS:\n'
	print '  --enable-id-stripping      : Scour will remove all un-referenced ID attributes'
	print '  --disable-group-collapsing : Scour will not collapse <g> elements'
	print ''
	quit()	

# returns a tuple with:
# input stream, output stream, and a list of options specified on the command-line
def parseCLA():
	args = sys.argv[1:]

	# by default the input and output are the standard streams
	input = sys.stdin
	output = sys.stdout
	options = []
	validOptions = [
					'--disable-group-collapsing',
					'--enable-id-stripping',
					]
					
	i = 0
	while i < len(args):
		arg = args[i]
		i += 1
		if arg == '-i' :
			if i < len(args) :
				input = open(args[i], 'r')
				i += 1
				continue
			else:
				printSyntaxAndQuit()
		elif arg == '-o' :
			if i < len(args) :
				output = open(args[i], 'w')
				i += 1
				continue
			else:
				printSyntaxAndQuit()
		elif arg in validOptions :
			options.append(arg)
		else :
			print 'Error!  Invalid argument:', arg
			printSyntaxAndQuit()
			
	return (input, output, options)

if __name__ == '__main__':

	(input, output, options) = parseCLA()
	
	# if we are not sending to stdout, then print out app information
	bOutputReport = False
	if output != sys.stdout :
		bOutputReport = True
		printHeader()

	# do the work
	in_string = input.read()
	out_string = scourString(in_string, options)
	output.write(out_string)

	# Close input and output files
	input.close()
	output.close()

	# output some statistics if we are not using stdout
	if bOutputReport :
		print " Number of unreferenced id attributes removed:", numIDsRemoved 
		print " Number of elements removed:", numElemsRemoved
		print " Number of attributes removed:", numAttrsRemoved
		print " Number of style properties fixed:", numStylePropsFixed
		print " Number of raster images embedded inline:", numRastersEmbedded
		oldsize = os.path.getsize(input.name)
		newsize = os.path.getsize(output.name)
t		sizediff = (newsize / oldsize);
		print " Original file size:", oldsize, "bytes; new file size:", newsize, "bytes (" + str(sizediff)[:5] + "x)"
