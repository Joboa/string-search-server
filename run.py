"""Linux script wrapped in python for running server and client."""

import subprocess
import socket
import configparser

# Reading the configs.ini file and storing the data in the c
# onfig_data variable.
config_data = configparser.ConfigParser()
config_data.read("configs.ini")

# Host and port from the config file.
HOST = config_data["socket_info"]["HOST"]
PORT = int(config_data["socket_info"]["PORT"])
SOCK_ADDRESS = (HOST, PORT)

# Running the server.py file in the background.
server_process = subprocess.Popen(["python3", "server.py"])

# Waiting for the server to start.
while True:
    try:
        with socket.create_connection((SOCK_ADDRESS)):
            break
    except ConnectionRefusedError:
        pass

# Run the second command
client_process = subprocess.run(["python3", "client.py"])

# Killing the server process.
server_process.kill()
