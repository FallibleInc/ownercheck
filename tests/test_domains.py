import io
import uuid
import subprocess
import responses
from ownercheck.domains import (_verify_cname,
								_verify_txt_record,
								_verify_meta_tag,
								_verify_file_exists,
								verify_domain)
from ownercheck.db import generate_code
from .conf import TEST_DOMAIN



def test_verify_cname():
	p = subprocess.Popen(['host', '-t', 'CNAME', 'developers.google.com'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	out, err = p.communicate()
	expected = str(out).split(' ')[-1].strip()
	if expected.endswith("'"):
		expected = expected.rstrip("'")
	if expected.endswith("\\n"):
		expected = expected[:-2]
	print(expected)
	assert _verify_cname('developers.google.com', expected) == True
	assert _verify_cname('developers.google.com', str(uuid.uuid4())) == False


def test_verify_txt_record():
	p = subprocess.Popen(['host', '-t', 'TXT', 'google.com'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	out, err = p.communicate()
	expected = None
	try:
		expected = str(out).split('"')[-2].strip()
	except:
		pass
	assert _verify_txt_record("google.com", expected) == True
	assert _verify_txt_record("google.com", str(uuid.uuid4())) == False


@responses.activate
def test_verify_meta_tag():
	responses.add(responses.GET,
				  'http://' + TEST_DOMAIN,
                  body=io.open('tests/data/google.web.html', encoding='utf-8').read(),
                  status=200,
                  content_type='text/html')
	assert _verify_meta_tag(TEST_DOMAIN, "origin", "referrer") == True
	assert _verify_meta_tag(TEST_DOMAIN, str(uuid.uuid4()), "fallible") == False


@responses.activate
def test_verify_file_exists():
	responses.add(responses.GET,
				  'http://' + TEST_DOMAIN + '/robots.txt',
                  body='',
                  status=200,
                  content_type='text/html')
	random_str = str(uuid.uuid4())
	responses.add(responses.GET,
				  'http://' + TEST_DOMAIN + '/' + random_str,
                  body='',
                  status=404,
                  content_type='text/html')
	assert _verify_file_exists(TEST_DOMAIN, "robots.txt") == True
	assert _verify_file_exists(TEST_DOMAIN, random_str) == False


def test_verify_domain():
	pass


