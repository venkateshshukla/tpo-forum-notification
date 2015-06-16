#!/usr/bin/env python
# Script to get the list of notices and save them locally

import os
import logging

import extract
from notice import Notice
from notice_db import NoticeWrapper

# Save the notices as json in gen/json folder by parsing gen/notice_board.html
def insert(root = None):
	logging.debug("called : %s", __name__)
	logging.debug("argument root : %s", root)

	if root is None:
		logging.debug("empty root is received")
		root = os.path.abspath(os.path.dirname(__file__)) + "/gen/json"
	if not os.path.isdir(root):
		logging.debug("making directory : %s", root)
		os.makedirs(root)

	notices = extract.get_notice_list(False)
	if notices is None:
		logging.error("error getting notice list")
		return None
	count = 0
	for notice in notices:
		notice['updated'] = False
		notice['sent'] = False
		timestamp = str(notice['timestamp'])
		path = root + '/' + timestamp + '.json'
		if os.path.isfile(path):
			continue;
		else:
			count += 1
			print "Saved notice dated '{}' titled '{}'.".format(notice['time'], notice['title'])
			logging.info("Saved notice dated %s titled %s",
					notice['time'], notice['title'])

			n = Notice(timestamp)
			n.save_json(notice)

	logging.info("%d notices inserted", count)
	return count

def insert_db():
	"""
	Save the notices in Notice sqlite database
	"""
	logging.debug("called : %s", __name__)

	notices = extract.get_notice_list(False)
	if notices is None:
		logging.error("error getting notice list")
		return None

	count = 0
	for notice in notices:
		if NoticeWrapper.insert_dict(notice):
			count += 1
			print "Added notice dated '{}' titled '{}'.".format(
					notice['time'], notice['title'])
			logging.info("Added notice dated %s titled %s",
					notice['time'], notice['title'])
			pass
		else:
			continue

	logging.info("%d notices inserted", count)
	return count

# If run as standalone script, call insert()
if __name__ == '__main__':
	log_level = logging.WARNING
	log_format = "%(asctime)s\t%(levelname)s\t%(filename)s\t%(funcName)s()\t%(message)s"
	logging.basicConfig(format=log_format, level=log_level)

	logging.debug("starting %s", __file__)
	num = insert()
	if num is not None:
		logging.info("saved %d notices", num)
		print "Saved %d notices."%num
	logging.debug("finished %s", __file__)

