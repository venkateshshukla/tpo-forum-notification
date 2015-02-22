# User defined errors for this application

import logging
from time import strftime

class TpoError(Exception):
	''' Base class for exception in TPO module'''
	pass

class TpoJsonError(TpoError):
	''' Error while JSON transaction'''
	def __init__(self, msg):
		logging.error("TpoJsonError : %s", msg)
		self.msg = "{} : {}\n".format(strftime("%Y-%m-%d %H:%M:%S"), msg)

	def __str__(self):
		return repr(self.msg)

