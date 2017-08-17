from flask import Flask
from flask_mongoengine import MongoEngine

application = app = Flask(__name__)
#app.config.from_object('config')
#app.config["MONGODB_SETTINGS"] = {'DB': "Robot"}
db = MongoEngine(app)

import views

