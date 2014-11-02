# Script to login to IIT BHU TPO Forum

import requests
baseurl = "http://www.iitbhu.ac.in/tpo/forum"

# Get session id for logging in the forum.
def get_sid():
	print "Starting a new session."
	url = baseurl + "/ucp.php"
	sid_key = 'iitbhu_phpbb3_sid'

	response = requests.get(url)
	cookies = response.cookies
	sid = cookies[sid_key]

	print "New session started with session id : ", sid
	return sid, cookies

# Using the session id and the cookies, login to the forum using a POST request
def login(sid, cookies):
	print "Trying to login to the forum"
	url = baseurl + "/ucp.php?mode=login"
	username = "student"
	password = "inspire"
	redirect = "/viewforum.php?f=163"
	login = "login"

	payload = {}
	payload["username"] = username
	payload["password"] = password
	payload["sid"] = sid
	payload["redirect"] = redirect
	payload[login] = login

	response = requests.post(url, cookies=cookies, data=payload)

	success_msg = "You have been successfully logged in."
	if success_msg in response.text:
		print "You have been successfully logged in."
		return 1, response.cookies
	else:
		print "Error during login."
		return 0, response.cookies


sid, cookies = get_sid()
r, cookies = login(sid, cookies)

