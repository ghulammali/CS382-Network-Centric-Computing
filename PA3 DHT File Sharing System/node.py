import socket
import hashlib
import threading
import os
import time

global nodeList
nodeList = []

global host
host = "localhost"
maxNodes = 100
sleeptime = 5


class node:
	def __init__(self, node_Port):
		self.key = calculate_nodehash(host + str(node_Port))
		self.nodeIP = host
		self.port = node_Port
		self.predeccessor = node_Port
		self.successor = node_Port
		#self.nodeHash = node_hash
		self.second_successor = node_Port
		self.files = []


def clientMenu(node):
	while True:
		inputUser = input("Enter 1 to print node links.\nEnter 2 to go to File Mode.\nEnter 0 to exit.\n")
		if inputUser =="0":
			LeaveNetwork(node)
			break
		elif inputUser=="1":
			print("Your node key is: ", node.key, " with port: ",node.port)
			print("Your Predeccessor node key is: ", calculate_nodehash(host + str(node.predeccessor))," with port: ", node.predeccessor)
			print("Your Successor node key is: ", calculate_nodehash(host + str(node.successor))," with port: ", node.successor)
			print("Your 2nd Successor node key is: ", calculate_nodehash(host + str(node.second_successor))," with port: ", node.second_successor)
		elif inputUser=="2":
			print("Oops.... \nLooks like this feature isn't available at the moment.\n")
		else:
			print("Invalid input.. lol")


def calculate_nodehash(input):
	#key = host + str(port)
	key = input.encode('utf-8')
	return int(hashlib.sha1(key).hexdigest(), 16) % maxNodes


# def calculate_filehash(filename):
# 	filename = filename.encode('utf-8')
# 	key = hashlib.sha256(filename)
# 	key = key.hexdigest()
# 	return key


def newClient(node, port):
	soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	soc.connect((host, int(port)))
	soc.send('one node only'.encode('utf-8'))
	response = soc.recv(1024).decode('utf-8')
	if response == 'Do':
		node.successor = port
		node.predeccessor = port
		soc.send('A node joined'.encode('utf-8'))
		response = soc.recv(1024)
		soc.send(str(node.port).encode('utf-8'))
		soc.close()
	if response == 'Dont':
		soc.send('return predeccessor'.encode('utf-8'))
		predeccessor_port = soc.recv(1024).decode('utf-8')
		predeccessor_port = int(predeccessor_port)
		predeccessorKey = calculate_nodehash(host+str(predeccessor_port))
		othernodeKey = calculate_nodehash(host+str(port))
		
		# either between the successor and predeccessor or vice versa
		if (node.key < othernodeKey) and (((node.key > predeccessorKey) and (othernodeKey > predeccessorKey)) or ((node.key < predeccessorKey) and (othernodeKey < predeccessorKey))):
			locationInNetwork(node, port, soc, predeccessor_port)

		elif (node.key > othernodeKey) and (predeccessorKey > othernodeKey) and (node.key > predeccessorKey):
			locationInNetwork(node, port, soc, predeccessor_port)
		#if not then repeat above step at successor of this node
		else:
			soc.send('return successor'.encode('utf-8'))
			succ = soc.recv(1024).decode('utf-8')
			succ = int(succ)
			soc.close()
			newClient(node, succ)


def setupSecondSuccessor(node):
	soc = socket.socket()
	soc.connect((host, int(node.successor)))
	soc.send('get second successor'.encode('utf-8'))
	#print("get second successor sent")
	second = soc.recv(1024).decode('utf-8')
	node.second_successor = int(second)
	#print("get second successor received")
	soc.close()
	#check if only two nodes
	soc = socket.socket()
	soc.connect((host, int(node.predeccessor)))
	soc.send('return predeccessor'.encode('utf-8'))
	#print("return predeccessor sent")
	pred = soc.recv(1024).decode('utf-8')
	#print("return predeccessor received")
	soc.close()
	if (node.port!=int(pred)):
		soc = socket.socket()
		soc.connect((host, int(pred)))
		soc.send('new second successor'.encode('utf-8'))
		#print("new second successor sent")
		response = soc.recv(1024)
		#print("new second successor received")
		soc.send(str(node.port).encode('utf-8'))
		soc.close()


#predecessor of predecessor
def updateSecondSuccessor(node):
	soc = socket.socket()
	port = node.successor
	soc.connect((host, port))
	soc.send('return successor'.encode('utf-8'))
	new_second_succ = int(soc.recv(1024).decode('utf-8'))
	soc.close()
	node.second_successor = new_second_succ


def locationInNetwork(node, othernodePort, soc, pred_port):
	soc.send('new predecessor'.encode('utf-8'))
	#print("new predecessor sent")
	response = soc.recv(1024)
	#print("new predecessor received")
	soc.send(str(node.port).encode('utf-8'))
	node.successor = int(othernodePort)
	soc.close()
	soc2 = socket.socket()
	soc2.connect((host, int(pred_port)))
	#print("new successor sent")
	soc2.send('new successor'.encode('utf-8'))
	response = soc2.recv(1024).decode('utf-8')
	#print("new successor received")
	soc2.send(str(node.port).encode('utf-8'))
	node.predeccessor = pred_port
	soc2.close()
	soc2 = socket.socket()
	soc2.connect((host, int(pred_port)))
	#print("update 2nd successor sent")
	soc2.send('update 2nd successor'.encode('utf-8'))
	response = soc2.recv(1024)
	#print("update 2nd successor received")
	soc2.send(str(node.successor).encode('utf-8'))
	soc2.close()


def LeaveNetwork(node):
	#one node
	if node.port==node.successor and node.port==node.predeccessor:
		print("\nA node left, Network is now empty.")
		os._exit(0)
		
	#2 nodes
	elif node.successor == node.predeccessor:
		soc = socket.socket()
		soc.connect((host, node.successor))
		soc.send('A node left'.encode('utf-8'))
		response = soc.recv(1024)
		soc.close()
		print("\nA node left, Only One node left in Network.")
		os._exit(0)
		
	#more than 2 nodes
	else:
		print("\nA node is leaving, reconfiguring nodes in Network.")
		soc = socket.socket()
		soc.connect((host, node.successor))
		soc.send('predeccessor leaving'.encode('utf-8'))
		response = soc.recv(1024)
		soc.send(str(node.port).encode('utf-8'))
		response = soc.recv(1024)
		soc.send(str(node.predeccessor).encode('utf-8'))
		response = soc.recv(1024)
		soc.close()
		soc = socket.socket()
		soc.connect((host, node.predeccessor))
		soc.send('successor leaving'.encode('utf-8'))
		response = soc.recv(1024)
		soc.send(str(node.successor).encode('utf-8'))
		response = soc.recv(1024)
		if node.second_successor==node.port:
			soc.send(str(node.successor).encode('utf-8'))
		else:
			soc.send(str(node.second_successor).encode('utf-8'))
		response = soc.recv(1024)
		soc.close()
		print("\nA node left, Network reconfigured Successfully.")
		os._exit(0)
		

def pingSuccessor(node):
	ping = 0
	while True:
		if node.port==node.successor and node.port==node.predeccessor:
			pass
		else:
			soc = socket.socket()
			try:
				soc.connect((host,int(node.successor)))
				ping = 0
				soc.close()
			except socket.error:
				ping += 1
				if ping >= 3:
					print("A node just went down in Network.\nReconfiguring nodes in Network.")
					node.successor = node.second_successor
					updateSecondSuccessor(node)
					soc = socket.socket()
					soc.connect((host, node.successor))
					soc.send('new predecessor'.encode('utf-8'))
					response = soc.recv(1024)
					soc.send(str(node.port).encode('utf-8'))
					soc.close()
					soc = socket.socket()
					soc.connect((host, node.predeccessor))
					soc.send('update 2nd successorleaving'.encode('utf-8'))
					soc.close()
					print("\nNetwork reconfigured Successfully.")
					ping = 0
		time.sleep(sleeptime)


def clientThread(node):
	t = threading.Thread(target=pingSuccessor, args=(node,))
	t.daemon = True
	t.start()
	print("\nWelcome to DHT Network... ^_^\n")
	clientMenu(node)
			

def serverThread(clientSock, serverNode):
	#otherport = int(otherport)
	while True:
		msg = clientSock.recv(1024).decode('utf-8')
		if msg == 'one node only':
			if serverNode.port==serverNode.predeccessor and serverNode.port==serverNode.successor:
				clientSock.send('Do'.encode('utf-8'))
			else:
				clientSock.send('Dont'.encode('utf-8'))
		if msg == 'A node joined':
			clientSock.send('ok'.encode('utf-8'))
			port = clientSock.recv(1024).decode('utf-8')
			port = int(port)
			serverNode.successor = port
			serverNode.predeccessor = port
		if msg == 'A node left':
			clientSock.send('ok'.encode('utf-8'))
			serverNode.predeccessor = serverNode.port
			serverNode.successor = serverNode.port
		if msg == 'return predeccessor':
			clientSock.send(str(serverNode.predeccessor).encode('utf-8'))
		if msg == 'return successor':
			clientSock.send(str(serverNode.successor).encode('utf-8'))
		if msg == 'new predecessor':
			clientSock.send('ok'.encode('utf-8'))
			pred = clientSock.recv(1024).decode('utf-8')
			serverNode.predeccessor = int(pred)
		if msg == 'predeccessor leaving':
			clientSock.send('ok'.encode('utf-8'))
			nodeleft = clientSock.recv(1024).decode('utf-8')
			nodeleft = int(nodeleft)
			clientSock.send('ok'.encode('utf-8'))
			pred = clientSock.recv(1024).decode('utf-8')
			pred = int(pred)
			clientSock.send('ok'.encode('utf-8'))
			serverNode.pred = pred
			if nodeleft == serverNode.second_successor:
				serverNode.second_successor = serverNode.port
		if msg == 'new second successor':
			clientSock.send('ok'.encode('utf-8'))
			r = clientSock.recv(1024).decode('utf-8')
			serverNode.second_successor = int(r)
		if msg == 'successor leaving':
			clientSock.send('ok'.encode('utf-8'))
			succ = clientSock.recv(1024).decode('utf-8')
			serverNode.successor = int(succ)
			clientSock.send('ok'.encode('utf-8'))
			sec = clientSock.recv(1024).decode('utf-8')
			serverNode.second_successor = int(sec)
			clientSock.send('ok'.encode('utf-8'))
			soc = socket.socket()
			soc.connect((host, int(serverNode.predeccessor)))
			soc.send('update 2nd successorleaving'.encode('utf-8'))
			soc.close()
		if msg == 'new successor':
			clientSock.send('ok'.encode('utf-8'))
			succ = clientSock.recv(1024).decode('utf-8')
			serverNode.successor = int(succ)
		if msg == 'get second successor':
			clientSock.send(str(serverNode.successor).encode('utf-8'))
		if msg == 'update 2nd successor':
			clientSock.send('ok'.encode('utf-8'))
			secsuc = clientSock.recv(1024).decode('utf-8')
			serverNode.second_successor = int(secsuc)
		if msg == 'update 2nd successorleaving':
			updateSecondSuccessor(serverNode)


def main():
	port = int(input("Enter port of this node: "))
	object = node(port)
	print("Key of this node is: " + str(object.key))

	s = socket.socket()
	s.bind((host,port))
	s.listen(maxNodes)

	print("Enter port of another known node in Network, else enter 0: ")
	check = int(input())
	if check != 0:
		newClient(object, check)
		setupSecondSuccessor(object)

	tc = threading.Thread(target=clientThread, args=(object,))
	tc.daemon = True
	tc.start()
	while True:
		client, addr = s.accept()
		ts = threading.Thread(target=serverThread, args=(client, object))
		ts.daemon = True
		ts.start()
	s.close()
	
if __name__=="__main__":
	main()