from HTMLParser import HTMLParser
import requests
import dns.resolver
import db
from conf import CHECK_TYPES, CNAME_VALUE, META_TAG_NAME


db.init()


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
    except dns.resolver.NoAnswer:
        return False
    except dns.resolver.Timeout:
        return False
    return False


class MetaTagParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.value = None

    def handle_starttag(self, tag, attrs):
        if tag.lower() == 'meta':
            found_tag = False
            for attribute in attrs:
                if attribute[0] == 'name' and attribute[1] == META_TAG_NAME:
                    found_tag = True
                if found_tag and attribute[0] == 'content':
                    self.value = attribute[1]


def _verify_meta_tag(domain, expected_value, tag=META_TAG_NAME):
    r = requests.get('http://' + domain)
    text = r.text
    parser = MetaTagParser()
    parser.feed(text)
    if parser.value == expected_value:
        return True
    else:
        return False


def _verify_file_exists(domain, filename):
    r = requests.get('/'.join(['http:/', domain, filename]))
    if 200 <= r.status_code < 300:
        return True
    else:
        return False


def verify_domain(domain, check_type):
    code = db.get_code(domain, check_type)

    if check_type not in CHECK_TYPES:
        raise InvalidVerificationType(
            '%s not in %s' % (check_type, str(CHECK_TYPES)))

    if code is None:
        raise NoVerificationCodeExists(
            'No verification code found for %s'
            % str((domain, check_type)))

    if check_type == 'CNAME':
        return _verify_cname(code)
    elif check_type == 'TXT':
        return _verify_txt_record(domain, code)
    elif check_type == 'METATAG':
        return _verify_meta_tag(domain, code)
    elif check_type == 'FILE':
        _verify_file_exists(domain, code)
