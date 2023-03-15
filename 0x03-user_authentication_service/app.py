#!/usr/bin/env python3
"""
Flask app
"""
from sqlalchemy.orm.exc import NoResultFound
from flask import url_for, redirect
from flask import Flask, jsonify, request, abort, make_response
from auth import Auth


AUTH = Auth()

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR']


@app.route('/', strict_slashes=False)
def welcome():
    """
    Welcome greetings
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users():
    """
    """
    email = request.form['email']
    password = request.form['password']
    # credentials = {'email': email, 'hashed_password': password}

    try:
        new_user = AUTH.register_user(email, password)
        return jsonify({"email": f"{email}", "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def user_session():
    """
    creates a new user session
    """
    email = request.form['email']
    password = request.form['password']

    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        response = make_response(jsonify({"email": f"{email}",
                                          "message": "logged in"}))
        response.set_cookie('session_id', session_id)
        return response
    else:
        abort(401)


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """
    delete a user session
    """
    session_id = request.cookies.get('session_id')
    if session_id:
        user = AUTH.get_user_from_session_id(session_id)
        if not user:
            abort(403)
        AUTH.destroy_session(user.id)
        return redirect(url_for('welcome'))
    abort(403)


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile():
    """
    checks if a session_id is still on for a user
    """
    session_id = request.cookies.get('session_id')
    if session_id:
        user = AUTH.get_user_from_session_id(session_id)
        if user:
            return jsonify({"email": f"{user.email}"})
    abort(403)


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token():
    """
    reset password
    """
    email = request.form['email']
    try:
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({
            "email": f"{email}",
            "reset_token": f"{reset_token}"
            })
    except Exception:
        abort(403)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")
