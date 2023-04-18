import socket
from threading import Thread
from datetime import datetime

#creating flags & variables

# Sets the preselected IP and port for the chat server
# Eneter your machine's IP address for the host_name. Alternatively, you can enter "localhost"
host_name = "144.37.106.49"
port = 18000

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
MSG = ""

def listen_for_messages():
    global MSG
    while True:
        try:
            message = new_socket.recv(1024).decode()
        except ConnectionAbortedError:
            break
        MSG = message
        print("\n2" + message)

while True:
    #prompts menu with 3 options
    print("Please select one of the following options:")
    print("1. Get a report of the chatroom from the server.")
    print("2. Request to join the chatroom.")
    print("3. Quit the program.")
    choice = input()
    print("your choice:", choice)

    # Prompts the client for a username
    if choice == "2":
        # Creates the TCP socket
        new_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Connecting to", host_name, port, "...")
        new_socket.connect((host_name, port))
        print("Connected.")

        print("Type lowercase 'q' at anytime to quit!")
        name = input("Enter your a username: ")
        new_socket.send(name.encode())

        # Thread to listen for messages from the server
        t = Thread(target=listen_for_messages)
        t.daemon = True
        t.start()
        
       # print("MESSAGE " + MSG)
        if MSG == "The server rejects the join request. Another user is using this username.":
            print("FLAG")
            continue
        

        # if user is an admin send the admin name before appending time and username
        if name == "admin":
            print("Welcome Administrator")
            new_socket.send(name.encode())


        while True:
            # Recieves input from the user for a message
            to_send = input()

            # Allows the user to exit the chat room
            if to_send.lower() == "q":
                new_socket.send(to_send.encode())
                break

            if to_send.lower() == "info":
                new_socket.send(to_send.encode())

            # Appends the username and time to the clients message
            to_send = name + ": " + to_send
            date_now = datetime.now().strftime("[%H:%M] ")
            to_send = date_now + to_send

            # Sends the message to the server
            new_socket.send(to_send.encode())

        # close the socket
        new_socket.close()

    elif choice == "1":
        #do option 1, adding exit in the meantime
        exit()
        menu() #prints the menu again
    else:
        exit()


