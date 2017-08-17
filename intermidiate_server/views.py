from intermidiate_server import app
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

			print lat
				
@app.route("/only", methods=['POST'])
def register():
					New_user = request.json
					print New_user
					return "200"


