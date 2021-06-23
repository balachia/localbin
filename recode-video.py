#!/usr/bin/env python3

import subprocess
import argparse
import os

def init_parser():
    parser = argparse.ArgumentParser(
            usage = "%(prog)s [OPTION] [FILE]",
            description = "recode video file"
            )
    # parser.add_argument("-i", "--infile", required = True)
    # parser.add_argument("-o", "--outfile", required = True)
    parser.add_argument("infile", nargs = 1)
    parser.add_argument("-o", "--outfile")
    parser.add_argument("-c", "--crf", default = 20, type = int)
    parser.add_argument("--x265", action = "store_true")
    return parser

def main():
    parser = init_parser()
    args = parser.parse_args()
    print(args)

    infile = args.infile[0]
    outfile = args.outfile
    if outfile is None:
        basepath = os.path.splitext(infile)[0]
        outfile = "%s.%s.mp4" % (basepath, 'x265' if args.x265 else 'x264')

    ffmpeg_args = ["ffmpeg", "-hide_banner", "-i", infile]
    ffmpeg_args += (["-c:v", "libx265", "-tag:v", "hvc1"] if args.x265 else ["-c:v", "libx264"])
    ffmpeg_args += ["-preset", "slower", "-crf", str(args.crf), outfile]
    subprocess.call(ffmpeg_args)

if __name__ == '__main__':
    main()

# INFILE=$1
# OUTFILE=$2

# crf=20
# ffmpeg -hide_banner -i $INFILE -c:v libx264 -preset slower -crf ${crf} $OUTFILE

# crf=20
# ffmpeg -hide_banner -i $INFILE -c:v libx265 -preset slower -crf ${crf} -tag:v hvc1 $OUTFILE
