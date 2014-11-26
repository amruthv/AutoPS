#!/usr/bin/python

import rpclib
from zoodb import *

import sys

class StringRpcServer(rpclib.RpcServer):
    ## Fill in RPC methods here.
    def rpc_getString(self, username):
        print 'username type', type(username)
        print 'getting string for', username
        db = string_setup()
        userstr  = db.query(UserString).get(str(username))
        return userstr.userStr

    def rpc_setString(self, username, s):
        print 'set string for user {0} to {1}'.format(username, s)
        db = string_setup()
        userstr = db.query(UserString).get(str(username))
        userstr.userStr = s
        db.commit()
    
    def rpc_makeString(self, username):
        stringDb = string_setup()
        newstring = UserString()
        newstring.username = username
        stringDb.add(newstring)
        stringDb.commit()

(_, sockpath) = sys.argv

s = StringRpcServer()
s.run_sockpath_fork(sockpath)
