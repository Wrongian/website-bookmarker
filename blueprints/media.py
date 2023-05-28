from flask import Blueprint,render_template,send_file
from models.media import get_media, get_media_path,get_decrypted_img
from models.key import session_key
import io

file_blueprint = Blueprint("media",__name__,template_folder="templates",static_folder="static")

PLACEHOLDER_PATH="bongbong.gif"
@file_blueprint.route("/<int:media_id>")
def see_media(media_id):
    media = get_media(media_id)
    #check if exists
    if media:
        if media.is_encrypted and session_key():
            return send_file(io.BytesIO(get_decrypted_img(media_id,session_key())),mimetype="image/"+media.ext)
        else:
            #get the path
            media_path = get_media_path(media)
            #send the file to the user
            return send_file(media_path)
    else:
        #send the placeholder image instead
        return send_file(PLACEHOLDER_PATH)


@file_blueprint.route("/alt_media")
def alt_media():
    return send_file(PLACEHOLDER_PATH)


    