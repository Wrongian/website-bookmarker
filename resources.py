from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

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
app.config["IS_DEBUG"] = True
app.config["NUM_BACKUPS"] = 20
app.config["PORT"] = 5001


#init db
db = SQLAlchemy(app)

