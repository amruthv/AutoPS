#!/usr/bin/python

import getpass
import sys
import os

import login_repl_client
import bank_repl_client
import string_repl_client

QUIT = "quit"
LOGIN = "login"
VIEW_BALANCE = "view balance"
VIEW_STRING = "view string"
SET_STRING = "set string"
REGISTER = "register"
TRANSFER = "transfer"
UID = 70000


def main():
    changeUID()
    action = takeMainAction()
    if action == QUIT:
        sys.exit(0)
    elif action == "register":
        registerAccount()
    else:
        loginAccount()

def changeUID():
    os.setuid(UID)

def takeMainAction():
    while True:
        print("Type \"register\" to make an account. Type \"login\" to login to your account. Type \"quit\" to quit.")
        action = raw_input()
        if action == "register" or action == "login" or action == "quit":
            return action

def registerAccount():
    username = raw_input("Username: ")
    for char in username:
        if not (char.isalpha() or char.isdigit()):
            print "Only alpha numeric usernames"
            sys.exit(1)
    password = getpass.getpass("Password: ")
    result = register(username, password)
    if result == "Success":
        loggedInLoop(username)
    else:
        print "Failure to register"
        main()

def loginAccount():
    username = raw_input("Username: ")
    password = getpass.getpass("Password: ")
    result = login(username, password)
    if result == "Success":
        loggedInLoop(username)
    else:
        print "Failure to log in"
        main()

def loggedInLoop(username):
    while True:
        print("Type \"transfer (toWhom) (amount)\" to transfer money. Type \"view balance\" to view your balance. Type \"set string (yourString)\" to set the string for your account. Type \"view string\" to view the string for your account. Type \"quit\" to quit.")
        action = raw_input()
        actionParts = action.split(" ")
        if action == QUIT:
            sys.exit(0)
        result = None
        if action == VIEW_BALANCE:
            result = viewBalance(username)
        elif actionParts[0] == TRANSFER:
            if len(actionParts) != 3:
                result = "Wrong number of arguments. Try again"
            elif actionParts[1] == username:
                result = "Can't send money to yourself!"
            else:
                recipient = actionParts[1]
                amount = actionParts[2]
                result = transfer(username, recipient, amount)
        elif " ".join(actionParts[0:2]) == SET_STRING:
            result = setStringForUser(username, " ".join(actionParts[2:]))
        elif " ".join(actionParts[0:2]) == VIEW_STRING:
            result = getStringForUser(username)
        print result

def register(username, password):
    return login_repl_client.register(username, password)

def login(username, password):
    return login_repl_client.login(username, password)

def viewBalance(username):
    return bank_repl_client.viewBalance(username)

def transfer(username, recipient, amount):
    return bank_repl_client.transfer(username, recipient, amount)

def setStringForUser(username, userStr):
    return string_repl_client.setString(username, userStr)

def getStringForUser(username):
    return string_repl_client.getString(username)

if __name__ == '__main__':
    main()
