#!/usr/bin/env python

from pymongo import MongoClient
import json
import os
import time

from bson import json_util

client = MongoClient("mongodb://127.0.0.1:27017")
db = client['test']
collection_sprint = db.sprint
collection_store = db.store

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import os
import json
import SocketServer
import urlparse
import subprocess
import re
rootdir = '/Users/chiawei/Downloads/mongodb-osx-x86_64-3.4.6/bin/' #file location
ROUTES = ['/find', '/register']  # empty string for the 'default' match
 

#Create custom HTTPRequestHandler class
class KodeFunHTTPRequestHandler(BaseHTTPRequestHandler):
    
		def _set_headers(self):
			self.send_response(200)
			self.send_header('Content-type', 'application/json')
			self.end_headers()
    #handle GET command
#  	def do_GET(self):
#        try:
#            if self.path.endswith('.json'):
#							with open("rootdir"+self.path) as data_file:    
#								data = json.load(data_file)
#                #send code 200 response
#							self.send_response(200)
#
#                #send header first
#							self.send_header('Content-type','application/json')
#							self.end_headers()

                #send file content to client
#							self.wfile.write(data)
                #f.close()
#							return
            
#        except IOError:
#            self.send_error(404, 'file not found')

		def do_GET(self):
			if self.path.startswith(ROUTES[0]):
				self._set_headers()
				data2 = collection_store.find()[1]
				print(self.path)
				with open(rootdir+self.path) as data_file:    
					data = json.load(data_file)
				print data
				parsed_path = urlparse.urlparse(self.path)
				print "parsed_path=",parsed_path 
				request_id = parsed_path.path
				print "request_id="+request_id 
				response = subprocess.check_output(["python", request_id])
				self.wfile.write(json.dumps(data2,default=json_util.default))
				#write to client

		def do_POST(self):
			if self.path.startswith(ROUTES[1]):
				self._set_headers()
				parsed_path = urlparse.urlparse(self.path)
				request_id = parsed_path.path
				response = subprocess.check_output(["python", request_id])
				self.wfile.write(json.dumps(response))
			##post from react to ryan
		def do_HEAD(self):
			self._set_headers()
    
def run():
    print('http server is starting...')

    #ip and port of servr
    #by default http server port is 80
    server_address = ('127.0.0.1', 80)
    httpd = HTTPServer(server_address, KodeFunHTTPRequestHandler)
    print('http server is running...')
    httpd.serve_forever()
    
if __name__ == '__main__':
    run()
