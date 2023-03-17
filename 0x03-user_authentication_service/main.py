#!/usr/bin/env python3
"""
End-to-end integration test
"""
import requests


def register_user(email: str, password: str) -> None:
    """
    Test endpoint that registers a user
    """
    user = {'email': email, 'password': password}
    res = requests.post('http://localhost:5000/users', data=user)
    if res.status_code != 200:
        assert res.json() == {"message": "email already registered"}
    else:
        assert res.status_code == 200
        assert res.json() == {"email": f"{email}", "message": "user created"}


def log_in_wrong_password(email: str, password: str) -> None:
    """
    Test log in with wrong pwd
    """
    user = {'email': email, 'password': password}
    response = requests.post('http://localhost:5000/sessions', data=user)
    assert response.status_code == 401
    # print(response)


def profile_unlogged() -> None:
    """
    Test forunlogged profile
    """
    response = requests.get('http://localhost:5000/profile')
    session_id = response.cookies.get('session_id')
    if session_id is None:
        assert response.status_code == 403
    # print(response.status_code)


"""
def log_in(email: str, password: str) -> str:
    ""
    Test user login with correct credentials
    ""
    user = {'email': email, 'password': password}
    response = requests.post('http://localhost:5000/sessions', data=user)
    assert response.status_code != 200
    assert response.json() == {"email": "{email}", "message": "logged in"}
    return response.cookies.get('session_id')
"""


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    # session_id = log_in(EMAIL, NEW_PASSWD)
