#!/usr/bin/env python3
"""
class to manage the API authentication.
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """
    Authentication class
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        yet to be implemented
        """
        return False

    def authorization_header(self, request=None) -> str:
        """
        yet to be implemented
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        yet to be implemented
        """
        return None
