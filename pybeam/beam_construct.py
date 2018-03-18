#
# Copyright (c) 2013 Matwey V. Kornilov <matwey.kornilov@gmail.com>
# Copyright (c) 2013 Fredrik Ahlberg <fredrik@z80.se>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

from construct import *
from pybeam.eetf_construct import external_term

chunk_atom = PrefixedArray(Int32ub, PascalString(lengthfield = Int8ub, encoding="latin1"))

chunk_atu8 = PrefixedArray(Int32ub, PascalString(lengthfield = Int8ub, encoding="utf8"))

chunk_attr = external_term

chunk_cinf = external_term

chunk_code = Struct("headerlen" / Int32ub,
	"set" / Int32ub,
	"opcode_max" / Int32ub,
	"labels" / Int32ub,
	"functions" / Int32ub,
	Bytes(lambda ctx: ctx.headerlen-16),
	Bytes(lambda ctx: ctx._.size-ctx.headerlen-4),
	)

chunk_expt = Struct("entry" / PrefixedArray(Int32ub, Struct("function" / Int32ub,
	"arity" / Int32ub,
	"label" / Int32ub)))

chunk_impt = Struct("entry" / PrefixedArray(Int32ub, Struct("module" / Int32ub,
	"function" / Int32ub,
	"arity" / Int32ub)))

uncomp_chunk_litt = Struct("entry" / PrefixedArray(Int32ub, Prefixed(Int32ub, Struct("term" / external_term))))
chunk_litt = Struct(Int32ub,
	"data" / Prefixed(Computed(lambda ctx: ctx._.size-4),
		Compressed(uncomp_chunk_litt, "zlib")
	)
)

chunk_loct = PrefixedArray(Int32ub, Struct("function" / Int32ub,
	"arity" / Int32ub,
	"label" / Int32ub))

chunk = Struct(
	"chunk_name" / String(4),
	"size" / Int32ub,
	"payload" / Switch(this.chunk_name,
				{
#				"Abst" : chunk_abst,
				b"Atom" : chunk_atom,
				b"AtU8" : chunk_atu8,
				b"Attr" : chunk_attr,
				b"CInf" : chunk_cinf,
				b"Code" : chunk_code,
				b"ExpT" : chunk_expt,
#				"FunT" : chunk_funt,
				b"ImpT" : chunk_impt,
#				"Line" : chink_line,
				b"LitT" : chunk_litt,
				b"LocT" : chunk_loct,
#				"StrT" : chunk_strt,
#				"Trac" : chunk_trac,
				},
				default = Bytes(lambda ctx: ctx.size)
			),
# Aligned(4, ..)
	Padding(lambda ctx: (4 - ctx.size % 4) % 4, pattern = b'\00'),
	)

beam = Struct(
	"for1" / Const(b'FOR1'),
	"size" / Int32ub,
	"beam" / Const(b'BEAM'),
	"chunk" / GreedyRange(chunk),
	Terminated,
	)

__all__ = ["beam"]

