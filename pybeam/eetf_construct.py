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

# External Term Format

from erlang_types import AtomCacheReference, Reference, Port, Pid, String as etString, Binary
from construct import *

class TupleAdapter(Adapter):
	def _decode(self, obj, ctx):
# we got a list from construct and want to see a tuple
		return tuple(obj)
	def _encode(self, obj, ctv):
		return list(obj)

atom_cache_ref = ExprAdapter(UBInt8("atom_cache_ref"),
		encoder = lambda obj,ctx: obj.index,
		decoder = lambda obj,ctx: AtomCacheReference(obj))
small_integer = UBInt8("small_integer")
integer = SBInt32("integer")
float_ = ExprAdapter(String("float",31),
		encoder = lambda obj,ctx: "%.20e    " % obj,
		decoder = lambda obj,ctx: float(obj))
atom = PascalString("atom", length_field = UBInt16("length"))
reference = ExprAdapter(Sequence("reference",
		LazyBound("Node", lambda : term),
		UBInt32("ID"),
		UBInt8("Creation"),
		nested = False),
		encoder = lambda obj,ctx: (obj.node, obj.id, obj.creation),
		decoder = lambda obj,ctx: Reference(*obj))
port = ExprAdapter(Sequence("port",
		LazyBound("Node", lambda : term),
		UBInt32("ID"),
		UBInt8("Creation"),
		nested = False),
		encoder = lambda obj,ctx: (obj.node, obj.id, obj.creation),
		decoder = lambda obj,ctx: Port(*obj))
pid = ExprAdapter(Sequence("pid",
		LazyBound("Node", lambda : term),
		UBInt32("ID"),
		UBInt32("Serial"),
		UBInt8("Creation"),
		nested = False),
		encoder = lambda obj,ctx: (obj.node, obj.id, obj.serial, obj.creation),
		decoder = lambda obj,ctx: Pid(*obj))
small_tuple = TupleAdapter(PrefixedArray(LazyBound("small_tuple",lambda : term), length_field = UBInt8("arity")))
large_tuple = TupleAdapter(PrefixedArray(LazyBound("large_tuple",lambda : term), length_field = UBInt32("arity")))
nil = ExprAdapter(Sequence("nil"),
		encoder = lambda obj,ctx: (),
		decoder = lambda obj,ctx: [])
string = ExprAdapter(PascalString("string", length_field = UBInt16("length")),
		encoder = lambda obj,ctx: obj.value,
		decoder = lambda obj,ctx: etString(obj))
list_ = PrefixedArray(LazyBound("list",lambda : term), length_field = UBInt32("arity"))

def BigInteger(subconname, length_field = UBInt8("length")):
	def decode_big(obj,ctx):
		ret = sum([d << i*8 for (d,i) in zip(obj.value,range(0,len(obj.value)))])
		if obj.isNegative:
			return -ret
		return ret

	def encode_big(obj,ctx):
		isNegative = 0
		if obj < 0:
			isNegative = 1
			obj = -obj
		value = []
		while obj > 0:
			value.append(obj & 0xFF)
			obj = obj >> 8
		value.reverse()
		return Container(isNegative=isNegative, value=value, length=len(value))

	return ExprAdapter(Struct(subconname,
		length_field,
		UBInt8("isNegative"),
		Array(lambda ctx: ctx.length, UBInt8("value")),
		nested = False),
		encoder = encode_big,
		decoder = decode_big
	)

new_reference = Struct("new_reference",
		UBInt16("Len"),
		LazyBound("Node", lambda : term),
		UBInt8("Creation"),
		Array(lambda ctx: ctx.len, UBInt32("ID"))
	)

fun = Struct("fun",
		UBInt32("NumFree"),
		LazyBound("Pid", lambda : term),
		LazyBound("Module", lambda : term),
		LazyBound("Index", lambda : term),
		LazyBound("Uniq", lambda : term),
		Array(lambda ctx: ctx.len, LazyBound("FreeVars", lambda : term)),
	)


new_fun = Struct("new_fun",
		UBInt32("Size"),
		UBInt8("Arity"),
		String("Uniq",16),
		UBInt32("Index"),
		UBInt32("NumFree"),
		LazyBound("Pid", lambda : term),
		LazyBound("Module", lambda : term),
		LazyBound("Index", lambda : term),
		LazyBound("Uniq", lambda : term),
		Array(lambda ctx: ctx.len, LazyBound("FreeVars", lambda : term)),
	)


export = Struct("export",
		LazyBound("Module", lambda : term),
		LazyBound("Function", lambda : term),
		LazyBound("Arity", lambda : term),
	)

bit_binary = Struct("bit_binary",
		UBInt32("Len"),
		UBInt8("Bits"),
		String("Data", lambda ctx: ctx.len)
	)

term = ExprAdapter(Struct("term",
	UBInt8("tag"),
	Switch("payload", lambda ctx: ctx.tag,
                {
			82: UBInt8("atom_cache_ref"),
			97: UBInt8("small_integer"),
			98: UBInt32("integer"),
			99: ExprAdapter(String("float",31),
				lambda obj, ctx: "%.20e" % obj,
				lambda obj, ctx: float(obj)),
			100: PascalString("atom", length_field = UBInt16("length")),
			101: reference,
			102: port,
			103: pid,
			104: TupleAdapter(PrefixedArray(LazyBound("small_tuple",lambda : term), length_field = UBInt8("arity"))),
			105: TupleAdapter(PrefixedArray(LazyBound("large_tuple",lambda : term), length_field = UBInt32("arity"))),
#			106: nil,
			107: PascalString("string", length_field = UBInt16("length")),
			108: PrefixedArray(LazyBound("list",lambda : term), length_field = UBInt32("arity")),
			109: PascalString("binary", length_field = UBInt32("length")),
			110: BigInteger("small_big", length_field = UBInt8("length")),
			111: BigInteger("large_big", length_field = UBInt32("length")),
			114: new_reference,
			115: PascalString("small_atom"),
			117: fun,
			112: new_fun,
			113: export,
			77: bit_binary,
			70: BFloat64("new_float"),
			118: PascalString("atom_utf8", length_field = UBInt16("length")),
			119: PascalString("small_atom_utf8"),
                },
        ),
	), 
# FIXME: If we want to encode erlang data, we MUST put the tag code instead of zero here
		lambda obj, ctx: (0, obj),
		lambda obj, ctx: obj.payload
	)

__all__ = ["term"]


