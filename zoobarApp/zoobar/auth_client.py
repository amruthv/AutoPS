from debug import *
from zoodb import *
import rpclib

@catch_err
def login(userName, passWord):
    with rpclib.client_connect('/authsvc/sock') as c:
        ret = c.call('login', username = userName, password = passWord)
        return ret

@catch_err
def register(userName, passWord):
    with rpclib.client_connect('/authsvc/sock') as c:
        ret = c.call('register', username=userName, password=passWord) 
        return ret

@catch_err
def check_token(userName, Token):
    with rpclib.client_connect('/authsvc/sock') as c:
        ret = c.call('check_token', username=userName, token=Token)
        return ret
