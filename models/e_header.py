from resources import db
from sqlalchemy.sql import func,expression
from sqlalchemy import desc,asc
from sqlalchemy.orm import relationship
from sqlalchemy.ext.orderinglist import ordering_list, count_from_0
from models.e_link import ELink,e_delete_link,e_get_link
from sqlalchemy.types import LargeBinary
from sqlalchemy_utils import EncryptedType
from models.key import actual_key
from sqlalchemy_utils.types.encrypted.encrypted_type import AesEngine


class EHeader(db.Model):
    __tablename__ = "e_header"
    id = db.Column(db.Integer,primary_key= True)
    creation_date = db.Column(db.DateTime(timezone=True),nullable = False,server_default=func.now()) 
    #what links it sotres
    links = relationship("ELink",primaryjoin="EHeader.id == ELink.header",order_by = "ELink.position",collection_class=ordering_list("position"))
    #what category its in
    category = db.Column(db.Integer, db.ForeignKey("e_category.id"),nullable = False)
    #name of the header
    name = db.Column(EncryptedType(db.String,actual_key,AesEngine,"pkcs5"),nullable = False)
    #position in the category
    position = db.Column(db.Integer)
    
def e_get_header(header_id):
    header = db.session.query(EHeader).filter(EHeader.id == header_id).first()
    if header:
        return header
    return None

        
def e_add_header(category_id,name):
    new_header = EHeader(category = category_id,name = name)
    db.session.add(new_header)
    db.session.commit()
    return new_header

def e_get_links(header_id):
    header = e_get_header(header_id)
    return header.links

def e_delete_header(header_id):
    header = e_get_header(header_id)
    if header:
        for link in header.links:
            e_delete_link(link.id)
        db.session.delete(header) 
        db.session.commit()
    
def e_rename_header(header_id,new_name):
    header = e_get_header(header_id)
    if header:
        header.name = new_name
        db.session.add(header)
        db.session.commit()

    
def e_link_up(link_id):
    link = e_get_link(link_id)
    if link:
        header_id = link.header
        header = e_get_header(header_id)
        if header:
            pos = header.links.index(link)
            link = header.links.pop(pos) 
            header.links.insert(pos+1,link)
            #check length later
            db.session.commit()

def e_link_down(link_id):
    link = e_get_link(link_id)
    if link:
        header_id = link.header
        header = e_get_header(header_id)
        if header:
            pos = header.links.index(link)
            link = header.links.pop(pos) 
            if pos-1 >=0: 
                header.links.insert(pos-1,link)
            #check length later
            db.session.commit()

def e_change_category(header_id, category_id):
    header = e_get_header(header_id)
    if header:
        header.category = category_id
        db.session.add(header) 
        db.session.commit()

def e_get_all_headers():
    return db.session.query(EHeader).all()

def change_key_header():
    headers = e_get_all_headers()
    for header in headers:
        header_name = header.name
        header.name = header_name
        db.session.add(header)
    db.session.commit()