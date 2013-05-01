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
	def test_new_float(self):
		c = eetf_construct.new_float
		self.assertEqual(c.parse('\x40\x00\x00\x00\x00\x00\x00\x00'), 2.0 )
		self.assertEqual(c.parse('\xc0\x00\x00\x00\x00\x00\x00\x00'), -2.0 )
		self.assertEqual(c.parse(c.build(-3.1415926)),-3.1415926)
	def test_atom_utf8(self):
		c = eetf_construct.atom_utf8
		self.assertEqual(c.parse('\x00\x06myatom'), 'myatom')
                self.assertEqual(c.parse(c.build('robots')),'robots')
	def test_small_atom_utf8(self):
		c = eetf_construct.small_atom_utf8
		self.assertEqual(c.parse('\x06myatom'), 'myatom')
                self.assertEqual(c.parse(c.build('robots')),'robots')
	def test_atom(self):
		c = eetf_construct.atom
		self.assertEqual(c.parse('\x00\x06myatom'), 'myatom')
                self.assertEqual(c.parse(c.build('robots')),'robots')
	def test_small_atom(self):
		c = eetf_construct.small_atom
		self.assertEqual(c.parse('\x06myatom'), 'myatom')
                self.assertEqual(c.parse(c.build('robots')),'robots')
	def test_reference(self):
		c = eetf_construct.reference
		r = erlang_types.Reference("myatom",0x12,0x48)
		self.assertEqual(c.parse('\x64\x00\x06myatom\x00\x00\x00\x12\x48'), r)
		self.assertEqual(c.parse(c.build(r)),r)
		self.assertEqual(c.build(r),'\x64\x00\x06myatom\x00\x00\x00\x12\x48')
	def test_new_reference(self):
		c = eetf_construct.new_reference
		r = erlang_types.Reference("myatom",[0x12,0x13],0x48)
		self.assertEqual(c.parse('\x00\x02\x64\x00\x06myatom\x48\x00\x00\x00\x12\x00\x00\x00\x13'), r)
		self.assertEqual(c.parse(c.build(r)),r)
	def test_port(self):
		c = eetf_construct.port
		self.assertEqual(c.parse('\x64\x00\x06myatom\x00\x00\x00\x12\x48'), erlang_types.Port("myatom",0x12,0x48))
	def test_pid(self):
		c = eetf_construct.pid
		self.assertEqual(c.parse('\x64\x00\x06myatom\x00\x00\x00\x12\x00\x00\x00\x32\x48'), erlang_types.Pid("myatom",0x12,0x32,0x48))
	def test_small_typle(self):
		c = eetf_construct.small_tuple
		self.assertEqual(c.parse("\x02\x64\x00\x06myatom\x64\x00\x06robert"), ('myatom','robert'))
		self.assertEqual(c.parse(c.build((1,2,'myatom'))),(1,2,'myatom'))
	def test_large_typle(self):
		c = eetf_construct.large_tuple
		self.assertEqual(c.parse("\x00\x00\x00\x02\x64\x00\x06myatom\x64\x00\x06robert"), ('myatom','robert'))
		self.assertEqual(c.parse(c.build((1,2,'myatom'))),(1,2,'myatom'))
	def test_list(self):
		c = eetf_construct.list_
		self.assertEqual(c.parse('\x00\x00\x00\x02\x64\x00\x08YegorSaf\x64\x00\x0aRoBurToVoY'), ['YegorSaf','RoBurToVoY'])
		self.assertEqual(c.parse(c.build([1,2,3,'OO'])),[1,2,3,'OO'])
		self.assertEqual(c.parse(c.build(['Nu','poskoku'])),['Nu','poskoku'])
	def test_nil(self):
		c = eetf_construct.nil
		self.assertEqual(c.parse('\x6a'), [])
		self.assertEqual(c.parse(c.build([])),[])
	def test_bitbinary(self):
		c = eetf_construct.bit_binary
		self.assertEqual(c.parse('\00\00\00\x0a\x03RoBurToVoY'), erlang_types.BitBinary('RoBurToVoY',3))
		s = erlang_types.BitBinary('RoBurToVoY',1)
                self.assertEqual(c.parse(c.build(s)),s)
	def test_string(self):
		c = eetf_construct.string
		self.assertEqual(c.parse('\x00\x0aRoBurToVoY'), erlang_types.String('RoBurToVoY'))
		s = erlang_types.String('RoBurToVoY')
                self.assertEqual(c.parse(c.build(s)),s)
	def test_binary(self):
		c = eetf_construct.binary
		self.assertEqual(c.parse('\x00\x00\x00\x0aRoBurToVoY'), erlang_types.Binary('RoBurToVoY'))
		s = erlang_types.Binary('RoBurToVoY')
                self.assertEqual(c.parse(c.build(s)),s)
	def test_small_big(self):
		c = eetf_construct.small_big
		self.assertEqual(c.parse('\x02\x00\x02\x01'), 258)
		self.assertEqual(c.parse('\x02\x01\x02\x01'), -258)
		self.assertEqual(c.parse(c.build(123456789123456789L)),123456789123456789L)
	def test_large_big(self):
		c = eetf_construct.large_big
		self.assertEqual(c.parse('\x00\x00\x00\x02\x00\x02\x01'), 258)
		self.assertEqual(c.parse(c.build(123456789123456789L)),123456789123456789L)
	def test_fun(self):
		c = eetf_construct.fun
		self.assertEqual(c.parse('\00\00\00\x02\x64\x00\x06myatom\x64\x00\x06myatom\x61\x13\x64\x00\x06myatom\x64\x00\x06myatom\x64\x00\x06myatom'), erlang_types.Fun(None,None,None,'myatom',0x13,'myatom','myatom',['myatom','myatom']))
	def test_export(self):
		c = eetf_construct.export
		mfa = erlang_types.MFA('myatom','myat0m',0x13)
		self.assertEqual(c.parse('\x64\x00\x06myatom\x64\x00\x06myat0m\x61\x13'),mfa)
		self.assertEqual(c.parse(c.build(mfa)),mfa)

if __name__ == '__main__':
	suite = unittest.TestLoader().loadTestsFromTestCase(EETFConstructTest)
	unittest.TextTestRunner(verbosity=2).run(suite)

