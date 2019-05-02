#!/usr/bin/python3

import socket  

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 444
server_socket.bind((host, port))
server_socket.listen(3) # max number of connections

while True:
    client_socket, address = server_socket.accept()
    print("received connection from {0:s}".format(str(address)))
    message = "Hello! thank you for connecting to the server \r\n"
    client_socket.send(message.encode('utf-8'))
    client_socket.close()
