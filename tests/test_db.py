from ownercheck.db import setup_db, generate_code, get_code, remove_code
from .conf import TEST_DOMAIN


def test_generate_code():
    setup_db()
    assert generate_code(TEST_DOMAIN, 'TXT') != None
    assert generate_code(TEST_DOMAIN, 'TXT') != generate_code(
        TEST_DOMAIN, 'CNAME')
    assert generate_code(TEST_DOMAIN, 'TXT') == generate_code(
        TEST_DOMAIN, 'TXT')


def test_get_code():
    setup_db()
    code = generate_code(TEST_DOMAIN, 'FILE')
    assert get_code(TEST_DOMAIN, 'FILE') == code
    assert get_code(TEST_DOMAIN, 'METATAG') == None


def test_remove_code():
    setup_db()
    file_code = generate_code(TEST_DOMAIN, 'FILE')
    cname_code = generate_code(TEST_DOMAIN, 'CNAME')
    remove_code(TEST_DOMAIN, 'FILE')
    new_file_code = generate_code(TEST_DOMAIN, 'FILE')
    new_cname_code = generate_code(TEST_DOMAIN, 'CNAME')
    assert file_code != new_file_code
    assert cname_code == new_cname_code

