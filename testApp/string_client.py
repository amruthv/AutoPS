import rpclib

def setString(username, s): 
    with rpclib.client_connect('/stringsvc/sock') as c:
        ret = c.call('setString', username = username, s = s)
        return ret
def getString(username):
    with rpclib.client_connect('/stringsvc/sock') as c:
        ret = c.call('getString', username = username)
        return ret

