#!/usr/bin/env python
# First run of the application - Clean the gen folder and run login, insert,
# update scripts. Then add cron jobs.

import os
import shutil

from notice import Notice
from login import TpoSession
import insert
import update
import cron

# On first run, all the json file will have sent attribute set to false. On
# running the send script, 25 notifications would be sent to channel
# subscribers. This is not good. So, on the first run, set these attibutes to
# false
def sent_false():
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
	print "Found gen folder. Cleaning it up."
	shutil.rmtree(path)

# Login and save the html file to gen
tpo = TpoSession()
tpo.login()

# From the html file, extract and save the notices
num = insert.insert()
if num is None:
	print "Error encountered. Exiting."
	exit()
print "Inserted %d notices."%num

# Update the json files to include the notice details and attachments
update.update()

# Do not send redundant pushes on first run
sent_false()

# Finally, insert the cron jobs to enable automatic updates
cron.add_cron()

