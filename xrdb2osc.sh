#!/bin/sh

# load definitions and build echo lines
xrdb=$1; shift

PRE='\\033]'
POST='\\007'

COLOR_RE="^.*#define Ansi_([0-9]+)_Color #(......).*$"
FG_RE="^.*#define Foreground_Color #(......).*$"
BG_RE="^.*#define Background_Color #(......).*$"
CURSOR_RE="^.*#define Cursor_Color #(......).*$"

COLOR_FMT="${PRE}4;\\1;#\\2${POST}"
FG_FMT="${PRE}10;#\\1${POST}"
BG_FMT="${PRE}11;#\\1${POST}"
CURSOR_FMT="${PRE}12;#\\1${POST}"

RE="s/${BG_RE}/${BG_FMT}/p;s/${FG_RE}/${FG_FMT}/p;s/${CURSOR_RE}/${CURSOR_FMT}/p;s/${COLOR_RE}/${COLOR_FMT}/p;"

out=$(sed -n -E "$RE" "${xrdb}" | tr '\n' '\0')

if [ $# -eq 0 ]; then
    echo "$out\c"
else
    for file in $@; do
        echo "$out\c" > $file
    done
fi
