#!/usr/bin/python2.4
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

import cgi
import cgitb
cgitb.enable()
from scour import scourString

def main():
	# From what I can make out, cgi.FieldStorage() abstracts away whether this is a GET/POST
	# From http://www.linuxjournal.com/article/3616 it says that POST actually comes in via stdin
	# and GET comes in QUERY_STRING environment variable.
	form = cgi.FieldStorage()
	
	if not form.has_key('indoc'):
		doGet()
	else:
		doPut(form)

def doPut(form):
	print "Content-type: image/svg+xml\n"
	print scourString(form['indoc'].value, None)

def doGet():
	print "Content-type: text/html\n"

	print """
<!DOCTYPE html>
<html>
<head>
	<title>Scour it!</title>
</head>
<body>
<form method="POST" action="webscour.py">
	<p>Paste the SVG file here</p>
	<textarea cols="100" rows="40" name="indoc" id="indoc"></textarea>
	<p>Click "Go!" to Scour</p><input type="submit" value="Go!></input>
</form>
</body>
</html>
	"""
	
main()