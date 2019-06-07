#!/usr/bin/env python3

import time

from models import Users


def infinite_loop():
    # username = view.login_menu()
    username = input('Your app. username: ')
    password = input('Your app. password: ')

    ###
    user = User(username, password)
    stored_username = user.fetch_username()
    stored_password = user.fetch_password()


    if username == stored_username:
        if password == stored_password:
            return 'successful login'
        return 'catch-all type-thing'


if __name__  == '__main__':
    print(infinite_loop())
