__filename__ = "password.py"
__author__ = "Chris Byrd"
__credits__ = ["Chris Byrd"]
__license__ = "MIT"
__version__ = "0.6.6"
__maintainer__ = "Bartek Radwanski"
__email__ = "bartek.radwanski@gmail.com"
__status__ = "Stable"

"""Password hashing and authentication logic for DUM server."""

import binascii
import hashlib
import os


def hash_password(pwd):
    """Hash and return salted password.

    Args:
        pwd {string}

    Returns:
        string password hash
    """
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')

    _hash = hashlib.pbkdf2_hmac('sha512', pwd.encode('utf-8'), salt, 100000)
    _hash = binascii.hexlify(_hash)

    return (salt + _hash).decode('ascii')


def check_password(stored, provided):
    """Check that the provided password matches what we have for the user.

    Args:
        pwd {string}

    Returns:
        True if user authenticate, else False
    """
    salt = stored[:64]
    _pwd = stored[64:]

    _hash = hashlib.pbkdf2_hmac('sha512', provided.encode('utf-8'), salt.encode('ascii'), 100000)
    _hash = binascii.hexlify(_hash).decode('ascii')

    return _hash == _pwd

