import re
import responses
from ownercheck.apps import verify_app, fetch_apps
from conf import IOS_URL, ANDROID_URL, WEB_URL


@responses.activate
def test_fetch_apps():

	responses.add(responses.GET,
				  WEB_URL,
                  body=open('tests/data/snapchat.web.html').read(),
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
                  body=open('tests/data/twitter.android.html').read(),
                  status=200,
                  content_type='text/html',
                  match_querystring=True)
	responses.add(responses.GET,
				  IOS_URL,
                  body=open('tests/data/twitter.ios.html').read(),
                  status=200,
                  content_type='text/html',
                  match_querystring=True)
	assert verify_app(ANDROID_URL, 'twitter.com') == True
	assert verify_app(IOS_URL, 'twitter.com') == True

