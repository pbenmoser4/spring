from django.shortcuts import render
from bs4 import BeautifulSoup, NavigableString
import urllib2
import re
from chat.models import User

def soupify(address, user_agent='Mozilla/5.0'):
	url = urllib2.Request(address, headers={'User-Agent':user_agent})
	connection = urllib2.urlopen(url)
	return BeautifulSoup(connection)

def clean_link(link, base=""):
	if not re.match(r'^http', link):
		return base + str(link)
	else:
		return link

def clean_output(str):
	return re.sub(r'\s+?',' ',str)

def get_google_links(search_item):
		# setup the BeautifulSoup object here
	
	search = "http://www.google.com/search?hl=en&q=" + search_item
	soup = soupify(search)
	
	#retlist will hold the list of dictionary objects containing our search info
	
	retlist = []
	
	# all search results in the main window are stored in list items with
	# class value of 'g'
	
	for item in soup.find_all('li', class_='g'):
		
		# the dictionary that we are going to add to retlist
		
		add_dict = {}
		
		# the header within this list item contains the actual link,
		# along with the link text, which we parse out here
		
		header = item.find('h3', class_='r')
		title = ""
		for child in header.descendants:
			if isinstance(child, NavigableString):
				title += unicode(child)
		
		add_dict['title'] = title
		
		# now we have the 'title' text (what appears as a link on Google
		# Next, we will retrieve the actual link
		
		uncleaned_link = header.find('a').get('href')
		interest_start = uncleaned_link.find('q=htt')
		clean_link = ""
		
		# there's a chached or otherwise embedded link somewhere in there
		
		if interest_start > 0:
			interest_end = uncleaned_link.find('&', interest_start)
			clean_link = uncleaned_link[interest_start+2:interest_end]
		else:
			clean_link = "http://www.google.com" + uncleaned_link
		
		add_dict['title_link'] = clean_link
		
		# ok, so now we have the link of interest, as well as the title of 
		# that link, we can move on to storing link descriptions
		
		description = ''
		
		outer = item.find('div', class_='s')
		if outer:
			inner = outer.find('span', class_='st')
			for child in inner.descendants:
				if isinstance(child, NavigableString):
					description += unicode(child)
		
		description = re.sub(r'\s+?',' ',description)
		
		add_dict['description'] = description
		
		# append this item's dictionary to retlist
		
		retlist.append(add_dict)
		
	return retlist


def get_reddit(subreddit=""):
	
	"""
	This function will return a list of dictionary objects containing
	information from the website reddit.com. The default function call,
	get_reddit(), will return the contents of the frontpage. The function also
	takes a 'subreddit' argument, which can specify from which subreddit to
	pull content. Default value is "", which results in a scrape of the
	frontpage of reddit.com.
	
	Returns a list of dictionary objects of the following structure:
	{
		'type': media || non-media (possibilities for further development)
		'thumbnail_link': link to thumbnail image, or None
		'title': Post title text or None
		'title_link': Post link or None
	}
	"""
	
	# notes on reddit layout:
	# Each post thumbnail within an <a class="thumbnail" ... > tag
	#	img tag direct child of this link
	# Each title / description within a <div class="entry-unvoted" ... > tag
	#	<p class="title"> ==>  <a class="title" tabindex="#"> TITLE </a>
	# Maybe draw info from the comments of each link eventually, comments are linked
	# to through entry-unvoted div
	#	==> <ul class="flat-list buttons"> ==>  <li class="first"> 
	#						==> <a class="comments">
	
	# setup the BeautifulSoup object here
	
	add = ""
	if len(subreddit) > 0:
		add = "/r/" + subreddit
	
	soup = soupify("http://www.reddit.com/" + add)
	
	#retlist will hold the list of dictionary objects containing our search info
	
	retlist = []
	
	# each of the items displayed on the front page (or any page) are stored in divs
	
	for result in soup.find_all('div'):
		
		# instantiate the dictionary for this result, which we will append to the
		# retlist at the end of this for loop
		
		add_dict = {}
		
		# Each of the result divs appears to have multiple classes. 'thing' and
		# 'link' appear to be in each one of them. This seems to work running
		# locally
		
		if result.get('class') and 'thing' in result.get('class') and 'link' in result.get('class'):
			
			# Finding the thumbnail image associated with the result, or return 'none'
			# if there is no thumbnail image associated
			
			if result.find('a',class_='thumbnail'):
				link = result.find('a',class_='thumbnail')
				add_dict["type"] = 'media'
				if link.find('img'):
					add_dict["thumbnail_link"] = link.find('img').get('src')
				else:
					add_dict["thumbnail_link"] = None
			
			# If there is no thumbnail link at all, then we tag the link as 'non-
			# media, and store 'none' for the thumbnail link
			
			else:
				add_dict["type"] = 'non-media'
				add_dict["thumbnail_link"] = None
			
			# Finding the title of the entry, and retrieving its conents.
			
			for div in result.find_all('div'):
				if div.get('class') and 'entry' in div.get('class'):
					add_dict["title"] = div.find('a',class_='title').string
					link_new = div.find('a',class_='title').get('href')
					add_dict["link"] = clean_link(link_new, "http://www.reddit.com")
			if 'link' not in add_dict:
				add_dict["link"] = None
			if 'title' not in add_dict:
				add_dict["title"] = None
			retlist.append(add_dict)
	
	return retlist
