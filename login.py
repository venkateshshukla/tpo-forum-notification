#!/usr/bin/env python
# Script to login to IIT BHU TPO Forum

import os
import requests

class TpoSession:
	def __init__(self):
		self.baseurl = "http://www.iitbhu.ac.in/tpo/forum"
		self.username = "student"
		self.password = "inspire"
		self.sid = None
		self.cookies = None

	# Get session id for logging in the forum.
	def get_sid(self):
		print "Starting a new session."
		url = self.baseurl + "/ucp.php"
		sid_key = 'iitbhu_phpbb3_sid'

		response = requests.get(url)
		cookies = response.cookies
		sid = cookies[sid_key]

		print "New session started with session id : ", sid
		self.sid = sid
		self.cookies = cookies
		return sid

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

		success_msg = "You have been successfully logged in."
		if response.status_code != 200:
			print "Error connecting to the server"
			return 0, None
		if success_msg in response.text:
			print success_msg
			self.cookies = response.cookies
			return 1, response.cookies
		else:
			print "Error during login."
			return 0, response.cookies

	# Using the session id and login cookies, get the forum page showing notices
	def get_forum_page(self):
		payload = {}
		payload["sid"] = self.sid
		print "Retrieving the forum page."
		url = self.baseurl + "/viewforum.php?f=163"
		response = requests.get(url, cookies=self.cookies, data=payload)
		if response.status_code == 200:
			print "Forum page retrieved."
			return 1, response.content
		else:
			print "Error retrieving forum page."
			return 0, None

	# Get the forum page showing the notice details
	def get_forum_notice(self, offset):
		pass

	# Login and retrieve forum html
	def login(self):
		root = os.path.abspath(os.path.dirname(__file__)) + '/gen'
		if not os.path.isdir(root):
			os.makedirs(root)
		flname = root + '/notice_board.html'
		sid = self.get_sid()
		r1 = self.forum_login()

		if r1 == 1:
			r2, html = self.get_forum_page()
			if r2 == 1:
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
