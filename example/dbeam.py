#!/usr/bin/env python
#
# Quick and dirty BEAM disassembler
# using pybeam
#
# 131005 Fredrik Ahlberg <fredrik@z80.se>

import sys
import pybeam
from pybeam.opcodes import *
from pybeam.code_construct import beam_code

""" Human readable representation of operand. Performs lookup of atoms and literals """
def pretty_operand(o):
    if o[0] == TAG_LITERAL:
        return '%d' % o[1]
    elif o[0] == TAG_INTEGER:
        return '#%d' % o[1]
    elif o[0] == TAG_ATOM:
        if o[1] == 0:
            return 'nil'
        else:
            return '%s' % b.atoms[o[1]-1]
    elif o[0] == TAG_XREG:
        return 'x(%d)' % o[1]
    elif o[0] == TAG_YREG:
        return 'y(%d)' % o[1]
    elif o[0] == TAG_LABEL:
        return 'L%d' % o[1]
    elif o[0] == TAGX_FLOATLIT:
        return '#%e' % o[1]
    elif o[0] == TAGX_LITERAL:
        return '%s' % (b.literals[o[1]],)
    elif o[0] == TAGX_SELECTLIST:
        return '[\n\t\t%s\n\t]' % ',\n\t\t'.join(map(lambda x: '(%s, %s)' % (pretty_operand(x[0]), pretty_operand(x[1])), o[1]))
    elif o[0] == TAGX_ALLOCLIST:
        return 'alloc{%s}' % ', '.join(map(lambda x: '%s: %d' % ("words" if x[0] == 0 else "floats", x[1]), o[1]))
    elif o[0] == TAGX_FLOATREG:
        return 'f(%d)' % o[1]
    else:
        return 'wtf(%d,%s)' % (o[0], o[1])

if __name__ == '__main__':
    fname = sys.argv[1] if len(sys.argv) > 1 else '/usr/lib/erlang/lib/compiler-4.8.1/ebin/beam_dict.beam'
    b = pybeam.BeamFile(fname)

    print '# Module: %s' % b.modulename
    print '#'

    print '# Exports:\n#\t' + '\n#\t'.join(map(lambda x: '%s/%d' % (x[0],x[1]), b.exports))
    print '#'

    print '# Imports:\n#\t' + '\n#\t'.join(map(lambda x: '%s:%s/%d' % (x[0],x[1],x[2]), b.imports))
    print '#'

    print '# Attributes:\n#\t' + '\n#\t'.join(map(lambda x: '%s:\t%s' % (x[0],x[1]), b.attributes.items()))
    print '#'

    print '# CompileInfo:\n#\t' + '\n#\t'.join(map(lambda x: '%s:\t%s' % (x[0],x[1]), b.compileinfo.items()))
    print

    (_,_,_,_,code) = b.code

    for (op, operands) in beam_code.parse(code):
        if op == LABEL:
            print 'L%d:' % operands[0][1]
        elif op == LINE:
            print ' \t#line %s' % pretty_operand(operands[0])
        elif op == FUNC_INFO:
            print '\t#function %s:%s/%d' % (b.atoms[operands[0][1]-1], b.atoms[operands[1][1]-1], operands[2][1])
        elif op in (CALL_EXT, CALL_EXT_ONLY):
            print '\t%s %s %d' % (opnames[op], '%s:%s/%d'%b.imports[operands[1][1]], operands[0][1])
        elif op == CALL_EXT_LAST:
            print '\t%s %s %d %d' % (opnames[op], '%s:%s/%d'%b.imports[operands[1][1]], operands[0][1], operands[2][1])
        else:
            print '\t', opnames[op], ', '.join(map(pretty_operand, operands))

