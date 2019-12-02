"""Python Cookbook

Chapter 12, recipe 7 -- server.

Define the user and their credentials.
"""
import base64
from dataclasses import dataclass, field, asdict
import hashlib
import os
from typing import ClassVar, Optional


@dataclass
class User:
    """
    An individual user's information and a hash of their password.

    If password is omitted, a default is created that can never
    be matched.

    >>> from unittest.mock import Mock, NonCallableMock, patch
    >>> details = {'name': 'Noriko', 'email': 'x@example.com',
    ...     'lucky_number': 8, 'twitter': 'https://twitter.com/PacktPub',
    ...     'password': 'OpenSesame'}
    >>> with patch('Chapter_12.ch12_r07_user.os') as mocked_os:
    ...     mocked_os.urandom=Mock(return_value=bytes(range(30)))
    ...     u = User(**details)
    >>> u.check_password('opensesame')
    False
    >>> u.check_password('OpenSesame')
    True
    >>> u.password
    'sha384$AAECAwQFBgcICQoLDA0ODxAREhMUFRYXGBkaGxwd$CHHs2cBiijhxw9dp-aaTXkpD2IurHbYoPf9aQo2uJGYHhacW7GZCdxQQyVCuuY9w'
    >>> asdict(u)
    {'name': 'Noriko', 'email': 'x@example.com', 'twitter': 'https://twitter.com/PacktPub', 'lucky_number': 8, 'password': 'sha384$AAECAwQFBgcICQoLDA0ODxAREhMUFRYXGBkaGxwd$CHHs2cBiijhxw9dp-aaTXkpD2IurHbYoPf9aQo2uJGYHhacW7GZCdxQQyVCuuY9w'}

    >>> default_def = {'name': '', 'email': '', 'lucky_number': -1, 'twitter': ''}
    >>> with patch('Chapter_12.ch12_r07_user.os') as mocked_os:
    ...     mocked_os.urandom=Mock(return_value=bytes(range(30)))
    ...     u_d = User(**default_def)
    >>> u_d.check_password('')
    False
    >>> u_d.check_password('sha384$$')
    False
    """

    name: str
    email: str
    twitter: str
    lucky_number: int
    password: Optional[str] = field(default=None, repr=False)

    DIGEST: ClassVar = "sha384"
    ROUNDS: ClassVar = 100_000

    def __post_init__(self):
        """Update the user with a hash of their password."""
        if self.password is None:
            # Unmatchable because expected hash is not 48 bytes.
            self.password = "sha384$$"
        else:
            salt = os.urandom(30)
            hash = hashlib.pbkdf2_hmac(
                self.DIGEST, self.password.encode("utf-8"), salt, self.ROUNDS
            )
            self.password = "$".join(
                [
                    self.DIGEST,
                    base64.urlsafe_b64encode(salt).decode("ascii"),
                    base64.urlsafe_b64encode(hash).decode("ascii"),
                ]
            )

    def check_password(self, password: str) -> bool:
        """Does the supplied password recreate the expected hash?"""
        assert self.password, "Failed __post_init__()"
        digest, b64_salt, b64_expected_hash = self.password.split("$")
        salt = base64.urlsafe_b64decode(b64_salt)
        expected_hash = base64.urlsafe_b64decode(b64_expected_hash)
        computed_hash = hashlib.pbkdf2_hmac(
            digest, password.encode("utf-8"), salt, self.ROUNDS
        )
        return computed_hash == expected_hash
