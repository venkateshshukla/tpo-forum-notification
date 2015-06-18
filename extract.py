#!/usr/bin/env python
# Extract useful information from TPO Forum html page

import os.path
from bs4 import BeautifulSoup
import bs4
import re
from datetime import datetime
import logging

# Get timestamp from a time string
def get_timestamp(s):
	logging.debug("called : %s", __name__)
	logging.debug("argument s : %s", s)
	s = re.sub('(st|nd|rd|th),', ',', s)
	d = datetime.strptime(s, "%a %b %d, %Y %I:%M %p")
	return int(d.strftime("%s"))

# Given a list item tag enclosing a description list, extract all its info
def extract_info(li):
	logging.debug("called : %s", __name__)
	logging.debug("argument li : %s", li)

	dl = li.find('dl')
	dt = dl.find('dt')
	info = {}

	time = unicode(dt.contents[-1]).strip()
	time = time.strip(u'\xbb')
	time = time.strip()
	info['time'] = time
	info['timestamp'] = get_timestamp(time)

	a = dt.find('a')
	info['title'] = a.text
	info['url'] = a['href'].strip('\.')

	img = dt.find('img')
	if img is None:
		info['num_attachments'] = 0
	else:
		info['num_attachments'] = 1

	info['sent'] = False
	info['updated'] = False
	return info

# Print the information extracted from the description list
def print_info(info):
	logging.debug("called : %s", __name__)
	for n, i in enumerate(info):
		print i['timestamp'], '\t\t',
		print i['time'], '\t\t',
		print i['url'], '\t\t',
		print i['num_attachments'], '\t\t',
		print i['title']

		logging.info("%d : %s\t%s\t%s\t%s\t%s", n, i['timestamp'],
				i['time'], i['url'], i['num_attachments'],
				i['title'])

# Open file notice_board.html and extract all the useful information from it
def get_notice_list(p):
	logging.debug("called : %s", __name__)
	logging.debug("argument p : %s", str(p))
	if p is None:
		logging.error("empty p is received")
		return None
	elif type(p) is unicode or type(p) is str:
		logging.debug("html recieved in unicode or str")
		html = p
		pr = False
	elif type(p) is bool:
		logging.debug("bool recieved")
		pr = p
		logging.debug("reading html from /gen/notice_board.html")
		filename = os.path.abspath(os.path.dirname(__file__)) + '/gen/notice_board.html'

		if not os.path.isfile(filename):
			logging.error("No file with name %s is found. Please run 'python login.py' first",
					filename)
			return None

		f = open(filename, 'r')
		html = f.read()
		f.close()
	else:
		logging.error('recieved argument of no recognised type')
		return None

	logging.debug("making a BeautifulSoup")
	soup = BeautifulSoup(html)

	div = None
	for d in soup.find_all("ul"):
		if 'class' in d.attrs:
			x = d['class']
			if 'topics' in x:
				div = d
				break
	list_li = None

	if div is None:
		logging.error("Unable to find ul of class topiclist topics")
		return None

	list_li = div.find_all('li')

	if list_li is None:
		logging.error("Error getting list items from div topics")
		return None

	print "%d notices retreived from the noticeboard"%len(list_li)
	logging.info("%d notices retreived from the noticeboard", len(list_li))

	info = []
	for li in list_li:
		info.append(extract_info(li))
	if p:
		print_info(info)
	return info

# Given the html of notice detail page, extract its details and attachment link
def get_notice_details(html, attach):
	logging.debug("called : %s", __name__)
	logging.debug("argument attach : %s", attach)
	if html is None:
		logging.error("empty html received")
		return
	logging.debug("making a BeautifulSoup")
	soup = BeautifulSoup(html)
	div = None
	for d in soup.find_all('div'):
		if 'class' in d.attrs and d['class'][0] == 'postbody':
			div = d
			break
	if div is None:
		logging.error("No div with class 'postbody' found")
		return

	details = {}

	d = div.find('div')
	e = str(d)
	f = e.replace('<br/>', '\n')
	g = BeautifulSoup(f)
	h = g.text
	details['text'] = h.encode('ascii', 'ignore')

	if attach:
		attachments = []
		dl = div.find('dl')
		a_list = dl.find_all('a')
		for a in a_list:
			t = {}
			t['title'] = a.text
			t['url'] = a['href'].strip('\.')
			attachments.append(t)
		details['attachments'] = attachments
	return details

# If run as a standalone script, run get_notice_list printing info
if __name__ == "__main__":
	log_level = logging.WARNING
	log_format = "%(asctime)s\t%(levelname)s\t%(filename)s\t%(funcName)s()\t%(message)s"
	logging.basicConfig(format=log_format, level=log_level)

	logging.info("starting %s", __file__)
	get_notice_list(True)
	logging.info("finished %s", __file__)

