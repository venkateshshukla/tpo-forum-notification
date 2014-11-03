# Extract useful information from TPO Forum html page

from bs4 import BeautifulSoup
import bs4

# Given a list item tag enclosing a description list, extract all its info
def extract_info(li):
	dl = li.find('dl')
	dt = dl.find('dt')
	info = {}

	time = unicode(dt.contents[-1]).strip()
	time = time.strip(u'\xbb')
	time = time.strip()
	info['time'] = time

	a = dt.find('a')
	info['title'] = a.text
	info['link'] = a['href'].strip('\.')

	img = dt.find('img')
	if img is None:
		info['attachment'] = False
	else:
		info['attachment'] = True

	return info

# Print the information extracted from the description list
def print_info(info):
	for i in info:
		print i['time'], '\t\t',
		print i['link'], '\t\t',
		print i['attachment'], '\t\t',
		print i['title']


# Open file notice_board.html and extract all the useful information from it
def get_notice_list():
	f = open('notice_board.html', 'r')
	html = f.read()
	f.close()

	soup = BeautifulSoup(html)
	head = soup.body
	div = None
	for d in soup.find_all("ul"):
		if 'class' in d.attrs:
			#print d['class']
			x = d['class']
			if 'topics' in x:
				div = d
				break
	list_li = None

	if div is None:
		print "Unable to find ul of class topiclist topics"
		return None

	list_li = div.find_all('li')

	if list_li is None:
		print "Error getting list items from div topics"
		return None

	print "Got %d topics in the noticeboard"%len(list_li)

	info = []
	for li in list_li:
		info.append(extract_info(li))
	#print_info(info)
	return info

if __name__ == "__main__":
	get_notice_list()
