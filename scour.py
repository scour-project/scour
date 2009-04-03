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
# 3) Issue error if input.svg does not exist
# 4) Create the output file (issue error if cannot create)
# 5) Copy input file text to output file text
# 6) Read input file into memory using an XML library
# 7) Implement a function that will remove all unreferenced id attributes from
#    from an SVG document (xlink:href="#someid", fill="url(#someid)", etc)
# 8) Implement a function that will remove all gradients that have no id
# 9) Implement command-line options to run the above 2 rules

import sys

APP = 'Scour'
VER = '0.01'
COPYRIGHT = 'Copyright Jeff Schiller, 2009'

print APP + ' ' + VER
print COPYRIGHT

# parse command-line arguments
args = sys.argv[1:]

if( len(args) != 4 ):
	print 'Error!  Invalid number of arguments'
	quit()
	
infile = ''
outfile = ''
	
if( args[0] == '-i' ):
	infile = args[1]
elif( args[2] == '-i' ):
	infile = args[3]
	
if( args[0] == '-o' ):
	outfile = args[1]
elif(args[2] == '-o' ):
	outfile = args[3]

if( infile == '' ):
	print 'Error!  -i argument missing'
	quit()
	
if( outfile == '' ):
	print 'Error!  -o argument is missing'
	quit()
	
print 'infile=' + infile + ', outfile=' + outfile
