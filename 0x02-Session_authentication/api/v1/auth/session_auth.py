#!/usr/bin/env python3
"""
session authentication
"""
from api.v1.auth.auth import Auth
import uuid


class SessionAuth(Auth):
    """
    This class implements the session authentication for the API
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        creates a Session ID for a user_id
        """
        if user_id is None or type(user_id) is not str:
            return None
        else:
            self.session_id = str(uuid.uuid4())
            self.user_id_by_session_id[self.session_id] = user_id
        return self.session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        retrieving a User ID based on the Session ID and subsequently
        retrieving a user.
        """
        if session_id is None or type(session_id) is not str:
            return None
        else:
            return self.user_id_by_session_id.get(session_id)

