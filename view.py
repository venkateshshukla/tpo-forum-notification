#!/usr/bin/env python
# Veiw the generated files easily

import os
import json

# Given json file, return a formatted body to be sent to user
def json_text_body(notice):
	baseurl = "http://www.iitbhu.ac.in/tpo/forum"

	fstr = notice['time'] + "\n\n"
	if notice['updated']:
		fstr += notice['text']
		if notice['num_attachments'] > 0:
			fstr += "\n\nAttachments"
			slno = 0
			for a in notice['attachments']:
				slno += 1
				fstr += "\n{}. {} - {}".format(slno, a['title'],
						baseurl + a['url'])
		fstr += "\n\n"
	else:
		if notice['attachments'] == 1:
			fstr += "{} attachments.\n\n".format(notice['attachments'])
	fstr += "View page : {}".format(baseurl + notice['url'])
	return fstr

# Given path to json file, return a formatted body string without title
def json_text_path(path):
	f = open(path)
	txt = f.read()
	f.close()

	notice = json.loads(txt)
	return json_text_body(notice)

# Given path to json file, return a formatted body string with all the details
def json_text_raw(path):
	f = open(path)
	txt = f.read()
	f.close()

	baseurl = "http://www.iitbhu.ac.in/tpo/forum"
	notice = json.loads(txt)
	fstr = "{}\n\n{}\n\n".format(notice['title'], json_text_body(notice))
	fstr += "Number of attachments : {}\n".format(notice['num_attachments'])
	fstr += "Updated : {}\n".format(notice['updated'])
	fstr += "Sent : {}\n".format(notice['sent'])
	return fstr

# Print all the json files present in gen/json
def view_all_json():
	root = os.path.abspath(os.path.dirname(__file__))
	path = root + "/gen/json/"
	listdir = os.listdir(path)
	if 'old' in listdir:
		listdir.remove('old')
	for l in listdir:
		print "="*80
		print json_text_raw(path + l)
		print "="*80

if __name__ == "__main__":
	view_all_json()

