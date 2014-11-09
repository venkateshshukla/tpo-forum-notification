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

# Save the notice in form of an xml file in given path
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
	f.write('\t<url>')
	f.write(notice['url'])
	f.write('</url>\n')
	f,write('\t<text>\n')
	f.write(notice['text'])
	f.write('\t</text>\n')
	f.write('\t<num_attachments>')
	f.write(notice['num_attachments'])
	f.write('</num_attachments>\n')
	if notice['num_attachments'] != 0:
		f.write('\t<attachments>\n')
		for a in notice['attachments']:
			f.write('\t\t<title>{}</title>\n'.format(a['title']))
			f.write('\t\t<url>{}</url>\n'.format(a['url']))
		f.write('\t</attachments>\n')
	f.write('\t<updated>')
	if notice['updated']:
		f.write('1')
	else:
		f.write('0')
	f.write('</updated>\n')
	f.write('\t<sent>')
	if notice['sent']:
		f.write('1')
	else:
		f.write('0')
	f.write('</sent>\n')
	f.write('</notice>\n')
	f.close()


# Save the notices as xml in gen/xml folder by parsing gen/notice_board.html
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
		notice['updated'] = False
		notice['sent'] = False
		path = root + "/" + str(notice['timestamp']) + '.xml'
		if os.path.isfile(path):
			continue;
		else:
			count += 1
			print "Saved notice dated '{}' titled '{}'.".format(notice['time'], notice['title'])
			save_xml(path, notice);
	return count

# Save the notices as json in gen/json folder by parsing gen/notice_board.html
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

# Save the notices as fltype in given path
def insert(root = None, fltype = 'json'):
	if fltype == 'xml':
		return insert_xml(root)
	else:
		return insert_json(root)

# If run as standalone script, call insert()
if __name__ == '__main__':
	num = insert()
	if num is not None:
		print "Saved %d notices."%num

