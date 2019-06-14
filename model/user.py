#!/usr/bin/env python3
import sqlite3
from .orm import Sqlite3ORM
from .position import Position
import bcrypt



class User(Sqlite3ORM):

    fields = ['user_name', 'password', 'real_name', 'balance']
    dbtable = 'user_info'
    dbpath = 'trader.db'

    def __init__(self, **kwargs):
        self.pk = kwargs.get('pk')
        self.user_name = kwargs.get('user_name')
        self.password = kwargs.get('password')
        self.real_name = kwargs.get('real_name')
        self.balance = kwargs.get('balance', 0.0)

    def hash_password(self, password):
        """someuser.hash_password("somepassword") sets someusers self.password
        to a bcrypt encoded hash"""
        self.password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    @classmethod
    def login(cls, user_name, password):
        """ Search for the user with the given username (use one_where) and then
        use bcrypt's checkpw() to verify that the credentials are correct
        return none for bad credentials or the matching User instance on a
        successful login
        """
        user = cls.one_where("user_name=?", (user_name,))
        if user is None:
            return None
        if bcrypt.checkpw(password.encode(), user.password):
            return user
        return None

    def all_positions(self):
        positions = Position.many_where("user_info_pk=?", (self.pk,))
        return positions

    def positions_for_stock(self, ticker):
        """ return a user's position in one stock or None """
        position = Position.one_where("user_info_pk=? AND ticker=?", (self.pk, ticker))
        return position

    def buy(self, ticker, amount):
        """Buy a stock. If there is no current position, create one. If there is
        increase it's amount. No return value"""
        pass


