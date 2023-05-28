from resources import db
from sqlalchemy.sql import func
from models.media import delete_media

class Link(db.Model):
    id = db.Column(db.Integer,primary_key= True)
    #date of creation
    creation_date = db.Column(db.DateTime(timezone=True),nullable = False,server_default=func.now()) 
    #media attached to the link
    media = db.Column(db.Integer,db.ForeignKey("media.id",ondelete="CASCADE"),nullable=True) 
    #actual link
    link_text = db.Column(db.String,nullable = False)
    #name
    name = db.Column(db.String,nullable = True)
    #id of the category the link is in
    header= db.Column(db.Integer, db.ForeignKey("header.id"),nullable = False)
    #position in header
    position = db.Column(db.Integer)


def get_link(link_id):
    link = db.session.query(Link).filter(Link.id == link_id).first()
    if link:
        return link
    return None
    
def save_link(link_text,header_id,name = None, media= None):
    if media:
        media_id = media.id
    else:
        media_id = None
    new_link = Link(media = media_id,link_text = link_text,header= header_id,name = name)
    db.session.add(new_link)
    db.session.commit()
    return new_link

def delete_link(link_id):
    link = get_link(link_id)
    if link:
        if link.media:
            #delete the associated media
            delete_media(link.media) 
        #delete associated link
        db.session.delete(link)
        db.session.commit()

def change_header(link_id,header_id):
    link = get_link(link_id)
    if link:
        link.header = header_id
        db.session.add(link)
        db.session.commit()
    
def search_sim_link_paginate(link_text = "",name = "", header_id = None, page = 1):
    PER_PAGE = 30
    if header_id:
        links = db.session.query(Link).filter\
        ((Link.link_text.ilike("%" + link_text+ "%")) 
                                          &(Link.name.ilike("%" + name + "%"))
                                         &(Link.header == header_id) ).paginate(page  = page,per_page = PER_PAGE)
    else:
        links = db.session.query(Link).filter\
        ((Link.link_text.ilike("%" + link_text+ "%")) 
                                        &(Link.name.ilike("%" + name + "%"))).paginate(page = page, per_page = PER_PAGE)

    return links
    
