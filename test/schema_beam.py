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

from pybeam.schema import beam
from pybeam.schema.beam.chunks import Atom, AtU8, Attr, CInf, chunk
from construct import Container, StreamError
from construct.core import TerminatedError
import unittest

class BEAMConstructTest(unittest.TestCase):
	def setUp(self):
		pass
	def test_beam1(self):
		c = beam
		self.assertEqual(c.parse(b'FOR1\x00\x00\x00\x04BEAM'), [])
	def test_beam2(self):
		c = beam
		raw = b'FOR1\x00\x00\x02TBEAMAtU8\x00\x00\x002\x00\x00\x00\x07\x01m\x04fact\x06erlang\x01-\x01*\x0bmodule_info\x0fget_module_info\x00\x00Code\x00\x00\x00w\x00\x00\x00\x10\x00\x00\x00\x00\x00\x00\x00\x99\x00\x00\x00\x08\x00\x00\x00\x03\x01\x10\x99\x10\x02\x12"\x10\x01 \'5\x01\x03\x0e\x10\x10\x99\x10}\x05\x10\x00\x03\x11\x13@\x03\x04@\x13\x03\x99\x10\x04\x10%\x99\x10}\x05\x10\x10\x04\x03\x03\x12\x10\x13\x010+\x15\x03\x01@\x11\x03\x13\x01@\x99\x00\x02\x12b\x00\x01P@\x12\x03\x99\x00N\x10 \x01`\x99\x00\x02\x12b\x10\x01p@\x03\x13@\x12\x03\x99\x00N 0\x03\x00StrT\x00\x00\x00\x00ImpT\x00\x00\x004\x00\x00\x00\x04\x00\x00\x00\x03\x00\x00\x00\x04\x00\x00\x00\x02\x00\x00\x00\x03\x00\x00\x00\x05\x00\x00\x00\x02\x00\x00\x00\x03\x00\x00\x00\x07\x00\x00\x00\x01\x00\x00\x00\x03\x00\x00\x00\x07\x00\x00\x00\x02ExpT\x00\x00\x00(\x00\x00\x00\x03\x00\x00\x00\x06\x00\x00\x00\x01\x00\x00\x00\x07\x00\x00\x00\x06\x00\x00\x00\x00\x00\x00\x00\x05\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x02LocT\x00\x00\x00\x04\x00\x00\x00\x00Attr\x00\x00\x00(\x83l\x00\x00\x00\x01h\x02d\x00\x03vsnl\x00\x00\x00\x01n\x10\x007\xfc\x18\xc42\x03\xc0\xfa\xe0\x91w.a\xb8\xebqjjCInf\x00\x00\x00l\x83l\x00\x00\x00\x03h\x02d\x00\x07optionsl\x00\x00\x00\x01d\x00\rno_debug_infojh\x02d\x00\x07versionk\x00\x057.1.5h\x02d\x00\x06sourcek\x00!/home/matwey/rpmbuild/BUILD/m.erljDbgi\x00\x00\x00F\x83h\x03d\x00\rdebug_info_v1d\x00\x11erl_abstract_codeh\x02d\x00\x04nonel\x00\x00\x00\x01d\x00\rno_debug_infoj\x00\x00Line\x00\x00\x00\x15\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\x00\x00\x00\x01\x00\x00\x00\x00A\x00\x00\x00'
		parsed = c.parse(raw)
		self.assertEqual(len(raw), 604)
		self.assertEqual(len(parsed), 10)
	def test_beam3(self):
		c = beam
		self.assertRaises(TerminatedError, lambda: c.parse(b'FOR1\x00\x00\x00\x0cBEAMAtU8\x00\x00\x002'))
	def test_chunk_atom(self):
		c = Atom
		self.assertEqual(c.parse(b'\x00\x00\x00\x00'), [])
		self.assertEqual(c.parse(b'\x00\x00\x00\x01\x08burtovoy'),[u"burtovoy"])
		self.assertEqual(c.parse(b'\x00\x00\x00\x02\x08burtovoy\x08yegorsaf'), [u"burtovoy",u"yegorsaf"])
		self.assertEqual(c.parse(c.build([])), [])
		self.assertEqual(c.parse(c.build([u"burtovoy"])), [u"burtovoy"])
		self.assertEqual(c.parse(c.build([u"burtovoy",u"yegorsaf"])), [u"burtovoy",u"yegorsaf"])
		self.assertRaises(StreamError, c.parse, b'\x00\x00\xff\x00')
	def test_chunk_atu8(self):
		c = AtU8
		self.assertEqual(c.parse(b'\x00\x00\x00\x00'), [])
		self.assertEqual(c.parse(b'\x00\x00\x00\x01\x08burtovoy'),[u"burtovoy"])
		self.assertEqual(c.parse(b'\x00\x00\x00\x01\x10\xd0\x91\xd1\x83\xd1\x80\xd1\x82\xd0\xbe\xd0\xb2\xd0\xbe\xd0\xb9'),[u"\u0411\u0443\u0440\u0442\u043e\u0432\u043e\u0439"])
	def test_chunk_attr(self):
		c = Attr
		self.assertEqual(c.parse(b'\x83\x64\x00\x08burtovoy'), u"burtovoy")
		self.assertEqual(c.parse(c.build(u"burtovoy")), u"burtovoy")
		self.assertEqual(c.parse(b'\x83\x6a'), [])
	def test_chunk_cinf(self):
		c = CInf
		self.assertEqual(c.parse(b'\x83\x64\x00\x08burtovoy'), u"burtovoy")
		self.assertEqual(c.parse(c.build(u"burtovoy")), u"burtovoy")
		self.assertEqual(c.parse(b'\x83\x6a'), [])
	def test_chunk_litt(self):
		c = chunk
		littc = b'x\x9cc```d```j\xce\x02\x00\x01\x87\x00\xf1'
		litt = b'LitT\x00\x00\x00\x16\x00\x00\x00\x0a' + littc + b'\x00\x00'
		self.assertEqual(c.parse(litt).payload.data.entry[0].term, [])

