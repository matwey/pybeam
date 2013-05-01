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

class AtomCacheReference:
	def __init__(self, index):
		self.index = index
	def __eq__(self,other):
		return self.index == other.index

class Reference:
	def __init__(self, node, id, creation):
		self.node = node
		self.id = id
		self.creation = creation
	def __eq__(self,other):
		return self.node == other.node and self.id == other.id and self.creation == other.creation

class Port:
	def __init__(self, node, id, creation):
		self.node = node
		self.id = id
		self.creation = creation
	def __eq__(self,other):
		return self.node == other.node and self.id == other.id and self.creation == other.creation

class Pid:
	def __init__(self, node, id, serial, creation):
		self.node = node
		self.id = id
		self.serial = serial
		self.creation = creation
	def __eq__(self,other):
		return self.node == other.node and self.id == other.id and self.creation == other.creation and self.serial == other.serial

class String:
	def __init__(self, value):
		self.value = value

class Binary:
	def __init__(self, value):
		self.value = value

class Fun:
	def __init__(self, arity, uniq, index, module, oldindex, olduniq, pid, free):
		self.arity = arity
		self.uniq = uniq
		self.index = index
		self.module = module
		self.oldindex = oldindex
		self.olduniq = uniq
		self.pid = pid
		self.free = free

class MFA:
	def __init__(self, module, function, arity):
		self.module = module
		self.function = function
		self.arity = arity

class BitBinary:
	def __init__(self, value, bits):
		self.value = value
		self.bits = bits

