from resources import db,app
import io
import os
from encryption import encrypt_bytes,decrypt_bytes
from models.key import session_key

class Media(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #.png .jpg ,etc
    ext = db.Column(db.String(4), nullable=False)
    #if the file is encrypted
    is_encrypted = db.Column(db.Boolean,nullable = False,server_default = "0")
    #salt
    salt = db.Column(db.LargeBinary, nullable = True)

def save_media(img,is_encrypted = False,key = None):
    #create new media and save to db

    extension = img.filename.rsplit(".", 1)[1].lower()
    if is_encrypted:
        media = Media(ext = extension,is_encrypted = is_encrypted)
    else:
        media = Media(ext = extension,is_encrypted = is_encrypted)
    db.session.add(media)
    db.session.flush()
    media_path = get_media_path(media)

    img_buffer = io.BytesIO(img.read())
    #save unencrypted image
    if media.is_encrypted == False or key == None:
        #save image
        open(media_path,"wb").write(img_buffer.getvalue())
    else:
        #get encrypted bytes
        encrypted_byte_img, salt = encrypt_bytes(img_buffer.getvalue(),key) 
        #write img
        open(media_path,"wb").write(encrypted_byte_img)
        #add salt to the db
        media.salt = salt 

    db.session.add(media)
    db.session.commit()
    return media

def get_decrypted_img(media_id,key):
    media = get_media(media_id)
    if media and media.salt:
        path = get_media_path(media)
        encrypted_bytes = open(path,"rb").read()
        img_bytes = decrypt_bytes(encrypted_bytes,key,media.salt)
        return img_bytes


def get_media(media_id):
    media = db.session.query(Media).filter(media_id == Media.id).first()
    if media:
        return media
    return None


def get_media_path(media):
    #get folder name
    folder_name = app.config["MEDIA_FOLDER"] 
    #make path    
    if media.is_encrypted:
        return folder_name + "/" + str(media.id) + "." + "txt" #all encrypted files are txt
    return folder_name + "/" + str(media.id) + "." +  media.ext


def delete_media(media_id):
    media = get_media(media_id)
    if media:
        #remove the associated file first
        os.remove(get_media_path(media))
        #remove the media
        db.session.delete(media)
        db.session.commit()
    
def get_all_encrypted():
    return db.session.query(Media).filter(Media.is_encrypted == True).all()

def change_key_media(old_key):
    #get all encrypted media
    medias = get_all_encrypted()
    for media in medias:
        #decrypt then reencrypt wiht new key
        media_path = get_media_path(media)
        encrypted_bytes = open(media_path,"rb").read()
        unencrypted_bytes = decrypt_bytes(encrypted_bytes,old_key,media.salt)
        new_bytes,new_salt = encrypt_bytes(unencrypted_bytes,session_key())
        open(media_path,"wb").write(new_bytes)
        #save the relevant info
        media.salt = new_salt
        db.session.add(media)
    db.session.commit()
        