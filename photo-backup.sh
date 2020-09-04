#!/bin/sh

if [ "$1" == "" ]; then
    echo "Usage: photo-backup.sh FOLDER"
    exit 1
fi

WORKDIR=$HOME/Pictures/working
OUTDIR=/Volumes/home/Photos

cd $WORKDIR

# check that backup dir exists
if [[ -d $OUTDIR ]]; then
    rsync -av --info=progress2 --include="$1**" --exclude="*" . /Volumes/home/Photos/
else
    echo "Backup directory not found: $OUTDIR"
fi
