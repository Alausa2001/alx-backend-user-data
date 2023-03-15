#!/usr/bin/env python3
"""
In this task you will define a _hash_password method
that takes in a password string arguments and returns bytes.

The returned bytes is a salted hash of the input password,
hashed with bcrypt.hashpw.
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """
    hashes a paaaword
    """
    password = password.encode('utf-8')
    return bcrypt.hashpw(password, bcrypt.gensalt())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """

        """
        try:
            user_exist = self._db.find_user_by(email=email)
        except NoResultFound:
            hashed_password = _hash_password(password)
            new_user = self._db.add_user(email=email,
                                         hashed_password=hashed_password)
            return new_user
        if user_exist:
            raise ValueError("User {} already exists".format(email))
