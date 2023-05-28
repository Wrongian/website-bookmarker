from flask import Blueprint,render_template,request,redirect,url_for,session,send_from_directory,send_file
from forms import CategoryForm,Forms,DeleteCategoryForm,EnterKeyForm,MakeKeyForm,ChangeKeyForm
from models.category import get_all_categories,delete_category,get_category_choices
from models.key import verify_key,create_key,get_key,key_required,delete_session_key,change_key,session_key
from models.e_category import e_get_all_categories,e_get_category_choices,e_delete_category,change_key_category
from models.e_header import EHeader,change_key_header
from models.e_link import ELink,change_key_link
from models.media import change_key_media

main_blueprint = Blueprint("main",__name__,template_folder="templates",static_folder="static")

@main_blueprint.route("/",methods = ["GET"])
def index():
    #get forms
    category_form = CategoryForm()
    forms = Forms(
        {
            "category_form" : category_form
        }
    )
    #get categories 
    categories = get_all_categories()
    return render_template("startpage.html", forms = forms, categories = categories)


@main_blueprint.route("/delete_category",methods = ["GET","POST"])
def remove_category():
    delete_category_form = DeleteCategoryForm()
    if request.method == "POST":
        category_id = delete_category_form.category.data
        delete_category(category_id)
        redirect(url_for("main.index"))
    delete_category_form.category.choices = get_category_choices()
    forms = Forms({
        "delete_category_form" : delete_category_form
    })
    return render_template("delete_category.html",forms = forms) 

@main_blueprint.route("/hidden/delete_category",methods = ["GET","POST"])
@key_required
def e_remove_category():
    delete_category_form = DeleteCategoryForm()
    if request.method == "POST":
        category_id = delete_category_form.category.data
        e_delete_category(category_id)
        redirect(url_for("main.alt_index"))
    delete_category_form.category.choices = e_get_category_choices()
    forms = Forms({
        "delete_category_form" : delete_category_form
    })
    return render_template("delete_category.html",forms = forms,is_encrypted = True)

@main_blueprint.route("/key/enter",methods = ["GET","POST"])
def enter_key():
    #delete pass and enter pass 
    enter_key_form = EnterKeyForm()
    if get_key() == None:
        #if no key found, make one
        return redirect(url_for("main.make_key"))
    if enter_key_form.validate_on_submit():
        key_str = enter_key_form.key.data
        #save it into the session
        session["key"] = key_str
        return redirect(request.referrer)
    #get request
    forms = Forms({
        "enter_key_form": enter_key_form
    })
    return render_template("enter-key.html",forms = forms)

@main_blueprint.route("/key/make",methods = ["GET","POST"])
def make_key():
    make_key_form = MakeKeyForm()
    if get_key() != None:
        return redirect(url_for("main.index"))
    if make_key_form.validate_on_submit(): 
        #make key
        key_str = make_key_form.key.data
        create_key(key_str)
        #save key to session
        session["key"] = key_str
        redirect(request.referrer)
    #get
    forms = Forms({
        "make_key_form": make_key_form
    })
    return render_template("create-key.html",forms = forms)

@main_blueprint.route("/alt",methods = ["GET"])
@key_required
def alt_index():
    #get forms
    category_form = CategoryForm()
    forms = Forms(
        {
            "category_form" : category_form
        }
    )
    #get categories 
    categories = e_get_all_categories() 
    return render_template("startpage.html", forms = forms, categories = categories,is_encrypted = True)

@main_blueprint.route("/delete_key",methods = ["GET"])
@key_required
def remove_session_key():
    delete_session_key()
    return redirect(url_for("main.index"))

@main_blueprint.route("/change_key",methods = ["GET","POST"])
@key_required
def modify_key():
    change_key_form = ChangeKeyForm()

    if get_key() == None:
        redirect(url_for("main.make_key"))
    
    if change_key_form.validate_on_submit():
        old_key = session_key()
        new_key = change_key_form.key.data
        change_key(new_key)
        change_key_category()
        change_key_header()
        change_key_link()
        change_key_media(old_key)
        return redirect(request.url)

    forms = Forms({
        "change_key_form":change_key_form
    })
    return render_template("change-key.html",forms = forms)
        
