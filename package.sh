#!/bin/bash
SCOURVER="0.10"
cd ..
tar cvf scour/tarballs/scour-$SCOURVER.tar scour/scour.py scour/LICENSE scour/NOTICE scour/README.txt scour/release-notes.html
gzip scour/tarballs/scour-$SCOURVER.tar
cd scour
