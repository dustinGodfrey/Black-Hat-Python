import socket

#setting host - choose one to uncomment
#target_host = 'www.google.com'
target_host = "127.0.0.1"

target_port = 80

# create a socket object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect the client
client.connect((target_host, target_port))

# send some data - choose one to uncomment
#client.send(b"GET / HTTP/1.1\r\nHost: google.com\r\n\r\n")
client.send(b"Hello World!")

#receive some data
response = client.recv(4096)

print(response.decode())

client.close()
