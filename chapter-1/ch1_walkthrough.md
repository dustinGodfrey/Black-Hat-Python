# Chapter 1: Setting Up Python Environment

**This chapter goes over the set up of:**
- Kali Linux VM
- Installing Python
- Setting up a Virtual Environment
- Installing an IDE
- Code Hygiene

## Kali Linux VM:
- For these labs you will need a Kali Linux Virtual Machine. Depending on your OS and hardware there are several ways to do this. VirtualBox on Windows, UTM on MacOS, and a bare-metal Proxmox Server were all used during these labs.

## Installing Python:
- To determine what version you are using and to upgrade to the latest version

``` bash
python
sudo apt upgrade python3
```  


 ## Setting up a Virtual Environment:
- A virtual environment is a self contained environment where the plugins and modules that you import will live only within that environment. This is a way to run multiple environments where they need different versions of modules or different configurations. 

Install the Python3 Virtual Environment Package:

``` bash
sudo apt install python3-venv
```

 Next we create a directory for the environment to run inside of:

``` bash
mkdir bhp
cd bhp
```

Next we will create a virtual environment within that directory and activate it:

```
python3 -m venv venv3
source venv3/bin/activate
```

Your prompt will now change from kali@kali to (venv3) kali@kali. This lets you know that you are in the virtual environment and it is active.

To leave the virtual environment:

```bash
deactivate
```

You can use the pip executable to install Python packages:

```bash
pip install lxml
```

This should output the download process


## Installing an IDE:
- An integrated development environment (IDE) is a way to code efficiently by using tools built in that will include a code editor, syntax highlighting, auto indention, and a debugger. This is much easier to use and more reader friendly than command line text editors like nano and vim.

We will download VS Code to run in our Kali machine. Navigate to the [downloads page](https://code.visualstudio.com/download) for Visual Studio Code and download the latest version based on your system requirements. Navigate on your Kali machine to where you downloaded the file and run the following command:

```bash
sudo dpkg -i file_name
```


## Code Hygiene:
- The book covers the best way to layout your python code. This is recommended for easy of use and readability

Your code should be laid out in this order:

1. Package imports (in alphabetical order)

2. Module imports (in alphabetical order)

3. Functions

4. Classes

5. Main Code Block at Bottom


Running and Importing Code:
- There are 2 ways you can use the code in your main code block. For this example we will assume you have a file titled `scan.py`

1. In the command line you can execute this code by running:
```bash
python scan.py
```
	This will run the code from top to bottom and execute the block as is.

2. You can import the code into another program by adding at the top:
```bash
import scan
```
	This will allow you to use any of the modules defined functions and classes, but the main block will not be executed.

