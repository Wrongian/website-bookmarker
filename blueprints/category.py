from flask import render_template, Blueprint, redirect,url_for,session
from resources import db
from forms import LinkForm,HeaderForm,Forms,RenameHeaderForm, MoveHeaderForm,MoveLinkForm,CategoryForm
from models.media import save_media
from models.link import save_link 
from models.category import Category,get_category,get_headers,get_header_choices,get_category_choices,add_category,delete_category
from models.header import add_header
from models.key import key_required,session_key
from models.e_category import e_get_category,e_add_category,e_get_headers,e_get_header_choices,e_get_category_choices,e_delete_category
from models.e_link import e_save_link
from models.e_header import e_add_header

category_blueprint = Blueprint("category",__name__,template_folder="templates",static_folder="static")

@category_blueprint.route("/<int:category_id>")
def see_category(category_id):
    #get category
    category = get_category(category_id)
    #create form to send
    link_form = LinkForm()
    header_form = HeaderForm()
    rename_header_form = RenameHeaderForm()
    move_header_form = MoveHeaderForm()
    move_link_form = MoveLinkForm()
    forms = Forms({
        "link_form" :  link_form,
        "header_form" : header_form,
        "rename_header_form" : rename_header_form,
        "move_header_form" : move_header_form,
        "move_link_form" : move_link_form
    })
    #get the choices
    link_form.header.choices = get_header_choices(category_id)
    move_header_form.category.choices = get_category_choices()
    move_link_form.header.choices = get_header_choices(category_id)
    #check if category exists
    if category:
        #get headers
        headers = get_headers(category.id)
        return render_template("category.html",headers_list = headers,category = category,forms = forms)
    return render_template("not-found.html"),404

@category_blueprint.route("/hidden/<int:category_id>")
@key_required
def hidden_category(category_id):
    key = session_key()
    #fix later
    #get category
    category = e_get_category(category_id)
    #create form to send
    link_form = LinkForm()
    header_form = HeaderForm()
    rename_header_form = RenameHeaderForm()
    move_header_form = MoveHeaderForm()
    move_link_form = MoveLinkForm()
    forms = Forms({
        "link_form" :  link_form,
        "header_form" : header_form,
        "rename_header_form" : rename_header_form,
        "move_header_form" : move_header_form,
        "move_link_form" : move_link_form
    })
    #get the choices
    link_form.header.choices = e_get_header_choices(category_id)
    move_header_form.category.choices = e_get_category_choices()
    move_link_form.header.choices = e_get_header_choices(category_id)
    #check if category exists
    if category:
        #get headers
        headers = e_get_headers(category.id)
        return render_template("category.html",headers_list = headers,category = category,forms = forms,is_encrypted =True)
    return render_template("not-found.html"),404
     

@category_blueprint.route("/<int:category_id>/new_link",methods = ["POST"])
def new_link(category_id):
    link_form = LinkForm()
    file = link_form.media.data
    link_name = link_form.name.data
    header_id = link_form.header.data
    if file:
        #save file
        new_media = save_media(file)
    else:
        new_media = None
    link_text = link_form.link.data
    save_link(link_text,header_id,name = link_name,media  = new_media)#todo: error checking for category
    return redirect(url_for("category.see_category",category_id = category_id))

@category_blueprint.route("/hidden/<int:category_id>/new_link",methods = ["POST"])
@key_required
def e_new_link(category_id):
    link_form = LinkForm()
    file = link_form.media.data
    link_name = link_form.name.data
    header_id = link_form.header.data
    if file:
        #save file
        new_media = save_media(file,is_encrypted=True,key=session["key"])
    else:
        new_media = None
    link_text = link_form.link.data
    e_save_link(link_text,header_id,name = link_name,media  = new_media)#todo: error checking for category
    return redirect(url_for("category.hidden_category",category_id = category_id))



@category_blueprint.route("/<int:category_id>/new_header",methods = ["POST"])
def new_header(category_id):
    header_form = HeaderForm()
    header_name = header_form.name.data
    add_header(category_id,header_name)
    return redirect(url_for("category.see_category",category_id = category_id))

@category_blueprint.route("/hidden/<int:category_id>/new_header",methods = ["POST"])
@key_required
def e_new_header(category_id):
    header_form = HeaderForm()
    header_name = header_form.name.data
    e_add_header(category_id,header_name)
    return redirect(url_for("category.hidden_category",category_id = category_id))



@category_blueprint.route("/new_category",methods = ["POST"])
def create_new_category():
    category_form = CategoryForm()
    name = category_form.name.data
    file = category_form.media.data
    if file:
        #save file
        new_media = save_media(file)
    else:
        new_media = None
    add_category(name,new_media)
    return redirect(url_for("main.index"))

@category_blueprint.route("/new_e_category",methods = ["POST"])
@key_required
def create_new_e_category():
    category_form = CategoryForm()
    name = category_form.name.data
    file = category_form.media.data
    if file:
        #save file
        new_media = save_media(file,is_encrypted=True,key=session["key"])
    else:
        new_media = None
    e_add_category(name,new_media)
    return redirect(url_for("main.alt_index"))
