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
        checks if route requires authentication
        """
        if path is None or excluded_paths is None:
            return True

        for excluded_path in excluded_paths:
            if '*' in excluded_path:
                if path.startswith(excluded_path.replace('*', '')):
                    return False

        if path[-1] == '/':
            path = path
        else:
            path = path + '/'
        if path not in excluded_paths:
            return True
        return False

    def authorization_header(self, request=None) -> str:
        """
        returns the authorization credentials
        """
        if not request:
            return None
        else:
            return request.headers.get('Authorization', None)

    def current_user(self, request=None) -> TypeVar('User'):
        """
        yet to be implemented
        """
        return None
