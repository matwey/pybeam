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

from pybeam.beam_construct import beam

class BeamFile(object):
	def __init__(self, f):
		if not hasattr(f, 'read'):
			f = open(f, "rb")
		self._tree = beam.parse(f.read())

	def selectChunkByName(self, name):
		for c in self._tree.chunk:
			if c.chunk_name == name:
				return c
		raise KeyError(name)

	@property
	def atoms(self):
		try:
			return self.selectChunkByName(b"AtU8").payload
		except KeyError:
			pass
		return self.selectChunkByName(b"Atom").payload

	@property
	def attributes(self):
		attr = self.selectChunkByName(b"Attr")
		# convert from proplist to dict
		return dict(attr.payload)

	@property
	def code(self):
		code = self.selectChunkByName(b"Code").payload
		return (code.set, code.opcode_max, code.labels, code.functions, code.code)

	@property
	def compileinfo(self):
		cinf = self.selectChunkByName(b"CInf")
		return dict(cinf.payload)

	@property
	def exports(self):
		expt = self.selectChunkByName(b"ExpT")
		atoms = self.atoms
		return [(atoms[e.function-1], e.arity, e.label) for e in expt.payload.entry]

	@property
	def literals(self):
		return [e.term for e in self.selectChunkByName(b"LitT").payload.data.entry]

	@property
	def imports(self):
		impt = self.selectChunkByName(b"ImpT")
		atoms = self.atoms
		return [(atoms[e.module-1], atoms[e.function-1], e.arity) for e in impt.payload.entry]

	@property
	def modulename(self):
		return self.atoms[0]
