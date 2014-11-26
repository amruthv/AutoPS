import rpclib

def login(userName, passWord):
    with rpclib.client_connect('/loginsvc/sock') as c:
        ret = c.call('login', username = userName, password = passWord)
        return ret

def register(userName, passWord):
    with rpclib.client_connect('/loginsvc/sock') as c:
        ret = c.call('register', username=userName, password=passWord) 
        return ret
