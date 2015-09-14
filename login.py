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

		self.baseurl = os.environ.get('TPO_BASEURL', 'http://example.com')
		self.username = os.environ.get('TPO_USER', 'username')
		self.password = os.environ.get('TPO_PASS', 'password')
                self.noticeurl = os.environ.get('TPO_NOTICEURL', '/viewforum?id=0')

		self.sid = None
                self.session = None

        # Rather than using individual cookies, use Request session for
        # interactions with the forum
        def start_session(self):
                logging.debug("called : start_session_2")
                url = self.baseurl + "/ucp.php"

                session = requests.Session()

                logging.debug("sending a GET request to %s", url)
                response = session.get(url)
		logging.debug("recieved response status code : %d", response.status_code)

		if response.status_code != 200:
			logging.error("Error during connection : %s", response.reason)
			return False

		sid_key = "iitbhu_phpbb3_sid"
		sid = response.cookies[sid_key]

		logging.info("Session started with session id : %s", sid)

		self.sid = sid
                self.session = session
		return True


        # Using the session already created, login to the forum using a POST
        # request
        def forum_login(self):
                logging.debug("called : forum_login")
		url = self.baseurl + "/ucp.php?mode=login"
		redirect = self.noticeurl
		login = "login"

                if  self.sid is None or self.session is None:
                        logging.error("No sid, call start_session first")
                        return False

		payload = {}
		payload["username"] = self.username
		payload["password"] = self.password
		payload["login"] = login

		logging.debug("sending a POST request to url : %s", url)
		response = self.session.post(url,  data=payload)
		logging.debug("recieved response status code : %d", response.status_code)

		if response.status_code != 200:
			logging.error("Connection to server failed : %s", response.reason)
			return False

		if self.login_success_msg in response.text:
			logging.info(self.login_success_msg)
			return True
		else:
			logging.error("Error logging in to TPO forum.")
			logging.error(self.login_failed_msg)
			return False

	# Using the session id and login cookies, Get the forum page showing notices
	def get_forum_page(self):
		logging.debug("called : get_forum_page")
		if self.sid is None or self.session is None:
			logging.error("Tpo session cookies or sid not present")
			logging.info("Start a new session first using method start_session()")
			return None

		payload = {}
		payload["sid"] = self.sid

		url = self.baseurl + self.noticeurl

		logging.debug("sending a POST request to url : %s", url)
		response = self.session.get(url, params=payload)
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
		response = self.session.get(url, data=payload)
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

