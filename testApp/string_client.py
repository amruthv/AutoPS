from zoodb import *
import rpclib

def setStringForUser(username, userStr):
    with rpclib.client_connect('/stringsvc/sock') as c:
        ret = c.call('setStringForUser', username = username, userStr = userStr)
        return ret
