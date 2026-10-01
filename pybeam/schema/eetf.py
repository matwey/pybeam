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

import functools

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
	ImproperList,
	MFA,
	Pid,
	Port,
	Reference,
	String as etString,)

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
		return ImproperList(obj[1], obj[2])
	def _encode(self, obj, context, path):
		if isinstance(obj, ImproperList):
			return (len(obj.elements), obj.elements, obj.tail)
		return (len(obj), list(obj), [])

class MapAdapter(Adapter):
	def _decode(self, obj, context, path):
		return dict(obj)
	def _encode(self, obj, context, path):
		# Keys are written in term order, as term_to_binary/2 does with
		# the deterministic option and always does for small maps.
		return sorted(obj.items(), key=lambda kv: _term_key(kv[0]))

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
	# Choose the same encoding as term_to_binary(Term, [{minor_version, 2}])
	mapping = {
		AtomCacheReference : 82,
		float : 70,
		Reference : 114,
		Port : 102,
		Pid : 103,
		Binary : 109,
		bytes : 109,
		Fun : 112,
		MFA : 113,
		dict : 116,
		BitBinary : 77,
		ImproperList : 108,
	}
	cls = obj.__class__
	if cls in mapping:
		return mapping[cls]
	if isinstance(obj, int):
		if 0 <= obj <= 0xff:
			return 97
		if -0x80000000 <= obj <= 0x7fffffff:
			return 98
		return 110 if abs(obj).bit_length() <= 8 * 0xff else 111
	if isinstance(obj, str):
		return 119 if len(obj.encode("utf8")) <= 0xff else 118
	if isinstance(obj, etString):
		if len(obj) == 0:
			return 106
		return 107 if len(obj) <= 0xffff else 108
	if isinstance(obj, list):
		# Python lists stay lists on the way back, even if they hold bytes
		return 108 if obj else 106
	if isinstance(obj, tuple):
		return 104 if len(obj) <= 0xff else 105
	if isinstance(obj, dict):
		return 116
	raise TypeError("can't encode %r as an Erlang term" % (obj,))

# Erlang term order: number < atom < reference < fun < port < pid < tuple <
# map < nil < list < bitstring

def _term_rank(t):
	if isinstance(t, AtomCacheReference):
		return 1
	if isinstance(t, (int, float)):
		return 0
	if isinstance(t, str):
		return 1
	if isinstance(t, Reference):
		return 2
	if isinstance(t, (Fun, MFA)):
		return 3
	if isinstance(t, Port):
		return 4
	if isinstance(t, Pid):
		return 5
	if isinstance(t, dict):
		return 7
	if isinstance(t, (list, etString)) and len(t) == 0:
		return 8
	if isinstance(t, (list, etString, ImproperList)):
		return 9
	if isinstance(t, (Binary, bytes, BitBinary)):
		return 10
	if isinstance(t, tuple):
		return 6
	raise TypeError("can't compare %r as an Erlang term" % (t,))

def _cmp(a, b):
	return (a > b) - (a < b)

def _list_parts(t):
	if isinstance(t, ImproperList):
		return (list(t.elements), t.tail)
	return (list(t), [])

def _term_cmp(a, b):
	ra = _term_rank(a)
	rb = _term_rank(b)
	if ra != rb:
		return _cmp(ra, rb)
	if ra == 0:
		# In map key order integers come before floats of equal value
		return _cmp(a, b) or _cmp(isinstance(a, float), isinstance(b, float))
	if ra == 1:
		return _cmp(str(a), str(b))
	if ra == 6:
		return _cmp(len(a), len(b)) or _seq_cmp(a, b)
	if ra == 7:
		ka = sorted(a, key=_term_key)
		kb = sorted(b, key=_term_key)
		return (_cmp(len(a), len(b)) or _seq_cmp(ka, kb)
			or _seq_cmp([a[k] for k in ka], [b[k] for k in kb]))
	if ra == 9:
		(ea, ta) = _list_parts(a)
		(eb, tb) = _list_parts(b)
		for (x, y) in zip(ea, eb):
			c = _term_cmp(x, y)
			if c:
				return c
		n = min(len(ea), len(eb))
		# Once one list runs out, its tail is compared to the rest of the other
		rest_a = ImproperList(ea[n:], ta) if ea[n:] and ta != [] else (ea[n:] or ta)
		rest_b = ImproperList(eb[n:], tb) if eb[n:] and tb != [] else (eb[n:] or tb)
		if len(ea) == len(eb):
			return _term_cmp(ta, tb)
		return _term_cmp(rest_a, rest_b)
	if ra == 10:
		va = a.value if isinstance(a, BitBinary) else bytes(a)
		vb = b.value if isinstance(b, BitBinary) else bytes(b)
		return _cmp(va, vb)
	if ra == 8:
		return 0
	return _cmp(repr(a), repr(b))

def _seq_cmp(a, b):
	for (x, y) in zip(a, b):
		c = _term_cmp(x, y)
		if c:
			return c
	return _cmp(len(a), len(b))

_term_key = functools.cmp_to_key(_term_cmp)

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
		encoder=lambda obj, ctx: bytes(obj),
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
