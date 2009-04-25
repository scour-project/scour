#!/bin/bash
SCOURVER="0.10"
tar cvf scour-$SCOURVER.tar scour.py LICENSE NOTICE README.txt release-notes.html
gzip scour-$SCOURVER.tar
