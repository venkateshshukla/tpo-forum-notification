#!/usr/bin/env python
# Script to get the list of notices and save them locally

import os
import login
import extract
import json

def save_json(path, notice):
	f = open(path, 'w')
	json.dump(notice, f)
	f.close()

def save_xml(path, notice):
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


def insert_xml(root = None):
	if root is None:
		root = os.path.abspath(os.path.dirname(__file__)) + "/gen/xml"
	if not os.path.isdir(root):
		os.makedirs(root)
	notices = extract.get_notice_list(False)
	if notices is None:
		return None
	count = 0
	for notice in notices:
		path = root + "/" + str(notice['timestamp']) + '.xml'
		if os.path.isfile(path):
			continue;
		else:
			count += 1
			print "Saved notice dated '{}' titled '{}'.".format(notice['time'], notice['title'])
			save_xml(path, notice);
	return count

def insert_json(root = None):
	if root is None:
		root = os.path.abspath(os.path.dirname(__file__)) + "/gen/json"
	if not os.path.isdir(root):
		os.makedirs(root)
	notices = extract.get_notice_list(False)
	if notices is None:
		return None
	count = 0
	for notice in notices:
		path = root + '/' + str(notice['timestamp']) + '.json'
		if os.path.isfile(path):
			continue;
		else:
			count += 1
			print "Saved notice dated '{}' titled '{}'.".format(notice['time'], notice['title'])
			save_json(path, notice);
	return count

def insert(root = None, fltype = 'json'):
	if fltype == 'xml':
		return insert_xml(root)
	else:
		return insert_json(root)

if __name__ == '__main__':
	num = insert()
	if num is not None:
		print "Saved %d notices."%num

