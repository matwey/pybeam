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

from collections import namedtuple
import warnings

class AtomCacheReference(int):
	@property
	def index(self):
		warnings.warn("x.index is deprecated; use x instead", DeprecationWarning)
		return self

Reference = namedtuple("Reference", ["node", "id", "creation"])

Port = namedtuple("Port", ["node", "id", "creation"])

class String:
	def __init__(self, value):
		self.value = value
	def __eq__(self, other):
		return self.value == other.value
	def __repr__(self):
		return "'%s'" % self.value

class Binary:
	def __init__(self, value):
		self._value = value
	def __eq__(self, other):
		return self._value == other.value
	def __repr__(self):
		return "<<"+','.join(map(lambda x: str(ord(x)), self.value))+">>"

	@property
	def value(self):
		warnings.warn("x.value is deprecated; use x instead", DeprecationWarning)
		return self._value

Fun = namedtuple("Fun", ["arity", "uniq", "index", "module", "oldindex", "olduniq", "pid", "free"])

MFA = namedtuple("MFA", ["module", "function", "arity"])

BitBinary = namedtuple("BitBinary", ["value", "bits"])
