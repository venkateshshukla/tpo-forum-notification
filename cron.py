#!/usr/bin/env python
# Script for scheduling various scripts to be run at specific time intervals

import os
import logging
from crontab import CronTab

# Add cron jobs to system crontab
def add_cron():
	logging.debug("called : add_cron")
	cron = CronTab()

	# All cron job added by this application has comment
	# 'tpo_forum_notification'. This allows their easy removal and addition
	root = os.path.abspath(os.path.dirname(__file__))
	comment = 'tpo_forum_notification'

	# Remove all cron jobs added by this application.
	logging.info("removing cron jobs with comment : %s", comment)
	cron.remove_all(comment=comment)

	# The cron job to be run
	cmd_run = root + '/run.py'
	job_run = cron.new(command=cmd_run, comment=comment)
	job_run.minute.every(1)

	# Committing the change. Writing the new cron entries.
	logging.info("writing cron entries")
	cron.write()

	# Checking if the cron jobs are added by checking all cron with comment
	for job in cron:
		if job.comment == comment:
			logging.info("added cron job : %s", job)
			print job

if __name__ == "__main__":
	log_level = logging.INFO
	log_format = "%(asctime)s\t%(levelname)s\t%(filename)s\t%(funcName)s()\t%(message)s"
	logging.basicConfig(format=log_format, level=log_level)

	logging.info("starting %s", __file__)
	add_cron()
	logging.info("finished %s", __file__)

