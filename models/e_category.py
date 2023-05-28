from resources import db
from sqlalchemy.sql import func,expression
from sqlalchemy import desc,asc
from sqlalchemy.orm import relationship
from sqlalchemy.ext.orderinglist import ordering_list
from models.e_header import EHeader,e_get_header,e_delete_header
from sqlalchemy.types import LargeBinary
from sqlalchemy_utils import EncryptedType
from models.key import actual_key
from sqlalchemy_utils.types.encrypted.encrypted_type import AesEngine



class ECategory(db.Model):
    __tablename__ = "e_category"
    id = db.Column(db.Integer,primary_key= True)
    #date of craetion of category
    creation_date = db.Column(db.DateTime(timezone=True),nullable = False,server_default=func.now()) 
    headers = relationship("EHeader",primaryjoin="ECategory.id == EHeader.category", order_by="EHeader.position",collection_class=ordering_list("position"))
    name = db.Column(EncryptedType(db.String,actual_key,AesEngine,"pkcs5"),nullable = False)
    #media attached to the link
    media = db.Column(db.Integer,db.ForeignKey("media.id",ondelete="CASCADE"),nullable=True) 
    

class WrapperCategory():
    def __init__(self,id,creation_date,headers,name,media = None):
        self.id = id
        self.creation_date = creation_date
        self.headers = headers
        self.name = name
        self.media = media 
        

    
def e_get_category(category_id):
    category = db.session.query(ECategory).filter(ECategory.id == category_id).first()
    if category:
        return category
    return None

def e_get_headers(category_id):
    category = e_get_category(category_id)
    return category.headers

def e_get_header_choices(category_id):
    headers = e_get_headers(category_id)
    #make da choices (value,label) list
    choice_list = []
    for header in headers:
        choice_list.append((header.id,header.name))
    return choice_list

def e_get_category_choices():
    categories = db.session.query(ECategory).all() 
    choice_list = []
    for category in categories:
        choice_list.append((category.id,category.name))
    return choice_list
    

def e_header_up(header_id):
    header = e_get_header(header_id)
    if header:
        category = e_get_category(header.category)
        if category:
            pos = category.headers.index(header)
            header = category.headers.pop(pos) 
            category.headers.insert(pos+1,header)
            #check length later
            db.session.commit()
            
def e_header_down(header_id):
    header = e_get_header(header_id)
    if header:
        category = e_get_category(header.category)
        if category:
            pos = category.headers.index(header)
            header = category.headers.pop(pos) 
            if pos-1 >= 0:
                category.headers.insert(pos-1,header)
            #check length later
            db.session.commit()

def e_add_category(name,media = None):
    if media:
        media_id = media.id
    else:
        media_id = None
    new_category = ECategory(name = name,media = media_id) 
    db.session.add(new_category)
    db.session.commit()
    return new_category

def e_get_all_categories():
    categories = db.session.query(ECategory).all()
    return categories
            

def e_delete_category(category_id):
    category = e_get_category(category_id)
    if category:
        for header in category.headers:
            e_delete_header(header.id)
        db.session.delete(category)
        db.session.commit()

def change_key_category():
    categories = e_get_all_categories()
    for category in categories:
        name = category.name
        category.name = name
        db.session.add(category)
    db.session.commit()