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

from pybeam import beam_construct
from construct import *
import unittest

class BEAMConstructTest(unittest.TestCase):
	def setUp(self):
		pass
	def test_beam(self):
		c = beam_construct.beam
		self.assertEqual(c.parse(b'FOR1\x00\x00\x00\x00BEAM'), Container(for1=b"FOR1", beam=b"BEAM", chunk=[], size=0))
	def test_chunk_atom(self):
		c = beam_construct.chunk_atom
		self.assertEqual(c.parse(b'\x00\x00\x00\x00'), [])
		self.assertEqual(c.parse(b'\x00\x00\x00\x01\x08burtovoy'),[u"burtovoy"])
		self.assertEqual(c.parse(b'\x00\x00\x00\x02\x08burtovoy\x08yegorsaf'), [u"burtovoy",u"yegorsaf"])
		self.assertEqual(c.parse(c.build([])), [])
		self.assertEqual(c.parse(c.build([u"burtovoy"])), [u"burtovoy"])
		self.assertEqual(c.parse(c.build([u"burtovoy",u"yegorsaf"])), [u"burtovoy",u"yegorsaf"])
		self.assertRaises(StreamError, c.parse, b'\x00\x00\xff\x00')
	def test_chunk_atu8(self):
		c = beam_construct.chunk_atu8
		self.assertEqual(c.parse(b'\x00\x00\x00\x00'), [])
		self.assertEqual(c.parse(b'\x00\x00\x00\x01\x08burtovoy'),[u"burtovoy"])
		self.assertEqual(c.parse(b'\x00\x00\x00\x01\x10\xd0\x91\xd1\x83\xd1\x80\xd1\x82\xd0\xbe\xd0\xb2\xd0\xbe\xd0\xb9'),[u"\u0411\u0443\u0440\u0442\u043e\u0432\u043e\u0439"])
	def test_chunk_attr(self):
		c = beam_construct.chunk_attr
		self.assertEqual(c.parse(b'\x83\x64\x00\x08burtovoy'), u"burtovoy")
		self.assertEqual(c.parse(c.build(u"burtovoy")), u"burtovoy")
		self.assertEqual(c.parse(b'\x83\x6a'), [])
	def test_chunk_cinf(self):
		c = beam_construct.chunk_cinf
		self.assertEqual(c.parse(b'\x83\x64\x00\x08burtovoy'), u"burtovoy")
		self.assertEqual(c.parse(c.build(u"burtovoy")), u"burtovoy")
		self.assertEqual(c.parse(b'\x83\x6a'), [])
	def test_chunk_litt(self):
		c = beam_construct.chunk
		littc = b'x\x9cc```d```j\xce\x02\x00\x01\x87\x00\xf1'
		litt = b'LitT\x00\x00\x00\x16\x00\x00\x00\x0a' + littc + b'\x00\x00'
		self.assertEqual(c.parse(litt).payload.data.entry[0].term, [])

