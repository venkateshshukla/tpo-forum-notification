#!/usr/bin/env python
# Script to login to IIT BHU TPO Forum

import os
import requests
import logging
import time

class TpoSession(object):
	"A session for interaction with the TPO Forum"

	login_failed_msg = "The board requires you to be registered and logged in to view this forum."
	login_success_msg = "You have been successfully logged in."

	def __init__(self):
		logging.debug("created object : TpoSession")
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
		logging.debug("setting baseurl : %s", url)
		self._baseurl = url

	@baseurl.deleter
	def baseurl(self):
		del self._baseurl

	@property
	def username(self):
		return self._username

	@username.setter
	def username(self, name):
		logging.debug("setting username : %s", name)
		self._username = name

	@username.deleter
	def username(self):
		del self._username

	@property
	def password(self):
		return self._password

	@password.setter
	def password(self, pwd):
		logging.debug("setting password : %s", pwd)
		self._password = pwd

	@password.deleter
	def password(self):
		del self._password

	@property
	def sid(self):
		return self._sid

	@sid.setter
	def sid(self, x):
		logging.debug("setting sid : %s", str(x))
		self._sid = x

	@sid.deleter
	def sid(self):
		del self._sid

	@property
	def cookies(self):
		return self._cookies

	@cookies.setter
	def cookies(self, ck):
		logging.debug("setting cookies : %s", str(ck))
		self._cookies = ck

	@cookies.deleter
	def cookies(self):
		del self._cookies

	# Get session id for logging in the forum.
	def start_session(self):
		logging.debug("called : start_session")
		url = self.baseurl + "/ucp.php"
		sid_key = "iitbhu_phpbb3_sid"

		logging.debug("sending a GET request to %s", url)
		response = requests.get(url)
		logging.debug("recieved response status code : %d", response.status_code)

		if response.status_code != 200:
			logging.error("Error during connection : %s", response.reason)
			return False

		cookies = response.cookies
		sid = cookies[sid_key]

		logging.info("Session started with session id : %s", sid)

		self.sid = sid
		self.cookies = cookies
		return True

	# Using the session id and the cookies, login to the forum using a POST request
	def forum_login(self):
		logging.debug("called : forum_login")
		url = self.baseurl + "/ucp.php?mode=login"
		redirect = "/viewforum.php?f=163"
		login = "login"

		payload = {}
		payload["username"] = self.username
		payload["password"] = self.password
		payload["sid"] = self.sid
		payload["login"] = login

		logging.debug("sending a POST request to url : %s", url)
		response = requests.post(url, cookies=self.cookies, data=payload)
		logging.debug("recieved response status code : %d", response.status_code)

		if response.status_code != 200:
			logging.error("Connection to server failed : %s", response.reason)
			return False

		if self.login_success_msg in response.text:
			logging.info(self.login_success_msg)
			self.cookies = response.cookies
			return True
		else:
			logging.error("Error logging in to TPO forum.")
			logging.error(self.login_failed_msg)
			return False

	# Using the session id and login cookies, Get the forum page showing notices
	def get_forum_page(self):
		logging.debug("called : get_forum_page")
		if self.sid == None or self.cookies == None:
			logging.error("Tpo session cookies or sid not present")
			logging.info("Start a new session first using method start_session()")
			return None

		payload = {}
		payload["sid"] = self.sid

		url = self.baseurl + "/viewforum.php?f=163"

		logging.debug("sending a POST request to url : %s", url)
		response = requests.get(url, cookies=self.cookies, data=payload)
		logging.debug("recieved response with status %s",
				str(response.status_code))

		if response.status_code == 200:
			if self.login_failed_msg in response.content:
				logging.error("recieved : %s",
						self.login_failed_msg)
				logging.error("not logged in to the forum")
				logging.info("first login to the forum using forum_login()")
				return None
			logging.info("Forum page retrieved.")
			return response.content
		else:
			logging.error("Error retrieving forum page : " +
					response.reason)
			return None

	# Get the forum page showing the notice details
	def get_forum_notice(self, offset = None):
		logging.debug("called : get_forum_notice")
		logging.debug("param offset : %s", offset)
		if offset == None:
			logging.error("Empty offset recieved")
			logging.info("Offset is empty. Include notice url")
			return None
		if self.sid == None or self.cookies == None:
			logging.error("TPO session cookies or sid missing")
			logging.info("Start a new session first using method start_session()")
			return None

		payload = {}
		payload["sid"] = self.sid

		url = self.baseurl + offset

		logging.debug("sending a GET request to url : %s", url)
		response = requests.get(url, cookies=self.cookies, data=payload)
		logging.debug("recieved response status code : %d",
				response.status_code)

		if response.status_code == 200:
			if self.login_failed_msg in response.content:
				logging.error("received : %s",
						self.login_failed_msg)
				logging.error("not logged in the TPO forum")
				logging.info("Login first by running method orum_login()")
				return None
			logging.info("Notice retrieved.")
			return response.content
		else:
			logging.error("Error retrieving notice page : %s",
					response.reason)
			return None

	# Login and retrieve forum html
	def login(self):
		logging.debug("called : login")
		root = os.path.abspath(os.path.dirname(__file__)) + "/gen"
		if not os.path.isdir(root):
			logging.debug("making directory : %s", root)
			os.makedirs(root)
		flname = root + "/notice_board.html"

		# Start a TPO session
		logging.info("starting a new TPO session")
		if not self.start_session():
			logging.error("Error starting a tpo session. Exiting")
			return None

		logging.info("logging in to the TPO forum")
		r1 = self.forum_login()

		if r1:
			logging.info("getting the notice board page")
			html = self.get_forum_page()
			if html is not None:
				logging.debug("writing html to file : %s", flname)
				f = open(flname, "w")
				f.write(html)
				f.close()
				logging.debug("file %s written", flname)
				return html
			else:
				logging.error("Empty html recieved. Exiting")
				return None
		else:
			logging.error("Login to forum failed. Exiting")
			return None

if __name__ == "__main__":
	log_level = logging.INFO
	log_format = "%(asctime)s\t%(levelname)s\t%(filename)s\t%(funcName)s()\t%(message)s"
	logging.basicConfig(format=log_format, level=log_level)

	logging.info("starting %s", __file__)
	tpo = TpoSession()
	tpo.login()
	logging.info("finished %s", __file__)

