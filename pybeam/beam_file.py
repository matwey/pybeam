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

from pybeam.schema import beam

class BeamFile(object):
	def __init__(self, f):
		if not hasattr(f, 'read'):
			f = open(f, "rb")
		self._chunks = beam.parse(f.read())

	def selectChunkByName(self, name):
		return self._chunks.get(name)

	@property
	def atoms(self):
		atom = self.selectChunkByName(b"AtU8")
		atom = atom if atom is not None else self.selectChunkByName(b"Atom")
		return atom

	@property
	def attributes(self):
		attr = self.selectChunkByName(b"Attr")
		# convert from proplist to dict
		return dict(attr) if attr is not None else None

	@property
	def code(self):
		code = self.selectChunkByName(b"Code")
		return (code.set, code.opcode_max, code.labels, code.functions, code.code)

	@property
	def compileinfo(self):
		cinf = self.selectChunkByName(b"CInf")
		return dict(cinf) if cinf is not None else None

	@property
	def exports(self):
		expt = self.selectChunkByName(b"ExpT")
		atoms = self.atoms
		return [(atoms[e.function-1], e.arity, e.label) for e in expt.entry] if expt is not None else None

	@property
	def literals(self):
		litt = self.selectChunkByName(b"LitT")
		return litt.entry if litt is not None else None

	@property
	def imports(self):
		impt = self.selectChunkByName(b"ImpT")
		atoms = self.atoms
		return [(atoms[e.module-1], atoms[e.function-1], e.arity) for e in impt.entry] if impt is not None else None

	@property
	def modulename(self):
		return self.atoms[0]
