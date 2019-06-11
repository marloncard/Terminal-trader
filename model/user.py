#!/usr/bin/env python3
import sqlite3
from .orm import Sqlite3ORM

#TABLENAME = "user_info"


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


    # def _insert(self):
    #     with sqlite3.connect(DBNAME) as conn:
    #         curr = conn.cursor()
    #         SQL = """
    #                 INSERT INTO user_info(user_name, password, real_name, balance)
    #                 VALUES(?,?,?,?);
    #               """
    #         curr.execute(SQL, (self.user_name, self.password, self.real_name, self.balance))
    #         #  .lastrowid returns row id of last modified row
    #         self.pk = curr.lastrowid

    def _update(self):
        with sqlite3.connect(self.dbpath) as conn:
            curr = conn.cursor()
            SQL = """
                    UPDATE user_info 
                    SET user_name=?, password=?, real_name=?, balance=?
                    WHERE pk=?;
                  """
            curr.execute(SQL, (self.user_name,
                               self.password,
                               self.real_name,
                               self.balance,
                               self.pk))

  
    @classmethod 
    def frompk(cls, pk):
        '''
        A class method is bound to the class rather than the object;
        doesn't require creation of class instance. The first parameter
        is always the class itself (cls)
        '''
        with sqlite3.connect(cls.dbpath) as conn:
            # The 'Row' instance is a optimized row_factory for connection
            # objects. Supports mapping access by column names and index;
            # Also iteration, representation, equality testing and len()
            conn.row_factory = sqlite3.Row
            curr = conn.cursor()
            SQL = """
                SELECT * FROM user_info
                WHERE pk=?;
                """
            curr.execute(SQL, (pk,))
            row = curr.fetchone()
            if not row:
                return None
            user = cls(**row)
            return user

