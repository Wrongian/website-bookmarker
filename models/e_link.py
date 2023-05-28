from resources import db
from sqlalchemy.sql import func
from models.media import delete_media
from sqlalchemy.types import LargeBinary
from sqlalchemy_utils import EncryptedType
from models.key import actual_key
from sqlalchemy_utils.types.encrypted.encrypted_type import AesEngine
import re

class ELink(db.Model):
    __tablename__ = "e_link"
    id = db.Column(db.Integer,primary_key= True)
    #date of creation
    creation_date = db.Column(db.DateTime(timezone=True),nullable = False,server_default=func.now()) 
    #media attached to the link
    media = db.Column(db.Integer,db.ForeignKey("media.id",ondelete="CASCADE"),nullable=True) 
    #actual link
    link_text = db.Column(EncryptedType(db.String,actual_key,AesEngine,"pkcs5"),nullable = False)
    #name
    name = db.Column(EncryptedType(db.String,actual_key,AesEngine,"pkcs5"),nullable = True)
    #id of the category the link is in
    header= db.Column(db.Integer, db.ForeignKey("e_header.id"),nullable = False)
    #position in header
    position = db.Column(db.Integer)


def e_get_link(link_id):
    link = db.session.query(ELink).filter(ELink.id == link_id).first()
    if link:
        return link
    return None

def e_save_link(link_text,header_id,name = None, media= None,):
    if media:
        media_id = media.id
    else:
        media_id = None
    new_link = ELink(media = media_id,link_text = link_text,header= header_id)
    if name:
        new_link.name = name
    db.session.add(new_link)
    db.session.commit()
    return new_link

def e_delete_link(link_id):
    link = e_get_link(link_id)
    if link:
        if link.media:
            #delete the associated media
            delete_media(link.media) 
        #delete associated link
        db.session.delete(link)
        db.session.commit()

def e_change_header(link_id,header_id):
    link = e_get_link(link_id)
    if link:
        link.header = header_id
        db.session.add(link)
        db.session.commit()
    
def e_get_all_links():
    return db.session.query(ELink).all()

#https://github.com/kvesteri/sqlalchemy-utils/issues/454#
#https://stackoverflow.com/questions/74344006/sqlalchemy-using-filter-to-an-encrypted-column
def e_search_sim_link_paginate(link_text = "",name = "", header_id = None, page = 1):
    PER_PAGE = 30
    #have to make my own cuz the built in ver doesnt work aiee
    #probably really slow

    #get all links
    links = e_get_all_links()
    def fil_func(link):
        is_true = True
        if link.name:
            if re.search(name,link.name):
                is_true = is_true and True
            else: 
                is_true = False
        if re.search(link_text,link.link_text):
            is_true = is_true and True
        else:
            is_true = False
        return is_true

    def fil_func_header(link):
        if header_id == link.header and fil_func(link) :
            return True
        return False

    #filter the list
    if header_id:
        filtered_list =  list(filter(fil_func_header,links))    
    else:
        filtered_list =  list(filter(fil_func,links))
    
    #paginate
    if page<1:
        return []
    start_page = PER_PAGE*(page-1)
    end_page = PER_PAGE*page
    return filtered_list[start_page:end_page] 

def change_key_link():
    #remember to change the key first
    links = e_get_all_links()
    for link in links:
        name = link.name
        text = link.link_text
        link.name = name
        link.link_text = text
        db.session.add(link)
    db.session.commit()
    
