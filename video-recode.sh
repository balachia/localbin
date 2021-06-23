#!/bin/sh

WORKDIR=$HOME/Pictures/working
if [ "$1" == "" ]; then
    echo "Usage: photo-backup.sh FOLDER"
    ls $WORKDIR
    exit 1
fi

INDIR=$WORKDIR/$1/_video
OUTDIR=$WORKDIR/$1/video

mkdir -p $OUTDIR

#for file in $(find $INDIR -iregex ".*\.mp4" -printf "\n"); do
for file in $(ls $INDIR | grep .MP4); do
    fn=$(basename -s .MP4 $file)
    mode=x265
    echo "\n============================================================"
    echo $file
    echo "============================================================\n"
    case $mode in
        x264)
            crf=20
            post=x264.crf${crf}
            ffmpeg -hide_banner -i $INDIR/$file -c:v libx264 -preset slow -crf ${crf} $OUTDIR/$fn.$post.mp4
            ;;
        x265)
            crf=20
            post=x265.crf${crf}
            ffmpeg -hide_banner -i $INDIR/$file -c:v libx265 -preset slower -crf ${crf} -tag:v hvc1 $OUTDIR/$fn.$post.mp4
            ;;
        hevc)
            post=hevc.4000
            ffmpeg -hide_banner -i $INDIR/$file -c:v hevc_videotoolbox -profile:v main -b:v 4000k $OUTDIR/$fn.hevc.4000.mp4
            ;;
    esac
    echo "============================================================"
    echo PSNR
    echo "============================================================"
    ffmpeg -hide_banner -i $INDIR/$file -i $OUTDIR/$fn.$post.mp4 -filter_complex "psnr" -f null /dev/null
    #sleep 10
done
