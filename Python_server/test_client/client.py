from socket import *
import json
#s=socket(AF_INET, SOCK_STREAM)

#s.bind(('',5555))
#m=s.recvfrom(1024)
#recv = json.loads(m)
#print recv
sock = socket(AF_INET, SOCK_STREAM)
sock.setsockopt(SOL_SOCKET,SO_REUSEADDR, 1)
sock.bind(('127.0.0.1', 5555))
sock.listen(5)
while True:
	clientConn, clientAddr = sock.accept()
	print("Got connection from", clientAddr)
	while (1):
		clientNameReq = sock.recv(1024)
		print(json.loads(clientNameReq))
