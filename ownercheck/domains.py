try:
    from HTMLParser import HTMLParser
except ImportError:
    from html.parser import HTMLParser
import requests
import dns.resolver
from .db import setup_db, get_code
from .conf import CHECK_TYPES, CNAME_VALUE, META_TAG_NAME, FAKE_USER_AGENT


# Create db tables if not already created
setup_db()


class InvalidVerificationType(Exception):
    pass


class NoVerificationCodeExists(Exception):
    pass


def _verify_cname(subdomain, expected_value=CNAME_VALUE):
    try:
        records = dns.resolver.query(subdomain, 'CNAME')
        record = records[0].to_text()
        if record.endswith('.'):
            record = record[:-1]
        if expected_value.endswith('.'):
            expected_value = expected_value[:-1]
        if record == expected_value:
            return True
    except dns.resolver.NoAnswer:
        return False
    except dns.resolver.Timeout:
        return False
    return False


def _verify_txt_record(domain, expected_value):
    try:
        records = dns.resolver.query(domain, 'TXT')
        for r in records:
            record = r.to_text()
            if record.startswith('"') and record.endswith('"'):
                record = record[1:-1]
            if record == expected_value:
                return True
    except (dns.resolver.NoAnswer, dns.resolver.Timeout):
        return False
    return False


class MetaTagParser(HTMLParser):
    """
        Given a meta tag name, saves it's content in value
    """

    def __init__(self, meta_tag_name):
        HTMLParser.__init__(self)
        self.value = None
        self.tag_name = meta_tag_name

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag.lower() == 'meta' and attrs.get('name') == self.tag_name:
            self.value = attrs['content']


def _verify_meta_tag(domain, expected_value, tag=META_TAG_NAME):
    r = requests.get(
        'http://' + domain,
        headers={
            'User-Agent': FAKE_USER_AGENT})
    text = r.text
    parser = MetaTagParser(tag)
    parser.feed(text)
    return bool(parser.value == expected_value)


def _verify_file_exists(domain, filename):
    r = requests.get('/'.join(['http:/', domain, filename]))
    return bool(200 <= r.status_code < 300)


def verify_domain(domain, check_type):
    code = get_code(domain, check_type)

    if check_type not in CHECK_TYPES:
        raise InvalidVerificationType(
            '%s not in %s' % (check_type, str(CHECK_TYPES)))

    if code is None:
        raise NoVerificationCodeExists(
            'No verification code found for %s'
            % str((domain, check_type)))

    response = False

    if check_type == 'CNAME':
        response = _verify_cname(code)
    elif check_type == 'TXT':
        response = _verify_txt_record(domain, code)
    elif check_type == 'METATAG':
        response = _verify_meta_tag(domain, code)
    elif check_type == 'FILE':
        response = _verify_file_exists(domain, code)

    return response
