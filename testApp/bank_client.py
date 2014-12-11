from zoodb import *
import rpclib

@catch_err
def transfer(username, recipient, amount):
    with rpclib.client_connect('/banksvc/sock') as c:
        ret = c.call('transfer', username = username, recipient = recipient, amount = amount)
        return ret
@catch_err
def viewBalance(username):
    with rpclib.client_connect('/banksvc/sock') as c:
        ret = c.call('balance', username = username)
        return ret

