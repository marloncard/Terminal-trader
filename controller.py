#!/usr/bin/env python3

import time

import views
from models import User


def infinite_loop():
    views.main_menu()
    # username = view.login_menu()
    # username = input('Your app. username: ')
    # password = input('Your app. password: ')
    login_info = views.login_view()

    ##TODO: Add database connection for user table
    user = User(login_info[0], login_info[1])
    while user == False:
        #user = False
        if user:
            pass
        else:
            login_info = views.login_view()

    '''
    stored_username = user.fetch_username()
    stored_password = user.fetch_password()


    if username == stored_username:
        if password == stored_password:
            return 'successful login'
        return 'catch-all type-thing'
    '''


if __name__  == '__main__':
    print(infinite_loop())
