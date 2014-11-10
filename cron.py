#!/usr/bin/env python
# Script for scheduling various scripts to be run at specific time intervals

import os
from crontab import CronTab

# Add cron jobs to system crontab
def add_cron():
	cron = CronTab()

	root = os.path.abspath(os.path.dirname(__file__))
	comment = 'tpo_forum_notification'

	cron.remove_all(comment=comment)

	cmd_login = root + '/login.py'
	job_login = cron.new(command=cmd_login, comment=comment)
	job_login.minute.every(1)

	cmd_insert = root + '/insert.py'
	job_insert = cron.new(command=cmd_insert, comment=comment)
	job_insert.minute.every(2)

	cmd_update = root + '/update.py'
	job_update = cron.new(command=cmd_update, comment=comment)
	job_update.minute.every(3)

	cmd_send = root + '/send.py'
	job_send = cron.new(command=cmd_send, comment=comment)
	job_send.minute.every(5)

	cron.write()

	# Checking if the cron jobs are added by checking all cron with comment
	for job in cron:
		if job.comment == comment:
			print job

if __name__ == "__main__":
	add_cron()

