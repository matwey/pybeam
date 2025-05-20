#
# Copyright (c) 2013 Fredrik Ahlberg <fredrik@z80.se>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files = the "Software"), to deal
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

NOP					= 0x00
LABEL				= 0x01
FUNC_INFO			= 0x02
INT_CODE_END		= 0x03
CALL				= 0x04
CALL_LAST			= 0x05
CALL_ONLY			= 0x06
CALL_EXT			= 0x07
CALL_EXT_LAST		= 0x08
BIF0				= 0x09
BIF1				= 0x0a
BIF2				= 0x0b
ALLOCATE			= 0x0c
ALLOCATE_HEAP		= 0x0d
ALLOCATE_ZERO		= 0x0e
ALLOCATE_HEAP_ZERO	= 0x0f
TEST_HEAP			= 0x10
INIT				= 0x11
DEALLOCATE			= 0x12
K_RETURN			= 0x13
SEND				= 0x14
REMOVE_MESSAGE		= 0x15
TIMEOUT				= 0x16
LOOP_REC			= 0x17
LOOP_REC_END		= 0x18
WAIT				= 0x19
WAIT_TIMEOUT		= 0x1a
IS_LT				= 0x27
IS_GE				= 0x28
IS_EQ				= 0x29
IS_NE				= 0x2a
IS_EQ_EXACT			= 0x2b
IS_NE_EXACT			= 0x2c
IS_INTEGER			= 0x2d
IS_FLOAT			= 0x2e
IS_NUMBER			= 0x2f
IS_ATOM				= 0x30
IS_PID				= 0x31
IS_REFERENCE		= 0x32
IS_PORT				= 0x33
IS_NIL				= 0x34
IS_BINARY			= 0x35
IS_LIST				= 0x37
IS_NONEMPTY_LIST	= 0x38
IS_TUPLE			= 0x39
TEST_ARITY			= 0x3a
SELECT_VAL			= 0x3b
SELECT_TUPLE_ARITY	= 0x3c
JUMP				= 0x3d
K_CATCH				= 0x3e
CATCH_END			= 0x3f
MOVE				= 0x40
GET_LIST			= 0x41
GET_TUPLE_ELEMENT	= 0x42
SET_TUPLE_ELEMENT	= 0x43
PUT_STRING			= 0x44
PUT_LIST			= 0x45
PUT_TUPLE			= 0x46
PUT					= 0x47
BADMATCH			= 0x48
IF_END				= 0x49
CASE_END			= 0x4a
CALL_FUN			= 0x4b
IS_FUNCTION			= 0x4d
CALL_EXT_ONLY		= 0x4e
BS_PUT_INTEGER		= 0x59
BS_PUT_BINARY		= 0x5a
BS_PUT_FLOAT		= 0x5b
BS_PUT_STRING		= 0x5c
FCLEARERROR			= 0x5e
FCHECKERROR			= 0x5f
FMOVE				= 0x60
FCONV				= 0x61
FADD				= 0x62
FSUB				= 0x63
FMUL				= 0x64
FDIV				= 0x65
FNEGATE				= 0x66
MAKE_FUN2			= 0x67
K_TRY				= 0x68
TRY_END				= 0x69
TRY_CASE			= 0x6a
TRY_CASE_END		= 0x6b
RAISE				= 0x6c
BS_INIT2			= 0x6d
BS_BITS_TO_BYTES	= 0x6e
BS_ADD				= 0x6f
APPLY				= 0x70
APPLY_LAST			= 0x71
IS_BOOLEAN			= 0x72
IS_FUNCTION2		= 0x73
BS_START_MATCH2		= 0x74
BS_GET_INTEGER2		= 0x75
BS_GET_FLOAT2		= 0x76
BS_GET_BINARY2		= 0x77
BS_SKIP_BITS2		= 0x78
BS_TEST_TAIL2		= 0x79
BS_SAVE2			= 0x7a
BS_RESTORE2			= 0x7b
GC_BIF1				= 0x7c
GC_BIF2				= 0x7d
IS_BITSTR			= 0x81
BS_CONTEXT_TO_BINARY= 0x82
BS_TEST_UNIT		= 0x83
BS_MATCH_STRING		= 0x84
BS_INIT_WRITABLE	= 0x85
BS_APPEND			= 0x86
BS_PRIVATE_APPEND	= 0x87
TRIM				= 0x88
BS_INIT_BITS		= 0x89
BS_GET_UTF8			= 0x8a
BS_SKIP_UTF8		= 0x8b
BS_GET_UTF16		= 0x8c
BS_SKIP_UTF16		= 0x8d
BS_GET_UTF32		= 0x8e
BS_SKIP_UTF32		= 0x8f
BS_UTF8_SIZE		= 0x90
BS_PUT_UTF8			= 0x91
BS_UTF16_SIZE		= 0x92
BS_PUT_UTF16		= 0x93
BS_PUT_UTF32		= 0x94
ON_LOAD				= 0x95
RECV_MARK           = 0x96
RECV_SET            = 0x97
GC_BIF3             = 0x98
LINE                = 0x99

""" Opcode arity """
arity = (
		0,1,3,0,2,3,2,2,3,2,4,5,
		2,3,2,3,2,1,1,0,0,0,0,2,
		1,1,2,4,4,4,4,4,4,4,4,4,
		4,4,3,3,3,3,3,3,3,2,2,2,
		2,2,2,2,2,2,2,2,2,2,3,3,
		3,1,2,1,2,3,3,3,3,3,2,1,
		1,0,1,1,3,2,2,2,5,5,5,4,
		2,1,1,2,2,5,5,5,2,1,0,1,
		2,2,4,4,4,4,3,1,2,1,1,1,
		2,6,3,5,1,2,2,3,5,7,7,7,
		5,3,2,2,5,6,2,2,2,2,1,3,
		4,0,8,6,2,6,5,4,5,4,5,4,
		3,3,3,3,3,0,1,1,7,1)

""" Human readable opcode names """
opnames = (
		"nop",
		"label",
		"func_info",
		"int_code_end",
		"call",
		"call_last",
		"call_only",
		"call_ext",
		"call_ext_last",
		"bif0",
		"bif1",
		"bif2",
		"allocate",
		"allocate_heap",
		"allocate_zero",
		"allocate_heap_zero",
		"test_heap",
		"init",
		"deallocate",
		"return",
		"send",
		"remove_message",
		"timeout",
		"loop_rec",
		"loop_rec_end",
		"wait",
		"wait_timeout",
		"-m_plus",
		"-m_minus",
		"-m_times",
		"-m_div",
		"-int_div",
		"-int_rem",
		"-int_band",
		"-int_bor",
		"-int_bxor",
		"-int_bsl",
		"-int_bsr",
		"-int_bnot",
		"is_lt",
		"is_ge",
		"is_eq",
		"is_ne",
		"is_eq_exact",
		"is_ne_exact",
		"is_integer",
		"is_float",
		"is_number",
		"is_atom",
		"is_pid",
		"is_reference",
		"is_port",
		"is_nil",
		"is_binary",
		"-is_constant",
		"is_list",
		"is_nonempty_list",
		"is_tuple",
		"test_arity",
		"select_val",
		"select_tuple_arity",
		"jump",
		"catch",
		"catch_end",
		"move",
		"get_list",
		"get_tuple_element",
		"set_tuple_element",
		"-put_string",
		"put_list",
		"put_tuple",
		"put",
		"badmatch",
		"if_end",
		"case_end",
		"call_fun",
		"-make_fun",
		"is_function",
		"call_ext_only",
		"-bs_start_match",
		"-bs_get_integer",
		"-bs_get_float",
		"-bs_get_binary",
		"-bs_skip_bits",
		"-bs_test_tail",
		"-bs_save",
		"-bs_restore",
		"-bs_init",
		"-bs_final",
		"bs_put_integer",
		"bs_put_binary",
		"bs_put_float",
		"bs_put_string",
		"-bs_need_buf",
		"fclearerror",
		"fcheckerror",
		"fmove",
		"fconv",
		"fadd",
		"fsub",
		"fmul",
		"fdiv",
		"fnegate",
		"make_fun2",
		"try",
		"try_end",
		"try_case",
		"try_case_end",
		"raise",
		"bs_init2",
		"-bs_bits_to_bytes",
		"bs_add",
		"apply",
		"apply_last",
		"is_boolean",
		"is_function2",
		"bs_start_match2",
		"bs_get_integer2",
		"bs_get_float2",
		"bs_get_binary2",
		"bs_skip_bits2",
		"bs_test_tail2",
		"bs_save2",
		"bs_restore2",
		"gc_bif1",
		"gc_bif2",
		"-bs_final2",
		"-bs_bits_to_bytes2",
		"-put_literal",
		"is_bitstr",
		"bs_context_to_binary",
		"bs_test_unit",
		"bs_match_string",
		"bs_init_writable",
		"bs_append",
		"bs_private_append",
		"trim",
		"bs_init_bits",
		"bs_get_utf8",
		"bs_skip_utf8",
		"bs_get_utf16",
		"bs_skip_utf16",
		"bs_get_utf32",
		"bs_skip_utf32",
		"bs_utf8_size",
		"bs_put_utf8",
		"bs_utf16_size",
		"bs_put_utf16",
		"bs_put_utf32",
		"on_load",
		"recv_mark",
		"recv_set",
		"gc_bif3",
		"line")

# Operand types
TAG_LITERAL			= 0
TAG_INTEGER			= 1
TAG_ATOM			= 2
TAG_XREG			= 3
TAG_YREG			= 4
TAG_LABEL			= 5
TAG_CHARACTER		= 6
TAG_EXTENDED		= 7

# Extended operand types
TAGX_BASE			= 8
TAGX_FLOATLIT		= 8+0
TAGX_SELECTLIST		= 8+1
TAGX_FLOATREG		= 8+2
TAGX_ALLOCLIST		= 8+3
TAGX_LITERAL		= 8+4
