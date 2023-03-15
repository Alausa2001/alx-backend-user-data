#!/usr/bin/env python3
"""
Main file
"""
import bcrypt
from auth import _hash_password


pwd = "Heo Holbern"
en = pwd.encode()
hashed = _hash_password(pwd)
print(hashed)

if bcrypt.checkpw(en, hashed):
    print("It matches")
else:
    print("Not a match")

