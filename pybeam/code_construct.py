#
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
from opcodes import *

beam_integer = IfThenElse("value", lambda ctx: ctx.tag & 0x08 == 0,
	ExprAdapter(UBInt8("b"),
		decoder = lambda obj, ctx: obj >> 4,
		encoder = None),
	IfThenElse("value", lambda ctx: ctx.tag & 0x10 == 0,
		ExprAdapter(UBInt16("w"), decoder = lambda obj, ctx: ((obj & 0xe000)>>5)|(obj & 0xff), encoder = None),
		String("s", length = lambda ctx: 2+(ctx.tag >> 5))
		)
	)

beam_selectlist = Struct("s",
	UBInt8("dummy_tag"),
	Struct("length",
		Peek(UBInt8("tag")),
		beam_integer),
	Array(lambda ctx: ctx.length.value / 2,
		ExprAdapter(Struct("value",
				LazyBound("op", lambda : beam_operand),
				LazyBound("label", lambda : beam_operand)
			),
			encoder = None,
			decoder = lambda obj,ctx: (obj.op, obj.label),
			)
		),
	)

beam_alloclist = Struct("s",
	UBInt8("dummy_tag"),
	Struct("length",
		Peek(UBInt8("tag")),
		beam_integer),
	Array(lambda ctx: ctx.length.value,
		ExprAdapter(Struct("value",
			Struct("a",
				Peek(UBInt8("tag")),
				beam_integer),
			Struct("b",
				Peek(UBInt8("tag")),
				beam_integer),
			),
			encoder = None,
			decoder = lambda obj,ctx: (obj.a, obj.b),
			)
		),
	)

beam_floatreg = Struct("s",
	UBInt8("dummy_tag"),
	Peek(UBInt8("tag")),
	beam_integer)

beam_literal = Struct("s",
	UBInt8("dummy_tag"),
	Peek(UBInt8("tag")),
	beam_integer)

beam_extended = ExprAdapter(
	Switch("payload", lambda ctx: ctx.type,
		{
			#TAGX_FLOATLIT:
			TAGX_SELECTLIST: beam_selectlist,
			TAGX_FLOATREG: beam_floatreg,
			TAGX_ALLOCLIST: beam_alloclist,
			TAGX_LITERAL: beam_literal,
		}, default = Probe()),
	encoder = None,
	decoder = lambda obj,ctx: obj.value
	)

beam_operand = ExprAdapter(
	Struct("operand",
		Peek(UBInt8("tag")),
		Value("type", lambda ctx: (ctx.tag >> 4)+TAGX_BASE if ctx.tag & 0x07 == TAG_EXTENDED else ctx.tag & 0x07),
		IfThenElse("value", lambda ctx: ctx.type >= TAGX_BASE,
			beam_extended,
			beam_integer
			)
		),
	encoder = None,
	decoder = lambda obj,ctx: (obj.type, obj.value)
	)

beam_instruction = ExprAdapter(
	Struct("instr",
		UBInt8("opcode"),
		Array(lambda ctx: arity[ctx.opcode], beam_operand)
		),
	encoder = None,
	decoder = lambda obj,ctx: (obj.opcode, obj.operand)
	)

beam_code = OptionalGreedyRange(beam_instruction)

__all__ = ["beam_instruction", "beam_code"]

