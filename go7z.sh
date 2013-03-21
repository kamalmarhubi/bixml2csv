#!/bin/sh

FILE=$1
OUTDIR=${2-csv}
BASENAME=`basename $FILE .7z`
DIRNAME=`dirname $FILE`
7z e -so $DIRNAME/$BASENAME.7z \
	| python parse.py --header -v 2> $OUTDIR/$BASENAME.stderr \
	| xz > $OUTDIR/$BASENAME.csv.xz
