[![Python](https://github.com/matwey/pybeam/actions/workflows/python.yml/badge.svg)](https://github.com/matwey/pybeam/actions/workflows/python.yml)
[![PyPI version](https://badge.fury.io/py/pybeam.svg)](https://badge.fury.io/py/pybeam)
[![Documentation Status](https://readthedocs.org/projects/pybeam/badge/?version=latest)](http://pybeam.readthedocs.io/en/latest/?badge=latest)

pybeam
======
Python module to parse Erlang BEAM files.

Pull-requests are always welcome.

## Quick start:
```python
import pybeam
p = pybeam.BeamFile("/usr/lib64/erlang/lib/appmon-2.1.14.1/ebin/appmon.beam")
print(p.imports)
print(p.exports)
print(p.atoms)
```

## References
* [Erlang BEAM file format](http://www.erlang.se/~bjorn/beam_file_format.html)
* [Erlang external term format](http://erlang.org/doc/apps/erts/erl_ext_dist.html)
* [BEAM file format](http://synrc.com/publications/cat/Functional%20Languages/Erlang/BEAM.pdf)
* [BEAM Wisdoms](http://beam-wisdoms.clau.se/en/latest/)
