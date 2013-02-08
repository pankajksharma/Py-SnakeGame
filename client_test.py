from network import client

client1 = client.Client('localhost', 7792)

while True:
	data = client1.socket.recv(256)
	print data