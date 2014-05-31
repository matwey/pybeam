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

from pybeam.erlang_types import AtomCacheReference, Reference, Port, Pid, String as etString, Binary, Fun, MFA, BitBinary
from construct import *
import sys

if sys.version > '3':
	long = int

class TupleAdapter(Adapter):
	def _decode(self, obj, ctx):
# we got a list from construct and want to see a tuple
		return tuple(obj)
	def _encode(self, obj, ctv):
		return list(obj)

class ListAdapter(Adapter):
	def _decode(self, obj, ctx):
		if type(obj[2]) == type(list()) and obj[2] == []:
			return obj[1]
		obj[1].append(obj[2])
		return obj[1]
	def _encode(self, obj, ctx):
		return (len(obj), obj, [])

class MapAdapter(Adapter):
	def _decode(self, obj, ctx):
		return dict(obj)
	def _encode(self, obj, ctx):
		return list(obj.items())

def BigInteger(subconname, length_field = UBInt8("length")):
	def decode_big(obj,ctx):
		(length, isNegative, value) = obj
		ret = sum([d << i*8 for (d,i) in zip(value,range(0,len(value)))])
		if isNegative:
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
		return (len(value), isNegative, value)

	return ExprAdapter(Sequence(subconname,
		length_field,
		UBInt8("isNegative"),
		Array(lambda ctx: ctx.length, UBInt8("value")),
		nested = False),
		encoder = encode_big,
		decoder = decode_big)

def tag(obj,ctx):
	mapping = {
		AtomCacheReference : 82,
		int : 98,
		float : 70,
		str : 100,
		Reference : 114,
		Port : 102,
		Pid : 103,
		tuple : 105,
		etString : 107,
		list : 108,
		Binary : 109,
		long : 111,
		Fun : 112,
		MFA : 113,
		map : 116,
		BitBinary : 77,	
	}
	if obj == []:
		return 106
	else: 
		return mapping[obj.__class__]

atom_cache_ref = ExprAdapter(UBInt8("atom_cache_ref"),
		encoder = lambda obj,ctx: obj.index,
		decoder = lambda obj,ctx: AtomCacheReference(obj))
small_integer = UBInt8("small_integer")
integer = SBInt32("integer")
float_ = ExprAdapter(String("float",31,padchar='\00',encoding="latin1"),
		encoder = lambda obj,ctx: "%.20e    " % obj,
		decoder = lambda obj,ctx: float(obj.strip()))
atom = PascalString("atom", length_field = UBInt16("length"), encoding="latin1")
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
string = ExprAdapter(PascalString("string", length_field = UBInt16("length"), encoding=None),
		encoder = lambda obj,ctx: obj.value,
		decoder = lambda obj,ctx: etString(obj))
list_ = ListAdapter(Sequence("list",
		UBInt32("length"),
		Array(lambda ctx: ctx.length, LazyBound("elements", lambda : term)),
		LazyBound("tail", lambda : term),
		nested = False,
		))
binary = ExprAdapter(PascalString("binary", length_field = UBInt32("length")),
		encoder = lambda obj,ctx: obj.value,
		decoder = lambda obj,ctx: Binary(obj))
small_big = BigInteger("small_big", length_field = UBInt8("length"))
large_big = BigInteger("large_big", length_field = UBInt32("length"))
new_reference = ExprAdapter(Sequence("new_reference",
		UBInt16("Len"),
		LazyBound("Node", lambda : term),
		UBInt8("Creation"),
		Array(lambda ctx: ctx.Len, UBInt32("ID")),
		nested = False),
		encoder = lambda obj,ctx: (len(obj.id), obj.node, obj.creation, obj.id),
		decoder = lambda obj,ctx: Reference(obj[1], obj[3], obj[2]))
small_atom = PascalString("small_atom", encoding="latin1")
fun = ExprAdapter(Sequence("fun",
		UBInt32("NumFree"),
		LazyBound("Pid", lambda : term),
		LazyBound("Module", lambda : term),
		LazyBound("Index", lambda : term),
		LazyBound("Uniq", lambda : term),
		Array(lambda ctx: ctx.NumFree, LazyBound("FreeVars", lambda : term)),
		nested = False),
                encoder = lambda obj,ctx: (len(obj.free), obj.pid, obj.module, obj.oldindex, olj.olduniq, obj.free) ,
                decoder = lambda obj,ctx: Fun(None, None, None, obj[2], obj[3], obj[4], obj[1], obj[5]))
# new fun to be implemented later
new_fun = fun
export = ExprAdapter(Sequence("export",
		LazyBound("Module", lambda : term),
		LazyBound("Function", lambda : term),
		LazyBound("Arity", lambda : term),
		nested = False),
		encoder = lambda obj,ctx: (obj.module, obj.function, obj.arity),
		decoder = lambda obj,ctx: MFA(*obj))
bit_binary = ExprAdapter(Sequence("bit_binary",
		UBInt32("Len"),
		UBInt8("Bits"),
		String("Data", lambda ctx: ctx.Len),
		nested = False),
		encoder = lambda obj,ctx: (len(obj.value), obj.bits, obj.value),
		decoder = lambda obj,ctx: BitBinary(obj[2],obj[1]))
new_float = BFloat64("new_float")
atom_utf8 = PascalString("atom_utf8", length_field = UBInt16("length"), encoding="utf8")
small_atom_utf8 = PascalString("small_atom_utf8", encoding="utf8")
key_value = ExprAdapter(Sequence("key_value",
	LazyBound("key", lambda : term),
	LazyBound("value", lambda : term)),
		encoder = lambda obj,ctx: obj,
		decoder = lambda obj,ctx: tuple(obj)
	)
map = MapAdapter(PrefixedArray(key_value, length_field = UBInt32("arity")))

term = ExprAdapter(Sequence("term",
	UBInt8("tag"),
	Switch("payload", lambda ctx: ctx.tag,
                {
			82: atom_cache_ref,
			97: small_integer,
			98: integer,
			99: float_,
			100: atom,
			101: reference,
			102: port,
			103: pid,
			104: small_tuple,
			105: large_tuple,
			106: nil,
			107: string,
			108: list_,
			109: binary,
			110: small_big,
			111: large_big,
			114: new_reference,
			115: small_atom,
			116: map,
			117: fun,
			112: new_fun,
			113: export,
			77: bit_binary,
			70: new_float,
			118: atom_utf8,
			119: small_atom_utf8,
                },),
	nested = False),
		lambda obj, ctx: (tag(obj, ctx), obj),
		lambda obj, ctx: obj[1]
	)

erl_version_magic = Magic(b'\x83')

external_term = SeqOfOne("external_term",erl_version_magic,term)

__all__ = ["term", "external_term"]


