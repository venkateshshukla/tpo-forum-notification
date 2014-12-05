#!/usr/bin/env python
# Interface to access json files representing the notices of TPO Notice Board

import os
import json
from error import TpoJsonError

gendir = os.path.abspath(os.path.dirname(__file__)) + "/gen/json/"

def exists(filename):
	''' Return if the file exists in the gen/json folder'''
	return os.path.exists(gendir + filename)

def touch(filename):
	''' Simulate the touch event of linux. Without time stuff'''
	if os.path.exists(gendir + filename):
		os.utime(filename, None)
	else:
		open(filename, 'a').close()

def remove(filename):
	''' Remove the file sent by filename.'''
	os.remove(gendir + filename)

class Notice:
	''' Class for all interaction with JSON file in notices. '''
	def __init__(self, name):
		if name is None:
			raise TpoJsonError("No json filename provided.")
		self.name = name

	def set_lock(self, name=None):
		if name is None:
			name = self.name
		lockname = name + '.lock'
		if exists(lockname)
			raise TpoJsonError("Lock already present for file {}.".format(name))
		touch(lockname)

	def del_lock(self, name=None):
		if name is None:
			name = self.name
		lockname = name + '.lock'
		if not exists(lockname):
			raise TpoJsonError("No lock present for file {}.".format(name))
		remove(lockname)

	def is_locked(self, name=None):
		if name is None:
			name = self.name
		lockname += '.lock'
		if exists(lockname):
			return True
		else:
			return False

	def get_json(self, name=None):
		if name is None:
			name = self.name

		# Sanity check
		if name is None:
			raise TpoJsonError("Null filename.")

		if not os.path.exists(gendir + name):
			raise TpoJsonError("Queried JSON file does not exist.")

		# Wait as the file is already in use
		while is_locked(name):
			pass

		# Extract the data by opening the file
		set_lock(name)
		f = open(gendir + name)
		txt = f.read()
		f.close()
		data = json.loads(txt)
		del_lock(name)
		return data

	def set_json(self, name=None, data):

		# Sanity check
		if data is None:
			return
		if name is None:
			return

		touch(name)

		# Wait as the file is already in use
		while is_locked(name):
			pass

		# Set lock and dump the json
		set_lock(name)
		f = open(gendir + name, 'w')
		json.dump(data, f)
		f.close()
		del_lock(name);

