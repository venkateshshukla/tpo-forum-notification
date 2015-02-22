#!/usr/bin/env python
# Script to login to IIT BHU TPO Forum

import os
import requests

class TpoSession(object):
	"A session for interaction with the TPO Forum"

	login_failed_msg = "The board requires you to be registered and logged in to view this forum."
	login_success_msg = "You have been successfully logged in."

	def __init__(self):
		self.baseurl = "http://www.iitbhu.ac.in/tpo/forum"
		self.username = "student"
		self.password = "inspire"
		self.sid = None
		self.cookies = None

	@property
	def baseurl(self):
		return self._baseurl

	@baseurl.setter
	def baseurl(self, url):
		self._baseurl = url

	@baseurl.deleter
	def baseurl(self):
		del self._baseurl

	@property
	def username(self):
		return self._username

	@username.setter
	def username(self, name):
		self._username = name

	@username.deleter
	def username(self):
		del self._username

	@property
	def password(self):
		return self._password

	@password.setter
	def password(self, pwd):
		self._password = pwd

	@password.deleter
	def password(self):
		del self._password

	@property
	def sid(self):
		return self._sid

	@sid.setter
	def sid(self, x):
		self._sid = x

	@sid.deleter
	def sid(self):
		del self._sid

	@property
	def cookies(self):
		return self._cookies

	@cookies.setter
	def cookies(self, ck):
		self._cookies = ck

	@cookies.deleter
	def cookies(self):
		del self._cookies

	# Get session id for logging in the forum.
	def start_session(self):
		print "Starting a new session."
		url = self.baseurl + "/ucp.php"
		sid_key = 'iitbhu_phpbb3_sid'

		response = requests.get(url)

		if response.status_code != 200:
			print "Error : %d"%response.status_code
			print "Failed to start session. Check network connection."
			return False

		cookies = response.cookies
		sid = cookies[sid_key]

		print "New session started with session id : ", sid
		self.sid = sid
		self.cookies = cookies
		return True

	# Using the session id and the cookies, login to the forum using a POST request
	def forum_login(self):
		print "Trying to login to the forum"
		url = self.baseurl + "/ucp.php?mode=login"
		redirect = "/viewforum.php?f=163"
		login = "login"

		payload = {}
		payload["username"] = self.username
		payload["password"] = self.password
		payload["sid"] = self.sid
		payload["login"] = login

		response = requests.post(url, cookies=self.cookies, data=payload)

		if response.status_code != 200:
			print "Error connecting to the server"
			return False
		if self.login_success_msg in response.text:
			print self.login_success_msg
			self.cookies = response.cookies
			return True
		else:
			print "Error during login."
			return False

	# Using the session id and login cookies, get the forum page showing notices
	def get_forum_page(self):
		if self.sid == None or self.cookies == None:
			print "Start a new session first using method start_session()"
			return None
		payload = {}
		payload["sid"] = self.sid
		print "Retrieving the forum page."
		url = self.baseurl + "/viewforum.php?f=163"
		response = requests.get(url, cookies=self.cookies, data=payload)
		if response.status_code == 200:
			if self.login_failed_msg in response.content:
				print "Login first by running method forum_login()"
				return None
			print "Forum page retrieved."
			return response.content
		else:
			print "Error retrieving forum page."
			return None

	# Get the forum page showing the notice details
	def get_forum_notice(self, offset = None):
		if offset == None:
			print "Offset is empty. Include notice url"
			return None
		if self.sid == None or self.cookies == None:
			print "Start a new session first using method start_session()"
			return None
		payload = {}
		payload["sid"] = self.sid

		#print "Retrieving forum notice"
		url = self.baseurl + offset
		response = requests.get(url, cookies=self.cookies, data=payload)
		if response.status_code == 200:
			if self.login_failed_msg in response.content:
				print "Login first by running method forum_login()"
				return None
			#print "Forum notice retrieved."
			return response.content
		else:
			print "Error retrieving notice page."
			return None

	# Login and retrieve forum html
	def login(self):
		root = os.path.abspath(os.path.dirname(__file__)) + '/gen'
		if not os.path.isdir(root):
			os.makedirs(root)
		flname = root + '/notice_board.html'

		# Start a TPO session
		if not self.start_session():
			print 'Exiting'
			return None

		r1 = self.forum_login()

		if r1:
			html = self.get_forum_page()
			if html is not None:
				f = open(flname, 'w')
				f.write(html)
				f.close()
				return html
			else:
				print "Exiting."
				return None
		else:
			print "Exiting."
			return None

if __name__ == "__main__":
	from time import strftime
	print strftime("%Y-%m-%d %H:%M:%S")
	print __file__
	tpo = TpoSession()
	tpo.login()
