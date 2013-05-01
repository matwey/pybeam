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

from pybeam import eetf_construct
from pybeam import erlang_types
import unittest

class EETFConstructTest(unittest.TestCase):
	def setUp(self):
		pass
	def test_atom_cache_ref(self):
		c = eetf_construct.atom_cache_ref
		self.assertEqual(c.parse('\x23'), erlang_types.AtomCacheReference(0x23))
		self.assertEqual(c.parse(c.build(erlang_types.AtomCacheReference(0x23))),erlang_types.AtomCacheReference(0x23))
	def test_small_integer(self):
		c = eetf_construct.small_integer
		self.assertEqual(c.parse('\x23'), 0x23)
		self.assertEqual(c.parse(c.build(123)),123)
	def test_integer(self):
		c = eetf_construct.integer
		self.assertEqual(c.parse('\00\xff\00\x11'), 0xff0011)
		self.assertEqual(c.parse('\xff\xff\xff\xff'), -1)
		self.assertEqual(c.parse(c.build(0xff0011)),0xff0011)
	def test_float(self):
		c = eetf_construct.float_
		self.assertEqual(c.parse('     1.12344300000000002910e+04'), 11234.43)
		self.assertEqual(c.parse(c.build(-3.1415926)),-3.1415926)

if __name__ == '__main__':
	suite = unittest.TestLoader().loadTestsFromTestCase(EETFConstructTest)
	unittest.TextTestRunner(verbosity=2).run(suite)

