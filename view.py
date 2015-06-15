#!/usr/bin/env python
# Veiw the generated files easily

import os
import logging

from notice import Notice

# Remove redundant tabs
def clean_tabs(text):
	logging.debug("called : %s", __name__)
	lines = text.split('\n')
	para = ''
	for line in lines:
		para += line.strip()
		para += '\n'
	return para

# Given json file, return a formatted body to be sent to user
def json_text_body(notice):
	logging.debug("called : %s", __name__)
	logging.debug("argument notice : %s", str(notice))
	baseurl = os.environ.get('TPO_BASEURL', 'http://example.com')

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
		if notice['num_attachments'] == 0:
			pass
		elif notice['num_attachments'] == 1:
			fstr += "1 attachment.\n\n"
		else:
			fstr += "{} attachments.\n\n".format(notice['num_attachments'])
	fstr += "View page : {}".format(baseurl + notice['url'])
	return clean_tabs(fstr)

# Given path to json file, return a formatted body string without title
def json_text_path(path):
	logging.debug("called : %s", __name__)
	logging.debug("argument path : %s", path)
	n = Notice(path)
	notice = n.get_json()
	return json_text_body(notice)

# Given path to json file, return a formatted body string with all the details
def json_text_raw(path):
	logging.debug("called : %s", __name__)
	logging.debug("argument path : ", path)
	n = Notice(path)
	notice = n.get_json()

	baseurl = os.environ.get('TPO_BASEURL', 'http://example.com')
	fstr = "{}\n\n{}\n\n".format(notice['title'], json_text_body(notice))
	fstr += "Number of attachments : {}\n".format(notice['num_attachments'])
	fstr += "Updated : {}\n".format(notice['updated'])
	fstr += "Sent : {}\n".format(notice['sent'])
	return fstr

# Print all the json files present in gen/json
def view_all_json():
	logging.debug("called : %s", __name__)
	root = os.path.abspath(os.path.dirname(__file__))
	path = root + "/gen/json/"
	listdir = os.listdir(path)
	listdir.sort()
	if 'old' in listdir:
		listdir.remove('old')
	for l in listdir:
		print "="*80
		print json_text_raw(path + l)
		print "="*80

if __name__ == "__main__":

	log_level = logging.INFO
	log_format = "%(asctime)s\t%(levelname)s\t%(filename)s\t%(funcName)s()\t%(message)s"
	logging.basicConfig(format=log_format, level=log_level)

	logging.debug("starting %s", __file__)
	view_all_json()
	logging.debug("finished %s", __file__)

