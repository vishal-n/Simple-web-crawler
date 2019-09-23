
import urllib.request
from bs4 import BeautifulSoup
import re
import requests
import threading
import sys

def get_page(url):
	"""
	Returns the contents of a web page.
	"""

	with urllib.request.urlopen(url) as response:
		contents = response.read()

	return contents

#print(get_page("https://www.google.com/"))

def print_all_links(url):
	page = str(get_page(url))

	while(get_next_target(url) != None, 0):
		url, end_pos = get_next_target(url)
		if(url):
			page = page[end_pos:]
		else:
			break

def get_all_links(url):
	"""
	Returns all the links in a web page.
	"""

	links = []
	try:
		data = get_page(url)
		soup = BeautifulSoup(data, features="html.parser")
		for link in soup.find_all('a'):
			links.append(link.get('href'))
		for item in links:
			print(item)
	except ValueError as ve:
		print("Error reading the url: {}, {}".format(url, ve))
	except Exception as ex:
		print("Error reading the url: {}, {}".format(url, ex))
	except: 
		print("Error reading the url: {}, {}".format(url))

	return links

crawled = []
#depth = 0

def crawl_web(url):
	global depth
	global crawled 

	links = get_all_links(url)
	crawled.append(url)
	for link in links:
		if link not in crawled:
			crawl_web(link)

#crawl_web("https://stackoverflow.com/")

if __name__ == '__main__':

	t1 = threading.Thread(target=get_page, args=(sys.argv[1],))
	t2 = threading.Thread(target=get_all_links, args=(sys.argv[1],))
	t3 = threading.Thread(target=crawl_web, args=(sys.argv[1],))

	t1.start()
	t2.start()
	t3.start()

	t1.join()
	t2.join()
	t3.join()
