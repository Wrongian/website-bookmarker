from resources import db
from sqlalchemy.sql import func,expression
from sqlalchemy import desc,asc
from sqlalchemy.orm import relationship
from sqlalchemy.ext.orderinglist import ordering_list
from models.link import Link
from models.header import Header,get_header,delete_header

class Category(db.Model):
    id = db.Column(db.Integer,primary_key= True)
    #date of craetion of category
    creation_date = db.Column(db.DateTime(timezone=True),nullable = False,server_default=func.now()) 
    headers = relationship("Header",order_by="Header.position",collection_class=ordering_list("position"))
    name = db.Column(db.String,nullable = False)
    #media attached to the link
    media = db.Column(db.Integer,db.ForeignKey("media.id",ondelete="CASCADE"),nullable=True) 
    
def get_category(category_id):
    category = db.session.query(Category).filter(Category.id == category_id).first()
    if category:
        return category
    return None

def get_headers(category_id):
    category = get_category(category_id)
    return category.headers

def get_header_choices(category_id):
    headers = get_headers(category_id)
    #make da choices (value,label) list
    choice_list = []
    for header in headers:
        choice_list.append((header.id,header.name))
    return choice_list

def get_category_choices():
    categories = db.session.query(Category).all() 
    choice_list = []
    for category in categories:
        choice_list.append((category.id,category.name))
    return choice_list
    

def header_up(header_id):
    header = get_header(header_id)
    if header:
        category = get_category(header.category)
        if category:
            pos = category.headers.index(header)
            header = category.headers.pop(pos) 
            category.headers.insert(pos+1,header)
            #check length later
            db.session.commit()
            
def header_down(header_id):
    header = get_header(header_id)
    if header:
        category = get_category(header.category)
        if category:
            pos = category.headers.index(header)
            header = category.headers.pop(pos) 
            if pos-1 >= 0:
                category.headers.insert(pos-1,header)
            #check length later
            db.session.commit()

def add_category(name,media = None):
    if media:
        media_id = media.id
    else:
        media_id = None
    new_category = Category(name = name,media = media_id) 
    db.session.add(new_category)
    db.session.commit()
    return new_category

def get_all_categories():
    categories = db.session.query(Category).all()
    return categories
            

def delete_category(category_id):
    category = get_category(category_id)
    if category:
        for header in category.headers:
            delete_header(header.id)
        db.session.delete(category)
        db.session.commit()
