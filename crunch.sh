#!/bin/bash
mkdir $1
for FILE in `ls fulltests`
do
	echo Doing $FILE:
	./scour.py -i fulltests/$FILE -o $1/$FILE 2>> $1/report.txt
done
