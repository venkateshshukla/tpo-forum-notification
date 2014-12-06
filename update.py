#!/usr/bin/env python
# Update the json file present in gen/json folder

import os
import sys
from bs4 import BeautifulSoup
from login import TpoSession
import extract
import insert
from notice import Notice

root = os.path.abspath(os.path.dirname(__file__))
gendir = root + '/gen/'
jsondir = gendir + 'json/'

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

# Check if the json is erroneous
def erroneous_json(notice):
	if notice['title'] == "":
		return True
	if notice['time'] == "":
		return True
	if notice['url'] == "":
		return True
	return False

# Given the path of the json file, update it to include detail and attachment
def update_json(tpo, name, sent = None, updated = None):
	path = jsondir + name
	if not os.path.isfile(path):
		return

	n = Notice(name)
	notice = n.get_json()

	# If the json is erroneous, i.e, has empty fields like topic etc, start
	# fresh by removing the json file. This way the json will be reloaded at
	# next cron update.
	if erroneous_json(notice):
		print "Encountered errnoneous json {}. Deleting.".format(path)
		os.remove(path)
		return False

	# If notice is updated, do not update it once more.
	if notice['updated']:
		return False

	html = tpo.get_forum_notice(notice['url'])
	if html is None:
		return False

	details = extract.get_notice_details(html, notice['num_attachments'] == 1)
	if details is None:
		return False

	notice['updated'] = True
	notice['text'] = details['text']
	if notice['num_attachments'] == 1:
		notice['attachments'] = details['attachments']
		notice['num_attachments'] = len(details['attachments'])

	n.save_json(notice)

	return True

# Perform an update operation for the given notice name
def update_name(name):
	tpo = TpoSession()
	tpo.start_session()
	tpo.forum_login()
	return update_json(tpo, name)

# Perform an update operation for the notices
def update():
	if not os.path.isdir(jsondir):
		return

	clean_old(jsondir)

	filelist = os.listdir(jsondir)

	up_count = 0
	tpo = TpoSession()
	tpo.start_session()
	tpo.forum_login()
	print "Updating notices"
	for f in filelist:
		if update_json(tpo, f):
			up_count += 1
			sys.stdout.write("\r{} Notices updated.".format(up_count))
			sys.stdout.flush()
	if up_count == 0:
		print '0 Notices updated.'
	else:
		print ''
	return up_count

# If run as a standalone script, run update()
if __name__ == '__main__':
	from time import strftime
	print strftime("%Y-%m-%d %H:%M:%S")
	print __file__
	n = update()

