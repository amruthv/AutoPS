from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import *
import os

UserStringBase = declarative_base()
CredBase = declarative_base()
BankBase = declarative_base()

class Bank(BankBase):
    __tablename__ = "bank"
    username = Column(String(128), primary_key=True)
    zoobars = Column(Integer, nullable=False, default=10)

class Cred(CredBase):
    __tablename__ = "cred"
    username = Column(String(128), primary_key=True)
    password = Column(String(128))
    salt = Column(Binary)

class UserString(UserStringBase):
    __tablename__ = "userstring"
    username = Column(String(128), primary_key=True)
    userStr = Column(String(5000), nullable=False, default="")    

def dbsetup(name, base):
    thisdir = os.path.dirname(os.path.abspath(__file__))
    dbdir   = os.path.join(thisdir, "db", name)
    if not os.path.exists(dbdir):
        os.makedirs(dbdir)

    dbfile  = os.path.join(dbdir, "%s.db" % name)
    engine  = create_engine('sqlite:///%s' % dbfile,
                            isolation_level='SERIALIZABLE')
    base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)
    return session()


def string_setup():
    return dbsetup("userstring", UserStringBase)

def cred_setup():
    return dbsetup("cred", CredBase)

def bank_setup():
    return dbsetup("bank", BankBase)

def 

import sys
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Usage: %s [init-person|init-transfer]" % sys.argv[0]
        exit(1)

    cmd = sys.argv[1]
    if cmd == 'init-string':
        string_setup()
    elif cmd == 'init-cred':
        cred_setup()
    elif cmd == 'init-bank':
        bank_setup()
    else:
        raise Exception("unknown command %s" % cmd)
