import socket
from threading import Thread
import time

HEADER = 16 #Default 16 header for fixed length of the int of real msg_length
#Write Private IP of own system
SERVER_HOST = "X.X.X.X" #Can be found by typing ipconfig in cmd and entering IPV4 address displayed under LAN Network
SERVER_PORT = 49876


s = socket.socket()
print(f"[CLIENT] Connecting to {SERVER_HOST}:{SERVER_PORT}")#Creating socket for client
try:
    s.connect((SERVER_HOST, SERVER_PORT))#Connecting with server
except Exception:
    print(f"[!]Error: Please Check the server_host IP {SERVER_HOST} entered in the file client.py is correct or not.")
    time.sleep(10)
else:
    print("[SERVER] Connected.")

    name = input("Enter your name: ")
    def listen_for_messages():#Listen to message given by server
        while True:
            msg_length = s.recv(HEADER).decode()#decoding header to get message length
            msg_length = int(msg_length)
            msg = s.recv(msg_length).decode()#decoding message
            print("\n" + msg)


    t = Thread(target=listen_for_messages)#starting thread for each client to listen to message

    t.daemon = True

    t.start()
    while True:#All message delivery package stuff lie here
        to_send =  input()
        if to_send.lower() == 'q': #Disconnect message
            break
        msg_length = len(to_send) + len(name) + 2 #Correcting final msg_length to send
        send_length = str(msg_length).encode()
        send_length += b' ' * (HEADER - len(send_length)) #PAdding the right amount for buffer
        s.send(send_length)#sending the fixed msg length first
        to_send = f"[{name}]{to_send}"
        s.send(to_send.encode())#Sending msg

    s.close() #Closing the client.py after closing connection
