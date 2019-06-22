#!/usr/bin/env python3
'''
All input comes from views
'''
import time
from terminal_app.styletext import ColorText
from . import views
from model.user import User
from model.user import InsufficientFundsError, InsufficientSharesError
from model.util import get_price


def run():
    views.main_menu()
    while True:
        main_selection = input("\n\nWhat would you like to do today? ")
        if main_selection.lower() == "l":
            while True:
                login_info = views.login_view()
                user = user_password_attempt(login_info[0], login_info[1])
                if user is not None:
                    account_loop(user)
                    break
                else:
                    print("Incorrect password, please try again \n")
                    continue

        elif main_selection.lower() == "n":
            create_user=views.create_user()
            new_user = User(user_name=create_user[0],
                            password=create_user[1],
                            real_name=create_user[2],
                            balance=create_user[3])
            new_user.hash_password(create_user[1])
            new_user.save()
            ColorText("green", "Successfully added!")
            time.sleep(1)
            run()
        elif main_selection.lower() == "x":
            views.exit_view()
    
def account_loop(user):
    selection = views.user_account_view(user.real_name, user.balance)
    while True:
        if selection.strip() == "1":
            pos = user.all_positions()
            print("{:<10}{:>10}".format("Ticker", "Amount"))
            for p in pos:
                print("{:<10}{:>10}".format(p.ticker, p.amount))
            input("Enter to continue...")
            account_loop(user)
        elif selection.strip() == "2":
            ticker = input("Enter ticker symbol ")
            print(get_price(ticker))
            input("Enter to continue...")
            account_loop(user)
        elif selection.strip() =="3":
            ticker = input("Enter ticker symbol: ")
            buy_amt = int(input("Enter amount of shares you want to buy: "))
            try:
                user.buy(ticker,buy_amt)
            except InsufficientFundsError:
                print("")
                ColorText("red", "\nInsufficient Funds")
                time.sleep(1)
                account_loop(user)
            account_loop(user)

        elif selection.strip() == "4":
            ticker = input("Enter ticker symbol: ")
            sell_amt = int(input("Enter amount of shares you want to sell: "))
            try:
                user.sell(ticker,sell_amt)
            except InsufficientSharesError:
                print("")
                ColorText("red", "\nInsufficent Shares")
                time.sleep(1)
            account_loop(user)
        elif selection.strip() == "5":
            trades = user.all_trades()
            print("{:<10}{:>10}{:>10}".format("Date", "Ticker", "Price", "Shares"))
            for p in trades:
                print("{:<10}{:<10}{:>10}{:>10}".format(p.time, p.ticker, p.price, p.volume))
            input("Enter to continue...")
            account_loop(user)
        elif selection.strip() == "6":
            ticker = input("Enter ticker symbol: ")
            trades = user.trades_for(ticker)

            print("{:<10}{:>10}{:>10}".format("Ticker", "Price", "Shares"))
            for p in trades:
                print("{:<10}{:>10}{:>10}".format(p.ticker, p.price, p.volume))

            input("Enter to continue...")
            account_loop(user)
        elif selection.strip() == "7":
            deposit = int(input("Enter the deposit amount: $"))
            user.balance += deposit
            user.save()
            ColorText("green", "Success!")
            time.sleep(1)
            account_loop(user)
        elif selection.strip() == "8":
            run()
        





def user_password_attempt(username, password):
    """ input username and password, on successful login, return the user object
    on a failed login return none """
    return User.login(username,password)

def login_loop():
    while True:
        view.login_view()
        user_name = input("Username:" )
        user_password = input("Username:" )
        user = User()
        user.login(user_name, user_password)


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
