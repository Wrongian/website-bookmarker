from flask import render_template,Blueprint,redirect,url_for,request
from resources import db
from models.link import get_link,save_link,delete_link,change_header
from models.e_link import e_get_link,e_delete_link,e_change_header
from models.header import link_up, link_down
from models.e_header import e_link_down,e_link_up
from models.media import get_media
from forms import LinkForm,MoveLinkForm
from models.media import save_media
from models.key import key_required

link_blueprint = Blueprint("link",__name__,template_folder="templates",static_folder="static")

@link_blueprint.route("/<int:link_id>",methods = ["GET"])
def see_link(link_id : int):
    #get link obj
    link = get_link(link_id)
    #check if link exists
    if link:
        #get media
        media = get_media(link.media)
        #check if media exists
        if media:
            return render_template("link.html", media_id = media.id,link_text = link.link_text)
        else:
            #add placeholder media
            return render_template("link.html",link_text = link.link_text)
    
    return render_template("not-found.html"),404

@link_blueprint.route("/<int:link_id>/delete",methods = ["POST"])
def remove_link(link_id):
    delete_link(link_id)
    return redirect(request.referrer)

@link_blueprint.route("/hidden/<int:link_id>/delete",methods = ["POST"])
@key_required
def e_remove_link(link_id):
    e_delete_link(link_id)
    return redirect(request.referrer)


        

@link_blueprint.route("/<int:link_id>/move_up",methods = ["POST"])
def move_link_up(link_id):
    link_up(link_id)
    return redirect(request.referrer)

@link_blueprint.route("/<int:link_id>/move_down",methods = ["POST"])
def move_link_down(link_id):
    link_down(link_id)
    return redirect(request.referrer)

@link_blueprint.route("/hidden/<int:link_id>/move_up",methods = ["POST"])
def e_move_link_up(link_id):
    e_link_up(link_id)
    return redirect(request.referrer)

@link_blueprint.route("/hidden/<int:link_id>/move_down",methods = ["POST"])
def e_move_link_down(link_id):
    e_link_down(link_id)
    return redirect(request.referrer)



@link_blueprint.route("/<int:link_id>/move",methods = ["POST"])
def move_to_header(link_id):
    move_link_form = MoveLinkForm()
    header_id = move_link_form.header.data
    change_header(link_id,header_id)
    return redirect(request.referrer)

@link_blueprint.route("/hidden/<int:link_id>/move",methods = ["POST"])
def e_move_to_header(link_id):
    move_link_form = MoveLinkForm()
    header_id = move_link_form.header.data
    e_change_header(link_id,header_id)
    return redirect(request.referrer)