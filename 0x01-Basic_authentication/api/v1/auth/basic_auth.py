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
