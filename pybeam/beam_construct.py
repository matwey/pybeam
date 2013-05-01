#
# Copyright (c) 2013 Matwey V. Kornilov <matwey.kornilov@gmail.com>
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
from eetf_construct import term

chunk_atom = Struct("chunk_atom",
	UBInt32("len"),
	Array(lambda ctx: ctx.len, PascalString("atom"))
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

chunk_loct = Struct("chunk_loct",
	UBInt32("len"),
	Array(lambda ctx: ctx.len, Struct("entry",
			UBInt32("function"),
			UBInt32("arity"),
			UBInt32("label"),
		)
	)
	)

chunk_attr = Struct("chunk_attr",
	Const(UBInt8("131"),131),
	term
	)

chunk_cinf = Struct("chunk_cinf",
	Const(UBInt8("131"),131),
	term
	)

chunk = Struct("chunk",
	String("chunk_name",4),
	UBInt32("size"),
	SeqOfOne("payload",
		Switch("payload", lambda ctx: ctx.chunk_name,
			{
			"Atom" : chunk_atom,
			"ExpT" : chunk_expt,
			"ImpT" : chunk_impt,
#			"Code" : chunk_code,
#			"StrT" : chunk_strt,
			"Attr" : chunk_attr,
			"CInf" : chunk_cinf,
			"LocT" : chunk_loct,
#			"Trac" : chunk_trac,
			},
			default = String("skip", lambda ctx: ctx.size)
		),
		Padding(lambda ctx: (4 - ctx.size % 4) % 4, pattern = "\00"),
		nested = False,
	)
	)

beam = Struct("beam",
	Const(String('for1',4),'FOR1'),
	UBInt32("size"),
	Const(String('beam',4),'BEAM'),
	GreedyRange(chunk),
	Terminator,
	)

__all__ = ["beam"]

