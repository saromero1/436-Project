import socket
from threading import Thread
from datetime import datetime

# Create and Bind a TCP Server Socket
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_name = socket.gethostname()
s_ip = socket.gethostbyname(host_name)
port = 18000
serverSocket.bind((host_name, port))

#Flags
REPORT_REQUEST_FLAG = 0
REPORT_RESPOSE_FLAG = 0
JOIN_REQUEST_FLAG = 0
JOIN_REJECT_FLAG = 0
JOIN_ACCEPT_FLAG = 0
NEW_USER_FLAG = 0
QUIT_REQUEST_FLAG = 0
QUIT_ACCEPT_FLAG = 0
ATTACHEMENT_FLAG = 0
NUMBER = 0
USERNAME = ""
FILENAME = ""
PAYLOAD_LENGTH = 0
PAYLOAD = ""

# Outputs Bound Contents
print("Socket Bound")
print("Server IP: ", s_ip, " Server Port:", port)

# Listens for 10 Users
serverSocket.listen(10)

# Creates a set of clients
client_List = set()
msgList = []
userList = []
client_info = []

# Function to send a message to all connected clients
def broadcast(msg):
    for client_socket in client_List:
        client_socket.send(msg.encode())

def menu_list(my_list, my_tuples):

    result = []
    for t in my_tuples:
        result.extend(list(t))

    result = my_list + result
    my_string = ', '.join(str(x) for x in result)

    return my_string

# Function to constantly listen for an client's incoming messages and sends them to the other clients
def clientWatch(cs):
    adminFlag = 0
    JOIN_REJECT_FLAG = 0
    QUIT_REQUEST_FLAG = 0
    global NUMBER

    #first
    name = cs.recv(1024).decode()
    if name == "REPORT_REQUEST":
        online_users = len(userList)
        client_socket.send(str(online_users).encode())
        client_info.pop()
        if online_users == 0:
            data = '0'
        else:
            data = menu_list(userList, client_info)
        client_socket.send(data.encode())
        QUIT_REQUEST_FLAG = 1
    else:

        if NUMBER > 3:
            JOIN_REJECT_FLAG = 1

        if name in userList:
            JOIN_REJECT_FLAG = 1

        print(JOIN_REJECT_FLAG)
        userList.append(name)
        timestamp = datetime.now().strftime("[%H:%M] ")
        broadcast(timestamp + "Server: " + name + " has joined the chatroom.\n")
        msgList.append(timestamp + "Server: " + name + " has joined the chatroom.\n")
        print("The current list of user is: ", userList)

        # Print chat log when a new user enters

        if (JOIN_REJECT_FLAG != 1):
            for x in msgList:
                # print(x)
                cs.send((x + "\n").encode())

    while True:
        try:
            if JOIN_REJECT_FLAG == 1:
                if NUMBER > 3:
                    cs.send("REJECTED1".encode())
                else:
                    cs.send("REJECTED2".encode())

            # Constantly listens for incoming message from a client 2nd
            msg = cs.recv(1024).decode()

            # if user enters admin as user name set admin Flag to 1, let server and client know admin connected
            if msg == "admin":
                adminFlag = 1
                print("Admin Connected")
                adminMsg = "Type 'viewall' to view all recorded messages"
                cs.send(adminMsg.encode())
                continue

            # if q is entered remove the client from the client list and close connection
            if msg == "q":
                if QUIT_REQUEST_FLAG == 1:
                    print("Client Disconnected")
                    client_List.remove(cs)
                    NUMBER -= 1
                    cs.close()
                    print("The current list of user is: ", userList)
                    break

                else:
                    print("Client Disconnected")
                    client_List.remove(cs)
                    NUMBER -= 1
                    broadcast(timestamp + "Server: " + name + " has left the chatroom.\n")
                    msgList.append(timestamp + "Server: " + name + " has left the chatroom.\n")
                    userList.remove(name)
                    cs.close()
                    print("The current list of user is: ", userList)
                    client_info.pop()
                    break

            if msg == "REPORT_REQUEST":
                cs.send("it worked".encode())

            if msg == "info":
                print("Here is the info mate")
                print(client_List)

        except Exception as e:
            print("Error")
            client_List.remove(cs)
        # splits of last word of message (due to username and time being sent)
        newMsg = msg.split()
        # print(newMsg[-1])
        # checks if user is an admin and has entered 'viewall', sends messageList to the admin client
        if adminFlag and newMsg[-1] == "viewall":
            print("Admin Accessed Chat Log")
            cs.send(("----------Chatlog----------").encode())
            for x in msgList:
                # print(x)
                cs.send((x + "\n").encode())
            cs.send(("\n----------EndLog----------").encode())
            continue

        # Iterates through clients and sends the message to all connected clients
        msgList.append(msg)
        broadcast(msg)
while True:
    # Continues to listen / accept new clients
    client_socket, client_address = serverSocket.accept()
    print(client_address, "Connected!")
    client_info.append(client_address)
    NUMBER += 1
    # Adds the client's socket to the client set
    client_List.add(client_socket)
    # Send a message to all connected clients that a new user has joined
    #broadcast("Server:" + client_address[0] + " has joined the chatroom.\n")
    # Create a thread that listens for each client's messages
    t = Thread(target=clientWatch, args=(client_socket,))
    # Make a daemon so thread ends when main thread ends
    t.daemon = True
    t.start()
