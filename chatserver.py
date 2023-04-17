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

# Function to send a message to all connected clients
def broadcast(msg):
    for client_socket in client_List:
        client_socket.send(msg.encode())



# Function to constantly listen for an client's incoming messages and sends them to the other clients
def clientWatch(cs):
    adminFlag = 0
    name = cs.recv(1024).decode()
    timestamp = datetime.now().strftime("[%H:%M] ")
    broadcast(timestamp + "Server: " + name + " has joined the chatroom.\n")
    while True:
        try:
            # Constantly listens for incoming message from a client
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
                print("Client Disconnected")
                client_List.remove(cs)
                broadcast(timestamp + "Server: " + name + " has left the chatroom.\n")
                cs.close()

                break
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
    # Adds the client's socket to the client set
    client_List.add(client_socket)

    # Send a message to all connected clients that a new user has joined
    #broadcast("Server:" + client_address[0] + " has joined the chatroom.\n")

    # Create a thread that listens for each client's messages
    t = Thread(target=clientWatch, args=(client_socket,))

    # Make a daemon so thread ends when main thread ends
    t.daemon = True

    t.start()

# Close out clients
for cs in client_List:
    cs.close()
# Close socket
s.close()
