#!/usr/bin/env python3
import sqlite3


class Database:

    def __init__(self):
        self.connection = sqlite3.connect('new.db')
        self.cursor     = self.connection.cursor()

    def __enter__(self):
        return self

    def __exit__(self, type_, value, traceback):
        if self.connection:
            if self.cursor:
                self.connection.commit()
                self.cursor.close()
            self.connection.close()

    def create_table(self, table_name):
        self.cursor.execute(
            f'DROP TABLE IF EXISTS {table_name};')
        self.cursor.execute(
            f'''CREATE TABLE {table_name}(
                pk INTEGER PRIMARY KEY AUTOINCREMENT);''')

    def add_column(self, table_name, column_name, column_type):
        self.cursor.execute(
            f'''ALTER TABLE {table_name}
                ADD COLUMN {column_name} {column_type};''')
        

if __name__ == '__main__':
    with Database() as db:
        db.cursor.execute(
            '''DROP TABLE IF EXISTS users;''')
        db.cursor.execute(
            '''CREATE TABLE users(
                pk INTEGER PRIMARY KEY AUTOINCREMENT,
                    username VARCHAR,
                    password VARCHAR
                );''')
        other_username = 'cookiemonster'
        db.cursor.execute(
            f'''INSERT INTO 
                users(username, password) 
                VALUES('{other_username}', ?)
        ;''',("opensesame",))
