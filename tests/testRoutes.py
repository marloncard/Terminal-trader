#!/usr/bin/env python3
"""
Tests for routes
python3 -m unittest tests/testRoutes.py
"""
from unittest import TestCase
from model.user import User
from model.position import Position
from model.trade import Trade
from flask_app.app import app
from schema import build_user, build_positions, build_trades
import json
import os


BASE_URL = 'http://localhost:5000/api/'


class TestRoutes(TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.app = app.test_client()
    
        build_user()
        build_positions()
        build_trades()

        mike = User(**{
        "user_name": "mikebloom",
        "password": "password",
        "real_name": "Mike Bloom",
        "balance": 0.0
        })
        mike.hash_password("password")
        mike.api_key = "11111111111111111111"
        mike.save()

        return app

    def tearDown(self):
        pass

    def test_create_account(self):
        endpoint = 'create_account'
        paul = {
        "user_name": "muadib",
        "real_name": "Paul Muadib",
        "password": "password"}
        response = self.app.post(BASE_URL+endpoint,
                                data=json.dumps(paul),
                                content_type='application/json')
        paul = User.from_pk(2)
        self.assertEqual(response.status_code, 201, "status code should be 201")
        self.assertEqual(paul.user_name, "muadib", "Paul's username should be 'muadib'")

    def test_deposit_route(self):
        endpoint = 'deposit/'
        mike = User.from_pk(1)
        self.assertEqual(mike.user_name, "mikebloom")
        deposit = {"amount":1500.0}
        response = self.app.post(BASE_URL+endpoint+mike.api_key,
                                 data=json.dumps(deposit),
                                 content_type='application/json')                               
        mike = User.from_pk(1)
        self.assertEqual(response.status_code, 201, "status Code should be 201")
        self.assertEqual(mike.balance, 1500.0, "Mike's balance should equal 1500")

    def test_account_info(self):
        pass

    def test_get_api_key(self):
        pass