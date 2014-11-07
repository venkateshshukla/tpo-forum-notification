#!/usr/bin/env python
# Script to get the list of notices and save them locally

import os
import login
import extract

def save_xml(root, notice):
	path = root + "/" + str(notice['timestamp'])
	f = open(path, 'w')
	f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
	f.write('<notice>\n')
	f.write('\t<title>')
	f.write(notice['title'])
	f.write('</title>\n')
	f.write('\t<time>')
	f.write(notice['time'])
	f.write('</time>\n')
	f.write('\t<timestamp>')
	f.write(str(notice['timestamp']))
	f.write('</timestamp>\n')
	f.write('\t<link>')
	f.write(notice['link'])
	f.write('</link>\n')
	f.write('\t<attachment>')
	if notice['attachment']:
		f.write('1')
	else:
		f.write('0')
	f.write('</attachment>\n')
	f.write('</notice>\n')
	f.close()


def insert(root):
	if root is None:
		root = os.path.abspath(os.path.dirname(__file__)) + "/gen/xml"
	if not os.path.isdir(root):
		os.makedirs(root)
	notices = extract.get_notice_list(False)
	if notices is None:
		return None
	count = 0
	for notice in notices:

		if os.path.isfile(root + "/" + str(notice['timestamp'])):
			continue;
		else:
			count += 1
			print "Saved notice dated '{}' titled '{}'.".format(notice['time'], notice['title'])
			save_xml(root, notice);
	return count

if __name__ == '__main__':
	num = insert(None)
	if num is not None:
		print "Saved %d notices."%num

