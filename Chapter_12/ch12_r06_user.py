"""Python Cookbook

Chapter 12, recipe 6, Implementing authentication for web services
Server-side model for the user and their credentials.
"""
import base64
from dataclasses import dataclass, field, asdict
import hashlib
import os
import re
import secrets
import string
from typing import Optional, cast, Match
from werkzeug.security import generate_password_hash, check_password_hash

# Typical implementation. Lacks constant-time guarantees.
# Shows concept only.

DIGEST = "sha384"
ROUNDS = 100_000
SALT_SIZE = 30

def make_hash(password: str) -> str:
    """Set password to a hash of supplied password."""
    alphabet = string.ascii_letters + string.digits
    salt = bytes(
        ord(secrets.choice(alphabet))
        for _ in range(SALT_SIZE))
    hash = hashlib.pbkdf2_hmac(
        DIGEST, password.encode("utf-8"), salt, ROUNDS
    )
    return "$".join(
        [
            f"pbkdf2:{DIGEST}:{ROUNDS}",
            salt.decode("ascii"),
            hash.hex(),
        ]
    )

def check_hash(hash: str, password: str) -> bool:
    """Does the supplied password recreate the expected hash?"""
    method, salt_text, hex_expected_hash = hash.split("$")
    salt = salt_text.encode("ASCII")
    expected_hash = bytes.fromhex(hex_expected_hash)
    method_detail = re.compile(
        r"pbkdf2:([^:]+):(\d+)|pbkdf2:([^:]+)"
    )
    if details := method_detail.match(method):
        details = cast(Match, details)
        if details.group(1) is not None:
            digest = details.group(1)
            rounds = int(details.group(2))
        else:
            digest = details.group(3)
            rounds = ROUNDS

        computed_hash = hashlib.pbkdf2_hmac(
            digest, password.encode("utf-8"), salt, rounds
        )
        return computed_hash == expected_hash
    else:
        hasher = hashlib.new(method)
        hasher.update(salt)
        hasher.update(password.encode("utf-8"))
        computed_hash = hasher.digest()
        return computed_hash == expected_hash


@dataclass
class User:
    """
    An individual user's information and a hash of their password.

    If password is omitted, a default is created that can never
    be matched.

    >>> details = {'name': 'Noriko',
    ...      'email': 'x@example.com',
    ...      'lucky_number': 8,
    ...      'twitter': 'https://twitter.com/PacktPub'}
    >>> u = User(**details)
    >>> u.set_password('OpenSesame')
    >>> u.check_password('opensesame')
    False
    >>> u.check_password('OpenSesame')
    True

    >>> from pprint import pprint
    >>> db_row = asdict(u)
    >>> pprint(db_row)  # doctest: +ELLIPSIS
    {'email': 'x@example.com',
     'lucky_number': 8,
     'name': 'Noriko',
     'password': 'pbkdf2:sha256:...',
     'twitter': 'https://twitter.com/PacktPub'}
    >>> u2 = User(**db_row)
    >>> u.check_password('opensesame')
    False
    >>> u.check_password('OpenSesame')
    True

    >>> default_def = {'name': '', 'email': '', 'lucky_number': -1, 'twitter': ''}
    >>> default_user = User(**default_def)
    >>> default_user.check_password('')
    False
    >>> default_user.check_password('md5$x$')
    False
    """

    name: str
    email: str
    twitter: str
    lucky_number: int
    password: Optional[str] = field(default="md5$x$", repr=False)

    def set_password(self, password: str) -> None:
        # self.password = make_hash(password)
        self.password = generate_password_hash(
            password
        )

    def check_password(self, password: str) -> bool:
        # return check_hash(self.password, password)
        return check_password_hash(
            self.password, password)

test_v_werkzeug = """
>>> mp = make_hash("OpenSesame")
>>> mp  # doctest: +ELLIPSIS
'pbkdf2:sha384:100000$...
>>> wp = generate_password_hash("OpenSesame")
>>> wp  # doctest: +ELLIPSIS
'pbkdf2:sha256:150000$...
>>> check_password_hash(mp, "nope")
False
>>> check_password_hash(mp, "OpenSesame")
True
>>> check_hash(wp, "nope")
False
>>> check_hash(wp, "OpenSesame")
True
"""

__test__ = {n: v for n, v in locals().items() if n.startswith("test_")}
