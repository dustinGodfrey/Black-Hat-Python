## TCP Server

- A TCP server is useful for building services such as internal tooling, simple message brokers, proxies, or lab testing utilities. This example demonstrates a multi-threaded server that can handle multiple clients concurrently.

- This script involves sockets and multithreading. Multithreading allows multiple execution threads to run concurrently within a single process, enabling the server to handle multiple client connections without blocking. Multithreading is useful for tasks that involve waiting, like file handling or network requests, which is what we are using it for in this example.

1. First we import the modules `socket` and `threading`.
2. Next, set the IP and PORT variables with the desired address and port number for the server.
3. Now create the main function of the program.
	1. Create the socket for the server with socket.AF_INET and socket.SOCK_STREAM for a TCP connection.
	2. Bind the server to the IP and Port number with `.bind()` 
	3. Allow the server to listen for incoming connections, with a backlog queue size of 5 using  `.listen()`
	4. Print an output that the server is listening.
4. Now create a `while True` loop inside the main function to continuously accept incoming connections and delegate each client socket to a handler function running in a separate thread.
	1. When a client connects, we receive the client socket in the 'client' variable and the remote connection details in the address variable
	2. We print an acceptance message with the IP and Port number of the client listed
	3. Create a new thread object that targets the `handle_client` function and passes the client socket as an argument, allowing the connection to be processed independently.
	4. We will start the thread to handle the client connection. At this point the program loops and it is ready to receive another connection
5. Next we will create the handle_client function to handle the connection that the 'main' function picked up.
	1. The function has a parameter 'client_socket' which is passed in from the main function. The function then sets it to 'sock' for ease of use
	2. The function reads up to 1024 bytes of data from the client socket using  `.recv()`, which retrieves available data from the TCP stream.
	3. Next, a message is printed displaying the decoded form of what was received.
	4. Then there is some data that is sent back to the client, in this case a simple string.
6. To Test: Open your Kali terminal in split screen, on the first terminal window run your tcp_server.py code, you should see *Listening on 0.0.0.0:9998*. On your second terminal run the tcp_client.py code from the TCP Client module. You should see the string your tcp_client was coded with appear on your tcp_server screen, along with *Accepted Connection from 127.0.0.1:60987*. On your tcp_client screen you should see the response string from the server. 
<p align="center"> <img src="https://i.imgur.com/ziFNm6L.png" width="75%" alt="server-client"/></p>
