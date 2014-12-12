from zoodb import *
from debug import *

import hashlib
import random
import pbkdf2
import os

def newtoken(credDb, cred):
    hashinput = "%s%.10f" % (cred.password, random.random())
    cred.token = hashlib.md5(hashinput).hexdigest()
    credDb.commit()
    return cred.token

def login(username, password):
    credDb = cred_setup()
    cred = credDb.query(Cred).get(username)
    if not cred:
        return None
    if pbkdf2.PBKDF2(password, cred.salt).hexread(32) == cred.password:
        return newtoken(credDb, cred)
    else:
        return None

def register(username, password):
    credDb = cred_setup()
    cred = credDb.query(Cred).get(username)
    if cred:
        return None
    newcred = Cred()
    salt = os.urandom(32)
    passwordHash = pbkdf2.PBKDF2(password, salt).hexread(32)
    newcred.username = username
    newcred.password = passwordHash
    newcred.salt = salt
    credDb.add(newcred)
    credDb.commit()
    personDb = person_setup()
    newperson = Person()
    newperson.username = username
    personDb.add(newperson)
    personDb.commit()
    return newtoken(credDb, newcred)

def check_token(username, token):
    credDb = cred_setup()
    cred = credDb.query(Cred).get(username)
    if cred and cred.token == token:
        return True
    else:
        return False

