from resources import db
from sqlalchemy.sql import func,expression
from sqlalchemy import desc,asc
from sqlalchemy.orm import relationship
from sqlalchemy.ext.orderinglist import ordering_list, count_from_0
from models.link import Link,delete_link,get_link

class Header(db.Model):
    id = db.Column(db.Integer,primary_key= True)
    creation_date = db.Column(db.DateTime(timezone=True),nullable = False,server_default=func.now()) 
    #what links it sotres
    links = relationship("Link",order_by = "Link.position",collection_class=ordering_list("position"))
    #what category its in
    category = db.Column(db.Integer, db.ForeignKey("category.id"),nullable = False)
    #name of the header
    name = db.Column(db.String,nullable = False)
    #position in the category
    position = db.Column(db.Integer)

    
def get_header(header_id):
    category = db.session.query(Header).filter(Header.id == header_id).first()
    if category:
        return category
    return None

def add_header(category_id,name):
    new_header = Header(category = category_id,name = name)
    db.session.add(new_header)
    db.session.commit()
    return new_header

def get_links(header_id):
    header =  get_header(header_id)
    return header.links

def delete_header(header_id):
    header = get_header(header_id)
    if header:
        for link in header.links:
            delete_link(link.id)
        db.session.delete(header) 
        db.session.commit()
    
def rename_header(header_id,new_name):
    header = get_header(header_id)
    if header:
        header.name = new_name
        db.session.add(header)
        db.session.commit()

    
def link_up(link_id):
    link = get_link(link_id)
    if link:
        header_id = link.header
        header = get_header(header_id)
        if header:
            pos = header.links.index(link)
            link = header.links.pop(pos) 
            header.links.insert(pos+1,link)
            #check length later
            db.session.commit()

def link_down(link_id):
    link = get_link(link_id)
    if link:
        header_id = link.header
        header = get_header(header_id)
        if header:
            pos = header.links.index(link)
            link = header.links.pop(pos) 
            if pos-1 >=0: 
                header.links.insert(pos-1,link)
            #check length later
            db.session.commit()

def change_category(header_id, category_id):
    header = get_header(header_id)
    if header:
        header.category = category_id
        db.session.add(header) 
        db.session.commit()



