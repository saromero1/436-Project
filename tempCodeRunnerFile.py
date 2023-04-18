
            if to_send.lower() == "q" or NEW_USER_FLAG == 1:
                new_socket.send("q".encode())
                break

            if to_send.lower() == "info":