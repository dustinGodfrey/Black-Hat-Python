import socket

#setting target host and port
target_host = "localhost"
target_port = 9997

#create a socket object
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#send some data
client.sendto(b"Hello World!",(target_host,target_port))

#receive some data
data, addr = client.recvfrom(4096)

#decode and print the response
print(data.decode())

#close the socket
client.close()