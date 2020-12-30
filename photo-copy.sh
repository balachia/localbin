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
OUTDIRRAW="$OUTDIR/raw-$OUT"
OUTDIRVID="$OUTDIR/video-$OUT"
mkdir -p "$OUTDIR" "$OUTDIRRAW" "$OUTDIRVID"

# find raw folders
#INDIR="/Volumes/$DIR/DCIM/100MSDCF/"
INDIR=$(find "/Volumes/$DIR/DCIM" -maxdepth 1 -type d -name "*MSDCF" -print)
INDIRLINES=$(echo $INDIR | wc -l)
echo "Reading:\n$INDIR"

if [ $INDIRLINES -gt 1 ]; then
    echo "Too many directories"
    exit 1
fi

# copy raws
rsync -av --info=progress2 --include "*.ARW" --exclude "*" "$INDIR/" "$OUTDIRRAW"

# TODO: copy loose jpegs

# TODO: copy videos
