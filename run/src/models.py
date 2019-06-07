#!/usr/bin/env python3

import json
import requests

from mappers import Database



class User:

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def login(self):
        with Database() as d:
            d.cursor.execute(
                f'''SELECT password
                    FROM users
                    WHERE username='{self.username}';''')
        password = d.cursor.fetchone()[0]
        if password:
            if self.password == password:
                return True
        return False

def lookup(company):
    api = lookup_api()
    query = api + company
    return json.loads(requests.get(query).text)[0]['Symbol']
    #print(query)

def quote(symbol):
    api = quote_api()
    query = api + symbol
    return json.loads(requests.get(query).text)['LastPrice']
    #print(query)

def quote_api():
    endpoint = 'http://dev.markitondemand.com/MODApis/Api/v2/Quote/json?symbol='
    return endpoint

def lookup_api():
    endpoint = 'http://dev.markitondemand.com/MODApis/Api/v2/lookup/json?input='
    return endpoint

if __name__ == '__main__':
    #user = User('cookiemonster', 'opensesame')
    #print(user.login())
    #symbol =  input('stock symbol ')
    #print(quote(symbol))
    company = input("company name: ")
    print(lookup(company))

