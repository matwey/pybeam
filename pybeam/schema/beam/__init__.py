from construct import this
from construct import (
	Const,
	FixedSized,
	GreedyRange,
	Int32ub,
	Struct,)

from pybeam.schema.beam.chunks import chunk

beam = Struct(
	"for1" / Const(b'FOR1'),
	"size" / Int32ub,
	"beam" / Const(b'BEAM'),
	"chunks" / FixedSized(this.size, GreedyRange(chunk)))

__all__ = ["beam"]
