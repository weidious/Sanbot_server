from tmp_server import app
from datetime import datetime
import json
import os
import socket
from socket import *
import sys
from flask import render_template, request
from models import bot 
from mongoengine.queryset.visitor import Q
#need further handle update

@app.route("/", methods=['GET'])
def basic():
			print "hi"
			return "200"


@app.route("/test", methods=['GET'])
def tt():
			print "hi2"
			return "200"


@app.route("/relay", methods=['POST'])
def relay():
			print request.json['client_ip']	
			cs = socket(AF_INET, SOCK_STREAM)
			cs.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
      #cs.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
			cs.connect((request.json['client_ip'], 5555))
			#cs.connect(("127.0.0.1", 5555))
			cs.send(json.dumps(res))
			cs.close()
			return "200"
