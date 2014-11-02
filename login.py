# Script to login to IIT BHU TPO Forum

import requests

# Get session id for logging in the forum.
def get_sid():
	url = "http://iitbhu.ac.in/tpo/forum/ucp.php"
	sid_key = 'iitbhu_phpbb3_sid'

	response = requests.get(url)
	cookies = response.cookies
	sid = cookies[sid_key]
	return sid, cookies

sid, cookies = get_sid()
print sid

