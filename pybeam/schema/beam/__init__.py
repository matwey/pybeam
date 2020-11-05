#
# Copyright (c) 2013-2018 Matwey V. Kornilov <matwey.kornilov@gmail.com>
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

from construct import Adapter, Const, FocusedSeq, GreedyRange, Int32ub, Prefixed, Terminated

from pybeam.schema.beam.chunks import chunk


class DictAdapter(Adapter):
	def _decode(self, obj, context, path):
		return dict(obj)

	def _encode(self, obj, context, path):
		return obj.items()

beam = FocusedSeq("chunks",
	Const(b'FOR1'),
	"chunks" / Prefixed(Int32ub, FocusedSeq("chunks",
		Const(b'BEAM'),
		"chunks" / DictAdapter(GreedyRange(chunk)),
		Terminated)))

__all__ = ["beam"]
