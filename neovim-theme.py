#!/usr/bin/env python

import argparse
import neovim
from collections import defaultdict

parser = argparse.ArgumentParser(description='Retheme neovim at socket')
parser.add_argument('path', type=str)
parser.add_argument('theme_path', type=str)
args = parser.parse_args()

print(args.path)
print(args.theme_path)

nv = neovim.attach('socket', path=args.path)

with open(args.theme_path, mode='r') as fin:
    theme = fin.read().strip()

print(theme)

theme_dict = defaultdict(lambda x: 'ThemeDark')
theme_dict.update({
    'light' : 'ThemeLight',
    'dark'  : 'ThemeDark'})

nv.call(theme_dict[theme])
