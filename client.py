"""Sends a query to the server."""

import configparser
import socket
import sys


# Reading the configs.ini file and storing the data in the
# config_data variable.
config_data = configparser.ConfigParser()
config_data.read("configs.ini")

# Reading the configs.ini file and storing the data in the
# config_data variable from configs
DATA_FORMAT = config_data["socket_info"]["DATA_FORMAT"]
PAYLOAD_SIZE = int(config_data["socket_info"]["PAYLOAD_SIZE"])
HOST = config_data["socket_info"]["HOST"]
PORT = int(config_data["socket_info"]["PORT"])
SOCK_ADDRESS = (HOST, PORT)


def send_request(query):
    """Send a request to the server.

    It creates a socket and connects it to the server, sends the
    query, receives the response, and closes the socket

    :param query: The string to be searched in the database
    """
    try:
        # Creating a socket, connecting to the server
        client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_sock.connect(SOCK_ADDRESS)
        message = query.encode(DATA_FORMAT)
        client_sock.send(message)

        # message from the server
        data = client_sock.recv(PAYLOAD_SIZE).decode(DATA_FORMAT)

        # Checking the data received from the server
        if data == "STRING NOT FOUND\n":
            print("STRING NOT FOUND\n")
        elif data == "STRING EXISTS\n":
            print("STRING EXISTS\n")
        client_sock.close()

    # Catching the error and printing it.
    except socket.error as err:
        print(f"Error creating socket: {err}")
        sys.exit(1)
