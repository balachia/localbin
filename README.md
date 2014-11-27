# ~/.local/bin

## CriticMarkup.py

Strips [CriticMarkup](http://criticmarkup.com/) from files. Kind of hackish:

 - strips addition, highlight, end of substitution (`~~}`) tags
 - strips all text between deletion, comment, and beginning of substition tags
    (`{~~` - `~>`)

This has the natural side effect of stripping any such things from verbatim
code, so we'll have to see if we ever run into that problem.

### TODO:

 - make a STDIN/STDOUT option


## bibclean.py

Cleans the messy bibtex thing [Mendeley](http://www.mendeley.com) spits out, by
running it through [`bibtexparser`](https://pypi.python.org/pypi/bibtexparser).
Several reasons for this:

1. standardize keys
2. unbreak Mendeley's mangling of non-ASCII characters, such as {\o}

### TODO:

 - keep this thing from breaking old keys: right now, it can conceivably rewrite
 old keys. I want to figure out a way to sort items by date of addition into the
 database.


## marked-gpp

STDIN -> STDOUT wrapper for
[gpp](http://files.nothingisreal.com/software/gpp/gpp.html), because that's what
[Marked](http://marked2app.com/) needs.

