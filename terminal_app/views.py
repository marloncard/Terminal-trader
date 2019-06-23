#!/usr/bin/env python3
from .styletext import ColorText
import os
import sys
import time



def main_menu():
    os.system("clear")
    print("\n"*3+(39*"*"))
    ColorText("red","Welcome to Terminal Trader")
    print(39*"*"+"\n"*3)

    ColorText("blue","[l] Login")
    ColorText("blue","[n] New Account")
    ColorText("blue","[x] Exit")

def login_view():
    os.system("clear")
    print("\n"*2)
    ColorText("green", "Enter Username & Password")
    print("\n"*2)
    user_name = input("Username: ")
    user_passw = input("Password: ")
    return (user_name, user_passw)

def user_account_view(real_name, balance):
    os.system("clear")
    ColorText("blue", "Welcome to Terminal Trader {}".format(real_name))
    print("\nYour current balance is: ${:,.2f}".format(balance))
    print("")
    print("")
    ColorText("white", "1) View Positions")
    ColorText("white", "2) Lookup Stock Price")
    ColorText("white", "3) Buy")
    ColorText("white", "4) Sell")
    ColorText("white", "5) See Trade History")
    ColorText("white", "6) See Trades for one stock")
    ColorText("white", "7) Deposit Money")
    ColorText("white", "8) View API Key")
    ColorText("white", "9) Logout")
    return input("\n\nWhat's your selection? ")


def create_user():
    try:
        user_name = input("Enter a User Name: ")
        password = input("Enter a secure password: ")
        real_name = input("Enter your full name: ")
        balance = int(input("Enter a starting balance: $"))
        return (user_name, password, real_name, balance)
    except:
        ColorText("red", "Invalid Input")
        time.sleep(1)
        os.system("clear")
        main_menu()
        create_user()
    
def api_view(key):
    print("\n\nYour API Key is: \n")
    ColorText("white", "{}".format(key))

def exit_view():
    print("")
    ColorText("blue", "Thanks for stopping by!")
    time.sleep(1)
    sys.exit()

if __name__ == '__main__':
    main_menu()