import socket
from threading import Thread
#from functions import listen_for_client

HEADER = 16  #Reserved bytes for msg recv
SERVER = socket.gethostbyname(socket.gethostname()) #Get the IP of device it is running
SERVER_PORT = 49876

client_sockets = set() #Creates a set for the no. of clients connected

''' the below line will create a socket for the server '''
s = socket.socket() #With default AF_INET and SOCK_STREAM

s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #Use to deal with OS Error of addr already in use

s.bind((SERVER, SERVER_PORT)) #Binds the socket with the IP_ADDRESS of server and port

s.listen(5) #Max no. of devices that can be connected is 5
print(f"[SERVER] Listening as {SERVER}:{SERVER_PORT}")
def quit(msg_length,msg,cs):#quit method for clean up and closing connection
    cs.send(msg_length.encode())
    cs.send(msg.encode())
    cs.close()
    client_sockets.remove(cs)
    print(f"No. of clients connected to server are {len(client_sockets)}")

def checker(msg_length,msg,cs): #checker method for checking
    if "quit" in msg:
        quit(msg_length,msg,cs)
        return False
    else:
        return True

def listen_for_client(cs):
    msg_length=""
    msg=""
    while True:
        try:
            msg_length = cs.recv(HEADER).decode()#Decoding the msg length first
            msg_length1 = int(msg_length)
            msg = cs.recv(msg_length1).decode()#Decoding msg
        except Exception as e:     #close the connection if the above block result in error
            print(f"[!] Error: {e}")
            client_sockets.remove(cs)
        else:
            pass #Countinues if not
        if checker(msg_length,msg,cs):
            for client_socket in client_sockets:#getting the no. of client iterables
                client_socket.send(msg_length.encode())#Again encoding msg_length for client to broadcast
                client_socket.send(msg.encode())#Encoding the real msg
        else:
            break#For terminating the thread


while True:
    '''accept() func will give 2 outputs first (here recevied by client_socket)
     are the socket of client {file obj of the socket[dont worry about this]} second the address of the client
     mainly its IP and port '''
    client_socket, client_address = s.accept() #Connection establish between client and server
    print(f"[SERVER] {client_address} connected.")
    client_sockets.add(client_socket)
    print(f"No. of clients connected to server are {len(client_sockets)}")
    '''#Starting a new thread so that the accept() func wont block the server and result in halt
    because of the thread the server can parallely process multiple client without even waiting for single client'''
    t = Thread(target=listen_for_client, args=(client_socket,))
    t.daemon = True
    t.start()

for cs in client_sockets:#once the while loop break closing all sockets
    cs.close()


s.close()
