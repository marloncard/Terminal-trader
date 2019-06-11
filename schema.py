#!/usr/bin/env python3

import sqlite3


class Schema:

    def __init__(self):
        self.connection = sqlite3.connect('trader.db')
        self.cursor = self.connection.cursor()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        if self.connection:
            if self.cursor:
                self.connection.commit()
                self.cursor.close()
            self.connection.close()


    def create_table(self, table_name):
        self.cursor.execute(
        f'DROP TABLE IF EXISTS {table_name};'
        )
        self.cursor.execute(
        f'''CREATE TABLE {table_name}(
            pk INTEGER PRIMARY KEY AUTOINCREMENT
         );''')

    def modify_table(self, table_name, column_name, column_type):
        self.cursor.execute(
        f'''ALTER TABLE {table_name}
            ADD COLUMN {column_name} {column_type};
         ''')


def build_user():
        Schema().create_table('user_info')  
        Schema().modify_table('user_info', 'user_name', 'VARCHAR')
        Schema().modify_table('user_info', 'real_name', 'VARCHAR')
        Schema().modify_table('user_info', 'password', 'VARCHAR')
        Schema().modify_table('user_info', 'balance', 'FLOAT')

if __name__ == '__main__':
    build_user()
