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
from pybeam.eetf_construct import term, external_term
import codecs

erl_version_magic = Magic(b'\x83')

chunk_atom = Rename("chunk_atom", PrefixedArray(PascalString("atom", encoding="latin1"), length_field = UBInt32("len")))

chunk_attr = Rename("chunk_attr", external_term)

chunk_cinf = Rename("chunk_cinf", external_term)

chunk_code = Struct("chunk_code",
	UBInt32("headerlen"),
	UBInt32("set"),
	UBInt32("opcode_max"),
	UBInt32("labels"),
	UBInt32("functions"),
	Bytes("skip", lambda ctx: ctx.headerlen-16),
	Bytes("code", lambda ctx: ctx._.size-ctx.headerlen-4),
	)

chunk_expt = Struct("chunk_expt",
	UBInt32("len"),
	Array(lambda ctx: ctx.len, Struct("entry",
			UBInt32("function"),
			UBInt32("arity"),
			UBInt32("label"),
		)
	)
	)

chunk_impt = Struct("chunk_impt",
	UBInt32("len"),
	Array(lambda ctx: ctx.len, Struct("entry",
			UBInt32("module"),
			UBInt32("function"),
			UBInt32("arity"),
		)
	)
	)

chunk_litt = Struct("chunk_litt",
	UBInt32("len_uncompressed"),
	TunnelAdapter(
		ExprAdapter(Bytes("data", length = lambda ctx: ctx._.size-4),
			encoder = lambda obj,ctx: codecs.encode(obj,"zlib_codec"),
	                decoder = lambda obj,ctx: codecs.decode(obj,"zlib_codec")
		),
		Struct("uncompressed",
			UBInt32("len"),
			Array(lambda ctx: ctx.len, Struct("entry",
					UBInt32("len"),
					erl_version_magic,
					term
				)
			)
		)
	)
	)

chunk_loct = Struct("chunk_loct",
	UBInt32("len"),
	Array(lambda ctx: ctx.len, Struct("entry",
			UBInt32("function"),
			UBInt32("arity"),
			UBInt32("label"),
		)
	)
	)

chunk_strt = Struct("chunk_strt",
	PascalString("string", length_field = UBInt32("len"), encoding="latin1")
	)

chunk = Struct("chunk",
	String("chunk_name",4),
	UBInt32("size"),
	If(lambda ctx: ctx.size > 0,
		SeqOfOne("payload",
			Switch("payload", lambda ctx: ctx.chunk_name,
				{
#				"Abst" : chunk_abst,
				b"Atom" : chunk_atom,
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
				default = Bytes("skip", lambda ctx: ctx.size)
			),
			Padding(lambda ctx: (4 - ctx.size % 4) % 4, pattern = "\00"),
			nested = False,
		),
		[]
		)
	)

beam = Struct("beam",
	Const(String('for1',4),b'FOR1'),
	UBInt32("size"),
	Const(String('beam',4),b'BEAM'),
	OptionalGreedyRange(chunk),
	Terminator,
	)

__all__ = ["beam"]

