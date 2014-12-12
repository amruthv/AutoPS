#!/usr/bin/python

import rpclib
from zoodb import *

import sys

class StringRpcServer(rpclib.RpcServer):
    ## Fill in RPC methods here.
    def rpc_getString(self, username):
        db = string_setup()
        userstr  = db.query(UserString).get(username)
        return userstr.userStr

    def rpc_setString(self, username, s):
        db = string_setup()
        userstr = db.query(UserString).get(username)
        userstr.userStr = s
        db.commit()
        return "Success"
    
    def rpc_makeString(self, username):
        stringDb = string_setup()
        newstring = UserString()
        newstring.username = username
        stringDb.add(newstring)
        stringDb.commit()

(_, sockpath) = sys.argv

s = StringRpcServer()
s.run_sockpath_fork(sockpath)
