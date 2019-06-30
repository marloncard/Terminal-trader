#!/usr/bin/env python3
import sqlite3
from .orm import Sqlite3ORM
from .position import Position
from .trade import Trade
from .util import get_price
import datetime
import bcrypt
import random


class InsufficientFundsError(Exception):
    pass

class InsufficientSharesError(Exception):
    pass


class User(Sqlite3ORM):

    fields = ['user_name', 'password', 'real_name', 'balance', 'api_key']
    dbtable = 'user_info'
    dbpath = 'trader.db'

    def __init__(self, **kwargs):
        self.pk = kwargs.get('pk')
        self.user_name = kwargs.get('user_name')
        self.password = kwargs.get('password')
        self.real_name = kwargs.get('real_name')
        self.balance = kwargs.get('balance', 0.0)
        self.api_key = kwargs.get('api_key')

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
        position = Position.one_where("user_info_pk=? AND ticker=? AND amount > 0", (self.pk, ticker))
        return position

    def buy(self, ticker, amount):
        """ buy a stock. if there is no current position, create one, if there is
        increase its amount. no return value """
        if amount < 1:
            raise ValueError
        ticker_price = get_price(ticker)
        cost = (ticker_price) * amount
        if self.balance < cost:
            raise InsufficientFundsError
        self.balance -= cost
        current_position = self.positions_for_stock(ticker)
        if current_position is None:
            current_position = Position(ticker=ticker, amount=0, user_info_pk=self.pk)
        current_position.amount += amount
        current_position.save()
        new_trade = Trade(ticker=ticker.lower(), volume=amount, price=ticker_price, user_info_pk=self.pk)
        new_trade.save()
        self.save()
        return new_trade

    def sell(self, ticker, amount):
        """ sell a stock. if there is not current"""
        if amount < 0:
            raise ValueError
        cost = get_price(ticker) * amount
        position = self.positions_for_stock(ticker)
        if position is None or amount > position.amount:
            raise InsufficientSharesError
        position.amount -= amount
        self.balance += cost
        position.save()
        new_trade = Trade(ticker=ticker.lower(),
                          volume=amount,
                          price=get_price(ticker),
                          user_info_pk=self.pk)
        if position.amount == 0:
            position.delete()
        else:
            position.save()
        new_trade.save()
        self.save()
        return new_trade

    def all_trades(self):
        """Return a list of trade objects for every trade made by this user
        arranged oldest to newest"""
        trades = Trade.many_where("user_info_pk=? ORDER BY time", (self.pk,))
        return trades

    def trades_for(self, ticker):
        """ return a list of Trade objects for each trade of a given stock for
            this user, arranged oldest to newest """
        return Trade.many_where("user_info_pk=? AND ticker=? ORDER BY time ASC",
                                (self.pk, ticker.lower()))

    @classmethod
    def richest(cls):
        return cls.many_where(' TRUE ORDER BY balance DESC')[0]

    def generate_api_key(self):
        self.api_key = str(random.randrange(10000000000000000000,99999999999999999999))
        return self.api_key

    @classmethod
    def api_authenticate(cls, api_key):
        '''
        Similar to the login method, only instead of a username and password, it will
        take an api key value as its argument. If the key exists in the users table,
        the method returns the User object that matches that row, otherwise it returns
        none.

        * Write a unit test to test that this method works.
        '''
        user = cls.one_where("api_key=?", (api_key,))
        if user is None:
            return None
        return user
        

    def json(self):
        '''
        Prepare user data to be jsonified.
        '''
        return {"User Name":self.user_name, 
                "Real Name":self.real_name, 
                "Balance":self.balance,
                "API Key":self.api_key}