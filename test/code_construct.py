#
# Copyright (c) 2013 Fredrik Ahlberg <fredrik@z80.se>
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

from pybeam.code_construct import beam_operand, beam_instruction
from pybeam.opcodes import *
from construct import *
import unittest

class CodeConstructTest(unittest.TestCase):
    def test_operand_integer(self):
        self.assertEqual(beam_operand.parse('\x11'), (TAG_INTEGER, 1))
        self.assertEqual(beam_operand.parse('\xa9\x39'), (TAG_INTEGER, 1337))
        self.assertEqual(beam_operand.parse('\x19\xfe\xc6'), (TAG_INTEGER, -314))
        self.assertEqual(beam_operand.parse('\x59\x00\xff\xff\xff'), (TAG_INTEGER, 16777215))
        self.assertEqual(beam_operand.parse('\x99\x00\xe8\xd4\xa5\x10\x00'), (TAG_INTEGER, 1e12))
        self.assertEqual(beam_operand.parse('\x99\xff\x17\x2b\x5a\xf0\x00'), (TAG_INTEGER, -1e12))
        self.assertEqual(beam_operand.parse('\x0d\xb0'), (TAG_LABEL, 176))
        self.assertEqual(beam_operand.parse('\xf9\x00\x00\xff\xff\xff\xff\xff\xff\xff\xff'), (TAG_INTEGER, 0xffffffffffffffff))
        self.assertEqual(beam_operand.parse('\xf9\x00\xff\x00\x00\x00\x00\x00\x00\x00\x01'), (TAG_INTEGER, -0xffffffffffffffff))

    def test_instruction(self):
        # op = 0x28 = IS_GE
        #  1 = 0x0d, 0xb0 = L176
        #  2 = 0xf9, 0x00, 0x00, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff = Int 0xffffffffffffffff
        #  3 = 0x63 = X(6)
        self.assertEqual(beam_instruction.parse('\x28\x0d\xb0\xf9\x00\x00\xff\xff\xff\xff\xff\xff\xff\xff\x63'),
                (IS_GE, [(TAG_LABEL, 176), (TAG_INTEGER, 0xffffffffffffffff), (TAG_XREG, 6)]))

        # op = 0x10 = TEST_HEAP
        #  1 = 0x37 (ALLOC_LIST)
        #      0x20 -> length = 2
        #       0x00 0x00 -> words: 0
        #       0x10 0x10 -> floats: 1
        #  2 = 0x10 -> 1
        self.assertEqual(beam_instruction.parse('\x10\x37\x20\x00\x00\x10\x10\x10'),
                (TEST_HEAP, [(TAGX_ALLOCLIST, [(0, 0), (1, 1)]), (TAG_LITERAL, 1)]))

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(CodeConstructTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
