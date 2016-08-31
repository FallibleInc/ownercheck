from HTMLParser import HTMLParser
import urlparse
import requests


class MobileAppLinksParser(HTMLParser):
	
	def __init__(self):
		HTMLParser.__init__(self)
		self.app_links = set([])

	def handle_starttag(self, tag, attrs):
		if tag == 'a':
			for attr in attrs:
				if attr[0] == 'href':
					parsed_url = urlparse.urlparse(attr[1])
					if parsed_url.netloc == 'play.google.com':
						self.app_links.add((attr[1], 'Android'))
					elif parsed_url.netloc == 'itunes.apple.com':
						self.app_links.add((attr[1], 'iOS'))


class AllLinksParser(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self.links = set([])

	def handle_starttag(self, tag, attrs):
		if tag == 'a':
			for attr in attrs:
				if attr[0] == 'href':
					self.links.add(attr[1])



class InvalidAppStoreURL(Exception):
	pass


def verify_app(appstore_url, domain):
	parsed_url = urlparse.urlparse(appstore_url)
	app_store = None
	if parsed_url.netloc == 'play.google.com':
		app_store = 'Android'
	elif parsed_url.netloc ==  'itunes.apple.com':
		app_store = 'iOS'
	else:
		raise InvalidAppStoreURL()

	parser = AllLinksParser()
	r = requests.get(appstore_url)
	parser.feed(r.text)

	for i in parser.links:
		if app_store == 'Android':
			if urlparse.urlparse(i).netloc == 'www.google.com':
				try:
					page_domain = urlparse.urlparse(urlparse.urlparse(i).query.split('&')[0].split('=')[1]).netloc
					if page_domain == domain:
						return True
				except:
					pass
		else:
			if urlparse.urlparse(i).netloc == domain:
				return True
	return False


def fetch_apps(url):
	r = requests.get(url)
	parser = MobileAppLinksParser()
	parser.feed(r.text)
	return list(parser.app_links)



