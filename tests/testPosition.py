#!/usr/bin/env python3
"""
To execute from base of project directory run: 
python3 -m unittest tests/testUser.py
To run all tests run: 
python3 -m unittest tests discover
"""
from model.user import User
from model.position import Position
from unittest import TestCase
from schema import build_user, build_positions


class TestPosition(TestCase):

    def setUp(self):
        build_user()
        build_positions()

        mike = User(**{
            "user_name": "mikebloom",
            "real_name": "Mike Bloom",
            "balance": 10000.0
        })
        mike.hash_password("password")
        mike.save()

        aapl = Position(**{
            "ticker": "aapl",
            "amount": 5,
            "user_info_pk": mike.pk
        })
        tsla = Position(**{
            "ticker": "tsla",
            "amount": 10,
            "user_info_pk": mike.pk
        })
        aapl.save()
        tsla.save()

    def teardown(self):
        pass

    def testDummy(self):
        pass

    def testOneWhere(self):
        pass

    def testSave(self):
        pass

    def testAllPositions(self):
        mike = User.from_pk(1)
        positions = mike.all_positions()
        self.assertIsInstance(positions, list, "all positions returns a list")
        firstposition = positions[0]
        self.assertIsInstance(firstposition, Position, "Return is a list of Positions")

    def testPosition(self):
        mike = User.from_pk(1)
        position = mike.positions_for_stock("aapl")
        self.assertIsInstance(position, Position, "PFS returns Position object")
