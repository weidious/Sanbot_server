from flask import Flask
from flask_mongoengine import MongoEngine

application = app = Flask(__name__)
#app.config.from_object('config')
#app.config["MONGODB_SETTINGS"] = {'DB': "Robot"}
db = MongoEngine(app)
#class phone(db.EmbeddedDocument):
#		macAddress = db.StringField(max_length = 255)
#		phoneNumber = db.StringField(max_length = 255)

class User(db.Document):
		firstName = db.StringField(max_length=255, required=True)
		lastName = db.StringField(max_length=255, required=True)
		email = db.StringField(max_length=255, required=True)
		physicalDisability = db.StringField(max_length=255)
		language = db.StringField(max_length = 255)
		phoneMacAddress = db.StringField(max_length = 255)
		phoneNumber = db.StringField(max_length = 255)

		
class Store(db.Document):
		physical_address = db.StringField(max_length=511, required=True)
		client_ip = db.StringField(max_length=255, required=True)
		latitudeMin = db.FloatField(required = True)
		latitudeMax = db.FloatField(required = True)
		longitudeMin = db.FloatField(required = True)
		longitudeMax = db.FloatField(required = True)

class RFID_Reader(db.Document):
		tagId = db.FloatField(required = True)
		product = db.StringField(max_length=255, required=True)



class missing(db.Document):
		tagId = db.FloatField(required = True)
		product = db.StringField(max_length=255, required=True)

from datetime import datetime
import json
import os
import socket
from socket import *
import sys
from flask import render_template, request
from mongoengine.queryset.visitor import Q
#need further handle update

@app.route("/", methods=['GET'])
def basic():
			print "hi"
			return "200"


@app.route("/relay", methods=['POST'])
def relay():
			lat = request.args.get('lat')
			print lat
			lng = request.args.get('lng')
			print lng
			_email = request.args.get('email')
			print _email
			foundStore = Store.objects.get(Q(latitudeMin__lt=lat)&Q(latitudeMax__gt=lat)& Q(longitudeMin__lt=lng)&Q(longitudeMax__gt=lng))
			foundUser = User.objects.get(email = _email)
			res = json.loads(foundUser.to_json());
			res["client_ip"]=foundStore.client_ip
			
			cs = socket(AF_INET, SOCK_STREAM)  
			cs.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
      #cs.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
			cs.connect((foundStore.client_ip, 5555))
			print "connected" 			
			cs.send(json.dumps(res)) 			
			cs.close()
			return json.dumps(res)
				


import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from werkzeug.contrib.fixers import ProxyFix

application.wsgi_app = ProxyFix(application.wsgi_app)

if __name__ == "__main__":
    application.run(threaded=True)


