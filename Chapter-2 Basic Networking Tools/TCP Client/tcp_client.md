# Chapter 2: Basic Networking Tools


## TCP Client
- A TCP Client allows you to connect to a server using the Transmission Control Protocol. TCP is suited for applications that require reliable, ordered, and error-checked delivery of data. Protocols such as HTTP, HTTPs, FTP, SMTP, and Telnet all use TCP. The TCP data packets are ordered, ensuring the receiving system obtains the correct packets in the correct order. 

- TCP uses a 3-way handshake to ensure the data is reliably sent and received. 
  1. The client sends a SYN (synchronize) message to the server, letting the server know that the client wants to connect.
	2. The server responds with a SYN-ACK (synchronize & acknowledge), letting the client know that is is ready to accept the transmission.
	3. The client sends an ACK (acknowledge) message back, confirming the connection between the two systems

- Each TCP segment includes a header containing control and sequencing information about the data being sent. This includes:
	- Source and Destination Ports
	- Sequence Number - Position of the first byte
	- Acknowledgement Number - Next byte to be received
	- Header Length
	- Control Flags:
		- URG - Urgent Data
		- ACK - Acknowledgement Valid
		- PSH - Push Data Immediately
		- RST - Reset Connection
		- SYN - Synchronize Sequence Numbers
		- FIN - Terminate the Connection
	- Window Size
	- Checksum - Used for Error Detection
	- Urgent Pointer - Position of Urgent Data

- A TCP Client can be written to test for services, send garbage data, fuzz, or perform any number of other tasks. Sometimes you will not have the tools available to perform the task at hand so you would have to build those from scratch.

**Steps to Create TCP Client**

1. We begin by importing the `socket` module. A socket is one endpoint of a two way communication between two programs running on the network. These sockets will be a piece of data that will carry the ip address and port number. 
2. Next we will set the Target Host and the Target Port Number. The Target is the server that we are sending the TCP request and data to. We will use localhost *127.0.0.1* for this demo.
3. A socket object is created by calling the socket module and passing in two parameters.
	1. The 'socket.AF_INET' parameter tells the socket that it will be an IPv4 address
	2. The 'socket.SOCK_STREAM' parameter tells the socket that this will be a TCP client
4. Now we will connect to the client, calling the name we assigned to the socket with the connect tag `.connect()`. It gets passed two parameters, target_host and target_port, the address and port number assigned earlier to connect with.
5. Next we will create some data to send to the client by using the send tag `.send()`. This data will be in the form of bytes. The 'b' call in front of the string returns bytes. 

>The first DEMO is using the target 'www.google.com' and data 'GET request'.
>- This DEMO shows how you can get a response back, coded in the next step. Netcat will not pick up on this.

>The second DEMO is using the target '127.0.0.1' and data "Hello World".
>- This DEMO shows how you can send a string to your localhost and have it show up scanning with Netcat. Netcat does not automatically respond unless data is manually sent back. 

6. After sending some data, we might want to receive data. This is done by using `.recv()` on the client, and specify the number of bytes of data to receive back from the connected socket. We then assign the response to a variable so it can be decoded in the next step.
7. We will print out a decoded version of the response, by passing the response variable into `.decode()`. 
8. Lastly we will close the socket.
9. To Test: open a terminal in Kali and run `nc -lnvp 80` to launch Netcat into listening for TCP on port 80. This will catch your sent data. (nc = netcat, -l = listen, -n = numeric, v = verbose, p = port)

At this point we have successfully created a TCP Client with Python. In the next steps we will create a UDP Client.
