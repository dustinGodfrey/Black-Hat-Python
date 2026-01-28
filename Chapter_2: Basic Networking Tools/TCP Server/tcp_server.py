import socket
import threading

#Set the IP address and Port number to assign to the Server
IP = '0.0.0.0'
PORT = 9998

#Creating the main function
def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)              #Creating the socket
    server.bind((IP, PORT))                                                 #Binding the IP and PORT to the server
    server.listen(5)                                                        #Allows the server to have 5 active connections 
    print(f'[*] Listening on {IP}:{PORT}')                                  #Display an output

    while True:
        client, address = server.accept()                                   #Accepting the connection and parsing the data
        print(f'[*] Accepted Connection from {address[0]}:{address[1]}')    #Printing an acceptance message
        client_handler = threading.Thread(target=handle_client, args=(client,)) #Creating thread and passing client to next function
        client_handler.start()

def handle_client(client_socket):
    with client_socket as sock:
        request = sock.recv(1024)
        print(f'[*] Received: {request.decode("utf-8")}')
        sock.send(b'Hello Client!')

if __name__ == '__main__':
    main()
