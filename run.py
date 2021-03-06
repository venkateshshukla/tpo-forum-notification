#! /usr/bin/env python
# The python script that is run on every minute and does all the task
# sequentially

import os
import sys
import time
import logging

import insert
import update
import send
from login import TpoSession
from notice_db import NoticeWrapper

def run():
	# Login and save the html file to gen
	logging.info('Login and saving notice board html to gen')
	tpo = TpoSession()
	tpo.login()

	# From the html file, extract and save the notices
	logging.info('Extracting notice from notice board html.')
	num = insert.insert()
	if num is None:
		logging.error("Error encountered during extraction. Exiting.")
		exit()
	logging.info("Inserted %d notices.", num)

	# Update the json files to include the notice details and attachments
	logging.info('Updating json files')
	update.update()

	# Send the unsent notices
	logging.info('Sending unsent notices.')
	send.send_unsent()

	logging.info("Finished running script.")

def run_db():
	# Login and save the html file to gen
	logging.info('Login and saving notice board html to gen')
	tpo = TpoSession()
	tpo.login()

	NoticeWrapper.init_db()

	# From the html file, extract and save the notices
	logging.info('Saving the notices to database.')
	num = insert.insert_db()
	if num is None:
		logging.error("Error encountered during extraction. Exiting.")
		exit()
	logging.info("Inserted %d notices.", num)

	# Update the json files to include the notice details and attachments
	logging.info('Updating json files')
	update.update_db()

	# Send the unsent notices
	logging.info('Sending unsent notices.')
	send.send_unsent_db()

	NoticeWrapper.deinit_db()

	logging.info("Finished running script.")

if __name__ == '__main__':
	log_dir = os.path.abspath(os.path.dirname(__file__)) + '/logs'
	if not os.path.isdir(log_dir):
		logging.debug("making directory : %s", log_dir)
		os.makedirs(log_dir)

	log_level = logging.INFO
	log_file = "{}/{}.log".format(log_dir, time.strftime("%Y_%m_%d"))
	log_format = "%(asctime)s\t%(levelname)s\t%(filename)s\t%(funcName)s()\t%(message)s"
	logging.basicConfig(filename=log_file, format=log_format, level=log_level)
	if len(sys.argv) == 2 and sys.argv[1] == 'db':
		run_db()
	else:
		run()
