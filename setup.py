###############################################################################
#
# Copyright (C) 2013-2014 Tavendo GmbH
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
###############################################################################

import os
import re

from setuptools import find_packages, setup

LONGDESC = """
Scour is an SVG optimizer/cleaner that reduces the size of scalable
vector graphics by optimizing structure and removing unnecessary data.

It can be used to create streamlined vector graphics suitable for web
deployment, publishing/sharing or further processing.

The goal of Scour is to output a file that renderes identically at a
fraction of the size by removing a lot of redundant information created
by most SVG editors. Optimization options are typically lossless but can
be tweaked for more agressive cleaning.

Website
  - http://www.codedread.com/scour/ (original website)
  - https://github.com/scour-project/scour (today)

Authors:
  - Jeff Schiller, Louis Simard (original authors)
  - Tobias Oberstein (maintainer)
  - Patrick Storz (maintainer)
"""

VERSIONFILE = os.path.join(os.path.dirname(os.path.realpath(__file__)), "scour", "__init__.py")
verstrline = open(VERSIONFILE, "rt").read()
VSRE = r"^__version__ = u['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, verstrline, re.M)
if mo:
    verstr = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))


setup(
    name='scour',
    version=verstr,
    description='Scour SVG Optimizer',
    #   long_description = open("README.md").read(),
    long_description=LONGDESC,
    license='Apache License 2.0',
    author='Jeff Schiller',
    author_email='codedread@gmail.com',
    url='https://github.com/scour-project/scour',
    platforms=('Any'),
    install_requires=['six>=1.9.0'],
    packages=find_packages(),
    zip_safe=True,
    entry_points={
        'console_scripts': [
           'scour = scour.scour:run'
        ]},
    classifiers=["License :: OSI Approved :: Apache Software License",
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
    keywords='svg optimizer'
)
