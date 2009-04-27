#!/bin/bash
mkdir $1
for FILE in `ls fulltests`
do
	./scour.py -i fulltests/$FILE -o $1/$FILE >> $1/report.txt
done
	