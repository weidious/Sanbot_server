from local_server import app
from datetime import datetime
import json
import os
import socket
from socket import *
import sys
from flask import render_template, request
from models import User,Store,RFID_Reader,missing
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
				
