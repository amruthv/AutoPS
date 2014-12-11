#!/usr/bin/python

from zoodb import *
import rpclib
import sys
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import *
import os

class StringRpcServer(rpclib.RpcServer):
    ## Fill in RPC methods here.
    def rpc_getString(self, username):
        db = string_setup()
        person = db.query(String).get(username)
        return person.s
    def rpc_setString(self, username, s):
	db = string_setup()
	string = db.query(String).get(username)
	string.s = s
	db.commit()

(_, sockpath) = sys.argv

s = StringRpcServer()
s.run_sockpath_fork(sockpath)
