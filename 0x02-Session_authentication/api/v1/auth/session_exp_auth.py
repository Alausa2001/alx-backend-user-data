#!/usr/bin/env python3
"""
Actually you have 2 authentication systems:

    Basic authentication
    Session authentication
    Now you will add an expiration date to a Session ID.
"""
import os
from datetime import datetime, timedelta
from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """
    implement a session autentication where
    the session id has an expiration time
    """
    user_id_by_session_id = {}
    session_dict = {}

    def __init__(self):
        """
        overloads SessionAuth __init__
        """
        try:
            duration = int(os.getenv('SESSION_DURATION'))
            if duration:
                self.session_duration = duration
            else:
                self.session_duration = 0
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """
        create a session id
        """
        # self.user_id_by_session_id = {}
        # self.session_dict = {}

        self.session_id = super().create_session(user_id)
        if not self.session_id:
            return None

        self.session_dict['user_id'] = user_id
        self.session_dict['created_at'] = datetime.now()
        self.user_id_by_session_id[self.session_id] = self.session_dict
        return self.session_id

    def user_id_for_session_id(self, session_id=None):
        """
        returns a user_id related to a session id
        provided the session is has not expired
        """
        if not session_id:
            return None
        if self.user_id_by_session_id.get(session_id) is None:
            return None
        if self.session_duration <= 0:
            for key in self.session_dict.keys():
                if key == 'user_id':
                    return key
        if self.session_dict.get('created_at') is None:
            return None

        created_at = self.session_dict.get('created_at')
        expire_time = created_at + timedelta(seconds=self.session_duration)
        if expire_time < datetime.now():
            return None
        return self.session_dict.get('user_id')
