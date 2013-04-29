from beam_construct import beam

class BeamFile(object):
	def __init__(self, filename):
		self._tree = beam.parse(file(filename,"r").read())

	
