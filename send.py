#!/usr/bin/env python
# Send notification to subscribers on finding any new notice.
# For sending notifications, Pushbullet API is used. This gives the benefit of
# multiplatform support (Chrome, android and firefox) and easy implementation.
# For more details on Pushbullet API, look at https://docs.pushbullet.com/

import os
import json
import requests
import view

# Given a notice, send all the details to channel
def send_json(notice):
        if notice is None:
                return
        # Pushbullet needs access token to your account.
        # This is an old token and does not work. Replace it with yours
	# Push url remains same for everyone.
	# Channel tag is essential for sending a push message to channel
	# subscribers
        auth_token = "v1K2CgrcMgI8GMVY6FXcq3YueVn696RW2ZujAfWNgp38u"
	push_url = "https://api.pushbullet.com/v2/pushes"
	channel_tag = "iitbhutpo-test"

	auth = requests.auth.HTTPBasicAuth(auth_token, '')

	headers = {'content-type' : 'application/json'}

	payload = {}
	payload['type'] = 'note'
	payload['title'] = notice['title']
	payload['body'] = view.json_text_body(notice)
	payload['channel_tag'] = channel_tag

	data = json.dumps(payload)

	print "Sending notice {} dated {}.".format(notice['title'], notice['time'])
	response = requests.post(push_url, auth=auth, headers=headers, data=data)
	if response.status_code == 200:
		print "Success"
		return True
	else:
		print "Failed,", response.status_code, response.reason
		return False

# Given path of json file, send a notification.
def send_path(path):
	if path is None:
		return
	f = open(path)
	txt = f.read()
	f.close()

	notice = json.loads(txt)
	if not notice['sent']:
		if send_json(notice):
			# If notice is sent, save it locally. So that it is not
			# sent again.
			notice['sent'] = True
			f = open(path, 'w')
			json.dumps(notice, f)
			f.close()
			return True
		else:
			return False
	else:
		return False

# Check all the json file and sent notifications for unsent messages.
def send_unsent():
	root = os.path.abspath(os.path.dirname(__file__))
	path = root + "/gen/json/"

	filelist = os.listdir(path)
	if 'old' in filelist:
		filelist.remove('old')

	filelist.sort()

	send_count = 0
	for f in filelist:
		if send_path(path + f):
			send_count += 1
			print "\r%d notifications sent."%send_count
	if send_count == 0:
		print "0 notifications sent."
	else:
		print ""
	return send_count

if __name__ == "__main__":
	s = send_unsent()

