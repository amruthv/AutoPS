from zoodb import *
import rpclib

@catch_err
def transfer(sender, recipient, zoobars):
    with rpclib.client_connect('/banksvc/sock') as c:
        ret = c.call('transfer', sender = sender, recipient = recipient, zoobars = zoobars)
        return ret
@catch_err
def balance(username):
    with rpclib.client_connect('/banksvc/sock') as c:
        ret = c.call('balance', username = username)
        return ret

@catch_err
def make_bank(username):
    with rpclib.client_connect('/banksvc/sock') as c:
        ret = c.call('make_bank', username = username)
        return ret
