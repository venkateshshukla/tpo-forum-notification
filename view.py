#!/usr/bin/env python
# Veiw the generated files easily

import os
import json

# Given path to json file, print it
def view_json(path):
	f = open(path)
	txt = f.read()
	f.close()

	baseurl = "http://www.iitbhu.ac.in/tpo/forum"
	notice = json.loads(txt)
	fstr = "="*80
	fstr += "\n{}\n\nTime\t:\t{}\nAttch\t:\t{}\n".format(notice['title'],
			notice['time'], notice['num_attachments'])
	fstr += "Url\t:\t{}\n".format(baseurl + notice['url'])
	fstr += "Updated\t:\t{}\n".format(notice['updated'])
	fstr += "Sent\t:\t{}\n\n".format(notice['sent'])
	if notice['updated']:
		fstr += notice['text']
		if notice['num_attachments'] > 0:
			fstr += "\n\nAttachments\n\n"
			for a in notice['attachments']:
				fstr += "{}\t\t{}\n".format(a['title'], baseurl + a['url'])
	fstr += "="*80
	fstr += "\n"
	print fstr

# Print all the json files present in gen/json
def view_all_json():
	root = os.path.abspath(os.path.dirname(__file__))
	path = root + "/gen/json/"
	listdir = os.listdir(path)
	if 'old' in listdir:
		listdir.remove('old')
	for l in listdir:
		view_json(path + l)

if __name__ == "__main__":
	view_all_json()

