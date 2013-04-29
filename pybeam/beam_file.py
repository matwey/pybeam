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

