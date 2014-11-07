#!/usr/bin/env python
# Update the json file present in gen/json folder

import os
from bs4 import BeautifulSoup
import json
import login
import extract
import insert

def clean_old(path):
	full_path = os.path.abspath(path)
	if len(full_path) < 9:
		return
	if full_path[-9:] != '/gen/json':
		print 'Cannot clean folder that is not gen/json :', full_path
		return
	max_size = 25
	filelist = os.listdir(path)
	if len(filelist) <= max_size:
		print 'No more than %d files present. No cleanup needed.'%max_size
		return
	filelist.sort(reverse=True)
	old_path = full_path + '/old'
	for f in filelist[max_size:]:
		os.rename(full_path + '/' + f, old_path + '/' + f)

def update_json(path):
	f = open(path, 'r')
	txt = f.read()
	f.close()
	notice = json.loads(txt)
	if notice['updated']:
		return False
	html = login.get_forum_notice(notice['url'])
	if html is None:
		return False
	details = extract.get_notice_details(html)
	if details is None:
		return False
	notice['updated'] = True
	notice['text'] = details['text']
	if notice['attachment']:
		notice['attachment-url'] = details['attachment-url']
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
	for f in filelist:
		if update_json(dirname + '/' + f):
			up_count += 1
	return up_count

# If run as a standalone script, run update()
if __name__ == '__main__':
	n = update()
	print "Updated %d notices."%n

