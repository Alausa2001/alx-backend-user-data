#!/usr/bin/env python3
"""
Implememt basic authentication
"""
import base64
from api.v1.auth.auth import Auth
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """
    Basic authentication
    """

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
        returns the Base64 part of the
        Authorization header for a Basic Authentication
        """
        if not authorization_header or type(authorization_header) is not str:
            return None
        if authorization_header[:6] != 'Basic ':
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(self, base64_authorization_header:
                                           str) -> str:
        """
        returns the decoded value of a Base64 string
        base64_authorization_header
        """
        if not base64_authorization_header:
            return None
        if type(base64_authorization_header) is not str:
            return None
        try:
            credential = base64.standard_b64decode(base64_authorization_header)
            return credential.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header:
                                 str) -> (str, str):
        """
         returns the user email and password from the Base64 decoded value.
        """
        if decoded_base64_authorization_header is None:
            return None, None
        if type(decoded_base64_authorization_header) is not str:
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        col_idx = decoded_base64_authorization_header.find(':')
        if col_idx > 0:
            email = decoded_base64_authorization_header[:col_idx]
            pwd = decoded_base64_authorization_header[col_idx + 1:]
            return email, pwd

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """
        returns the User instance based on his email and password
        """
        if not user_email or type(user_email) is not str:
            return None
        if not user_pwd or type(user_pwd) is not str:
            return None
        try:
            User.load_from_file()
            users_with_mail = User.search({'email': user_email})

            if not users_with_mail:
                return None

            if users_with_mail:
                for user in users_with_mail:
                    if user.is_valid_password(user_pwd):
                        return user
                return None

        except FileNotFoundError:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        complete Basic authentication.
        """
        auth_header = self.authorization_header(request)
        encoded_credential = \
            self.extract_base64_authorization_header(auth_header)
        credentials = \
            self.decode_base64_authorization_header(encoded_credential)
        email, pwd = self.extract_user_credentials(credentials)
        return self.user_object_from_credentials(email, pwd)
