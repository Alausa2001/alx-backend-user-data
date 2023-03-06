#!/usr/bin/env python3
"""
Implememt basic authentication
"""
import base64
from api.v1.auth.auth import Auth


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
