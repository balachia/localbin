#!/bin/sh

if [ "$1" == "" ]; then
    echo "USAGE: photo-copy.sh [-d|DIR]"
    echo "\tDIR\tSD card volume"
    echo "\t-d\tUse default DIR: \"NO NAME\"\n"
    ls /Volumes
    exit
elif [ "$1" == "-d" ]; then
    DIR="NO NAME"
else
    DIR="$1"
fi

OUT=$(date "+%Y-%m-%d")
OUTDIR="$HOME/Pictures/working/$OUT"
mkdir -p "$OUTDIR"

#INDIR="/Volumes/$DIR/DCIM/100MSDCF/"
INDIR=$(find "/Volumes/$DIR/DCIM" -maxdepth 1 -type d -name "*MSDCF" -print)
INDIRLINES=$(echo $INDIR | wc -l)
echo "Reading:\n$INDIR"

if [ $INDIRLINES -gt 1 ]; then
    echo "Too many directories"
    exit 1
else
    rsync -av --info=progress2 --include "*.ARW" --exclude "*" "$INDIR/" "$OUTDIR"
fi
