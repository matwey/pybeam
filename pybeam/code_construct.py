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
from construct.core import _read_stream
from opcodes import *

class BeamInteger(Construct):

	def _decode_bigint(self, s):
		v = int(s.encode("hex"), 16)
		if ord(s[0]) > 0x80:
			return v-(1 << (len(s))*8) 
		else:
			return v

	def __init__(self, name):
		Construct.__init__(self, name)

	def _parse(self, stream, context):
		tag = ord(_read_stream(stream, 1))

		# single byte or longer?
		if tag & 0x08:
			# 11 bits or longer?
			if tag & 0x10:
				# longer. 3-bit length or longer?
				if tag & 0xe0 == 0xe0:
					# long length!
					length = self._parse(stream, context) + (tag >> 5) + 2
					return self._decode_bigint(_read_stream(stream, length))
				else:
					# 3-bit length
					return self._decode_bigint(_read_stream(stream, 2+(tag >> 5)))
			else:
				# 11 bits
				w = ord(_read_stream(stream, 1))
				return ((tag & 0xe0)<<3)|w
		else:
			# four bits
			return tag >> 4

	def _build(self, obj, stream, context):
		pass

	def _sizeof(self, context):
		raise SizeofError("Can't calculate size")

beam_selectlist = Struct("s",
	UBInt8("dummy_tag"),
	BeamInteger("length"),
	Array(lambda ctx: ctx.length / 2,
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
	BeamInteger("length"),
	Array(lambda ctx: ctx.length,
		ExprAdapter(Struct("value",
			Struct("a",
				Peek(UBInt8("tag")),
				BeamInteger("value")),
			Struct("b",
				Peek(UBInt8("tag")),
				BeamInteger("value")),
			),
			encoder = None,
			decoder = lambda obj,ctx: (obj.a, obj.b),
			)
		),
	)

beam_floatlit = Struct("s",
	UBInt8("dummy"),
	BFloat64("value"))

beam_floatreg = Struct("s",
	UBInt8("dummy_tag"),
	Peek(UBInt8("tag")),
	BeamInteger("value"))

beam_literal = Struct("s",
	UBInt8("dummy_tag"),
	Peek(UBInt8("tag")),
	BeamInteger("value"))

beam_extended = ExprAdapter(
	Switch("payload", lambda ctx: ctx.type,
		{
			TAGX_FLOATLIT: beam_floatlit,
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
			BeamInteger("value")
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

