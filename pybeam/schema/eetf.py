#
# Copyright (c) 2013-2018 Matwey V. Kornilov <matwey.kornilov@gmail.com>
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

import sys
from six import text_type

from construct import this
from construct import (
	Adapter,
	Array,
	Bytes,
	Const,
	ExprAdapter,
	Float64b,
	GreedyBytes,
	Int16ub,
	Int32sb,
	Int32ub,
	Int8ub,
	LazyBound,
	PaddedString,
	PascalString,
	Prefixed,
	PrefixedArray,
	Sequence,
	Switch,
	)

from pybeam.erlang_types import (
	AtomCacheReference,
	Binary,
	BitBinary,
	Fun,
	MFA,
	Pid,
	Port,
	Reference,
	String as etString,)

if sys.version > '3':
	long = int

class TupleAdapter(Adapter):
	def _decode(self, obj, context, path):
		# we got a list from construct and want to see a tuple
		return tuple(obj)
	def _encode(self, obj, context, path):
		return list(obj)

class ListAdapter(Adapter):
	def _decode(self, obj, context, path):
		if isinstance(obj[2], list) and obj[2] == []:
			return obj[1]
		obj[1].append(obj[2])
		return obj[1]
	def _encode(self, obj, context, path):
		return (len(obj), obj, [])

class MapAdapter(Adapter):
	def _decode(self, obj, context, path):
		return dict(obj)
	def _encode(self, obj, context, path):
		return list(obj.items())

def BigInteger(length_field):
	def decode_big(obj, _ctx):
		(_length, isNegative, value) = obj
		ret = sum([d << i*8 for (d, i) in zip(value, range(0, len(value)))])
		if isNegative:
			return -ret
		return ret

	def encode_big(obj, _ctx):
		isNegative = 0
		if obj < 0:
			isNegative = 1
			obj = -obj
		value = []
		while obj > 0:
			value.append(obj & 0xFF)
			obj = obj >> 8
		return (len(value), isNegative, value)

	return ExprAdapter(Sequence("len" / length_field,
		"isNegative" / Int8ub,
		"value" / Array(lambda ctx: ctx.len, Int8ub)),
		encoder=encode_big,
		decoder=decode_big)

def tag(obj):
	mapping = {
		AtomCacheReference : 82,
		int : 98,
		float : 70,
		text_type : 118, # unicode in Python 2 and str in Python 3
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
	return mapping[obj.__class__]

# Recurrent term
term_ = LazyBound(lambda: term)

atom_cache_ref = ExprAdapter(Int8ub,
		encoder=lambda obj, ctx: obj,
		decoder=lambda obj, ctx: AtomCacheReference(obj))
small_integer = Int8ub
integer = Int32sb
float_ = ExprAdapter(PaddedString(31, encoding="ascii"),
		encoder=lambda obj, ctx: u"{:.20e}    ".format(obj),
		decoder=lambda obj, ctx: float(obj))
atom = PascalString(lengthfield=Int16ub, encoding="latin1")
reference = ExprAdapter(Sequence("node" / term_,
		"id" / Int32ub,
		"creation" / Int8ub),
		encoder=lambda obj, ctx: (obj.node, obj.id, obj.creation),
		decoder=lambda obj, ctx: Reference(*obj))
port = ExprAdapter(Sequence("node" / term_,
		"id" / Int32ub,
		"creation" / Int8ub),
		encoder=lambda obj, ctx: (obj.node, obj.id, obj.creation),
		decoder=lambda obj, ctx: Port(*obj))
pid = ExprAdapter(Sequence("node" / term_,
		"id" / Int32ub,
		"serial" / Int32ub,
		"creation" / Int8ub),
		encoder=lambda obj, ctx: (obj.node, obj.id, obj.serial, obj.creation),
		decoder=lambda obj, ctx: Pid(*obj))
small_tuple = TupleAdapter(PrefixedArray(Int8ub, term_))
large_tuple = TupleAdapter(PrefixedArray(Int32ub, term_))
nil = ExprAdapter(Sequence(),
		encoder=lambda obj, ctx: (),
		decoder=lambda obj, ctx: [])
string = ExprAdapter(Prefixed(Int16ub, GreedyBytes),
		encoder=lambda obj, ctx: obj,
		decoder=lambda obj, ctx: etString(obj))
list_ = ListAdapter(Sequence("len" / Int32ub,
		Array(this.len, term_),
		term_))
binary = ExprAdapter(Prefixed(Int32ub, GreedyBytes),
		encoder=lambda obj, ctx: obj,
		decoder=lambda obj, ctx: Binary(obj))
small_big = BigInteger(Int8ub)
large_big = BigInteger(Int32ub)
new_reference = ExprAdapter(Sequence("len" / Int16ub,
		"node" / term_,
		"creation" / Int8ub,
		"id" / Array(this.len, Int32ub)),
		encoder=lambda obj, ctx: (len(obj.id), obj.node, obj.creation, obj.id),
		decoder=lambda obj, ctx: Reference(obj[1], obj[3], obj[2]))
small_atom = PascalString(lengthfield=Int8ub, encoding="latin1")
fun = ExprAdapter(Sequence("num_free" / Int32ub,
		"pid" / term_,
		"module" / term_,
		"oldindex" / term_,
		"olduniq" / term_,
		"free" / Array(this.num_free, term_)),
		encoder=lambda obj, ctx: (len(obj.free), obj.pid, obj.module, obj.oldindex, obj.olduniq, obj.free),
		decoder=lambda obj, ctx: Fun(None, None, None, obj[2], obj[3], obj[4], obj[1], obj[5]))
# new fun to be implemented later
new_fun = fun
export = ExprAdapter(Sequence("module" / LazyBound(lambda: term),
		"function" / LazyBound(lambda: term),
		"arity" / LazyBound(lambda: term)),
		encoder=lambda obj, ctx: (obj.module, obj.function, obj.arity),
		decoder=lambda obj, ctx: MFA(*obj))
bit_binary = ExprAdapter(Sequence("len" / Int32ub,
		"bits" / Int8ub,
		"data" / Bytes(this.len)),
		encoder=lambda obj, ctx: (len(obj.value), obj.bits, obj.value),
		decoder=lambda obj, ctx: BitBinary(obj[2], obj[1]))
new_float = Float64b
atom_utf8 = PascalString(lengthfield=Int16ub, encoding="utf8")
small_atom_utf8 = PascalString(lengthfield=Int8ub, encoding="utf8")
key_value = ExprAdapter(Sequence(term_, term_),
		encoder=lambda obj, ctx: obj,
		decoder=lambda obj, ctx: tuple(obj))
map_ = MapAdapter(PrefixedArray(Int32ub, key_value))

term = ExprAdapter(Sequence("tag" / Int8ub,
	Switch(this.tag, {
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
		116: map_,
		117: fun,
		112: new_fun,
		113: export,
		77: bit_binary,
		70: new_float,
		118: atom_utf8,
		119: small_atom_utf8,
	})),
	encoder=lambda obj, ctx: (tag(obj), obj),
	decoder=lambda obj, ctx: obj[1],
	)

erl_version_magic = Const(b'\x83')

external_term = ExprAdapter(Sequence(erl_version_magic, term),
	encoder=lambda obj, ctx: (None, obj),
	decoder=lambda obj, ctx: obj[1])

__all__ = ["term", "external_term"]
