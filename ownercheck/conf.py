# Types of verification checks possible
CHECK_TYPES = ['CNAME', 'TXT', 'METATAG', 'FILE']

# The CNAME value that the user has to set if using CNAME verification
CNAME_VALUE = 'verify007dada.fallible.co'

# The name of the meta tag the user has to create
META_TAG_NAME = 'fallible'

# Refer db.py
SQLITE_TABLE = 'fa-ownercheck.db'

# Some websites do not respond properly without appearing as browsers
FAKE_USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0'
