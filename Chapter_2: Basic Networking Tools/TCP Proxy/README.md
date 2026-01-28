# TCP Proxy

>[!WARNING]
> As always, these labs are to demonstrate testing and penetration testing in a controlled lab environment. Nothing here should be used in an environment you do not have permission to explore.

>[!Note]
> Proxies are technologies that allow for the redirection of traffic through a server before being sent to its final location, an intermediary between your device and another. This server will make requests on behalf of the machine doing the requesting, and will forward that information back to the requester after the server receives the data from the other party.
>
>From a security standpoint, proxies can help enforce proper network segmentation and policy, allowing the engineer to set up source and destination IPs, ports, and rate limiting. This prevents direct host-to-host communication and allows for the data to be validated and inspected before being forwarded. Also, since this is a TCP connection you get the reliability benefits of ordered packets and retransmission. Logs are also centralized through one server so incident response and threat hunting become more effective.
>
> There are several types of proxies you can set up; HTTP/S Proxy for browser traffic, Transparent Proxy for caching, content filtering and parental controls, and many others. Building a TCP Proxy allows a user to set up communication between hosts, access network-based software, load balance, filter and log data.
> 
> For this exercise we will set up a TCP Proxy which will: 
> 1. Display the communication between the local and remote machines to the console
> 2. Receive data from an incoming socket from either the local or remote machine 
> 3. Manage the traffic direction between remote and local machines
> 4. Set up a listening socket and pass the accepted connection to the proxy handler

---

1. First we will import all necessary libraries:
	1. sys - allows to interact with system functions, such as command-line arguments, exit codes, stdout/stderr, etc.
	2. socket - allows setup of data sockets
	3. threading - allows the use of multithreading when setting up sockets and listeners

---

1. Now we create the first part of the code which is a string `HEX_FILTER`. It’s a 256-character translation table used to map bytes to printable output.  If `repr(chr(i))` is length 3 (like `'A'`), treat it as printable; otherwise map it to `.`. This string will later be used to generate the printable ASCII column in the hexdump output. Non-printable characters are replaced with a `.` so binary data can be safely displayed in the console.

---

1. Now the first function to create is `hexdump()`. 
	1. Hexdump accepts bytes and formats output in lines of 16 characters (default), and will display results
	2. If the source string is in bytes, the program will decode that string
	3. A empty list `results` is created which will hold our final display
	4. A for loop now starts, parsing through the source string
		1. The loop is set to pull out characters from the source in 16 character increments.
		2. It starts with the first character and slice up to 16 characters to produce one output line
		3. A 16 character line is saved to the variable `word`.
		4. The `translate()` function uses `HEX_FILTER` to produce a printable ASCII representation of the data, replacing non-printable characters with a `.`.
		5. A variable `hexa` is created, joining the characters created in word with a space and creating a string that will contain the ASCII value of the character `ord(c)`, extract out 2 uppercase hex values `:02X`. This just means that for each converted letter in `word` there will be a 2 digit hex value associated.
		6. A variable `hexwidth` is created which will create a number that is three times the size of the length. This is used for alignment padding in the final result as each hex byte is 3 characters in length. This will ensure aligned columns in the final display even if the final lines are shorter.
		7. A string containing an offset in hex padded to 4 digits `{i:04x}`, properly left aligned hex bytes `{hexa:<hexwidth}`, and the converted hex string `{printable}` is created and appended to `results`. 
			- The offset increments by 16 bytes per line, and is displayed in hexadecimal, so 16 decimal appears as 0x10.
		8. The loop continues if the string is more than 16 total lines, creating a new 16 byte line or less until the source string has been completely looped through. 
		9. The final `if` statement here will look to see if `show=True` and display each line of `results` if it is. Otherwise, nothing is printed and `results` is returned.

---

1. The next function to set up will be `receive_from()`. This function allows the two ends of the proxy to receive data.
	1. For receiving both local and remote data, we pass in the socket object to be used. The socket object will be configured later on.
	2. An empty byte string is created that will hold the information that is received from the socket.
	3. Next a timeout is set to stop the connection after a certain amount of time. This is expressed in SECONDS. If you are proxying traffic to other countries or are on a lossy connection, incrementing the timeout could be beneficial.
	4. The program will attempt to run a loop looking for data coming through the connection. If no data comes through before the timeout the loop will break. Otherwise it will store the received information in the `data` variable and returned to the caller, which could be either the local or remote machine.

---

1. Now we will set up two new functions, `request_handler` and `response_handler`. These functions will allow us to modify the request or response packets before they are sent by the proxy. These functions will allow processes such as modify the package contents, add fuzzing data, or adding in user credentials.

---

1. Now we set up a new function which will perform most of the logic in the code, `proxy_handler`. This function allows sending and receiving from both the local and remote hosts.
	1. This function starts out by creating a new socket `remote_socket` and connects it to the remote host and port.
	2. The handler has an argument for `receive_first`, this is a safeguard in case any connections require receiving data from the remote side before the connection can begin. If there is any data that comes through it is sent to the `hexdump` function.
	3. The variable `remote_buffer` is setup to send any response through the `response_handler` function. If a buffer is to be sent over, it is sent to the remote host along with a message containing the size of buffer.
	4. The main loop is now created to handle the sending and receiving of data.
		1. A variable `local_buffer` is setup to receive any data from the local client using the `receive_from` function.
		2. If data is received, a line is printed showing the size of the buffer, then `hexdump` is called to process it.
		3. `local buffer` is reassigned, sending the contents of the local buffer to `request_handler`, then sending it to the remote side. 
		4. A variable `remote_buffer` is setup to receive data from the remote socket using the `receive_from` function.
		5. If data is received, a line is printed showing the size of the buffer, then `hexdump` is called to process it.
		6. `remote_buffer` is reassigned, sending the contents of the remote buffer to `reponse_handler`, then sending it to the local client
		7. The final part of this loop will close the connections to the client and remote if no data is incoming or outgoing.

---

1. The function `server_loop` is now created to set up and manage the connections.
	1. First a socket is created for the server
	2. The function will then attempt to bind to the local host and port. If this does not work, error messages are displayed. If the connection succeeds, the server will begin listening on the `local_port`.
	3. A loop begins where `client_socket` and `addr` are assigned with the data values when the server accepts the incoming connection. When the server accepts, a message is displayed showing the connection information.
		1. When the server receives the connection is will start a new thread and send the data to the `proxy_handler`, which will handle the sending and receiving.
		2. The loop repeats looking for new fresh connections to accept and send to the handler again

---

1. The `main` function is created last.
	1. It starts by processing the command line request to start the program. If the argv excluding script name isn't 5, the program will print a message detailing proper command usage, then closes the program.
	2. If the command request has 5 arguments, the program will assign each argument to a variable:
		1. `local_host`
		2. `local_port`
		3. `remote_host`
		4. `remote_port`
		5. `receive_first` 
	3. The function will then send all the data to `server_loop` to begin setting up and managing connections.

---

#### To Test

>[!NOTE] 
>Testing will require three concurrent processes to run: a remote server hosting the data, the proxy acting as the middleman, and a client requesting the data. Although only two machines were used for this demonstration, three terminals are required. This is due to each role running as an independent process. 
>
> The client communicates with the proxy, the proxy establishes a separate connection to the remote server, and the proxy relays data between the two.

1. We will begin by hosting some data on the remote machine. We will do this with a python http server hosted on the machine. Before setting up the server, you can create a test directory, add some test files inside, then start the server from inside that directory on port 8000.

```bash
mkdir test_dir
cd test_dir
touch test1.txt
touch test2.py
touch test3.sh
python3 -m http.server 8000
```

2. On your local machine start the proxy server, with the local machine IP as the server IP, port 9000 as the port you will be hosting communications through, the IP of your remote host, the port the remote host will be serving the http server on, and 'False' for the receive_first argument.

```bash
python3 proxy.py 0.0.0.0 9000 192.168.x.x 8000 False
```

3. In a second terminal of your local machine you will set up a curl command to receive the data through the proxy server from the remote host using port 9000, the port the proxy server is serving through. Since the proxy server is serving locally we will use the loopback address.

```bash
curl -v http://127.0.0.1:9000
```

4. The proxy server console will display information first. It will begin by displaying "Listening on 0.0.0.0:9000". If the connection is received you will see a second message "Received incoming connection from 127.0.0.1:50080".
5. Next the proxy server will display the hexdump of the data being requested from client > remote, then a message "Sent to remote" as it sends the request over.
6. The remote server will receive the request and send back the data to the proxy server.
7. The proxy server then forwards this data to the local client in the second terminal window, where the request is displayed.

<p align="center"> <img src="https://i.imgur.com/flx5C5v.png" width="75%" alt="proxy_server"/></p>

The proxy logs each data flow in three stages: receiving data from one side, displaying its contents via a hexdump, and forwarding it to the opposite side. This process occurs independently for client requests and server responses.

<p align="center"> <img src="https://i.imgur.com/Ci49E1A.png" width="75%" alt="client_curl"/></p>

<p align="center"> <img src="https://i.imgur.com/2K3Fqy6.png" width="75%" alt="remote_server"/></p>
