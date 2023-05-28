from flask import Blueprint,render_template, request,jsonify,request
from models.link import search_sim_link_paginate
from models.e_link import e_search_sim_link_paginate
from forms import SearchForm, Forms
from models.category import get_category_choices,get_header_choices,get_category
from models.header import get_header
from models.e_category import e_get_category
from models.e_header import e_get_header
from models.key import key_required


search_blueprint = Blueprint("search",__name__,template_folder="template",static_folder="static")

@search_blueprint.route("/",methods = ["GET","POST"])
def search():
    #create form
    search_form = SearchForm()
    #for sending the search queries
    if request.method == "POST":
        #get form data
        link_text_search = search_form.link_text.data
        name_search = search_form.name.data

        #pagination
        page = search_form.page.data
        if not page:
            page = 1
            
        pagination = search_sim_link_paginate(link_text=link_text_search,name=name_search,page = page)
        links = pagination.items

        #make search data 
        search_data = get_search_data(links)
        return jsonify({
            "search_results": render_template("search-results.html",search_data = search_data,length = len(search_data))
        }) 
    #normal get request
    else:
        #populate forms
        forms = Forms({
        "search_form": search_form
        })
        return render_template("search.html",forms = forms)

@search_blueprint.route("/hidden",methods = ["GET","POST"])
@key_required
def e_search():
    #create form
    search_form = SearchForm()
    #for sending the search queries
    if request.method == "POST":
        #get form data
        link_text_search = search_form.link_text.data
        name_search = search_form.name.data
        #pagination
        page = search_form.page.data
        if not page:
            page = 1
            
        links = e_search_sim_link_paginate(link_text=link_text_search,name=name_search,page = page)

        #make search data 
        search_data = e_get_search_data(links)
        return jsonify({
            "search_results": render_template("search-results.html",search_data = search_data,length = len(search_data))
        }) 
    #normal get request
    else:
        #populate forms
        forms = Forms({
        "search_form": search_form
        })
        return render_template("search.html",forms = forms,is_encrypted=True)

def get_search_data(links):
    def search_data(link):
        header_id = link.header
        header = get_header(header_id)
        category_id = header.category
        category = get_category(category_id)
        return {
            "link":link,
            "header":header,
            "category": category
        }
    return list(map(search_data,links))


def e_get_search_data(links):
    def search_data(link):
        header_id = link.header
        header = e_get_header(header_id)
        category_id = header.category
        category = e_get_category(category_id)
        return {
            "link":link,
            "header":header,
            "category": category
        }
    return list(map(search_data,links))

