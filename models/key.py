from resources import db
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy.types import LargeBinary
import hashlib
from functools import wraps
from flask import session,url_for,redirect

#really bad workaround, to be changed later
actual_key = ""

class Key(db.Model):
    id = db.Column(db.Integer,primary_key= True)
    creation_date = db.Column(db.DateTime(timezone=True),nullable = False,server_default=func.now()) 
    key_hash = db.Column(db.LargeBinary)


def get_hash(string):
    hash = hashlib.sha256(string.encode("utf-8"))
    return hash.digest()

#only should have one key
def get_key():
    #todo : check if only 1 key later
    key = db.session.query(Key).first()
    if key:
        return key
    return None

    
def create_key(key_str):
    #check if another key
    global actual_key
    key = get_key()
    if key:
        db.session.delete(key)
    if "key" in session:
        del session["key"]
    key = Key(key_hash = get_hash(key_str))
    db.session.add(key)
    db.session.commit()
    session["key"] = key_str
    actual_key = key_str
    return key
    
def verify_key(key_str):
    global actual_key
    key = get_key()
    if key:
        if get_hash(key_str) == key.key_hash:
            actual_key = key_str
            return True
        else:
            return False
    return False


def key_required(f):
    #checks if needs key 
    @wraps(f)
    def func(*args,**kwargs):
        if "key" not in session:
            return redirect(url_for("main.index"))
        return f(*args,**kwargs)
    return func

def session_key():
    if "key" in session:
        return session["key"]
    return None

        
def delete_session_key():
    global actual_key
    if "key" in session:
        actual_key = ""
        del session["key"]

def change_key(key_str):
    global actual_key
    key = get_key()
    if key:
        key.key_hash = get_hash(key_str)
        session["key"] = key_str
        actual_key = key_str
        db.session.add(key)
        db.session.commit()
