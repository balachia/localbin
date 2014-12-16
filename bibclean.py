#!/usr/local/bin/python
import bibtexparser as btp
from bibtexparser.bparser import BibTexParser
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.customization import homogeneize_latex_encoding, convert_to_unicode
from bibtexparser.latexenc import string_to_latex
import os.path
from os import remove
import tempfile
from subprocess import call
import codecs
import re

bibtool = '''
key.format = {
    {%-2n(author) # %-2n(editor)}
    %d(year)}
sort = {on}
'''

def seek_errors(bibdat):
    entries = list(bibdat.entries)
    res = seek_error_sub(bibdat, entries, 0, len(entries) - 1)
    bibdat.entries=entries
    return res

def seek_error_sub(bibdat, entries, minidx, maxidx):
    #print('%s : %s' % (minidx, maxidx))

    #bibdat.entries = entries[minidx:maxidx]
    halfidx = (maxidx + minidx) / 2
    #if halfidx == minidx or halfidx == maxidx:
        #return []

    res = list()

    try:
        bibdat.entries = entries[minidx:halfidx]
        #tf.write(btp.dumps(bibdat))
        btp.dumps(bibdat)
    except:
        if halfidx - minidx == 1:
            res += [minidx]
        else:
            res += seek_error_sub(bibdat, entries, minidx, halfidx)
    else:
        res += []

    try:
        bibdat.entries = entries[halfidx:maxidx]
        #tf.write(btp.dumps(bibdat))
        btp.dumps(bibdat)
    except:
        if maxidx - halfidx == 1:
            res += [halfidx]
        else:
            res += seek_error_sub(bibdat, entries, halfidx, maxidx)
    else:
        res += []

    return res

# customization:
# have to preserve title formatting:
def preserve_title(record):
    record = convert_to_unicode(record)
    for val in record:
        if val not in ('id',):
            #logger.debug('Apply string_to_latex to: %s', val)
            record[val] = string_to_latex(record[val])
            if val == 'title':
                #logger.debug('Protect uppercase in title')
                #logger.debug('Before: %s', record[val])
                title = re.sub(r'(?<!\\)((\\\\)*)(\{|\})',r'\1',record[val])
                record[val] = '{' + title + '}'
                #logger.debug('After: %s', record[val])
    return record


# sanitize mendeley's terrible special character encoding
with open(os.path.expanduser('~/Documents/library.bib'), mode='r') as fin:
    parser = BibTexParser()
    #parser.customization = homogeneize_latex_encoding
    parser.customization = preserve_title
    bibdat = btp.load(fin, parser=parser)

errors = seek_errors(bibdat)
for err in errors:
    print(err)
    print(bibdat.entries[err])

if errors:
    raise SystemExit('Irreconcilable errors in bibtex')

# apparently that was enough to clean up...
#authors = [[x['author'], x['title']] for x in bibdat.entries if 'author' in x]

# now write out and try to bibtool some new keys?
bib_clean_name = tempfile.mkstemp()[1]
bibtool_script_name = tempfile.mkstemp()[1]

bib_clean = codecs.open(bib_clean_name, mode='w', encoding='utf8')
bibtool_script = codecs.open(bibtool_script_name, mode='w', encoding='utf8')

# write out the file
writer = BibTexWriter()
bib_clean.write(writer.write(bibdat))

bibtool_script.write(bibtool)

call(['bibtool',
    '-r', bibtool_script_name,
    '-o', os.path.expanduser('~/Documents/library-clean.bib'),
    '-i', bib_clean_name])

bib_clean.close()
bibtool_script.close()

remove(bib_clean_name)
remove(bibtool_script_name)
