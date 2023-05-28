from flask import Blueprint,redirect,url_for,request
from models.header import delete_header,rename_header,change_category
from models.e_header import e_delete_header,e_rename_header,e_change_category
from forms import RenameHeaderForm,MoveHeaderForm
from models.category import header_down,header_up
from models.e_category import e_header_down,e_header_up
from models.key import session_key,key_required

header_blueprint = Blueprint("header",__name__,template_folder="templates",static_folder="static")


@header_blueprint.route("<int:header_id>/delete",methods = ["POST"])
def remove_header(header_id):
    delete_header(header_id)
    return redirect(request.url)
    

@header_blueprint.route("<int:header_id>/rename",methods = ["POST"])
def change_header_name(header_id):
    header_form = RenameHeaderForm()
    rename_header(header_id,header_form.new_name.data)
    return redirect(request.referrer)

@header_blueprint.route("/<int:header_id>/move_up",methods = ["POST"])
def move_link_up(header_id):
    header_up(header_id)
    return redirect(request.referrer)

@header_blueprint.route("/<int:header_id>/move_down",methods = ["POST"])
def move_link_down(header_id):
    header_down(header_id)
    return redirect(request.referrer)

@header_blueprint.route("/<int:header_id>/move",methods = ["POST"])
def move_to_category(header_id):
    move_header_form = MoveHeaderForm()
    category_id = move_header_form.category.data
    change_category(header_id,category_id)
    return redirect(request.referrer)


@header_blueprint.route("/hidden/<int:header_id>/delete",methods = ["POST"])
@key_required
def e_remove_header(header_id):
    e_delete_header(header_id)
    return redirect(request.url)
    

@header_blueprint.route("/hidden/<int:header_id>/rename",methods = ["POST"])
@key_required
def e_change_header_name(header_id):
    header_form = RenameHeaderForm()
    e_rename_header(header_id,header_form.new_name.data)
    return redirect(request.referrer)

@header_blueprint.route("/hidden/<int:header_id>/move_up",methods = ["POST"])
@key_required
def e_move_link_up(header_id):
    e_header_up(header_id)
    return redirect(request.referrer)

@header_blueprint.route("/hidden/<int:header_id>/move_down",methods = ["POST"])
@key_required
def e_move_link_down(header_id):
    e_header_down(header_id)
    return redirect(request.referrer)

@header_blueprint.route("/hidden/<int:header_id>/move",methods = ["POST"])
@key_required
def e_move_to_category(header_id):
    move_header_form = MoveHeaderForm()
    category_id = move_header_form.category.data
    e_change_category(header_id,category_id)
    return redirect(request.referrer)