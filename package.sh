#!/bin/bash
SCOURVER="0.20"
cd ..
zip scour/tarballs/scour-$SCOURVER.zip scour/scour.py scour/svg_regex.py scour/LICENSE scour/NOTICE scour/README.txt scour/release-notes.html
cd scour
zip tarballs/scour-inkscape-extension-$SCOURVER.zip scour.inx scour.inkscape.py scour.py svg_regex.py
