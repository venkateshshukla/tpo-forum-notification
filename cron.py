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

	cmd_run = root + '/run.py'
	job_run = cron.new(command=cmd_run, comment=comment)
	job_run.minute.every(1)

	cron.write()

	# Checking if the cron jobs are added by checking all cron with comment
	for job in cron:
		if job.comment == comment:
			print job

if __name__ == "__main__":
	from time import strftime
	print strftime("%Y-%m-%d %H:%M:%S")
	print __file__
	add_cron()

