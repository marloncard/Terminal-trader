#!/usr/bin/env python3

import sqlite3
from model import User
from schema import build_user

build_user()

mike = User(**{
    "user_name": "mikebloom",
    "password": "password",
    "real_name": "Mike Bloom",
    "balance": 10000.0
})

assert mike.password == "password"
assert mike.pk is None
mike.save()

user1 = User.frompk(1)
assert user1.user_name == "mikebloom"

user2 = User.frompk(2)
assert user2 is None

mike.password = "12345"
mike.save()

mikeagain = User.frompk(1)
assert mikeagain.password == "12345"

print(mike._create_insert())

print("Test passed")
