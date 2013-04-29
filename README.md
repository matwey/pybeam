pybeam
======

Python module to parse Erlang BEAM files.

This is not ready yet, so pull-requests are welcome.

Quick start:
```python
import pybeam
p=pybeam.BeamFile("/usr/lib64/erlang/lib/appmon-2.1.14.1/ebin/appmon.beam")
print p.imports
print p.exports
print p.atoms
```
