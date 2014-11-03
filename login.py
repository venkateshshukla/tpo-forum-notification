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
def forum_login(sid, cookies):
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
	payload["login"] = login

	response = requests.post(url, cookies=cookies, data=payload)

	success_msg = "You have been successfully logged in."
	if success_msg in response.text:
		print success_msg
		return 1, response.cookies
	else:
		print "Error during login."
		return 0, response.cookies

# Using the session id and login cookies, get the forum page showing notices
def get_forum_page(sid, cookies):
	payload = {}
	payload["sid"] = sid
	print "Retrieving the forum page."
	url = baseurl + "/viewforum.php?f=163"
	response = requests.get(url, cookies=cookies, data=payload)
	if response.status_code == 200:
		print "Forum page retrieved."
		return 1, response.content
	else:
		print "Error retrieving forum page."
		return 0, None

# Login and retrieve forum html
def login():
	sid, cookies1 = get_sid()
	r1, cookies2 = login(sid, cookies1)

	if r1 == 1:
		r2, html = get_forum_page(sid, cookies2)
		if r2 == 1:
			f = open('forum.html', 'w')
			f.write(html)
			f.close()
			return html
		else:
			print "Exiting."
			return None
	else:
		print "Exiting."
		return None

