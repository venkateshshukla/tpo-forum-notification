#!/usr/bin/env python
# Script to login to IIT BHU TPO Forum

import os
import requests

class TpoSession:
	"A session for interaction with the TPO Forum"

	login_failed_msg = "The board requires you to be registered and logged in to view this forum."
	login_success_msg = "You have been successfully logged in."

	def __init__(self):
		self.baseurl = "http://www.iitbhu.ac.in/tpo/forum"
		self.username = "student"
		self.password = "inspire"
		self.sid = None
		self.cookies = None

	# Get session id for logging in the forum.
	def start_session(self):
		print "Starting a new session."
		url = self.baseurl + "/ucp.php"
		sid_key = 'iitbhu_phpbb3_sid'

		response = requests.get(url)
		cookies = response.cookies
		sid = cookies[sid_key]

		print "New session started with session id : ", sid
		self.sid = sid
		self.cookies = cookies

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
		self.start_session()
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
	tpo = TpoSession()
	tpo.login()
