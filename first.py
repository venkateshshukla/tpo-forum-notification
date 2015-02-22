#!/usr/bin/env python
# First run of the application - Clean the gen folder and run login, insert,
# update scripts. Then add cron jobs.

import os
import shutil
import time
import logging

from notice import Notice
from login import TpoSession
import insert
import update
import cron

log_dir = os.path.abspath(os.path.dirname(__file__)) + "/logs"
if not os.path.isdir(log_dir):
	logging.debug("making directory : %s", log_dir)
	os.makedirs(log_dir)
log_level = logging.DEBUG
log_file = "{}/{}.log".format(log_dir, time.strftime("%Y_%m_%d"))
log_format = "%(asctime)s\t%(levelname)s\t%(filename)s\t%(funcName)s()\t%(message)s"
logging.basicConfig(filename=log_file, format=log_format, level=log_level)

# On first run, all the json file will have sent attribute set to false. On
# running the send script, 25 notifications would be sent to channel
# subscribers. This is not good. So, on the first run, set these attibutes to
# false
def sent_false():
	logging.debug('called : sent_false')
	root = os.path.abspath(os.path.dirname(__file__))
	path = root + '/gen/json/'
	listfile = os.listdir(path)
	if 'old' in listfile:
		listfile.remove('old')
	for fl in listfile:
		n = Notice(fl)
		notice = n.get_json()
		if not notice['sent']:
			notice['sent'] = True
			n.save_json(notice)

root = os.path.abspath(os.path.dirname(__file__))
path = root + "/gen"

if os.path.isdir(path):
	logging.info("Found gen folder. Cleaning it up.")
	shutil.rmtree(path)

# Login and save the html file to gen
logging.info('Login and save html file to gen')
tpo = TpoSession()
tpo.login()

# From the html file, extract and save the notices
logging.info('From the html file, extract and save the notices')
num = insert.insert()
if num is None:
	logging.error("Error encountered during extraction. Exiting.")
	exit()
logging.info("Inserted %d notices.", num)

# Update the json files to include the notice details and attachments
logging.info('Updating the json files.')
update.update()

# Do not send redundant pushes on first run
logging.info('Setting the sent property to false.')
sent_false()

# Finally, insert the cron jobs to enable automatic updates
logging.info('Inserting cron jobs.')
cron.add_cron()

