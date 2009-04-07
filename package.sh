#!/bin/bash
SCOURVER="0.04"
tar cvf scour-$SCOURVER.tar scour.py LICENSE NOTICE README.txt
gzip scour-$SCOURVER.tar