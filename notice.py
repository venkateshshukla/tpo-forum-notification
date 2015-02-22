#!/usr/bin/env python
# Interface to access json files representing the notices of TPO Notice Board

import os
import json
import logging

from error import TpoJsonError

gendir = os.path.abspath(os.path.dirname(__file__)) + "/gen/json/"

def exists(filename):
	''' Return if the file exists in the gen/json folder'''
	logging.debug("called : exists")
	logging.debug("argument filename : %s", filename)

	return os.path.exists(gendir + filename)

def touch(filename):
	''' Simulate the touch event of linux. Without time stuff'''
	logging.debug("called : touch")
	logging.debug("argument filename : %s", filename)

	pathname = gendir + filename
	if os.path.exists(pathname):
		os.utime(pathname, None)
	else:
		open(pathname, 'a').close()

def remove(filename):
	''' Remove the file sent by filename.'''
	logging.debug("called : remove")
	logging.debug("argument filename : %s", filename)
	os.remove(gendir + filename)

class Notice(object):
	''' Class for all interaction with JSON file in notices. '''
	def __init__(self, name):
		logging.debug("created object : Notice")
		logging.debug("argument name : %s", name)
		if name is None:
			logging.error("No json filename provided")
			raise TpoJsonError("No json filename provided.")
		name = name.split('/')[-1]
		name = name.strip('\.json')
		self.name = name
		self.filename = name + '.json'
		self.lockname = name + '.lock'

	@property
	def name(self):
		return self._name
	@name.setter
	def name(self, n):
		logging.debug("setting _name : %s", n)
		self._name = n
	@name.deleter
	def name(self):
		del self._name

	@property
	def filename(self):
		return self._filename
	@filename.setter
	def filename(self, fn):
		logging.debug("setting _filename : %s", fn)
		self._filename = fn
	@filename.deleter
	def filename(self):
		del self._filename

	@property
	def lockname(self):
		return self._lockname
	@lockname.setter
	def lockname(self, ln):
		logging.debug("setting _lockname : %s", ln)
		self._lockname = ln
	@lockname.deleter
	def lockname(self):
		del self._lockname

	def set_lock(self):
		logging.debug("called : set_lock")
		if exists(self.lockname):
			logging.error("Lock already present for file : %s",
					self.name)
			raise TpoJsonError("Lock already present for file {}.".format(self.name))
		touch(self.lockname)

	def del_lock(self):
		logging.debug("called : del_lock")
		if not exists(self.lockname):
			logging.error("No lock present for file : %s".
					self.name)
			raise TpoJsonError("No lock present for file {}.".format(self.name))
		remove(self.lockname)

	def is_locked(self):
		logging.debug("called : is_locked")
		return exists(self.lockname)

	def get_json(self):
		''' Get the data contained in a JSON file.'''
		logging.debug("called : get_json")

		if not exists(self.filename):
			logging.error("Queried JSON file does not exist.")
			raise TpoJsonError("Queried JSON file does not exist.")

		# Wait as the file is already in use
		logging.debug("Waiting for lock to be removed.")
		while self.is_locked():
			pass
		logging.debug("Lock removed.")

		# Extract the data by opening the file
		logging.debug("Locking and opening file")
		self.set_lock()
		f = open(gendir + self.filename, 'r')
		txt = f.read()
		logging.debug("Closing file and removing lock")
		f.close()
		data = json.loads(txt)
		self.del_lock()
		return data

	def save_json(self, data):
		''' Save the json file in gen folder.'''
		logging.debug("called : save_json")
		logging.debug("argument data : %s", str(data))

		# Sanity check
		if data is None:
			logging.error("Recieved empty data")
			return None

		# Wait as the file is already in use
		logging.debug("Waiting for lock to be removed.")
		while self.is_locked():
			pass
		logging.debug("Lock removed")

		# Set lock and dump the json
		logging.debug("Locking and opening file.")
		self.set_lock()
		f = open(gendir + self.filename, 'w')
		json.dump(data, f)
		logging.debug("Closing file and removing lock")
		f.close()
		self.del_lock();

