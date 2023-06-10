from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
import json

#init app
app = Flask(__name__)

#setup app context
ctx = app.app_context()
ctx.push()

#app config
app.secret_key = str(os.urandom(16))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["MEDIA_FOLDER"] = "media"
app.config["DB_LOCATION"] = "instance/test.db"
#make sure this is an empty folder
app.config["BACKUP_FOLDER"] = "instance/backups"

def create_config():
    with open("config.json","w") as file:
        config_dict = {}
        #defaults 
        config_dict["port"] = 5000
        config_dict["num_backups"] = 20
        config_dict["is_debug"] = False
        file.write(json.dumps(config_dict))

def get_config():
    if os.path.isfile("config.json") == False:
        create_config()
    file = open("config.json","r")
    config_dict = dict(json.loads(file.read()))
    app.config["NUM_BACKUPS"] = config_dict["num_backups"]
    app.config["PORT"] = config_dict["port"]
    app.config["IS_DEBUG"] = config_dict["is_debug"]



    

get_config()

#init db
db = SQLAlchemy(app)

