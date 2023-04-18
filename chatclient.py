import socket
from threading import Thread
from datetime import datetime
#creating flags & variables
# Sets the preselected IP and port for the chat server
# Eneter your machine's IP address for the host_name. Alternatively, you can enter "localhost"
host_name = "144.37.124.178"
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
def parse_string(input_str):
    # Splitting the string into a list
    input_list = input_str.split(", ")

    # Creating a new list with formatted strings
    output_list = []
    for i in range(0, len(input_list)-2, 3):
        output_list.append(f"{i//3+1}. {input_list[i]} at IP: {input_list[i+2]} and port: {input_list[i+3]}")

    # Joining the list elements into a single string with newline character
    output_str = "\n".join(output_list)

    # Printing the output string
    print(output_str)


def listen_for_messages():
    while True:
        global NEW_USER_FLAG
        count = 0
        try:
            if count == 0:
                message = new_socket.recv(1024).decode()
                count = count + 1
        except ConnectionAbortedError:
            break

        if message == "REJECTED":
            NEW_USER_FLAG = 1
        else:
            NEW_USER_FLAG = 0
            print("\n" + message)

def get_chatroom_report():
    # Create a new socket to send the report request
    report_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    report_socket.connect((host_name, port))

    # Send the report request message to the server
    report_socket.send("REPORT_REQUEST".encode())

    # Listen for the response from the server
    report_response = report_socket.recv(1024).decode()
    report_response1 = report_socket.recv(1024).decode()

    #send quitting to server
    report_socket.send("q".encode())

    # Close the socket
    report_socket.close()

    # Print the response message from the server
    print("There are " + report_response + "active users in the chatroom.")
    parse_string(report_response1)


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

        # Thread to listen for messages from the server
        t = Thread(target=listen_for_messages)
        t.daemon = True
        t.start()
        
        #first s
        new_socket.send(name.encode())

        
        message = new_socket.recv(1024).decode()
        if message == "REJECTED1":
            print("The server rejects the join request. The chatroom has reached its maximum capacity.")
        elif message == "REJECTED2":
            print("The server rejects the join request. Another user is using this username.")

        print("Type lowercase ‘a’ and press enter at any time to upload an attachment to the chatroom.")

        # if user is an admin send the admin name before appending time and username
        if name == "damin":
            print("Welcome Administrator")
            new_socket.send(name.encode())
          


        while True:
            if message == "REJECTED1" or message == "REJECTED2":
                new_socket.send("q".encode())
                break
            # Recieves input from the user for a message
            to_send = input()
            # Allows the user to exit the chat room

            if to_send.lower() == "q" or NEW_USER_FLAG == 1:
                new_socket.send("q".encode())
                break

            if to_send.lower() == "info":
                new_socket.send(to_send.encode())

            if to_send.lower() == "a":
                print("Please enter the file path and name:")
                file_path = input()
                try:
                    with open(file_path, "r") as f:
                        file_content = f.read()
                        # Send the file content as a message to the server
                        to_send = file_content
                except:
                    print("Error: Could not open or read file")
                

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
        get_chatroom_report()
        exit()
    else:
        #new_socket.send("q".encode())
        exit()
#AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA