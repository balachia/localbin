#!/bin/sh

# color fg/default bg
for i in {0..15}; do
    [ $i == 8 ] && echo ''
    echo "\033[38;5;${i}m::\c"
done

echo '\033[0m\n'

# default fg/color bg
for i in {0..15}; do
    [ $i == 8 ] && echo ''
    echo "\033[48;5;${i}m::\c"
done

echo '\033[0m\n'

# swap fg/color bg
for i in {0..15}; do
    [ $i == 8 ] && echo ''
    echo "\033[7;38;5;${i}m::\c"
done



echo '\033[0m'
