#! /usr/bin/env python
# The python script that is run on every minute and does all the task
# sequentially

import insert
import update
import send
from login import TpoSession

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

# Send the unsent notices
send.send_unsent()

