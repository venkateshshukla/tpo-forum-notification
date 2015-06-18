#!/usr/bin/env python
# Schedule tasks to run at specific intervals without using crontab per se.
# This is useful for platform independent implementation and for deploying to
# interfaces such as heroku.

import logging
import os
import time

from apscheduler.schedulers.blocking import BlockingScheduler

from run import run_db

def run_job():
	log_dir = os.path.abspath(os.path.dirname(__file__)) + '/logs'
	if not os.path.isdir(log_dir):
		logging.debug("making directory : %s", log_dir)
		os.makedirs(log_dir)

	log_level = logging.INFO
	log_file = "{}/{}.log".format(log_dir, time.strftime("%Y_%m_%d"))
	log_format = "%(asctime)s\t%(levelname)s\t%(filename)s\t%(funcName)s()\t%(message)s"
	logging.basicConfig(filename=log_file, format=log_format, level=log_level)
	run_db()

if __name__ == '__main__':
	sched = BlockingScheduler()
	sched.add_job(run_job, 'interval', minutes=3)
	try:
	        sched.start()
	except (KeyboardInterrupt, SystemExit):
	        pass
