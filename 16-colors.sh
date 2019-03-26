#!/bin/sh

# color fg/default bg
for i in {0..15}; do
    [ $i == 8 ] && printf '\n'
    printf "\033[38;5;${i}m::"
done

printf '\033[0m\n\n'

# default fg/color bg
for i in {0..15}; do
    [ $i == 8 ] && printf '\n'
    printf "\033[48;5;${i}m::"
done

printf '\033[0m\n\n'

# swap fg/color bg
for i in {0..15}; do
    [ $i == 8 ] && printf '\n'
    printf "\033[7;38;5;${i}m::"
done



printf '\033[0m'
