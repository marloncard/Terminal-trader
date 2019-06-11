#!/usr/bin/env python3
import os

def main_menu():
    print("\n"*3+(39*"*"))
    os.system('echo "\033[1;34m Welcome to Trader Co. Trading Company \033[0m"')
    print(39*"*"+"\n"*3)
    
    os.system('echo "\033[1;32m [l] Login \033[0m"')
    os.system('echo "\033[1;35m [n] New Account \033[0m"')
    os.system('echo "\033[1;31m [x] Exit \033[0m"')

    main_selection = input("\n\nWhat would you like to do today? ")

def login_view():
    os.system('clear')
    print("\n"*2)
    os.system('echo "\033[1;32m Enter Username & Password \033[0m"')
    print("\n"*2)
    user_name = input("Username: ")
    user_passw = input("Password: ")
    return (user_name, user_passw)



def new_account_view():
    pass

def exit_view():
    pass

if __name__ == '__main__':
    main_menu()