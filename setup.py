###############################################################################
##
##  Copyright (C) 2013-2014 Tavendo GmbH
##
##  Licensed under the Apache License, Version 2.0 (the "License");
##  you may not use this file except in compliance with the License.
##  You may obtain a copy of the License at
##
##      http://www.apache.org/licenses/LICENSE-2.0
##
##  Unless required by applicable law or agreed to in writing, software
##  distributed under the License is distributed on an "AS IS" BASIS,
##  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
##  See the License for the specific language governing permissions and
##  limitations under the License.
##
###############################################################################

import re
from setuptools import setup, find_packages

LONGDESC = """
Scour is a SVG optimizer/sanitizer that can be used to produce SVGs for Web deployment.

Website
  - http://www.codedread.com/scour/ (original website)
  - https://github.com/codedread/scour (today)

Authors:
  - Jeff Schiller, Louis Simard (original authors)
  - Tobias Oberstein (maintainer)
"""

VERSIONFILE = "scour/__init__.py"
verstrline = open(VERSIONFILE, "rt").read()
VSRE = r"^__version__ = u['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, verstrline, re.M)
if mo:
    verstr = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))


setup (
   name = 'scour',
   version = verstr,
   description = 'Scour SVG Optimizer',
#   long_description = open("README.md").read(),
   long_description = LONGDESC,
   license = 'Apache License 2.0',
   author = 'Jeff Schiller',
   author_email = 'codedread@gmail.com',
   url = 'https://github.com/codedread/scour',
   platforms = ('Any'),
   install_requires = ['six>=1.9.0'],
   packages = find_packages(),
   zip_safe = True,
   entry_points = {
      'console_scripts': [
         'scour = scour.scour:run'
      ]},
   classifiers = ["License :: OSI Approved :: Apache Software License",
                  "Development Status :: 5 - Production/Stable",
                  "Environment :: Console",
                  "Intended Audience :: Developers",
                  "Intended Audience :: System Administrators",
                  "Operating System :: OS Independent",
                  "Programming Language :: Python",
                  "Topic :: Internet",
                  "Topic :: Software Development :: Build Tools",
                  "Topic :: Software Development :: Pre-processors",
                  "Topic :: Multimedia :: Graphics :: Graphics Conversion",
                  "Topic :: Utilities"],
   keywords = 'svg optimizer'
)
