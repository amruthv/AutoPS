#!/usr/bin/python

from zoodb import *
import rpclib
import sys
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import *
import os

class BankRpcServer(rpclib.RpcServer):
    ## Fill in RPC methods here.
    def rpc_transfer(self, username, recipient, amount):
        bankdb = bank_setup()
        usernamep = bankdb.query(Bank).get(username)
        recipientp = bankdb.query(Bank).get(recipient)
        if recipientp is None:
            return "Failure"
        amount = int(amount)
        username_balance = usernamep.zoobars - amount
        recipient_balance = recipientp.zoobars + amount

        if username_balance < 0 or recipient_balance < 0:
            raise ValueError()

        usernamep.zoobars = username_balance
        recipientp.zoobars = recipient_balance
        bankdb.commit()
        return "Success"

    def rpc_balance(self, username):
        db = bank_setup()
        person = db.query(Bank).get(username)
        return person.zoobars

    def rpc_make_bank(self, username):
	    bankdb = bank_setup()
	    bank = Bank()
	    bank.username = username
	    bank.zoobars = 10
	    bankdb.add(bank)
	    bankdb.commit()

(_, sockpath) = sys.argv

s = BankRpcServer()
s.run_sockpath_fork(sockpath)
