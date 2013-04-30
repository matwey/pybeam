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

from construct import *

atom_cache_ref = Struct("atom_cache_ref",
		UBInt8("AtomCacheReferenceIndex")
	)

small_integer_ext = Struct("small_integer_ext",
		UBInt8("Int")
	)

integer_ext = Struct("integer_ext",
		UBInt32("Int")
	)

float_ext = Struct("float_ext",
		String("Float",31)
	)

reference_ext = Struct("reference_ext",
		LazyBound("Node", lambda : term),
		UBInt32("ID"),
		UBInt8("Creation"),
	)

port_ext = Struct("port_ext",
		LazyBound("Node", lambda : term),
		UBInt32("ID"),
		UBInt8("Creation"),
	)

pid_ext = Struct("pid_ext",
		LazyBound("Node", lambda : term),
		UBInt32("ID"),
		UBInt32("Serial"),
		UBInt8("Creation"),
	)

small_tuple_ext = Struct("small_tuple_ext",
		UBInt8("Arity"),
		Array(lambda ctx: ctx.Arity, LazyBound("Elements",lambda : term))
	)

large_tuple_ext = Struct("large_tuple_ext",
		UBInt32("Arity"),
		Array(lambda ctx: ctx.Arity, LazyBound("Elements",lambda : term))
	)

list_ext = Struct("list_ext",
		UBInt32("Length"),
		Array(lambda ctx: ctx.Length-1, LazyBound("Elements",lambda : term)),
		LazyBound("Tail", lambda : term)
	)

small_big_ext = Struct("small_integer_ext",
		UBInt8("len"),
		UBInt8("isNegative"),
		String("data", lambda ctx: ctx.len)
	)

large_big_ext = Struct("large_integer_ext",
		UBInt32("len"),
		UBInt8("isNegative"),
		String("Data", lambda ctx: ctx.len)
	)

new_reference_ext = Struct("new_reference_ext",
		UBInt16("Len"),
		LazyBound("Node", lambda : term),
		UBInt8("Creation"),
		Array(lambda ctx: ctx.len, UBInt32("ID"))
	)

fun_ext = Struct("fun_ext",
		UBInt32("NumFree"),
		LazyBound("Pid", lambda : term),
		LazyBound("Module", lambda : term),
		LazyBound("Index", lambda : term),
		LazyBound("Uniq", lambda : term),
		Array(lambda ctx: ctx.len, LazyBound("FreeVars", lambda : term)),
	)


new_fun_ext = Struct("new_fun_ext",
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


export_ext = Struct("export_ext",
		LazyBound("Module", lambda : term),
		LazyBound("Function", lambda : term),
		LazyBound("Arity", lambda : term),
	)

bit_binary_ext = Struct("bit_binary_ext",
		UBInt32("Len"),
		UBInt8("Bits"),
		String("Data", lambda ctx: ctx.len)
	)

new_float_ext = Struct("new_float_ext",
		BFloat64("float")
	)

term = Struct("term",
	UBInt8("tag"),
	Switch("payload", lambda ctx: ctx.tag,
                {
			82: atom_cache_ref,
			97: small_integer_ext,
			98: integer_ext,
			99: float_ext,
			100: PascalString("atom_ext", length_field = UBInt16("length")),
			101: reference_ext,
			102: port_ext,
			103: pid_ext,
			104: small_tuple_ext,
			105: large_tuple_ext,
#			106: nil_ext,
			107: PascalString("string_ext", length_field = UBInt16("length")),
			108: list_ext,
			109: PascalString("binary_ext", length_field = UBInt32("length")),
			110: small_big_ext,
			111: large_big_ext,
			114: new_reference_ext,
			115: PascalString("small_atom_ext"),
			117: fun_ext,
			112: new_fun_ext,
			113: export_ext,
			77: bit_binary_ext,
			70: new_float_ext,
			118: PascalString("atom_utf8_ext", length_field = UBInt16("length")),
			119: PascalString("atom_utf8_ext"),
                },
        ),
	)

__all__ = ["term"]


