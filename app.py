from flask import render_template
from resources import app,db
import os
from blueprints.main import main_blueprint
from blueprints.media import file_blueprint
from blueprints.link import link_blueprint
from blueprints.header import header_blueprint
from blueprints.category import category_blueprint
from blueprints.search import search_blueprint
from models.category import Category
from backups import backup
#env vars
PORT = os.environ.get("PORT")

#register blueprints
app.register_blueprint(main_blueprint,url_prefix= "/")
app.register_blueprint(file_blueprint,url_prefix= "/file")
app.register_blueprint(link_blueprint,url_prefix="/link")
app.register_blueprint(header_blueprint, url_prefix = "/header")
app.register_blueprint(category_blueprint,url_prefix="/cat")
app.register_blueprint(search_blueprint,url_prefix="/search")

#error handling
@app.errorhandler(404)
def page_not_found(e):
    return render_template("not-found.html"), 404

def create_categories():
    #create categories
    new_category = Category(name="Anime")
    db.session.add(new_category)
    new_category = Category(name = "Utility")
    db.session.add(new_category)
    db.session.commit()

    
#run app
if __name__ == "__main__":
    backup()
    #remove all testing stuff before debugging
    if app.config["IS_DEBUG"] == True:
        db.drop_all()
    #create all tables
    db.create_all()
    #create da categories
    create_categories()
    #start the app
    app.run(debug=True,port=PORT,host="127.0.0.1") #use_reloader = False`` 