#!/bin/bash
SCOURVER="0.03"
tar cvf scour-$SCOURVER.tar scour.py LICENSE.txt README.txt
gzip scour-$SCOURVER.tar