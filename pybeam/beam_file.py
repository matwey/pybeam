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
