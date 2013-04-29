from construct import *

def align4(n):
	return n + ((n+4) % 4)

chunk_atom = Struct("chunk_atom",
	UBInt32("len"),
	Array(lambda ctx: ctx.len, PascalString("atom"))
	)

chunk_expt = Struct("chunk_expt",
	UBInt32("len"),
	Array(lambda ctx: ctx.len, Struct("entry",
			UBInt32("function"),
			UBInt32("arity"),
			UBInt32("label"),
		)
	)
	)

chunk_impt = Struct("chunk_impt",
	UBInt32("len"),
	Array(lambda ctx: ctx.len, Struct("entry",
			UBInt32("module"),
			UBInt32("function"),
			UBInt32("arity"),
		)
	)
	)

chunk_loct = Struct("chunk_loct",
	UBInt32("len"),
	Array(lambda ctx: ctx.len, Struct("entry",
			UBInt32("function"),
			UBInt32("arity"),
			UBInt32("label"),
		)
	)
	)

chunk = Struct("chunk",
	String("chunk_name",4),
	UBInt32("size"),
	Switch("payload", lambda ctx: ctx.chunk_name,
		{
		"Atom" : chunk_atom,
		"ExpT" : chunk_expt,
		"ImpT" : chunk_impt,
#		"Code" : chunk_code,
#		"StrT" : chunk_strt,
#		"Attr" : chunk_attr,
#		"CInf" : chunk_cinf,
		"LocT" : chunk_loct,
#		"Trac" : chunk_trac,
		},
		default = String("skip", lambda ctx: align4(ctx.size))
	),
	)

beam = Struct("beam",
	OneOf(String('for1',4),['FOR1']),
	UBInt32("size"),
	OneOf(String('beam',4),['BEAM']),
	GreedyRange(chunk),
	)

__all__ = ["beam"]

