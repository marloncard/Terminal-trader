#!/usr/bin/env python3
"""
To execute from base of project directory run: 
python3 -m unittest tests/testUser.py
To run all tests run: 
python3 -m unittest tests discover

Test becomes a museum of all bugs you've fixed
hw: in ORM, implement create_update and write a unittest
"""
from model.user import User
from unittest import TestCase
from schema import build_user

class TestUser(TestCase):
    
    def setUp(self):
        build_user()

        mike = User(**{
        "user_name": "mikebloom",
        "password": "password",
        "real_name": "Mike Bloom",
        "balance": 10000.0
        })

        mike.save()

    def tearDown(self):
        pass

    def testFromPk(self):
        mike = User.frompk(1)
        self.assertEqual(mike.real_name, "Mike Bloom",
            "Lookup from pk populates instance properties.")

    def testsavePk(self):
        # Test that pk is defined after a save
        greg = User(**{
            "username": "gregcoin",
            "realname": "Greg Smith",
            "balance": 200.0,
            "password": 12345
        })
        self.assertIsNone(greg.pk, 
            "pk value of new instance initializes to None")

        greg.save()

        self.assertGreater(greg.pk, 1,
            "pk is set after first save")

    def testSaveUpdate(self):
        mike = User.frompk(1)
        oldpk = mike.pk

        mike.balance = 0.0
        mike.save()

        self.assertEqual(mike.pk, oldpk,
            "pk does not change after save of existing row")

        mikeagain = User.frompk(1)
        self.assertAlmostEqual(mikeagain.balance, 0.0,
            "Updated properties saved to database and reloaded")

    def testInsert(self):
        Bob = User(**{
            "username": "Bigbob",
            "realname": "Robert Reeves",
            "balance": 10_000_000.0,
            "password": "1234rT$5"
        })
        