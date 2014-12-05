#!/usr/bin/env python
# Script to get the list of notices and save them locally

import os
import extract
import json

# Save the notice in form of json in given path
def save_json(path, notice):
	f = open(path, 'w')
	json.dump(notice, f)
	f.close()

# Save the notices as json in gen/json folder by parsing gen/notice_board.html
def insert(root = None):
	if root is None:
		root = os.path.abspath(os.path.dirname(__file__)) + "/gen/json"
	if not os.path.isdir(root):
		os.makedirs(root)
	notices = extract.get_notice_list(False)
	if notices is None:
		return None
	count = 0
	for notice in notices:
		notice['updated'] = False
		notice['sent'] = False
		path = root + '/' + str(notice['timestamp']) + '.json'
		if os.path.isfile(path):
			continue;
		else:
			count += 1
			print "Saved notice dated '{}' titled '{}'.".format(notice['time'], notice['title'])
			save_json(path, notice);
	return count

# If run as standalone script, call insert()
if __name__ == '__main__':
	num = insert()
	from time import strftime
	print strftime("%Y-%m-%d %H:%M:%S")
	print __file__
	if num is not None:
		print "Saved %d notices."%num

