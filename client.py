#!/usrbin/python3

import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 444
client.connect((host, port))
message = client.recv(1024) # max number of bytes
client.close()
print(message.decode('utf-8'))
