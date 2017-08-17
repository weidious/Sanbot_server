#!/usr/bin/env python

import httplib
import sys
import json
#get http server ip
http_server = sys.argv[1]
#create a connection
conn = httplib.HTTPConnection(http_server)

while 1:
		cmd = raw_input('input command (ex. GET index.html): ')
		cmd = cmd.split()
		if cmd[0] == 'exit': #tipe exit to end it
			break
    
    #request command to server
		conn.request(cmd[0], cmd[1])

    #get response from server
		rsp = conn.getresponse()
    
    #print server response and data
		print(rsp.status, rsp.reason)
		data_received = rsp.read()
		data = json.loads(data_received)
		print(data_received)
		for item in data:
			print(item["last_name"])
    
conn.close()
