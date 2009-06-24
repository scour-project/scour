#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  Scour Web
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

from mod_python import apache
from mod_python import util
from scour import scourString
from optparse import OptionParser

def form(req):
	return """<!DOCTYPE html>
<html>
<head>
	<title>Scrape Your SVG Files</title>
</head>
<body>
<form method="POST" action="fetch">
	<p>Scra.py uses <a href="http://codedread.com/scour/">Scour</a> to clean SVG files of unnecessary elements and attributes attempting to reduce file size and complexity without a loss in visual quality.  For full details, please see the Scour <a href="http://codedread.com/scour/">home page</a>.
	<p>Paste the SVG file below and click <input type="submit" value="Go!"> or set some <span>Options</span> first.  For a more complete description of the options, see the <a href="http://codedread.com/scour/#options">corresponding scour page</a>.</p>
	<div id="options"><ul>
		<input type="checkbox" id="convertStyleToXml" name="convertStyleToXml" checked>Convert styles to XML attributes</input>
		<input type="checkbox" id="collapseGroups" name="collapseGroups" checked>Collapse nested groups when possible</input>
		<input type="checkbox" id="stripIds" name="stripIds">Strip all unused id attributes</input>
		<input type="checkbox" id="simplifyColors" name="simplifyColors" checked>Simplify colors to #RGB format</input>
		<label>Digits of Precision</label>
		<select id="digits" name="digits">
			<option value="1">1</option>
			<option value="2">2</option>
			<option value="3">3</option>
			<option value="4">4</option>
			<option value="5" selected>5</option>
			<option value="6">6</option>
			<option value="7">7</option>
			<option value="8">8</option>
			<option value="9">9</option>
		</select>
    </div>
	<textarea cols="80" rows="30" name="indoc" id="indoc"></textarea>
</form>
</body>
</html>
	"""

# defaults
class ScourOptions:
	simple_colors = True
	style_to_xml = True
	group_collapse = True
	strip_ids = False
	digits = 5
	embed_rasters = False

# params are the form elements (if a checkbox is unchecked it will not be present)
def fetch(req, indoc,**params):
	req.content_type = "image/svg+xml"
	options = ScourOptions()

	# interpret form options
	if not params.has_key('convertStyleToXml'):
		options.style_to_xml = False
	if not params.has_key('collapseGroups'):
		options.group_collapse = False
	if params.has_key('stripIds'):
		options.strip_ids = True
	if not params.has_key('simplifyColors'):
		options.simple_colors = False
	options.digits = int(params['digits'])

	req.write(scourString(indoc,options))

