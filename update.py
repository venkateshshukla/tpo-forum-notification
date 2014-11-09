#!/usr/bin/env python
# Update the json file present in gen/json folder

import os
from bs4 import BeautifulSoup
import json
from login import TpoSession
import extract
import insert

# If more than max_size files present in json, move the old ones to old/
def clean_old(path):
	full_path = os.path.abspath(path)
	if len(full_path) < 9:
		return
	if full_path[-9:] != '/gen/json':
		print 'Cannot clean folder that is not gen/json :', full_path
		return
	max_size = 25
	filelist = os.listdir(path)
	if 'old' in filelist:
		filelist.remove('old')
	if len(filelist) <= max_size:
		print 'No more than %d files present. No cleanup needed.'%max_size
		return
	filelist.sort(reverse=True)
	old_path = full_path + '/old'
	if not os.path.isdir(old_path):
		os.makedirs(old_path)
	for f in filelist[max_size:]:
		print "Cleaning " + f
		os.rename(full_path + '/' + f, old_path + '/' + f)

# Given the path of the json file, update it to include detail and attachment
def update_json(tpo, path):
	if not os.path.isfile(path):
		return
	f = open(path, 'r')
	txt = f.read()
	f.close()
	notice = json.loads(txt)
	if notice['updated']:
		return False
	html = tpo.get_forum_notice(notice['url'])
	if html is None:
		return False
	details = extract.get_notice_details(html)
	if details is None:
		return False
	notice['updated'] = True
	notice['text'] = details['text']
	if notice['attachment']:
		notice['attachment-urls'] = details['attachment-urls']
	insert.save_json(path, notice)
	return True

# Perform an update operation for the notices
def update():
	root = os.path.abspath(os.path.dirname(__file__))
	dirname = root + '/gen/json'

	if not os.path.isdir(dirname):
		return

	clean_old(dirname)

	filelist = os.listdir(dirname)
	filelist.sort(reverse=True)

	up_count = 0
	tpo = TpoSession()
	tpo.start_session()
	tpo.forum_login()
	print "Updating notices"
	for f in filelist:
		if update_json(tpo, dirname + '/' + f):
			up_count += 1
	return up_count

# If run as a standalone script, run update()
if __name__ == '__main__':
	n = update()
	print "Updated %d notices."%n

