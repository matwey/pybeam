#
# Copyright (c) 2016 Matwey V. Kornilov <matwey.kornilov@gmail.com>
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

from pybeam import beam_file
from pybeam.erlang_types import String
import unittest
import io

class BEAMFileTest(unittest.TestCase):
	def setUp(self):
		self.raw = b'FOR1\x00\x00\x02\xd4BEAMAtom\x00\x00\x00U\x00\x00\x00\x08\x08ssh_math\x04ipow\x06crypto\x07mod_pow\x10bytes_to_integer\x0bmodule_info\x06erlang\x0fget_module_info\x00\x00\x00Code\x00\x00\x00\\\x00\x00\x00\x10\x00\x00\x00\x00\x00\x00\x00\x99\x00\x00\x00\x07\x00\x00\x00\x03\x01\x10\x99\x10\x02\x12"0\x01 \'\x15\x01#(\x15\x13\x01\x0c\x000\x99 \x070\x00\x99 \x08\x10\x10\x00\x010\x99\x00\x02\x12b\x00\x01@@\x12\x03\x99\x00N\x10 \x01P\x99\x00\x02\x12b\x10\x01`@\x03\x13@\x12\x03\x99\x00N 0\x03StrT\x00\x00\x00\x00ImpT\x00\x00\x004\x00\x00\x00\x04\x00\x00\x00\x03\x00\x00\x00\x04\x00\x00\x00\x03\x00\x00\x00\x03\x00\x00\x00\x05\x00\x00\x00\x01\x00\x00\x00\x07\x00\x00\x00\x08\x00\x00\x00\x01\x00\x00\x00\x07\x00\x00\x00\x08\x00\x00\x00\x02ExpT\x00\x00\x00(\x00\x00\x00\x03\x00\x00\x00\x06\x00\x00\x00\x01\x00\x00\x00\x06\x00\x00\x00\x06\x00\x00\x00\x00\x00\x00\x00\x04\x00\x00\x00\x02\x00\x00\x00\x03\x00\x00\x00\x02Attr\x00\x00\x00(\x83l\x00\x00\x00\x01h\x02d\x00\x03vsnl\x00\x00\x00\x01n\x10\x00\x8f\xde\xf9V}\xf3wr\x8a\x93\xc1p\xedDK\x9ajjCInf\x00\x00\x01@\x83l\x00\x00\x00\x04h\x02d\x00\x07optionsl\x00\x00\x00\x04h\x02d\x00\x06outdirk\x00</home/abuild/rpmbuild/BUILD/otp_src_17.1/lib/ssh/src/../ebinh\x02d\x00\x01ik\x007/home/abuild/rpmbuild/BUILD/otp_src_17.1/lib/kernel/srcd\x00\x10warn_unused_varsd\x00\ndebug_infojh\x02d\x00\x07versionk\x00\x055.0.1h\x02d\x00\x04timeh\x06b\x00\x00\x07\xe0a\x02a\x0fa\x0ba\x08a\x12h\x02d\x00\x06sourcek\x00A/home/abuild/rpmbuild/BUILD/otp_src_17.1/lib/ssh/src/ssh_math.erljLitT\x00\x00\x00\x18\x00\x00\x00\x0ax\x9cc```d```j\xce\x02\x00\x01\x87\x00\xf1\x00\x00'
		self.io = io.BytesIO(self.raw)
		self.beam = beam_file.BeamFile(self.io)
	def test_attr(self):
		self.assertDictEqual({'vsn': [205091931631091061218511176690734587535]}, self.beam.attributes)
	def test_atoms(self):
		self.assertListEqual(['ssh_math','ipow','crypto','mod_pow','bytes_to_integer','module_info','erlang','get_module_info'], self.beam.atoms)
	def test_compileinfo(self):
		self.assertDictEqual({
			'source': String(b'/home/abuild/rpmbuild/BUILD/otp_src_17.1/lib/ssh/src/ssh_math.erl'),
			'time': (2016, 2, 15, 11, 8, 18),
			'version': String(b'5.0.1'),
			'options': [
				('outdir', String(b'/home/abuild/rpmbuild/BUILD/otp_src_17.1/lib/ssh/src/../ebin')),
				('i', String(b'/home/abuild/rpmbuild/BUILD/otp_src_17.1/lib/kernel/src')),
				'warn_unused_vars',
				'debug_info'
			]}, self.beam.compileinfo)
	def test_exports(self):
		self.assertListEqual([('module_info', 1, 6), ('module_info', 0, 4), ('ipow', 3, 2)], self.beam.exports)
	def test_imports(self):
		self.assertListEqual([('crypto', 'mod_pow', 3), ('crypto', 'bytes_to_integer', 1), ('erlang', 'get_module_info', 1), ('erlang', 'get_module_info', 2)], self.beam.imports)
	def test_modulename(self):
		self.assertEqual('ssh_math', self.beam.modulename)
	def test_literals(self):
		self.assertListEqual([[]], self.beam.literals)
