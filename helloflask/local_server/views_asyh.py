from test_server import app
from datetime import datetime
from multiprocessing import Pool
import json
import os
import socket
from socket import *
import sys
from flask import render_template, request
from models import User,Store,RFID_Reader,missing
from mongoengine.queryset.visitor import Q
#need further handle update

@app.route("/RFinit", methods=['GET'])
def RFinit():
			try:
				_new = RFID_Reader.objects.get(tagId="11477423")
				if _new:
					return ('already exist',409) #conflict. the ue has to deregister before it can register again
			except RFID_Reader.DoesNotExist:
				rf1 = RFID_Reader(tagId=11477423,product = "Iphone8")
				rf1.save()
				rf2 = RFID_Reader(tagId=12082004,product = "Macbook Pro")
				rf2.save()
				rf3 = RFID_Reader(tagId=11660847,product = "Ipad air")
				rf3.save()
				return "200"

@app.route("/inventory", methods=['POST'])
def inventory():
			in_list = {}
			ss = set()
			in_list['total']=[]
			in_list['miss']=[]
			print type(request.json['tagId'])
			#el = eval(request.json['tagId']) 
			for elem in request.json['tagId']:
				print type(elem)
				foundItem = RFID_Reader.objects.get(tagId=elem)
				print foundItem
				ss.add(elem)
				templist = in_list['total']
				templist.append(json.loads(foundItem.to_json()))
				in_list['total']= templist
			
			for entry in missing.objects:
				entry.delete()
			for product in RFID_Reader.objects:
				print product['tagId']
				if product['tagId'] not in ss:
					miss = missing(tagId=product['tagId'],product=product['product'])
					miss.save()
					product.delete()
					print product['tagId']
					templist = in_list['miss']
					templist.append(json.loads(product.to_json()))
					in_list['miss']= templist
			with open("outfile.json", "w") as file:
				json.dump(in_list, file)
			return "200"


@app.route("/show", methods=['GET'])
def show():
			with open(os.getcwd()+"/outfile.json") as data_file:                                                       
				data = json.load(data_file)

			return json.dumps(data)

@app.route("/getMissing", methods=['GET'])
def getMissing():
				back = missing.objects.get().to_json()
				return back


@app.route("/getTotal", methods=['GET'])
def getTotal():
				back = RFID_Reader.objects.get().to_json()
				return back


@app.route("/init", methods=['GET'])
def init():
				try:
					st = Store.objects.get(physical_address="101 winter park, college station, tx 77840")
					if st:
						return ('already exist',409) #conflict. the ue has to deregister before it can register again
				except Store.DoesNotExist:
					store1 = Store(physical_address="101 winter park, college station, tx 77840",client_ip = "127.0.0.1",latitudeMin = 29.5,latitudeMax=31.5,longitudeMin=-96.5,longitudeMax= -94.5)
					store1.save()
					store2 = Store(physical_address="6480 sprint pkwy #13, overland park, ks 66251",client_ip = "10.78.198.143",latitudeMin = 37.5,latitudeMax=39.5,longitudeMin=	-95.5,longitudeMax= -93.5)
					store2.save()
					return "200"


@app.route("/", methods=['GET'])
def basic():
			print "hi"
			return "200"

def soc(dic):
			print "in soc"
			cs = socket(af_inet, sock_stream)  
			cs.setsockopt(sol_socket, so_reuseaddr, 1)
      #cs.setsockopt(sol_socket, so_broadcast, 1)
			cs.connect((dic["client_ip"], 5555))
			print "connected" 			
			cs.send(json.dumps(dic)) 			
			cs.close()


@app.route("/find", methods=['GET'])
def find():
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
			
			pool = Pool(processes=1)
			pool.apply_async(soc, res, ())
			return json.dumps(res)
				
@app.route("/register", methods=['POST'])
def register():
				print "In "+str(datetime.now())
				#phoneList = []
				#for mac, nu in request.json['phone']:
				#new_phone = phone(macAddress = request.json['phone']['macAddress'],phoneNumber =request.json['phone']['phoneNumber'])
				#phoneList.append(new_phone)
				try:
					ue = User.objects.get(email=request.json["email"])
					if ue:
						return ('Already exist',409) #conflict. The ue has to deregister before it can register again
				except User.DoesNotExist:
					New_user = User(firstName =request.json['firstName'],lastName = request.json['lastName'],email = request.json['email'],physicalDisability= request.json['physicalDisability'], language= request.json['language'],phoneMacAddress = request.json['phoneMacAddress'],phoneNumber = request.json['phoneNumber'])
					New_user.save()
				
					print "Out "+str(datetime.now())
					return "200"


