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
    def rpc_transfer(self, sender, recipient, zoobars):
	bankdb = bank_setup()
	senderp = bankdb.query(Bank).get(sender)
	recipientp = bankdb.query(Bank).get(recipient)

	sender_balance = senderp.zoobars - zoobars
	recipient_balance = recipientp.zoobars + zoobars

	if sender_balance < 0 or recipient_balance < 0:
	    raise ValueError()

	senderp.zoobars = sender_balance
	recipientp.zoobars = recipient_balance
	bankdb.commit()
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
