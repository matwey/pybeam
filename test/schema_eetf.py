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

import pybeam.schema.eetf as eetf
from pybeam import erlang_types
from six import int2byte
import unittest

class EETFConstructTest(unittest.TestCase):
	def setUp(self):
		pass
	def test_atom_cache_ref(self):
		c = eetf.atom_cache_ref
		self.assertEqual(c.parse(b'\x23'), erlang_types.AtomCacheReference(0x23))
		self.assertEqual(c.parse(c.build(erlang_types.AtomCacheReference(0x23))),erlang_types.AtomCacheReference(0x23))
	def test_small_integer(self):
		c = eetf.small_integer
		self.assertEqual(c.parse(b'\x23'), 0x23)
		self.assertEqual(c.parse(c.build(123)),123)
	def test_integer(self):
		c = eetf.integer
		self.assertEqual(c.parse(b'\00\xff\00\x11'), 0xff0011)
		self.assertEqual(c.parse(b'\xff\xff\xff\xff'), -1)
		self.assertEqual(c.parse(c.build(0xff0011)),0xff0011)
	def test_float(self):
		c = eetf.float_
		self.assertEqual(c.parse(b'     1.12344300000000002910e+04'), 11234.43)
		self.assertEqual(c.parse(b'1.00000000000000000000e+00\00\00\00\00\00'), 1.0)
		self.assertEqual(c.parse(c.build(-3.1415926)),-3.1415926)
	def test_new_float(self):
		c = eetf.new_float
		self.assertEqual(c.parse(b'\x40\x00\x00\x00\x00\x00\x00\x00'), 2.0 )
		self.assertEqual(c.parse(b'\xc0\x00\x00\x00\x00\x00\x00\x00'), -2.0 )
		self.assertEqual(c.parse(c.build(-3.1415926)),-3.1415926)
	def test_atom_utf8(self):
		c = eetf.atom_utf8
		self.assertEqual(c.parse(b'\x00\x08\xd0\xb0\xd1\x82\xd0\xbe\xd0\xbc'), u"\u0430\u0442\u043e\u043c")
		self.assertEqual(c.parse(c.build(u"\u0430\u0442\u043e\u043c")),u"\u0430\u0442\u043e\u043c")
	def test_small_atom_utf8(self):
		c = eetf.small_atom_utf8
		self.assertEqual(c.parse(b'\x08\xd0\xb0\xd1\x82\xd0\xbe\xd0\xbc'), u"\u0430\u0442\u043e\u043c")
		self.assertEqual(c.parse(c.build(u"\u0430\u0442\u043e\u043c")),u"\u0430\u0442\u043e\u043c")
	def test_atom1(self):
		c = eetf.atom
		self.assertEqual(c.parse(b'\x00\x06myatom'), u"myatom")
		self.assertEqual(c.parse(c.build(u"robots")),u"robots")
	def test_atom2(self):
		raw = b'\x00\x06r\xf2b\xf3ts'
		c = eetf.atom
		self.assertEqual(c.parse(raw), u"r\u00f2b\u00f3ts")
	def test_small_atom1(self):
		c = eetf.small_atom
		self.assertEqual(c.parse(b'\x06myatom'), u"myatom")
		self.assertEqual(c.parse(c.build(u"robots")),u"robots")
	def test_small_atom2(self):
		raw = b'\x06r\xf2b\xf3ts'
		c = eetf.small_atom
		self.assertEqual(c.parse(raw), u"r\u00f2b\u00f3ts")
	def test_reference(self):
		c = eetf.reference
		r = erlang_types.Reference(u"myatom",0x12,0x48)
		self.assertEqual(c.parse(b'\x64\x00\x06myatom\x00\x00\x00\x12\x48'), r)
		self.assertEqual(c.parse(c.build(r)),r)
		self.assertEqual(c.build(r),b'\x76\x00\x06myatom\x00\x00\x00\x12\x48')
	def test_new_reference(self):
		c = eetf.new_reference
		r = erlang_types.Reference(u"myatom",[0x12,0x13],0x48)
		self.assertEqual(c.parse(b'\x00\x02\x76\x00\x06myatom\x48\x00\x00\x00\x12\x00\x00\x00\x13'), r)
		self.assertEqual(c.parse(c.build(r)),r)
	def test_port(self):
		c = eetf.port
		self.assertEqual(c.parse(b'\x64\x00\x06myatom\x00\x00\x00\x12\x48'), erlang_types.Port("myatom",0x12,0x48))
	def test_pid(self):
		c = eetf.pid
		self.assertEqual(c.parse(b'\x64\x00\x06myatom\x00\x00\x00\x12\x00\x00\x00\x32\x48'), erlang_types.Pid("myatom",0x12,0x32,0x48))
	def test_small_tuple(self):
		c = eetf.small_tuple
		self.assertEqual(c.parse(b"\x02\x64\x00\x06myatom\x64\x00\x06robert"), ("myatom","robert"))
		self.assertEqual(c.parse(c.build((1,2,u"myatom"))),(1,2,u"myatom"))
	def test_large_tuple(self):
		c = eetf.large_tuple
		self.assertEqual(c.parse(b"\x00\x00\x00\x02\x64\x00\x06myatom\x64\x00\x06robert"), ("myatom","robert"))
		self.assertEqual(c.parse(c.build((1,2,u"myatom"))),(1,2,u"myatom"))
	def test_list(self):
		c = eetf.list_
		self.assertEqual(c.parse(b'\x00\x00\x00\x02\x64\x00\x08YegorSaf\x64\x00\x0aRoBurToVoY\x6a'), ["YegorSaf","RoBurToVoY"])
		self.assertEqual(c.parse(c.build([1,2,3,u"OO"])),[1,2,3,u"OO"])
		self.assertEqual(c.parse(c.build([u"Nu",u"poskoku"])),[u"Nu",u"poskoku"])
		attrs0 = b'\x00\x00\x00\x02h\x02d\x00\x03vsnl\x00\x00\x00\x01n\x10\x00\xb3\xf2\xab&|\xd3\xdeHL\xa0\x0fV\xdf\xc1\x05\x96jh\x02d\x00\tbehaviourl\x00\x00\x00\x01d\x00\ngen_serverjj'
		self.assertEqual(c.parse(attrs0), [("vsn", [199414093051598402244823387542347575987]), ("behaviour", ["gen_server"])])
		t1 = b'\x00\x00\x00\x01d\x00\x05alignm\x00\x00\x00\x02\x01\x00'
		self.assertEqual(c.parse(t1), ["align", erlang_types.Binary(b'\x01\x00')])
	def test_nil(self):
		c = eetf.nil
		self.assertEqual(c.parse(b'\x6a'), [])
		self.assertEqual(c.parse(c.build([])),[])
	def test_bitbinary(self):
		c = eetf.bit_binary
		self.assertEqual(c.parse(b'\00\00\00\x0a\x03RoBurToVoY'), erlang_types.BitBinary(b'RoBurToVoY',3))
		s = erlang_types.BitBinary(b'RoBurToVoY',1)
		self.assertEqual(c.parse(c.build(s)),s)
	def test_string(self):
		c = eetf.string
		self.assertEqual(c.parse(b'\x00\x0aRoBurToVoY'), erlang_types.String(b'RoBurToVoY'))
		s = erlang_types.String(b'RoBurToVoY')
		self.assertEqual(c.parse(c.build(s)),s)
		n = b"\x01\x00" + b"".join(map(int2byte, range(0,256)))
		self.assertListEqual(list(c.parse(n)), list(range(0,256)))
		self.assertEqual(c.build(erlang_types.String(b"".join(map(int2byte, range(0,256))))), n)
	def test_binary(self):
		c = eetf.binary
		self.assertEqual(c.parse(b'\x00\x00\x00\x0aRoBurToVoY'), erlang_types.Binary(b'RoBurToVoY'))
		s = erlang_types.Binary(b'RoBurToVoY')
		self.assertEqual(c.parse(c.build(s)),s)
	def test_small_big(self):
		c = eetf.small_big
		self.assertEqual(c.parse(b'\x02\x00\x02\x01'), 258)
		self.assertEqual(c.parse(b'\x02\x01\x02\x01'), -258)
		self.assertEqual(c.parse(c.build(123456789123456789)),123456789123456789)
	def test_large_big(self):
		c = eetf.large_big
		self.assertEqual(c.parse(b'\x00\x00\x00\x02\x00\x02\x01'), 258)
		self.assertEqual(c.parse(c.build(123456789123456789)),123456789123456789)
	def test_fun(self):
		c = eetf.fun
		self.assertEqual(c.parse(b'\00\00\00\x02\x64\x00\x06myatom\x64\x00\x06myatom\x61\x13\x64\x00\x06myatom\x64\x00\x06myatom\x64\x00\x06myatom'), erlang_types.Fun(None,None,None,"myatom",0x13,"myatom","myatom",["myatom","myatom"]))
	def test_export(self):
		c = eetf.export
		mfa = erlang_types.MFA(u"myatom",u"myat0m",0x13)
		self.assertEqual(c.parse(b'\x64\x00\x06myatom\x64\x00\x06myat0m\x61\x13'),mfa)
		self.assertEqual(c.parse(c.build(mfa)),mfa)
	def test_term(self):
		c = eetf.term
		self.assertEqual(c.parse(b'\x6f\x00\x00\x00\x02\x00\x02\x01'), 258)
		self.assertEqual(c.parse(c.build(258)), 258)
		self.assertEqual(c.parse(c.build([3,2,1])), [3,2,1])
		self.assertEqual(c.build(u"BurToVoY"), b'\x76\x00\x08BurToVoY')
	def test_external(self):
		c = eetf.external_term
		self.assertEqual(c.parse(b'\x83\x6f\x00\x00\x00\x02\x00\x02\x01'), 258)
		self.assertEqual(c.parse(c.build(258)), 258)
		self.assertEqual(c.parse(c.build([3,2,1])), [3,2,1])
		self.assertEqual(c.build(u"BurToVoY"), b'\x83\x76\x00\x08BurToVoY')
	def test_key_value(self):
		c = eetf.key_value
		self.assertEqual(c.parse(b'a\x01a\x02'), (1,2))
		self.assertEqual(c.parse(c.build((1,2))), (1,2))
	def test_map(self):
		c = eetf.map_
		self.assertEqual(c.parse(b'\x00\x00\x00\x02a\x01a\x02a\x03a\x04'), {1:2,3:4})
		self.assertEqual(c.parse(c.build({1:2,3:4})), {1:2,3:4})
