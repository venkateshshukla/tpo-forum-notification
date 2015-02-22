#!/usr/bin/env python
# Update the json file present in gen/json folder

import os
import sys
import logging
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
	logging.debug("called : clean_old")
	logging.debug("argument path : %s", path)

	full_path = os.path.abspath(path)
	# Full path must be something like "*/gen/json" anything smaller is not
	# considered
	if len(full_path) < 9:
		logging.error("path %s is too short to have /gen/json",
				full_path)
		return
	if full_path[-9:] != '/gen/json':
		logging.error('Cannot clean folder that is not gen/json :',
				full_path)
		return
	# Notice board contains 25 notices by default
	max_size = 25

	filelist = os.listdir(path)
	# Do not consider 'old' directory
	if 'old' in filelist:
		filelist.remove('old')

	# Check if clean up is actually needed
	if len(filelist) <= max_size:
		logging.info('Less than %d files present. No cleanup needed.',
				max_size)
		return

	# Reverso sort so that older files are kept at the end. This helps in
	# their removal
	filelist.sort(reverse=True)

	old_path = full_path + '/old'
	if not os.path.isdir(old_path):
		logging.debug('making old directory : %s', old_path)
		os.makedirs(old_path)

	for f in filelist[max_size:]:
		logging.info("moving file %s to directory %s", f, old_path)
		os.rename(full_path + '/' + f, old_path + '/' + f)

# Check if the json is erroneous
def erroneous_json(notice):
	logging.debug("called : erroneous_json")
	logging.debug("argument notice : %s", str(notice))
	if notice['title'] == "":
		logging.info("notice has empty title field")
		return True
	if notice['time'] == "":
		logging.info("notice has empty time field")
		return True
	if notice['url'] == "":
		logging.info("notice has empty url field")
		return True
	return False

# Given the path of the json file, update it to include detail and attachment
def update_json(tpo, name, sent = None, updated = None):
	logging.debug("called : update_json")
	logging.debug("argument name : %s", name)
	logging.debug("argument sent : %s", str(sent))
	logging.debug("argument updated : %s", str(updated))

	path = jsondir + name
	if not os.path.isfile(path):
		logging.error("json file '%s' is not present.", path)
		return

	n = Notice(name)
	notice = n.get_json()

	# If the json is erroneous, i.e, has empty fields like topic etc, start
	# fresh by removing the json file. This way the json will be reloaded at
	# next cron update.
	if erroneous_json(notice):
		logging.error("Encountered errnoneous json %s. Deleting.",
				str(path))
		os.remove(path)
		return False

	# If notice is updated, do not update it once more.
	if notice['updated']:
		logging.info("notice %s is already updated", name)
		return False

	# Get the notice page html from the TPO website
	logging.debug("Extracting notice page html from the TPO website")
	html = tpo.get_forum_notice(notice['url'])
	if html is None:
		logging.error("Failed getting html file of notice from TPO")
		return False

	# Extract information from the notice
	logging.debug("Extract useful information from the notice page.")
	details = extract.get_notice_details(html, notice['num_attachments'] == 1)
	if details is None:
		logging.error("Failed extracting information from the notice page.")
		return False

	logging.debug("Notice has been updated with information from the notice	page")
	notice['updated'] = True
	notice['text'] = details['text']
	if notice['num_attachments'] == 1:
		notice['attachments'] = details['attachments']
		notice['num_attachments'] = len(details['attachments'])

	logging.debug('Saving the updated notice')
	n.save_json(notice)

	return True

# Perform an update operation for the given notice name
def update_name(name):
	logging.debug("called : update_name")
	tpo = TpoSession()
	tpo.start_session()
	tpo.forum_login()
	return update_json(tpo, name)

# Perform an update operation for the notices
def update():
	logging.debug("called : update")
	if not os.path.isdir(jsondir):
		logging.error("no directory named %s", jsondir)
		return

	clean_old(jsondir)

	filelist = os.listdir(jsondir)

	up_count = 0
	tpo = TpoSession()
	tpo.start_session()
	tpo.forum_login()
	print "Updating notices"
	logging.info("Updating notices")
	for f in filelist:
		if update_json(tpo, f):
			up_count += 1
			sys.stdout.write("\r{} Notices updated.".format(up_count))
			sys.stdout.flush()
	if up_count == 0:
		print '0 Notices updated.'
	else:
		print ''
	logging.info("%d notice updated", up_count)
	return up_count

# If run as a standalone script, run update()
if __name__ == '__main__':
	log_level = logging.INFO
	log_format = "%(asctime)s\t%(levelname)s\t%(filename)s\t%(funcName)s()\t%(message)s"
	logging.basicConfig(format=log_format, level=log_level)

	logging.info("starting %s", __file__)
	n = update()
	logging.info("finished %s", __file__)

