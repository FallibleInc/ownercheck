"""
If you are using some other database, the functions can be safely
replaced with your own but having the same functionality and interface.
"""

import uuid
import sqlite3
from .conf import SQLITE_TABLE


def setup_db():
    conn = sqlite3.connect(SQLITE_TABLE)
    cursor = conn.cursor()
    try:
        cursor.execute('''
			CREATE TABLE codes
             (domain text, checktype text, value text)''')
        conn.commit()
    except:
        pass
    finally:
        conn.close()


def generate_code(domain, check_type):
    current_code = get_code(domain, check_type)
    if current_code is not None:
        return current_code
    uid = str(uuid.uuid4())
    conn = sqlite3.connect(SQLITE_TABLE)
    c = conn.cursor()
    c.execute('''
		INSERT INTO codes
		VALUES(?, ?, ?)''',
              (domain, check_type, uid))
    conn.commit()
    conn.close()
    return uid


def get_code(domain, check_type):
    conn = sqlite3.connect(SQLITE_TABLE)
    cursor = conn.cursor()
    cursor.execute('''
			   SELECT value FROM codes
			   WHERE domain=? AND checktype=?''',
                   (domain, check_type))
    row = cursor.fetchone()
    if row is not None:
        return row[0]
    else:
        return None


def remove_code(domain, check_type):
    conn = sqlite3.connect(SQLITE_TABLE)
    cursor = conn.cursor()
    cursor.execute('''
    	DELETE FROM codes WHERE domain=? AND checktype=?''',
                   (domain, check_type))
    conn.commit()
    conn.close()
