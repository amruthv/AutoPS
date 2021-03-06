#!/usr/bin/python

import rpclib
import pbkdf2
import bank_client
import string_client
from zoodb import *

import os
import sys

class LoginRpcServer(rpclib.RpcServer):
    ## Fill in RPC methods here.
    def rpc_login(self, username, password):
        credDb = cred_setup()
        cred = credDb.query(Cred).get(username)
        if not cred:
            return "Failure"
        if pbkdf2.PBKDF2(password, cred.salt).hexread(32) == cred.password:
            return "Success"
        else:
            return "Failure"        

    def rpc_register(self, username, password):
        credDb = cred_setup()
        cred = credDb.query(Cred).get(username)
        if cred:
            return "Failure"
        bank_client.makeBank(username)
        string_client.makeString(username) 
        newcred = Cred()
        salt = os.urandom(32)
        passwordHash = pbkdf2.PBKDF2(password, salt).hexread(32)
        newcred.username = username
        newcred.password = passwordHash
        newcred.salt = salt
        credDb.add(newcred)
        credDb.commit()
        return "Success"        

(_, sockpath) = sys.argv

s = LoginRpcServer()
s.run_sockpath_fork(sockpath)
