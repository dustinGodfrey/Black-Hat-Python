## UDP Client

- A UDP Client allows you to a server using the User Datagram Protocol. UDP is built for speed, providing fast, connectionless communication. Unlike TCP, UDP has no error checking, is not ordered, and does not wait for any acknowledgement to send the data. This is very useful when using real-time and time-sensitive applications. Some popular uses for UDP are video streaming, DNS, and VoIP.

- The UDP header is shorter than that of TCP, with only 4 fields being sent over:
	- Source Port
	- Destination Port
	- Length
	- Checksum (optional)

- A UDP Client is created in a very similar way to the TCP Client, only making two changes. 

**Steps to Create a UDP Client**

1. We begin by importing the *socket* module. A socket is one endpoint of a two way communication between two programs running on the network. These sockets will be a piece of data that will carry the ip address and port number. 
2. Next we will set the Target Host and the Target Port Number. The Target is the server that we are sending the UDP data to. We will use localhost *127.0.0.1* for this demo.
3. A socket object is created by calling the socket module and passing in two parameters.
	1. The 'socket.AF_INET' parameter tells the socket that it will be an IPv4 address
	2. The 'socket.SOCK_DGRAM' parameter tells the socket that this will be a UDP client
4. Next we will create some data to send to the client by using the send tag *.sendto()*. This data will be in the form of bytes. The 'b' call in front of the string returns bytes. We will pass in the data and the server you want to send it to.
5. To receive data back, we will call *.recvfrom()*, passing in the amount of bytes to receive back. We are assigning two variables here because we will receive 2 pieces of data back from this: the data and the details of the remote host and port.
6. We will print out a decoded version of the response, by passing the response variable into *.decode()*. 
7. Lastly we will close the socket.
8. To Test: open a terminal in Kali and run 'nc -ulp 9997' to launch Netcat into listening for UDP on port 80. This will catch your sent data. (nc = netcat, -u = udp, -l = listen, p = port)
