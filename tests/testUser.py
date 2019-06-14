#!/usr/bin/env python3
"""
To execute from base of project directory run: 
python3 -m unittest tests/testUser.py
To run all tests run: 
python3 -m unittest tests discover
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
        mike.hash_password("password")
        mike.save()

    def tearDown(self):
        pass

    def testFromPk(self):
        mike = User.from_pk(1)
        self.assertEqual(mike.real_name, "Mike Bloom",
            "Lookup from pk populates instance properties.")

    def testSavePk(self):
        # Test that pk is defined after a save
        greg = User(**{
            "user_name": "gregcoin",
            "real_name": "Greg Smith",
            "balance": 200.0,
            "password": "12345"
        })
        self.assertIsNone(greg.pk, 
            "pk value of new instance initializes to None")

        greg.save()

        self.assertGreater(greg.pk, 1,
            "pk is set after first save")

    def testSaveUpdate(self):
        mike = User.from_pk(1)
        oldpk = mike.pk

        mike.balance = 0.0
        mike.save()

        self.assertEqual(mike.pk, oldpk,
            "pk does not change after save of existing row")

        mikeagain = User.from_pk(1)
        self.assertAlmostEqual(mikeagain.balance, 0.0,
            "Updated properties saved to database and reloaded")


    def testOneWhere(self):
        mike = User.one_where("user_name=?", ('mikebloom',))
        self.assertIsNotNone(mike, "Query does not return None when row is found")
        self.assertEqual(mike.real_name, "Mike Bloom",
        "Object returned has correct properties")

    def testManyWhere(self):
        mike = User.many_where("user_name=?", ('mikebloom',))
        self.assertIsInstance(mike, list, "Many where returns a list")
        self.assertEqual(len(mike), 1,"list is 1 element")
        self.assertEqual(mike[0].real_name, "Mike Bloom", "All retrieves correct data")

    def testAll(self):
        mike = User.all()
        self.assertIsInstance(mike, list, "All returns a list")
        self.assertEqual(len(mike), 1, "List is 1 element")
        self.assertEqual(mike[0].real_name, "Mike Bloom", "many_where retrieves correct data")

    def testDelete(self):
        mike = User.from_pk(1)
        mike.delete()
        self.assertIsNone(mike.pk, "delete should set pk to None")
        secondmike = User.from_pk(1)
        self.assertIsNone(secondmike, ".delete removes row from db")

    def testLogin(self):
        notauser = User.login("carter", "notmypassword")
        self.assertIsNone(notauser, "bad credentials return the None object")

        mike = User.login("mikebloom", "password")
        self.assertEqual(mike.real_name, "Mike Bloom", "good credentials retrieve User object")