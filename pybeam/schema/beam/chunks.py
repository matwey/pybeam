#
# Copyright (c) 2013-2018 Matwey V. Kornilov <matwey.kornilov@gmail.com>
# Copyright (c) 2013      Fredrik Ahlberg <fredrik@z80.se>
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

from construct import this
from construct import (
	Aligned,
	Bytes,
	Compressed,
	GreedyBytes,
	Int32ub,
	Int8ub,
	PascalString,
	Prefixed,
	PrefixedArray,
	Sequence,
	Struct,
	Switch,)

from pybeam.schema.eetf import external_term

Atom = PrefixedArray(Int32ub, PascalString(lengthfield=Int8ub, encoding="latin1"))

AtU8 = PrefixedArray(Int32ub, PascalString(lengthfield=Int8ub, encoding="utf8"))

Attr = external_term

CInf = external_term

Code = Struct("headerlen" / Int32ub,
	"set" / Int32ub,
	"opcode_max" / Int32ub,
	"labels" / Int32ub,
	"functions" / Int32ub,
	Bytes(lambda ctx: ctx.headerlen-16),
	GreedyBytes)

ExpT = Struct("entry" / PrefixedArray(Int32ub, Struct("function" / Int32ub,
	"arity" / Int32ub,
	"label" / Int32ub)))

ImpT = Struct("entry" / PrefixedArray(Int32ub, Struct("module" / Int32ub,
	"function" / Int32ub,
	"arity" / Int32ub)))

uncomp_chunk_litt = PrefixedArray(Int32ub, Prefixed(Int32ub, external_term))
LitT = Struct(Int32ub,
	"entry" / Compressed(uncomp_chunk_litt, "zlib"))

LocT = PrefixedArray(Int32ub, Struct("function" / Int32ub,
	"arity" / Int32ub,
	"label" / Int32ub))

chunk = Sequence(
	"chunk_name" / Bytes(4),
	Aligned(4, Prefixed(Int32ub, Switch(this.chunk_name, {
#		"Abst" : chunk_abst,
		b"Atom" : Atom,
		b"AtU8" : AtU8,
		b"Attr" : Attr,
		b"CInf" : CInf,
		b"Code" : Code,
		b"ExpT" : ExpT,
#		"FunT" : chunk_funt,
		b"ImpT" : ImpT,
#		"Line" : chink_line,
		b"LitT" : LitT,
		b"LocT" : LocT,
#		"StrT" : chunk_strt,
#		"Trac" : chunk_trac,
	}, default=GreedyBytes))))

__all__ = ["chunk"]
