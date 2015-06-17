#!/usr/bin/env python
# Veiw the generated files easily

import os
import logging

from notice import Notice
from notice_db import NoticeWrapper

# Remove redundant tabs
def clean_tabs(text):
	logging.debug("called : %s", __name__)
	lines = text.split('\n')
	para = ''
	for line in lines:
		para += line.strip()
		para += '\n'
	return para

def get_text_dict(notice, only_body=False):
	"""
	Given notice dict, return a formatted body to be sent to user.

	params:
	  notice : a dict containing all notice information
	  only_body : a boolean - include only the body of the notice?
	"""
	logging.debug("called : %s", __name__)
	logging.debug("argument notice : %s", str(notice))
	baseurl = os.environ.get('TPO_BASEURL', 'http://example.com')

	if only_body:
		fstr = "{}\n\n".format(notice['time'])
	else:
		fstr = "{}\n\n{}\n\n".format(notice['title'], notice['time'])
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
	fstr += "View page : {}\n".format(baseurl + notice['url'])
	if not only_body:
		fstr += "Updated : {}\n".format(notice['updated'])
		fstr += "Sent : {}\n".format(notice['sent'])
	return clean_tabs(fstr)

def get_text_notice(notice, only_body=False):
	"""
	Given a Notice db instance, return a formatted body to be sent to user.

	params:
	  notice : a dict containing all notice information
	  only_body : a boolean - include only the body of the notice?
	"""
	logging.debug("called : %s", __name__)

	baseurl = os.environ.get('TPO_BASEURL', 'http://example.com')
	if only_body:
		fstr = "{}\n\n".format(notice.print_time)
	else:
		fstr = "{}\n\n{}\n\n".format(notice.title, notice.print_time)
	if notice.updated:
		fstr += notice.text
		if notice.num_attachments > 0:
			fstr += "\n\nAttachments"
			slno = 0
			a = notice.attachments
			while a is not None:
				slno += 1
				fstr += "\n{}. {} - {}".format(slno, a.title,
						baseurl + a.url)
				a = a.next
		fstr += "\n\n"
	else:
		if notice.num_attachments == 0:
			pass
		elif notice.num_attachments == 1:
			fstr += "1 attachment.\n\n"
		else:
			fstr += "{} attachments.\n\n".format(notice.num_attachments)
	fstr += "View page : {}\n".format(baseurl + notice.url)
	if not only_body:
		fstr += "Updated : {}\n".format(notice.updated)
		fstr += "Sent : {}\n".format(notice.sent)
	return clean_tabs(fstr)

def get_text_path(path):
	"""
	Given path to json file, return a formatted body string with all the details
	"""
	logging.debug("called : %s", __name__)
	logging.debug("argument path : ", path)
	n = Notice(path)
	notice = n.get_json()
	return get_text_dict(notice)

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
		print get_text_path(path + l)
		print "="*80

def view_db(num=25):
	"""
	Print all the notices present in the Notice database.
	"""
	logging.debug("called : %s", __name__)
	notices = NoticeWrapper.get_last(num)
	for notice in notices:
		print "="*80
		print get_text_notice(notice)
		print "="*80

if __name__ == "__main__":

	log_level = logging.INFO
	log_format = "%(asctime)s\t%(levelname)s\t%(filename)s\t%(funcName)s()\t%(message)s"
	logging.basicConfig(format=log_format, level=log_level)

	logging.debug("starting %s", __file__)
	view_all_json()
	logging.debug("finished %s", __file__)

