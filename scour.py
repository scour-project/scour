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
# 4) Accept file from stdin if no -i arg present
# 5) Write file to stdout if no -o present
# 6) Read input file into memory using an XML library
# 7) Implement a function that will remove all unreferenced id attributes from
#    from an SVG document (xlink:href="#someid", fill="url(#someid)", etc)
# 8) Implement a function that will remove all gradients that have no id
# 9) Implement command-line options to run the above 2 rules

import sys

APP = 'Scour'
VER = '0.01'
COPYRIGHT = 'Copyright Jeff Schiller, 2009'

print APP , VER
print COPYRIGHT

# parse command-line arguments
args = sys.argv[1:]

input = sys.stdin
output = sys.stdout

if( len(args) == 2):
	if( args[0] == '-i' ):
		input = open(args[1], 'r')
	elif( args[0] == '-o' ):
		output = open(args[1], 'w')
	else:
		sys.stderr.write('Invalid syntax\n')
		quit()

elif( len(args) == 4 ):
	if( args[0] == '-i' and args[2] == '-o' ):
		input = open(args[1], 'r')
		output = open(args[3], 'w')
	elif( args[0] == '-o' and args[2] == 'i' ):
		output = open(args[1], 'w')
		input = open(args[3], 'r')
	else:
		sys.stderr.write('Invalid syntax\n')
		quit()
	
elif( len(args) != 0 ):
	sys.stderr.write('Invalid syntax\n')
	quit()

# simply write the input to the output for now
output.write(input.read());

# Close input and output files
input.close()
output.close()
