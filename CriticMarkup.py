#!/usr/local/bin/python

# wrapper for CriticMarkup.pl that gets us out of STDIN/STDOUT
# nope: gonna have to rewrite it away from linewise operation

import re
import sys

cms = {
    'add':[r'\{\+\+|\+\+\}'],
    'hil':[r'\{==|==\}'],
    'subend':[r'~~\}'],
    'del':[r'\{--(.*)--\}', r'\{--(.*)$', r'^(.*)--\}'],
    'com':[r'\{>>(.*)<<\}', r'\{>>(.*)$', r'^(.*)<<\}'],
    'sub':[r'\{~~(.*)~>\}', r'\{~~(.*)$', r'^(.*)~>\}']
    }
cm_order = ['add','hil','subend','del','com','sub']

def cm_process(line, mode=None):
    if mode:
        (line,nsub) = re.subn(cms[mode][2],'',line)
        if nsub==0:
            return ('',mode)

    changes = dict()
    for k in cm_order:
        vs = cms[k]
        nsub = -1
        if len(vs) == 1:
            while nsub != 0:
                (line, nsub) = re.subn(vs[0],'',line)
        elif len(vs) == 3:
            while nsub != 0:
                (line, nsub) = re.subn(vs[0],'',line)
            (line, nsub) = re.subn(vs[1],'',line)
            if nsub > 0:
                return(line,k)

    return (line,None)

if __name__=='__main__':
    # open first argument
    # write to second
    # no error checking!
    fin = open(sys.argv[1], mode='r')
    fout = open(sys.argv[2], mode='w')

    mode=None
    for line in fin:
        #print(line),
        (line,mode) = cm_process(line,mode)
        fout.write(line)
        #print(str(mode) + ' :: ' + line)

    fin.close()
    fout.close()


