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
		self.assertEqual(c.parse(b'\x00\x00\x00\x01\x08burtovoy'),["burtovoy"])
		self.assertEqual(c.parse(b'\x00\x00\x00\x02\x08burtovoy\x08yegorsaf'), ["burtovoy","yegorsaf"])
		self.assertEqual(c.parse(c.build([])), [])
		self.assertEqual(c.parse(c.build(["burtovoy"])), ["burtovoy"])
		self.assertEqual(c.parse(c.build(["burtovoy","yegorsaf"])), ["burtovoy","yegorsaf"])
		self.assertRaises(RangeError, c.parse, b'\x00\x00\xff\x00')
	def test_chunk_attr(self):
		c = beam_construct.chunk_attr
		self.assertEqual(c.parse(b'\x83\x64\x00\x08burtovoy'), "burtovoy")
		self.assertEqual(c.parse(c.build("burtovoy")), "burtovoy")
		self.assertEqual(c.parse(b'\x83\x6a'), [])
	def test_chunk_strt(self):
		c = beam_construct.chunk_strt
		self.assertEqual(c.parse(b'\x00\x00\x00\x00'), Container(string=''))
		self.assertEqual(c.parse(b'\x00\x00\x00\x08burtovoy'), Container(string='burtovoy'))
		self.assertEqual(c.parse(c.build(Container(string=''))), Container(string=''))
		self.assertEqual(c.parse(c.build(Container(string='burtovoy'))), Container(string='burtovoy'))
	def test_chunk_cinf(self):
		c = beam_construct.chunk_cinf
		self.assertEqual(c.parse(b'\x83\x64\x00\x08burtovoy'), "burtovoy")
		self.assertEqual(c.parse(c.build("burtovoy")), "burtovoy")
		self.assertEqual(c.parse(b'\x83\x6a'), [])
	def test_chunk_litt(self):
		c = beam_construct.chunk
		littc = b'x\x9cc```d```j\xce\x02\x00\x01\x87\x00\xf1'
		litt = b'LitT\x00\x00\x00\x16\x00\x00\x00\x0a' + littc + b'\x00\x00'
		self.assertEqual(c.parse(litt).payload.data.entry[0].term, [])

