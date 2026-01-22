# Replacing Netcat

> [!NOTE]
>Netcat is a networking tool that allows the user to read and write data across the network, execute remote commands, send and receive files, and even open a remote shell. For penetration testing, this is extremely useful as some system you may be inside of will not have netcat installed but will in fact have python installed. Being able to write these quick scripts can give you network access using tools already present on the system rather than relying on externally installed utilities.
>
>All testing was performed in a controlled lab environment using private IP space

1. First import all necessary libraries
	1. argparse - allows user to define arguments for command-line interfaces
	2. socket - allows for the creating of sockets
	3. shlex - parsing command-line strings, splits strings into tokens for shell syntax
	4. subprocess - allows running commands with code
	5. sys - interacting with the system
	6. textwrap - allows wrapping and filling lines for formatted text
	7. threading - allows for multithreading
2. Create the `execute()` function, which will receive in a command and run it.
	1. The `execute()` function then defines a variable `output` which uses subprocess to receive the output of the command and display it as a string. 
	
---

1. Now we will create the main code block, which will handle command line arguments and call the rest of the functions.
2. We start by creating the command line interface with `argparse` module. This will allow us to set up certain commands to call within the app, such as uploading a file and executing commands.
3. Within the `argparse` module we can use the `epilog` tag to specify text to be displayed when the `--help` command is called. This epilog will list a series of examples of what the syntax should look like when dealing with this program. 
4. Next we will use the `parser.add_argument` call to create 6 arguments to use within the program:
	1. `-c` sets up an interactive shell
	2. `-e` allows for code execution
	3. `-l` indicates a listener should be set up
	4. `-p` specifies the port used for communications
	5. `-t` specifies up the target IP address
	6. `-u` specifies a file to upload
5. Both the sender and receiver can use this program, so some commands are set up for the sender and some are from the listener
	1. `-c`, `-e`, `-u` imply the `-l` argument due to those only applying to the listener side
	2. `-t`, `-p` are used to define the target listener, only applied to sender side
6. The variable `args` is created with the `parser.parse_args` call, which will take every argument created with `add_argument` and add them to a namespace object, allowing it to be called later on.
7. Next we set up a simple `if/else` to determine if we are set up as a listener. 
	1. If yes, the `NetCat` object is called (setup in next steps) with an empty buffer string.
	2. If no, we send the buffer content from `stdin`
8. We then call the run method to start

---

1. Now we will create the `NetCat` class. This will be placed above the `main` code block and below the `execute` function. 
2. The `NetCat` class is initialized with `args`, the arguments we created in the main block, and the `buffer`, a variable that holds data before it is sent somewhere, temporary storage.
3. Next we will create the socket object, having the first line set up a TCP socket, and the second line setting the socket options with `setsockopt`, which is passed in the arguments `SOL_SOCKET` which specifies that the option is applied at the socket level and `SO_REUSEADDR` allows the socket to re-bind to an IP and port that are in a TIME_WAIT state, which would normally be rejected by the operating system. The `1` tag indicates that `SO_REUSEADDR` option is enabled.
4. Now we create the `run` method, which delegates the execution to two methods.
	1. If the command is called to set up a listener, then the `listen` method is called.
	2. If no command is sent for the listener, it is assumed this will be a sender and calls the `send` method.
	3. Both of these methods will be created in the next steps.
	
---

1. Now we will create the `send` function below the `run` function.
2. We start by connecting the socket to the specified IP and Port
3. Create a simple `if` statement, if we have a buffer, that is sent to the target first
4. Next a `try/catch` block is set up so the program can be closed at anytime with a `KeyboardInterrupt`, CTRL+C
	1. Start a `while True` loop that sets the receiving length (`recv_len`) to 1 and set the `response` to an empty string.
	2. Start another `while` loop that sets the `data` variable to the data that will be received from the target. Set `recv_len` to the length of the data and add the decoded information into the `respose` string.
	3. Another small `if` statement is created to break the program if too little or no data is sent back.
	4. We will now run another `if` statement that processes the response if there is one
		1. The program will print the `response`
		2. The `buffer` becomes an input from the user with a newline added for crafting a reply.
		3. The socket sends the encoded buffer and starts the loop over
	5. If the user uses `Keyboard Interrupt`, the program will print a message, close the socket, and exit the program.

---

1. Now we will create the `listen` function below the `send` function.
2. We start by binding the socket to the target and port and set the socket to have a backlog of 5 connections
3. Now we begin a `while True` loop that will accept the connection from the socket, assigning the incoming socket to `client_socket` and setting the incoming address to `_` as this is not relevant information for this application. We are only passing the socket to the handler.
4. A new thread is created and a reference to the `handle` function is stored, along with the client socket, which will be passed to the function when the thread starts. We will create the `handle` function in the next step.

---

1. Finally we will create the `handle` function which executes tasks based on the arguments it receives from the command line.
2. We begin by creating the logic if the `execute` argument is used
	1. If the `execute` argument is called we set a variable `output` which will execute when called, then use `send` to send the encoded data
3. Next we create the logic if the `upload` argument is used.
	1. Set variable `file_buffer` to an empty bytes object, this will hold the data to be uploaded later on
	2. Running a `while True` loop we look for data coming in, and if we receive any data we will add that data to `file_buffer` until there is no more data coming in.
	3. We open the upload in `write/binary` mode and write the contents of `file_buffer` to that location.
	4. We add that data to a simple message, then send over the encoded data
4. Lastly we will create the logic if the `command` argument is used.
	1. Set variable `cmd_buffer` to an empty bytes object.
	2. Running a `while True` loop, we write a `try/except` block to break cleanly if any exception occurs.
	3. Inside the loop we send a prompt to the sender and wait for a command string to come back. As long as the sender does not press Enter or submit a newline the program will wait for a response.
	4. When the socket receives data, it will append that to `cmd_buffer`
	5. A variable `response` is created which will hold the execution of the decoded `cmd_buffer`. 
	6. If `response` is used the program will send the encoded version of the `cmd_buffer` data, executing the command.
	7. After the encoded data is sent, `cmd_buffer` clears and another prompt is sent

---

#### To Test:

>[!NOTE]
>There are five tests that we will run to see if everything is functioning properly.

1. 
Open a terminal on your Kali machine and run:

```bash
python3 netcat.py --help
```

You should see the help page that we coded in. This screen will show the usage, title, options, and the examples we set.

<p align="center"> <img src="https://i.imgur.com/ukCMsyF.png" width="75%" alt="netcat-help"/></p>

2. 
 On your local machine run the following code to start netcat in listen mode, with the target IP set to the IP of your local machine. There will be no output yet, as it will be waiting to receive data:
 
```bash
python3 netcat.py -t 192.168.x.x -p 5555 -l -c
```
 
 On your Kali machine run the following code to start netcat in client mode:

```bash
python3 netcat.py -t 192.168.x.x -p 5555
```

On your Kali machine there will be no output to start. Because the client reads from `stdin`, interactive behavior depends on terminal and OS handling of EOF, End Of File marker. In some environments `CTRL + D` may not behave as expected, so reversing client/server roles can be used as a workaround. Once you send over the EOF marker you should see the command prompt show up. From there you can issue commands to the machine and it will execute them. This can be anything from checking machine information, listing directories, or even opening apps. If your command does not execute  it may be stuck in the buffer, pressing `Enter` again should execute your code.

In this implementation, no output is displayed on the listener terminal. All command output is sent to the client over the socket and may not be displayed on the client side until the connection state changes (for example, when the client sends EOF or disconnects). This behavior is due to the client’s receive loop and TCP stream buffering, not delayed execution on the listener.

>[!IMPORTANT]
>Following the book we are supposed to reverse this section, launching the listener from Kali and connecting with the local machine, but due to my environment of MacOS + Tabby,  my EOF was not being recognized by the machine. I was receiving `^D` on my screen instead of it actually sending the marker. If you have this issue just reverse like we did above and it should fix the issue, as my Kali machine will accept the `CTRL + D` syntax.

<p align="center"> <img src="https://i.imgur.com/FV1i54o.png" width="75%" alt="netcat-listen"/></p>

3. 
On your local machine setup a listener again, but this time instead of issuing a command shell with `-c` we will set it up to execute a specific command with `-e`.

```bash
python3 netcat.py -t 192.168.x.x -p 5555 -l -e="ls -la"
```

Connect to the listener with your client the same way as before:

```bash
python3 netcat.py -t 192.168.x.x -p 5555
```

On your client side, issue the EOF marker again and you should receive the results of the executed command set by the listener. This is useful when you do not need to necessarily be inside the system to extract data. This is a clean and simple way to send data automatically to anyone who connects to the listener.

<p align="center"> <img src="https://i.imgur.com/ScsiosI.png" width="75%" alt="netcat-execute"/></p>
You can also run the actual program `netcat` on the client and receive the same data.

<p align="center"> <img src="https://i.imgur.com/NOkGxcf.png" width="75%" alt="netcat-execute"/></p>

4. 
Next we can use our `netcat.py` on the client side to request data. For this example I setup a simple python http server to host the contents of my directory on my local machine.

```bash
python3 -m http.server 8000
```

On the client machine I ran the following command to reach out with a request to that address where the directory is hosted

```bash
printf "GET / HTTP/1.1\r\n\r\n" | python3 netcat.py -t 192.168.x.x -p 8000
```

This should return some headers and metadata, then show the directory listing

<p align="center"> <img src="https://i.imgur.com/HmM4AvR.png" width="75%" alt="netcat-request"/></p>

5. 
The last test we will run demonstrates the Upload function of the netcat app. 
This part took some time to understand because it behaves differently than the other options.

Above, when the listener sets up with the `-c`(command shell) or `-e`(execute) this data is transferred from listener to client. When the client connects and issues an EOF marker the client will receive the command shell or the executed command as if they were on the listener machine.

Using the upload function it works backwards from this. The listener sets up using `-l` and `-u` with the `-u` tag, providing a destination path. The file does not need to exist. This file will receive data from the client.

```bash
python3 netcat.py -t 0.0.0.0 -p 5555 -l -u="uploaded_from_client.txt"
```

On the client side, connect to the listener but redirect stdin to the file to upload.

```bash
python3 netcat.py -t 192.168.x.x -p 5555 < sample.txt
```

After issuing this command from kali, wait 1-2 seconds then disconnect from the listener with `CTRL + C`. 

Stop the listener and check the directory, you should have a file titled `uploaded_from_client.txt`. If you read the contents of this file it should contain the contents of the `sample.txt` from the client side. 

```bash
ls -l uploaded_from_client.txt
cat uploaded_from_client.txt
```
