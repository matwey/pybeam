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

from beam_construct import beam

class BeamFile(object):
	def __init__(self, filename):
		self._tree = beam.parse(file(filename,"r").read())

	def selectChunkByName(self, name):
		for c in self._tree.chunk:
			if c.chunk_name == name:
				return c
		raise KeyError(name)

	@property
	def atoms(self):
		return self.selectChunkByName("Atom").payload.atom

	@property
	def exports(self):
		expt = self.selectChunkByName("ExpT")
		atoms = self.atoms
		return [(atoms[e.function], e.arity, e.label) for e in expt.payload.entry]

	@property
	def imports(self):
		impt = self.selectChunkByName("ImpT")
		atoms = self.atoms
		return [(atoms[e.module], atoms[e.function], e.arity) for e in impt.payload.entry]

	@property
	def attributes(self):
		attr = self.selectChunkByName("Attr")
		return attr	
