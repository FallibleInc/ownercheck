import re
from ownercheck.apps import verify_app, fetch_apps
import responses

IOS_URL = 'https://itunes.apple.com/in/app/twitter/id333903271?mt=8'
ANDROID_URL = 'https://play.google.com/store/apps/details?id=com.twitter.android&hl=en'

WEB_URL = 'https://snapchat.com'


@responses.activate
def test_fetch_apps():
	responses.add(responses.GET,
				  WEB_URL,
                  body=open('data/snapchat.web.html').read(),
                  status=200,
                  content_type='text/html')
	assert len(fetch_apps(WEB_URL)) == 2
	app_types = [i[1] for i in fetch_apps(WEB_URL)]
	app_types.sort()
	assert app_types == ['Android', 'iOS']


@responses.activate
def test_verify_app():
	responses.add(responses.GET,
				  ANDROID_URL,
                  body=open('data/twitter.android.html').read(),
                  status=200,
                  content_type='text/html')
	responses.add(responses.GET,
				  IOS_URL,
                  body=open('data/twitter.ios.html').read(),
                  status=200,
                  content_type='text/html')
	assert verify_app(ANDROID_URL, 'twitter.com') == True
	assert verify_app(IOS_URL, 'twitter.com') == True

