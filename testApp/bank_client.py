from zoodb import *
import rpclib

def transfer(username, recipient, amount):
    with rpclib.client_connect('/jail/banksvc/sock') as c:
        ret = c.call('transfer', username = username, recipient = recipient, amount = amount)
        return ret
def viewBalance(username):
    with rpclib.client_connect('/jail/banksvc/sock') as c:
        ret = c.call('balance', username = username)
        return ret
def makeBank(username):
    with rpclib.client_connect('/jail/banksvc/sock') as c:
        ret = c.call('make_bank', username = username)
        return ret
