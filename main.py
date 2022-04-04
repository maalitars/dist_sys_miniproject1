import sys
import time
from node import Node

# Comment by Maali Tars: file is based on seminar 8 and I have added my own changes

def start(num_of_nodes):

    sockets = []
    count = 0
    port = 8001
    
    for i in range(num_of_nodes):
        count += 1

        socket = Node(port, i)
        if i == 0:
            socket.access_granted = True

        port += 1
        socket.start()
        sockets.append(socket)

        for i, node1 in enumerate(sockets):
            if len(sockets) > i+1:
                successorNumber = i + 1
            else:
                successorNumber = 0

            if len(sockets) > successorNumber + 1:
                nextSuccessor = sockets[successorNumber + 1]
            else:
                nextSuccessor = sockets[0]
            sockets[i].next_successor = nextSuccessor
            if i==len(sockets) - 1:
                sockets[i].connect_with_node(sockets[0], sockets[0].port)
            else:
                sockets[i].connect_with_node(sockets[i + 1], sockets[i + 1].port)

    sockets = sorted(sockets, key=lambda node: node.id)
    print("Initial ring loaded.")

    waitCommand = 1
    while waitCommand:
        command = input('Enter command (Exit command to quit):').lower()
        if command == 'list':
            sockets = sorted(sockets, key=lambda node: node.id)
            for i in range(len(sockets)):
                print('P' + str(sockets[i].id) + "," + sockets[i].state)
        elif 'time-cs' in command:
            for i in range(len(sockets)):
                sockets[i].resource_timeout = command.split()[1]
        elif 'time-p' in command:
            for i in range(len(sockets)):
                sockets[i].timeout = command.split()[1]


        elif 'exit' == command:
            print('Program exit.')
            sys.exit(1)
        else:
            print('Command not recognized, please try again.')

        time.sleep(0.1)

def usage():
    print('Usage:')
    sys.exit(1)

if len(sys.argv) != 2:
    usage()
else:
    start(int(sys.argv[1]))
