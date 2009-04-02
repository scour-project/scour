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
# 0) Output program name and version
# 1) Process input arguments -i input.svg -o output.svg
# 2) Issue errors if any of those arguments are not present (display syntax)
# 3) Issue error if input.svg does not exist
# 4) Create the output file (issue error if cannot create)
# 5) Copy input file text to output file text
# 6) Read input file into memory using an XML library
# 7) Implement a function that will remove all unreferenced id attributes from
#    from an SVG document (xlink:href="#someid", fill="url(#someid)", etc)
# 8) Implement a function that will remove all gradients that have no id
# 9) Implement command-line options to run the above 2 rules

APP = "Scour"
VER = "0.01"
COPYRIGHT = "Copyright Jeff Schiller, 2009"

print APP + ' version ' + VER
print COPYRIGHT