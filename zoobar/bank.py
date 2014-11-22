from zoodb import *
from debug import *
from flask import g, request 
import time
import auth_client

def transfer(sender, recipient, zoobars, token):
    if not auth_client.check_token(sender, token):
        raise ValueError()

    bankdb = bank_setup()
    senderp = bankdb.query(Bank).get(sender)
    recipientp = bankdb.query(Bank).get(recipient)

    sender_balance = senderp.zoobars - zoobars
    recipient_balance = recipientp.zoobars + zoobars

    if sender_balance < 0 or recipient_balance < 0:
        raise ValueError()

    senderp.zoobars = sender_balance
    recipientp.zoobars = recipient_balance
    bankdb.commit()

    transfer = Transfer()
    transfer.sender = sender
    transfer.recipient = recipient
    transfer.amount = zoobars
    transfer.time = time.asctime()

    transferdb = transfer_setup()
    transferdb.add(transfer)
    transferdb.commit()

def make_bank(username):
    bankdb = bank_setup()
    bank = Bank()
    bank.username = username
    bank.zoobars = 10
    bankdb.add(bank)
    bankdb.commit()

def balance(username):
    db = bank_setup()
    person = db.query(Bank).get(username)
    return person.zoobars

def get_log(username):
    db = transfer_setup()
    return db.query(Transfer).filter(or_(Transfer.sender==username,
                                         Transfer.recipient==username))

