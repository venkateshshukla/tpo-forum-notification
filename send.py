#!/usr/bin/env python
# Send notification to subscribers on finding any new notice.
# For sending notifications, Pushbullet API is used. This gives the benefit of
# multiplatform support (Chrome, android and firefox) and easy implementation.
# For more details on Pushbullet API, look at https://docs.pushbullet.com/

import os
import json
import requests
import logging

import view
import update
from notice import Notice
from notice_db import NoticeWrapper

root = os.path.abspath(os.path.dirname(__file__))
path = root + "/gen/json/"

def push(title, body):
	"""
	Given the title and body of notification to be sent, send it to the
	pushbullet servers.

	params:
	  title : the title of notification to be sent
	  body : the body of the notification to be sent
	"""
	logging.debug("called : %s", __name__)

        # Pushbullet needs access token to your account.
	# Add environmental variables
	# TPO_PB_AUTH - The pushbullet auth token
	# TPO_PB_CHANNEL - The pushbullet channel name
	logging.info("preparing to send post request to pushbullet")
	push_url = "https://api.pushbullet.com/v2/pushes"
        auth_token = os.environ.get("TPO_PB_AUTH")
	channel_tag = os.environ.get("TPO_PB_CHANNEL")

	auth = requests.auth.HTTPBasicAuth(auth_token, '')
	headers = {'content-type' : 'application/json'}

	payload = {}
	payload['type'] = 'note'
	payload['title'] = title
	payload['body'] = body
	payload['channel_tag'] = channel_tag
	data = json.dumps(payload)

	response = requests.post(push_url, auth=auth, headers=headers,
			data=data)

	logging.info("Recieved response status code : %d", response.status_code)
	if response.status_code == 200:
		print "Success"
		logging.info("push successfully sent")
		return True
	else:
		print "Failed,", response.status_code, response.reason
		logging.error("sending push failed : %d : %s",
				response.status_code, response.reason)
		return False

def send_json(notice):
	'''Send the notification of notice for given json'''
	logging.debug("called : %s", __name__)
	logging.debug("argument notice : %s", str(notice))

        if notice is None:
		logging.error("empty notice is recieved")
                return

	time = notice['time']
	title = notice['title']
	body = view.get_text_dict(notice, True)

	print "Sending notice {} dated {}.".format(title, time)
	logging.info("Sending notice %s dated %s.", title, time)

	return push(title, body)

def send_notice(notice):
	"""
	Given a database Notice instance, send its notification.
	"""
	logging.debug("called : %s", __name__)

        if notice is None:
		logging.error("empty notice is recieved")
                return

	time = notice.print_time
	title = notice.title
	body = view.get_text_notice(notice, True)

	print "Sending notice {} dated {}.".format(title, time)
	logging.info("Sending notice %s dated %s.", title, time)

	return push_payload(data)

def send_name(filename):
	'''Send the notification for the notice of given json filename'''
	logging.debug("called : %s", __name__)
	logging.debug("argument filename : %s", filename)

	if filename is None:
		logging.error("empty filename received")
		return

	n = Notice(filename)
	notice = n.get_json()

	# If the notice is not updated, update it.
	logging.debug("checking if notice is updated")
	if not notice['updated']:
		update.update_json(filename)
		notice = n.get_json()

	# If the notice is not sent, send it.
	logging.debug("checking if notice is sent")
	if not notice['sent']:
		if send_json(notice):
			# If notice is sent, save it locally. So that it is not
			# sent again.
			logging.debug("notice is sent - saving it locally")
			notice['sent'] = True
			n.save_json(notice)
			return True
		else:
			logging.error("failed sending notice")
			return False
	else:
		logging.debug("notice is already sent")
		return False

def send_unsent():
	'''Send notifications for all notices that have not been sent yet.'''
	logging.debug("called : %s", __name__)

	filelist = os.listdir(path)
	if 'old' in filelist:
		filelist.remove('old')

	# Sorted filelist so that older json files are listed earlier. Due to
	# this, notices are sent in the order in which they arrive.
	filelist.sort()

	send_count = 0
	for f in filelist:
		if send_name(f):
			send_count += 1
			print "\r%d notifications sent."%send_count

	if send_count == 0:
		print "0 notifications sent."
	else:
		print ""

	logging.info("%d notifications sent", send_count)
	return send_count

def send_unsent_db():
	"""
	Send notification for all the unsent notices from the database
	"""
	notices = NoticeWrapper.get_unsent()

	send_count = 0
	for notice in notices:
		if send_notice(notice):
			send_count += 1
			print "\r%d notifications sent."%send_count

	if send_count == 0:
		print "0 notifications sent."
	else:
		print ""

	logging.info("%d notifications sent", send_count)
	return send_count

if __name__ == "__main__":
	log_level = logging.INFO
	log_format = "%(asctime)s\t%(levelname)s\t%(filename)s\t%(funcName)s()\t%(message)s"
	logging.basicConfig(format=log_format, level=log_level)

	logging.info("starting %s", __file__)
	s = send_unsent()
	logging.info("finished %s", __file__)

