try:
    from HTMLParser import HTMLParser
    from urlparse import urlparse
except ImportError:
    from html.parser import HTMLParser
    from urllib.parse import urlparse


import requests


class MobileAppLinksParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.app_links = set([])

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'a' and 'href' in attrs:
            parsed_url = urlparse(attrs['href'])
            if parsed_url.netloc == 'play.google.com':
                self.app_links.add((attrs['href'], 'Android'))
            elif parsed_url.netloc == 'itunes.apple.com':
                self.app_links.add((attrs['href'], 'iOS'))


class AllLinksParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.links = set([])

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'a' and 'href' in attrs:
            self.links.add(attrs['href'])


class InvalidAppStoreURL(Exception):
    pass


def verify_app(appstore_url, domain):
    parsed_url = urlparse(appstore_url)
    app_store = None
    if parsed_url.netloc == 'play.google.com':
        app_store = 'Android'
    elif parsed_url.netloc == 'itunes.apple.com':
        app_store = 'iOS'
    else:
        raise InvalidAppStoreURL()

    parser = AllLinksParser()
    r = requests.get(appstore_url)
    parser.feed(r.text)

    for i in parser.links:
        if app_store == 'Android' and urlparse(i).netloc == 'www.google.com':
            try:
                # Google Play store has the developer website as a query param
                page_domain = urlparse(
                    urlparse(i).query.split('&')[0].split('=')[1]).netloc
                if page_domain == domain:
                    return True
            except:
                pass
        else:
            if urlparse(i).netloc == domain:
                return True
    return False


def fetch_apps(url):
    r = requests.get(url)
    parser = MobileAppLinksParser()
    parser.feed(r.text)
    return list(parser.app_links)
