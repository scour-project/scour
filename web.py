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
from scour import scourString

def form(req):
	return """<!DOCTYPE html>
<html>
<head>
	<title>Scour it!</title>
</head>
<body>
<form method="POST" action="fetch">
	<p>Paste the SVG file here</p>
	<textarea cols="80" rows="30" name="indoc" id="indoc"></textarea>
	<p>Click "Go!" to Scour</p><input type="submit" value="Go!></input>
</form>
</body>
</html>
	"""

def fetch(req,indoc):
	req.content_type = "image/svg+xml"
	req.write(scourString(indoc))


