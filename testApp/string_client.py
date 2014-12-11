from zoodb import *
import rpclib

<<<<<<< HEAD
@catch_err
def setString(username, s): 
    with rpclib.client_connect('/stringsvc/sock') as c:
        ret = c.call('setString', username = username, s = s)
        return ret
@catch_err
def getString(username):
    with rpclib.client_connect('/stringsvc/sock') as c:
        ret = c.call('getString', username = username)
        return ret

=======
def setStringForUser(username, userStr):
    with rpclib.client_connect('/stringsvc/sock') as c:
        ret = c.call('setStringForUser', username = username, userStr = userStr)
        return ret
>>>>>>> 2d4ac17cfb84a73f76616b7a4855b88bd6fa6eb6
