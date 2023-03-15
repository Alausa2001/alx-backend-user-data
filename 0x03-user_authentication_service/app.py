#!/usr/bin/env python3
"""
Flask app
"""
# from sqlalchemy.orm.exc import NoResultFound
from flask import Flask, jsonify, request
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
    credentials = {'email': email, 'hashed_password': password}

    try:
        new_user = AUTH.register_user(email, password)
        return jsonify({"email": f"{email}", "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")
