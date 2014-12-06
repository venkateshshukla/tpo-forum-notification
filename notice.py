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
	pathname = gendir + filename
	if os.path.exists(pathname):
		os.utime(pathname, None)
	else:
		open(pathname, 'a').close()

def remove(filename):
	''' Remove the file sent by filename.'''
	os.remove(gendir + filename)

class Notice:
	''' Class for all interaction with JSON file in notices. '''
	def __init__(self, name):
		if name is None:
			raise TpoJsonError("No json filename provided.")
		name = name.split('/')[-1]
		name = name.strip('\.json')
		self.name = name
		self.filename = name + '.json'
		self.lockname = name + '.lock'

	def set_lock(self):
		if exists(self.lockname):
			raise TpoJsonError("Lock already present for file {}.".format(self.name))
		touch(self.lockname)

	def del_lock(self):
		if not exists(self.lockname):
			raise TpoJsonError("No lock present for file {}.".format(self.name))
		remove(self.lockname)

	def is_locked(self):
		return exists(self.lockname)

	def get_json(self):
		''' Get the data contained in a JSON file.'''
		if not exists(self.filename):
			raise TpoJsonError("Queried JSON file does not exist.")

		# Wait as the file is already in use
		while self.is_locked():
			pass

		# Extract the data by opening the file
		self.set_lock()
		f = open(gendir + self.filename, 'r')
		txt = f.read()
		f.close()
		data = json.loads(txt)
		self.del_lock()
		return data

	def save_json(self, data):
		''' Save the json file in gen folder.'''
		# Sanity check
		if data is None:
			return None

		# Wait as the file is already in use
		while self.is_locked():
			pass

		# Set lock and dump the json
		self.set_lock()
		f = open(gendir + self.filename, 'w')
		json.dump(data, f)
		f.close()
		self.del_lock();

